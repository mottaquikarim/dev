---
title: "Is json.Decoder broken in golang?!"
date: 2021-01-14T01:26:01Z
tags: ["golang"]
---

{{<toc>}}

**TL;DR**: No.

Although unintuitive, **`json.Decoder`** isn't actually broken! However, some of its behavior can appear **seemingly** wrong when used incorrectly. (Tread carefully.)

In this post, I will dive into the src code of **`json.Decoder`** and explore how it works; then I will make sense of these observed "incorrect" behaviors.

--

## The "Issue"

Let us start with a simple demonstration of the problem. Consider the following:

```golang
package main
import (
	"encoding/json"
	"fmt"
	"strings"
	"github.com/alecthomas/repr"
)
func main() {
	bad_json := `
{
  "hello": ["foobar"]
}", "foobaz"],
  "world": ["some other str"],
}`
	var fields map[string][]string
	reader := strings.NewReader(bad_json)
	if err := json.NewDecoder(reader).Decode(&fields); err != nil {
		fmt.Println("Error %w", err)
	}
	repr.Println(fields)
}
```
([playground](https://play.golang.org/p/8al6NRe96jw))

This code is fairly straightforward - given some JSON, attempt to decode it into a string map. If decoding fails, print the error.

Take a look at the JSON string more closely:

```golang
	bad_json := `
{
  "hello": ["foobar"]
}", "foobaz"],
  "world": ["some other str"],
}`
```

This JSON string is clearly malformatted. In particular, the issue is here:

```golang
}", "foobaz"],
```

We have a closing bracket `}` which shouldn't be followed by anything, but it is!


As such, we would expect any attempt at parsing to fail. And indeed, **json.Unmarshal**-ing this dude expectedly fails:

```golang
package main

import (
	"fmt"
	"encoding/json"
)

func main() {
	bad_json := `
{
  "hello": ["foobar"]
}", "foobaz"],
  "world": ["some other str"],
}`

	var fields map[string][]string
	err := json.Unmarshal([]byte(bad_json), &fields)
	fmt.Println(err)
}
```

([playground](https://play.golang.org/p/k-v9F9tjglZ))

```bash
invalid character '"' after top-level value
```

`<whomp></whomp>`

However, when running this "bad" json string against the `json.NewDecoder().Decode(...)` method, it is surprising to see that there is no error!!! Instead, everything after the offensive line is simply ignored!

Here's an excerpt from the codeblock above:

```golang
// ... set up code here
var fields map[string][]string
reader := strings.NewReader(bad_json)
if err := json.NewDecoder(reader).Decode(&fields); err != nil {
	// => We EXPECT this 
	fmt.Println("Error %w", err)
}
// But instead, we get this! 
repr.Println(fields)
```

Executing our code yields the following output:

```golang
map[string][]string{
  "hello": []string{
    "foobar",
  },
}
```

([playground](https://play.golang.org/p/8al6NRe96jw))

**W.T.F!**

Ok, so - this is unexpected! 

We would **expect** the `err != nil` condition to be **true**, forcing the `fmt.Println(...)` line to run and for `fields` to be empty. 

To find the answer, we'll need to go spelunking into golang's `json.Decoder` source code and implementation.

(Heads up, [others](https://ahmet.im/blog/golang-json-decoder-pitfalls/#2-jsondecoder-silently-ignores-invalid-syntax) have also warned about the behavior we are seeing here. However we will demonstrate by the end of this post that the observed behavior is in fact expected (once we have a better understanding of what it is doing) and not _really_ wrong.)

Alright. Let's do this.

## Grokking the `json` pkg

Our interest primarily lies in two structs within the [`src/encoding/json`](https://golang.org/src/encoding/json/) pkg:

* [`json.Decoder`](https://golang.org/src/encoding/json/stream.go#L14)
* [`json.scanner`](https://golang.org/src/encoding/json/scanner.go#L64)

The `scanner` struct is an internal mechanism used by the `Decoder` to parse a JSON string. It defines a collection of `state transition functions` and transition values that manage tracking various phases of parsing the JSON string itself.

For example, consider the following func in [`scanner.go#L263`](https://golang.org/src/encoding/json/scanner.go#L263) to better understand how transition functions return transition values.

```golang
func stateBeginString(s *scanner, c byte) int {
	// ... non relevant code lines
	if c == '"' {
		s.step = stateInString
		return scanBeginLiteral
	}
	// ... non relevant code lines
}
```

This is an example of a "state transition function". It marks the beginning of parsing a value in JSON that starts with `"` character.

Notice here if our input char (`c byte`) is `"`, we update our `step` attribute to the _next_ state transition function, in this case `stateInString`. Furthermore, we return a new transition value: `scanBeginLiteral` (indicating that our scanner is currently in the process of interpreting a token literal such as a number or a string in our JSON string).

The transition values are primarily used by code that actually calls the `scanner.step` transition functions, such as `Decoder` or `decodeState`, to understand the current state of parsing by the scanner.


Here's the [full list](https://golang.org/src/encoding/json/scanner.go#L114) of transitions values defined and returned by `scanner` state transition functions:

```golang
const (
	// Continue.
	scanContinue     = iota // uninteresting byte
	scanBeginLiteral        // end implied by next result != scanContinue
	scanBeginObject         // begin object
	scanObjectKey           // just finished object key (string)
	scanObjectValue         // just finished non-last object value
	scanEndObject           // end object (implies scanObjectValue if possible)
	scanBeginArray          // begin array
	scanArrayValue          // just finished array value
	scanEndArray            // end array (implies scanArrayValue if possible)
	scanSkipSpace           // space byte; can skip; known to be last "continue" result

	// Stop.
	scanEnd   // top-level value ended *before* this byte; known to be first "stop" result
	scanError // hit an error, scanner.err.
)
```


The `Decoder` struct, which is public, manages an instance of scanner as an attribute and tracks the state of JSON parsing (using the transition values such as `scanEnd` or `scanEndArray`). The added twist here (and this is significant) is that `Decoder` loads a _portion_ of the JSON string into a `buf` attribute and the scanner processes the JSON string in portions, reading chars one at a time from `buf`.

In addition to tracking the `scanner`, the `Decoder` struct also manages an instance of `decodeState`, which is the mechanism used to actually unmarshal data read from the JSON via the `scanner`.

For the purposes of our exploration, we will largely ignore the `decodeState` struct and instead focus primarily on the specifics of `scanner` and a few methods of the `Decoder`.

## Tracing `bad_json` through `json.Decoder`

Hopefully that was a good (but brief) introduction to how the json decoder _generally_ works to parse strings. Let us now apply this understanding to our initial example:

```golang
	bad_json := `
{
  "hello": ["foobar"]
}", "foobaz"],
  "world": ["some other str"],
}`
```

This poorly formatted JSON string is processed with `json.Decoder` like so (repeating from example on top):

```golang
var fields map[string][]string
reader := strings.NewReader(bad_json)
if err := json.NewDecoder(reader).Decode(&fields); err != nil {
	fmt.Println("Error %w", err)
}
```

Let's start at `json.NewDecoder` and given our new (high level) understanding of how the decoding process generally works, attempt to pinpoint exactly why/how the `Decode` method defies our expectations and does **NOT** raise an err when processing the `bad_json` string.


### 1. `json.NewDecoder` instantiates a `json.Decoder` struct

To begin, `json.NewDecoder` creates a new `Decoder` struct with an `r` attribute that manages an `io.Reader` instance.

```golang
func NewDecoder(r io.Reader) *Decoder {
	return &Decoder{r: r}
}
```

([sauce](https://golang.org/src/encoding/json/stream.go#L27))

From the golang src, here's the full definition of type `Decoder`:

```golang
// A Decoder reads and decodes JSON values from an input stream.
type Decoder struct {
	r       io.Reader
	buf     []byte
	d       decodeState
	scanp   int   // start of unread data in buf
	scanned int64 // amount of data already scanned
	scan    scanner
	err     error

	tokenState int
	tokenStack []int
}
```

([sauce](https://golang.org/src/encoding/json/stream.go#L14))

For the purposes of this analysis, we really only care about the following fields:

```golang
type Decoder struct {
	scanp   int   // start of unread data in buf
	scan    scanner
	err     error
}
```

**scanp**

This is an index that we advance from position 0 to the length of our buffer. As we advance this index, we read a single character from the buffer and analyze it via the `scanner` state machine.

**scan**

An instance of the internal `json.scanner` struct. At each value of `scanp`, we read the character from buffer and pass it into the `scanner.step` func which processes state transitions such as `stateBeginString` or `stateInString` (more on this shortly)


**err**

We expect `err` to be NOT `nil` when we run into malformed JSON. Clearly as it stands from our observations, `err` **IS** `nil` which is the problem.

Ok so - now we have an instance of `Decoder` available to us that knows to read data from our `bad_json` into an internal buffer. Now, let's look at how the `Decoder.Decode(...)` method of our `Decoder` struct commences parsing our JSON data.

### 2. `Decoder.Decode(v)` internally calls `Decoder.readValue()`

Consider the following snippet from the `Decoder.Decode()` implementation below:

```golang
func (dec *Decoder) Decode(v interface{}) error {
	// ... non relevant code lines

	// Read whole value into buffer.
	n, err := dec.readValue()
	if err != nil {
		return err
	}
	// ... non relevant code lines

	return err
}
```

([sauce](https://golang.org/src/encoding/json/stream.go#L49))

We are only focusing on the method call relevant to our current analysis - there are conditionals checked _before_ `readValue` is executed, which are simply sanity checks for various poorly formatted string states. These conditional checks work as expected so for the purposes of this analysis they are "uninteresting".

In short, `dec.readValue()` uses the `dec.scan` (which, recall, is an instance of the `json.scanner` struct) attribute to process chars in the buffer one by one until an error or a `scanEnd` transition value state is reached. (This is the focus of the next section)

Similarly, assuming `dec.readValue()` does not generate an error, there is some additional work done by the `Decode` method (this is the part indicated as "non relevant code lines" above) that actually relies on the `decodeState` struct to unmarshal the bytes read and processed by the `scanner`.

Having looked at `Decode`, let's now look at the src for `readValue` to understand how the `scanner` is used to process data in our JSON string and more importantly, generate errors for invalid JSON.

### 3. `Decoder.readValue` processes chars w/`scanner.step()`

At this point it is clear that whatever the "issue" is here with the behavior we observe, it must be in `readValue`. This func is somewhat long so let's only look at the relevant lines:

```golang
func (dec *Decoder) readValue() (int, error) {
	dec.scan.reset()

	scanp := dec.scanp
	var err error
Input:
	// help the compiler see that scanp is never negative, so it can remove
	// some bounds checks below.
	for scanp >= 0 {

		// Look in the buffer for a new value.
		for ; scanp < len(dec.buf); scanp++ {
			c := dec.buf[scanp]
			dec.scan.bytes++
			switch dec.scan.step(&dec.scan, c) {
			case scanEnd:
				// scanEnd is delayed one byte so we decrement
				// the scanner bytes count by 1 to ensure that
				// this value is correct in the next call of Decode.
				dec.scan.bytes--
				break Input
			case scanEndObject, scanEndArray:
				// scanEnd is delayed one byte.
				// We might block trying to get that byte from src,
				// so instead invent a space byte.
				if stateEndValue(&dec.scan, ' ') == scanEnd {
					scanp++
					break Input
				}
			case scanError:
				dec.err = dec.scan.err
				return 0, dec.scan.err
			}
		}

		// ... non relevant code lines
}
```

([full sauce](https://golang.org/src/encoding/json/stream.go#L89))

Upon inspection of this snippet, it is clear that `readValue()` generates an error if our `scanner.step` func returns a `scanError` transition value.

Because we _can clearly see_ that the parsing of our `bad_json` does **not** raise an error, it must be that the `scanEnd` or `scanEndObject`/`scanEndArray` state is reached before the "bad" formatting is processed by the `scanner`.

Still, let's be sure. Let's do one final exercise and run through our `bad_json` to prove to ourselves that indeed state `scanEnd` or `scanEndObject`/`scanEndArray` is reached before a `scanError` state can be processed.

### 4. Stepping through `Decoder.readValue` with `bad_json`

For convenience, here is `bad_json` again:

```golang
	bad_json := `
{
  "hello": ["foobar"]
}", "foobaz"],
  "world": ["some other str"],
}`
```

Let's start from the beginning. We just instantiated a new `Decoder` using `json.NewDecoder`. 

When we instantiate a `Decoder` struct here, we expect the following initial attributes:

```golang
// which character in the JSON string are we currently considering?
dec.scanp => 0

// initial scanner
dec.scan => scanner{}
```
(There are others, but these are the two we care about for now).

We then call `Decode` to start processing our `bad_json` string. The first line in `readValue` is:

```golang
dec.scan.reset()
```

This method importantly sets our `scanner.step` state transition function to `stateBeginValue`. 

After some initialization steps, we end up at the big `for` loop in `readValue`. To make things easier to grok, let's look at (only) the for loop again:

```golang
// Look in the buffer for a new value.
for ; scanp < len(dec.buf); scanp++ {
	c := dec.buf[scanp]
	dec.scan.bytes++
	switch dec.scan.step(&dec.scan, c) {
	case scanEnd:
		// scanEnd is delayed one byte so we decrement
		// the scanner bytes count by 1 to ensure that
		// this value is correct in the next call of Decode.
		dec.scan.bytes--
		break Input
	case scanEndObject, scanEndArray:
		// scanEnd is delayed one byte.
		// We might block trying to get that byte from src,
		// so instead invent a space byte.
		if stateEndValue(&dec.scan, ' ') == scanEnd {
			scanp++
			break Input
		}
	case scanError:
		dec.err = dec.scan.err
		return 0, dec.scan.err
	}
}
```

`scanp` here pertains to our `dec.scanp` attribute which is initially set to `0` a few lines above. So, our first char is `{` from `bad_json`.

We call `dec.scan.step` and pass in a reference to `scanner` and `c = "{"` as args. If the three expected transition states are _not_ returned (`scanEnd`, `scanEndObject`, `scanEndArray`) the loop continues and we advance to the next character (in this case `\n`).


### 5. `bad_json` iteration table

To better understand this code as it steps through the chars in `bad_json`, let's consider a table that describes the "state" of `Decoder` and `Decoder.scanner` as we iterate.

---

Here are the column definitions:

`row`

Mainly so that we can look closely at a few rows of this table.

`ch`

The current character we are considering within `bad_json`

`scanp`

The index corresponding to our current char.

`step`

This reflects two key items:

* **now**: the _current_ step saved in the `scanner.step` attribute
* **next**: the _new_ step returned after the **state transition func** completed running
* **ret**: the **transition value** returned by the **state transition func**

`step.parseState`

The `scanner` also initializes a stack to keep track of opening and closing brackets (for instance, as we parse a JSON string if we encounter a `{`, we add `parseObjectKey` (an iota, [sauce](https://golang.org/src/encoding/json/scanner.go#L136)) which indicates that we are currently inside `{}` and have encountered only the left side)


---

To interpret the table below, consider the follow approach:

**1**: from [**stream.go#L103**](https://golang.org/src/encoding/json/stream.go#L103), determine the state transition function (the transition function corresponds to **now** under the **step** col).

```golang
switch dec.scan.step(&dec.scan, c) {
```

In the case of **Row 1**, it would be:

```golang
switch dec.scan.step(&dec.scan, "{") {
```

**2**: Find the **step** function in [**scanner.go**](https://golang.org/src/encoding/json/scanner.go#L213). Walk through it with `c = "{"` or `c = "\n"`, etc (whatever is in the **ch** col)

In the case of **Row 1**, our step function would be:

```golang
// stateBeginValue is the state at the beginning of the input.
func stateBeginValue(s *scanner, c byte) int {
	if isSpace(c) {
		return scanSkipSpace
	}
	switch c {
	case '{':
		s.step = stateBeginStringOrEmpty
		return s.pushParseState(c, parseObjectKey, scanBeginObject)
	// ... more cases here, not relevant
	}
	// ... more logic here, not relevant
}
```

([sauce](https://golang.org/src/encoding/json/scanner.go#L213))

**3**: If, in `scanner` src, `pushParseState` or `popParseState` is called within the transition func, expect col **step.parseState** to reflect the value added or removed.

In the case of **Row 1**, `pushParseState` is called with `parseObjectKey` so we end up with one item in that array.

**4**: Once the **step** function has completed, it should have a return value (the transition value) and a new **step** function (could be same as **now**). Expect col **step**'s **ret** to correspond with the returned transition value and **next** to correspond to the _new_ value of `scanner.step`

In the case of **Row 1**, our returned transition value is `scanBeginObject` and our new step function is `stateBeginStringOrEmpty`.

Rinse and repeat until `scanEnd` or `scanError` is encountered.

(Note that below `\s` is just shorthand for `' '`)

| row | ch  | scanp | step                                                                                                  | step.parseState                 |
|-----|-----|-------|-------------------------------------------------------------------------------------------------------|---------------------------------|
| 1   | {   | 0     | **now**: stateBeginValue<br /> **ret**: scanBeginObject<br /> **next**: stateBeginStringOrEmpty       | parseObjectKey                  |
| 2   | \n  | 1     | **now**: stateBeginStringOrEmpty<br /> **ret**: scanSkipSpace<br /> **next**: stateBeginStringOrEmpty | parseObjectKey                  |
| 3   | "   | 2     | **now**: stateBeginStringOrEmpty<br /> **ret**: scanBeginLiteral<br /> **next**: stateInString        | parseObjectKey                  |
| 4   | h   | 3     | **now**: stateInString<br /> **ret**: scanContinue<br /> **next**: stateInString                      | parseObjectKey                  |
| 5   | ... |       |                                                                                                       |                                 |
| 6   | "   | 8     | **now**: stateInString<br /> **ret**: scanContinue<br /> **next**: stateEndValue                      | parseObjectKey                  |
| 7   | :   | 9     | **now**: stateEndValue<br /> **ret**: scanObjectKey<br /> **next**: stateBeginValue                   | parseObjectKey                  |
| 8   | \s  | 10    | **now** : stateBeginValue <br /> **ret** : scanSkipSpace <br /> **next** : stateBeginValue            | parseObjectKey                  |
| 9   | [   | 11    | **now** : stateBeginValue <br /> **ret** : scanBeginArray <br /> **next** : stateBeginValueOrEmpty    | parseObjectKey, parseArrayValue |
| 10  | "   | 12    | **now** : stateBeginValueOrEmpty <br /> **ret** : scanBeginLiteral <br /> **next** : stateInString    | parseObjectKey, parseArrayValue |
| 11  | ... |       |                                                                                                       |                                 |
| 12  | ]   | 20    | **now** : stateEndValue <br /> **ret** : scanEndArray <br /> **next** : stateEndValue                 | parseObjectKey                  |
| 13  | \s  | -     | **now** : stateEndValue <br /> **ret** : scanSkipSpace <br /> **next** : stateEndValue                | parseObjectKey                  |
| 14  | }   | 21    | **now** : stateEndValue <br /> **ret** : scanEndObject <br /> **next** : stateEndValue                |                                 |
| 15  | \s  | -     | **now** : stateEndValue <br /> **ret** : scanEnd <br /> **next** : stateEndTop                        |                                 |


### 6. Making sense of the final iteration steps

Hopefully, that table is helpful in grokking how the decoding logic works. In particular, let's zoom in on the final 4 rows (12-15).


**Row 12 + 13**

Let's look at the `stateEndValue` func:

```golang
// stateEndValue is the state after completing a value,
// such as after reading `{}` or `true` or `["x"`.
func stateEndValue(s *scanner, c byte) int {
	// ... not relevant currently
	ps := s.parseState[n-1]
	switch ps {
	// ... other cases here, not relevant
	case parseArrayValue:
		if c == ',' {
			s.step = stateBeginValue
			return scanArrayValue
		}
		if c == ']' {
			s.popParseState()
			return scanEndArray
		}
		return s.error(c, "after array element")
	}
	return s.error(c, "")
}
```

([sauce](https://golang.org/src/encoding/json/scanner.go#L277))

Here's the row:

| row | ch  | scanp | step                                                                                                  | step.parseState                 |
|-----|-----|-------|-------------------------------------------------------------------------------------------------------|---------------------------------|
| 12  | ]   | 20    | **now** : stateEndValue <br /> **ret** : scanEndArray <br /> **next** : stateEndValue                 | parseObjectKey                  |




Because `c = "["`, we can see that `s.popParseState()` is called (which removes `parseArrayValue` from our `parseState` stack)

Importantly, we are returned `scanEndArray`, which - from `readValue()` - we see requires special handling:

```golang
// Look in the buffer for a new value.
for ; scanp < len(dec.buf); scanp++ {
	c := dec.buf[scanp]
	dec.scan.bytes++
	switch dec.scan.step(&dec.scan, c) {
	// ... other cases here, not relevant
	case scanEndObject, scanEndArray:
		// scanEnd is delayed one byte.
		// We might block trying to get that byte from src,
		// so instead invent a space byte.
		if stateEndValue(&dec.scan, ' ') == scanEnd {
			scanp++
			break Input
		}
	case scanError:
		dec.err = dec.scan.err
		return 0, dec.scan.err
	}
}
```

This feels a bit like cheating but essentially, since `scanEndArray` is returned by our step function, we explicitly call `stateEndValue` to test and see if we have reached `scanEnd`. 

Let's look at the relevant lines of `stateEndValue` to understand the logic:

```golang
// stateEndValue is the state after completing a value,
// such as after reading `{}` or `true` or `["x"`.
func stateEndValue(s *scanner, c byte) int {
	n := len(s.parseState)
	if n == 0 {
		// Completed top-level before the current byte.
		s.step = stateEndTop
		s.endTop = true
		return stateEndTop(s, c)
	}
	if isSpace(c) {
		s.step = stateEndValue
		return scanSkipSpace
	}
	// ... ignore logic here, not relevant right now
	return s.error(c, "")
}
```

If our `parseState` stack were empty, it _would_ return `scanEnd` which could complete our loop. Otherwise, since we pass in `c = ' '` here, we "short circuit" and return the same `step` transition function.

**Row 14 + 15**

The final two iterations are very similar to the previous two iterations. The key difference is for the _last_ iteration (row 15), our `parseState` stack ends up being empty. As such, we actually enter into the `n == 0` condition:

```golang
// excerpt from stateEndValue
if n == 0 {
	// Completed top-level before the current byte.
	s.step = stateEndTop
	s.endTop = true
	return stateEndTop(s, c)
}
```

and return the coveted `scanEnd` transition value. In our `readValue()` func:

```golang
switch dec.scan.step(&dec.scan, c) {
// ... other cases here, not relevant
case scanEndObject, scanEndArray:
	// scanEnd is delayed one byte.
	// We might block trying to get that byte from src,
	// so instead invent a space byte.
	if stateEndValue(&dec.scan, ' ') == scanEnd {
		scanp++
		break Input
	}
// ...
}
```

the `stateEndValue(&dec.scan, ' ') == scanEnd` condition is satisfied and we **break** out of our loop. 

> In other words, the `Decode()` method does NOT error because we stop processing our JSON string before the scanner has a change to encounter the malformed portion of our `bad_json` string!

Expounding on this a bit: when that final `}` is read, `Decoder` says: "ok! I'm done. I have a completed scan." For this reason, it **never actually even tries to read the _rest_ of the line** even though there are plenty more characters left to read.


Additionally, note that we _could_ get it to return an error btw, if we call `Decode` again - since now it will start at `"` (the first char after `}`) and it will definitely see and raise an error then.

Furthermore, if we neglected to have the closing `}` as our first character, `Decoder.Decode` would actually catch the problem earlier.

Basically, `Decode` will always respect the closing `}` because it is expecting to read a _stream_ of data - meaning it **expects** JSON of the form:

```text
{...}
{...}
{...}
```

or even:

```text
{...}{...}{...}
```

Therefore, using `Decode` to read a single JSON document is not ideal. However it is worth noting that if we really wanted to, we still could use `Decode` to parse a single doc - we simply must alter how we leverage `Decode` to fully read out document body. 

Personally, the _proper_ way to use `Decode` really ought to be like so:

```golang
package main
import (
	"encoding/json"
	"fmt"
	"strings"
	"io"
)

func readJsonStream(jsonStr string, fields map[string][]string) error {
	reader := strings.NewReader(jsonStr)
	dec := json.NewDecoder(reader)
	for {
		err := dec.Decode(&fields)
		if err == io.EOF {
			break
		}
		if err != nil {
			fmt.Println(err)
			fmt.Println(fields)
			return err
		}
	}
	fmt.Println(fields)
	return nil
}

func main() {
	ok_json := `
{
  "hello": ["foobar"]
}{"world": ["some other str"]}`
	fmt.Println("++++++++++++++++++ ok json +++++++++++++++++++")
	_ = readJsonStream(ok_json, map[string][]string{})
	
	bad_json := `
{
  "hello": ["foobar"]
}", "foobaz"],
  "world": ["some other str"],
}`	
	fmt.Println("++++++++++++++++++ bad json +++++++++++++++++++")
	_ = readJsonStream(bad_json, map[string][]string{})

	seemingly_bad_but_not_json := `
{}{"world": ["some other str"]}{}{}{}{"hello": ["foobar"]}`	
	fmt.Println("++++++++++++++++++ not actually bad json +++++++++++++++++++")
	_ = readJsonStream(seemingly_bad_but_not_json, map[string][]string{})
}
```

([playground](https://play.golang.org/p/onYb03udRjk))

output:

```text
++++++++++++++++++ ok json +++++++++++++++++++
map[hello:[foobar] world:[some other str]]
++++++++++++++++++ bad json +++++++++++++++++++
json: cannot unmarshal string into Go value of type map[string][]string
map[hello:[foobar]]
++++++++++++++++++ not actually bad json +++++++++++++++++++
map[hello:[foobar] world:[some other str]]
```

Here, we continously decode in a loop, breaking only when `io.EOF` is reached or a non-nil error is discovered. In fact, with this refactor, we actually can safely use `Decoder` to parse any arbitrary JSON strings!

## Final Remarks

In short - `json.Decoder` is _not_ meant to be a standalone JSON unmarshal-er. Use `json.Unmarshal` for that. However, for streaming JSON tasks it has a few nice features that are quite useful and assuming your input is indeed streaming json it does not _actually_ silently ignore invalid syntax.

Personally, I would update this [comment](https://golang.org/src/encoding/json/stream.go#L13) in the docs:

> A Decoder reads and decodes JSON values from an input stream.

to include some more context and background about expected usage of `Decode`. Based on current documentation, it is not unreasonable to assume `Decoder` might be used interchangeably with `Unmarshal` and then become surprised with the unexpected behavior.

But, after all is said and done: `json.Decoder`'s behavior is not actually a bug, if anything it's a feature!
