---
title: "Is json.Decoder broken in golang?!"
date: 2021-01-14T01:26:01Z
---

{{<toc>}}

**TL;DR**: No.

Although unintuitive, **`json.Decoder`** isn't actually (_that_) evil! However, it can be unintuitive and **seemingly** wrong if used incorrectly. So - tread carefully.

In this post, I will dive into how **`json.Decoder`** seems to work and try and make sense of some observed behaviors.

--

## The "Issue"

Consider the following:

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

Clearly, we have a JSON string that is invalid here. So, what should we expect this code to do? 

And more importantly, empirically speaking, what does it _seem_ to do?

Let us begin by first looking at our JSON string more closely:

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


As such, we would expect any attempt at parsing to fail. Indeed, **json.Unmarshal**-ing this dude expectedly fails:

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

However, when running this "bad" json string against the the `json.NewDecoder` method, there is no error! Instead, everything after the offensive line is simply ignored!

Here's an excerpt from the codeblock above:

```golang
// ... set up code here
var fields map[string][]string
	reader := strings.NewReader(bad_json)
	if err := json.NewDecoder(reader).Decode(&fields); err != nil {
		fmt.Println("Error %w", err) // no error!
	}
	repr.Println(fields) // instead, we get this
```

This code above outputs the following:

```golang
map[string][]string{
  "hello": []string{
    "foobar",
  },
}
```

([playground](https://play.golang.org/p/8al6NRe96jw))

**WTF!**

This is unexpected! We would **expect** the `err != nil` condition to be true, forcing the `fmt.Println(...)` line to run and for `fields` to be empty. 

But like... **WHY?!** tho?

To find the answer, let's take a dive into the `json.Decoder` source.

(Heads up, [others](https://ahmet.im/blog/golang-json-decoder-pitfalls/#2-jsondecoder-silently-ignores-invalid-syntax) have also warned about the behavior we are seeing here. But we will see by the end of this post that the behavior highligted is in fact expected and not _really_ wrong.)

Alright. Let's do this.

## How **`json.Decode`** works

There are two major files in the **`json`** pkg we will want to consider for our exploration:

* **[src/encoding/json/stream.go](https://golang.org/src/encoding/json/stream.go)**
* **[src/encoding/json/scanner.go](https://golang.org/src/encoding/json/scanner.go)**

Let's begin with this line of code from our playground example:

```golang
if err := json.NewDecoder(reader).Decode(&fields); err != nil {
	fmt.Println("Error %w", err) // no error!
}
```

and start tracing it from **stream.go**. **`json.NewDecoder()`** simply returns a **Decoder** struct, which looks like this:

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

* **scanp**: The Decoder will track the current index of str in buffer
* **scar**: An instance of the internal `json.scanner` struct - this manages the logic of JSON parsing (mainly)
* **err**: We expect `err` to be NOT `nil` when we run into malformed JSON, clearly as it stands from our observations, `err` **IS** `nil` which is the problem.

 Our goal then, is to **figure out why** `Decoder.err` is `nil` when we run into the first character in our JSON string that is invalid.

 Let's now consider **`json.Decder.Decode()`**, our entrypoint invoked to actually decode our JSON string into a go datastruct:

 ```golang
func (dec *Decoder) Decode(v interface{}) error {
	if dec.err != nil {
		return dec.err
	}

	if err := dec.tokenPrepareForDecode(); err != nil {
		return err
	}

	if !dec.tokenValueAllowed() {
		return &SyntaxError{msg: "not at beginning of value", Offset: dec.InputOffset()}
	}

	// Read whole value into buffer.
	n, err := dec.readValue()
	if err != nil {
		return err
	}
	dec.d.init(dec.buf[dec.scanp : dec.scanp+n])
	dec.scanp += n

	// Don't save err from unmarshal into dec.err:
	// the connection is still usable since we read a complete JSON
	// object from it before the error happened.
	err = dec.d.unmarshal(v)

	// fixup token streaming state
	dec.tokenValueEnd()

	return err
}
 ```

Let's break this up conditional by conditional:

```golang
if dec.err != nil {
	return dec.err
}
```

Of course, when we start, `dec.err` is `nil` so nothing to do here.

```golang
if err := dec.tokenPrepareForDecode(); err != nil {
	return err
}
```

The purpose of this method is to advance our `scanp` attribute if we witness a comma **,** or colon **:** before we continue. (See for yourself [here](https://golang.org/src/encoding/json/stream.go#L306)) 

```golang
if !dec.tokenValueAllowed() {
	return &SyntaxError{msg: "not at beginning of value", Offset: dec.InputOffset()}
}
```

This is another helper method that ensures we are not parsing something random, like `35": "abc"`. (If you want, feel free to validate these, here's a [playground](https://play.golang.org/p/nasJAYUDsow) link -- the output may look weird but the error struct is defined in [src/encoding/json/decode.go#L124](https://golang.org/src/encoding/json/decode.go#L124))

Ok **NOW** here is the fun part:

```golang
// Read whole value into buffer.
n, err := dec.readValue()
if err != nil {
	return err
}
```

`readValue` pulls in our JSON string into buffer and presumably parses it as it reads. We **expect**, therefore, that `readValue()` ought to return an `err`. However, it does not.

This method is a bit long, so we will only look at a few specific lines. Find the entire source [here](https://golang.org/src/encoding/json/stream.go#L89).

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

		// ... more stuff here ...
}
```

Upon inspecting this bit of code, a few things are clear:

* **readValue** is where the meat of our functionality lives - `scanp` advances here as we compare each character in our buffer against the `dec.scan.step` function.
* The output of `dec.scan.step` appears to be `iota`s that we use to check for various states.
* it is clear that `scanError` is the only time we can expect to get any true error. 

However, since we are _not_ seeing our expected error output, it **must** mean the code is getting lost in `case scanEnd` or `case scanEndObject, scanEndArray` somewhere. 

To proceed further, we will not have to jump one final level into the **[src/encoding/json/scanner.go](https://golang.org/src/encoding/json/scanner.go)** file.

## Understanding **`json.scanner`** state transition functions

The first bit of code to consider is this:

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

([sauce](https://golang.org/src/encoding/json/scanner.go#L114))

These values are returned by the `scanner`'s state transition functions which help us keep track of _where_ we are as we consume our JSON string char by char.

IN particular, note that `scanEnd, scanEndObject, scanEndArray, scanError` are all present here. Three of these four vars are used in `func stateEndValue` ([sauce](https://golang.org/src/encoding/json/scanner.go#L277)). As it turns out, understanding how `stateEndValue` works will actually bring our efforts to fruition and explain why this functionality works in the way that it does.

But first - what the heck are these `state*` funcs anyways?

Let's start by looking at the `scanner` type definition, the `reset()` method and the `stateBeginValue` function (only relevant parts displayed):

```golang
type scanner struct {
	// The step is a func to be called to execute the next transition.
	// Also tried using an integer constant and a single func
	// with a switch, but using the func directly was 10% faster
	// on a 64-bit Mac Mini, and it's nicer to read.
	step func(*scanner, byte) int

	// ... more attrs here

	// Stack of what we're in the middle of - array values, object keys, object values.
	parseState []int

	// ... more attrs here
}

// ... more definitions/methods here

// reset prepares the scanner for use.
// It must be called before calling s.step.
func (s *scanner) reset() {
	s.step = stateBeginValue
	s.parseState = s.parseState[0:0]
	// ... more lines of code here
}

// stateBeginValue is the state at the beginning of the input.
func stateBeginValue(s *scanner, c byte) int {
	if isSpace(c) {
		return scanSkipSpace
	}
	switch c {
	case '{':
		s.step = stateBeginStringOrEmpty
		return s.pushParseState(c, parseObjectKey, scanBeginObject)
	case '[':
		s.step = stateBeginValueOrEmpty
		return s.pushParseState(c, parseArrayValue, scanBeginArray)
	case '"':
		s.step = stateInString
		return scanBeginLiteral
	// ... more cases here
	}
	// ... more code here
}
```

Sauce(s)

* **[scanner](https://golang.org/src/encoding/json/scanner.go#L64)**
* **[reset()](https://golang.org/src/encoding/json/scanner.go#L148)**
* **[stateBeginValue](https://golang.org/src/encoding/json/scanner.go#L202)**


Looking at this code, it starts to become clearer that `scanner.state` stores a function that stores the logic to perform the next "transition" (ie: going from "{" to the "\"" char or from "5" to "]" in a list of nums, etc).

`reset()` gets us started with our initial state and each state function uses consts such as `scanEndObject` or `scanEndArray` to help represent and facilitate the transition.  

## Understanding **`json.Decode(...)`** behavior, but really tho

Let's now apply our observations to how decoding works (and then we will walk through our malformed JSON example).


Suppose we had the following JSON string:

```json
{}
```

and we wanted to decode this with `json.Decoder.Decode(...)`. (NOTE: the examples in the subsections below will primarily be pseudocode to make grokking this easier).

### 1. Init Decoder.

```golang
dec := json.Decoder{r: strings.NewReader(`{}`)}
/*
dec.scanp == 0
dec.scan == &scanner{}
*/
```

This will set our inital `scanp` int to 0 and initialize a new `json.scanner` for us

Here are the main variables we will keep track of:

```golang
// which character in the JSON string are we currently considering?
dec.scanp

// what is our transition function?
dec.scan.step

// are we in an open "{"? "["? are they balanced?
dec.scan.parseState

```

### 2. Invoke **`json.Decoder.Decode(...)`** (calls **`readValue()`**)

```golang
err := dec.Decode(interface{}{})
```

This called `dec.readValue()` which first resets our scanner:

```golang
dec.readValue()
```

Our state currently:

```golang
dec.scanp = 0

// this is our starting transition function
dec.scan.step == stateBeginValue 

// empty
dec.scan.parseState = []int{}
```

### 3. **`readValue()`** begins advancing scanp from 0.


These lines within `readValue` are invoked:

```golang
// Look in the buffer for a new value.
for ; scanp < len(dec.buf); scanp++ {
	c := dec.buf[scanp]
	dec.scan.bytes++
	switch dec.scan.step(&dec.scan, c) {
	// ... more stuff
```

Because `dec.scanp` is `0`, we know that `c` from above is:
```golang
switch dec.scan.step(&dec.scan, "{") 
```

And in scanner, `stateBeginValue` processes this as:

```golang
// ... c is "{" currently
switch c {
	case '{':
		s.step = stateBeginStringOrEmpty
		return s.pushParseState(c, parseObjectKey, scanBeginObject)
// ... 
```

Our `dec.scan.parseState` contains a reference to `{` indicating we are within brackets.

Because `readValue` handles custom logic on `scanEnd`, `scanEndObject, scanEndArray` or `scanError` and since our `stateBeginValue` raised no errors, our step advances to: `stateBeginStringOrEmpty`

Our state currently:

```golang
dec.scanp = 1

// this is our starting transition function
dec.scan.step == stateBeginStringOrEmpty 

// empty
dec.scan.parseState = []int{scanBeginObject,}
```

(`scanBeginObject` is a golang `iota` (or, enum if you will) representing our opening curly bracket)

### 4. **`scanp`** advances us to the next and final char: `}`


here's what the `stateBeingStringOrEmpty` func looks like:

```golang
// stateBeginStringOrEmpty is the state after reading `{`.
func stateBeginStringOrEmpty(s *scanner, c byte) int {
	if isSpace(c) {
		return scanSkipSpace
	}
	if c == '}' {
		n := len(s.parseState)
		s.parseState[n-1] = parseObjectValue
		return stateEndValue(s, c)
	}
	return stateBeginString(s, c)
}

```

In our case, `c` is `}` so we will "pop" our parseState stack and return `stateEndValue` which will give us one of the `scanEnd`, `scanEndObject, scanEndArray` terms we want in `readValues`.

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
	// ... more stuff here ...
}
```

`stateEndValue` then advances us to `stateEndTop` (since our `parseState` was just emptied by the previous `stateBeginStringOrEmpty`). Now this _will_ return - you guessed it - `scanEnd`!

```golang
// stateEndTop is the state after finishing the top-level value,
// such as after reading `{}` or `[1,2,3]`.
// Only space characters should be seen now.
func stateEndTop(s *scanner, c byte) int {
	if !isSpace(c) {
		// Complain about non-space byte on next call.
		s.error(c, "after top-level value")
	}
	return scanEnd
}
```

```golang
dec.scanp = 1

// this is our starting transition function
dec.scan.step == stateEndTop 

// empty
dec.scan.parseState = []int{}
```

## Cleaning up

At this point, we end up back in `readValue`, where:

```golang
func (dec *Decoder) Decode(v interface{}) error {
	// ... code here, ignoring

	// Read whole value into buffer.
	n, err := dec.readValue()
	if err != nil {
		return err
	}
	dec.d.init(dec.buf[dec.scanp : dec.scanp+n])
	dec.scanp += n

	// Don't save err from unmarshal into dec.err:
	// the connection is still usable since we read a complete JSON
	// object from it before the error happened.
	err = dec.d.unmarshal(v)

	// fixup token streaming state
	dec.tokenValueEnd()

	return err
}
```

As we can see here:

```golang
dec.d.init(dec.buf[dec.scanp : dec.scanp+n])
```
we initialize `dec.d` with all the characters we read in `readValue` which is then used to unmarshal our data. (`readValue` returns the number of bytes we read till `scanEnd`, we never actually update the `scanp` attribute on the struct so we use those two ints to figure out how many characters to initialize with. Then we update the stuct 'scanp' with the number of chars we read so that we don't reread the same data twice)

## Explaining our intial observation

So - having gone through that exercise, let's now finally go back and explain our initial issue:

```golang
	bad_json := `
{
  "hello": ["foobar"]
}", "foobaz"],
  "world": ["some other str"],
}`
```

What's happening here is this:

```golang
}", "foobaz"],
```

When that final `}` is read, `Decoder` says: "ok! I'm done. I have a completed scan." For this reason, it **never actually even tries to read the _rest_ of the line**. 

We _could_ get it to return an error btw, if we call `Decode` again - since now it will start at `"` (the first char after `}`) and it will definitely see and raise an error then.

Furthermore, if we neglected to have the closing `}` as our first character, `Decoder.Decode` would catch the problem earlier.

Basically, `Decode` will always respect the closing `}` because it is reading a _stream_ of data - meaning it **expects** JSON of the form:

```golang
/*
{...}
{...}
{...}
*/
```

or even:

```golang
/*
{...}{...}{...}
*/
```

And for what it's worth, the _proper_ way to use `json.Decode` really ought to be used like so:

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

```golang
/*
++++++++++++++++++ ok json +++++++++++++++++++
map[hello:[foobar] world:[some other str]]
++++++++++++++++++ bad json +++++++++++++++++++
json: cannot unmarshal string into Go value of type map[string][]string
map[hello:[foobar]]
++++++++++++++++++ not actually bad json +++++++++++++++++++
map[hello:[foobar] world:[some other str]]
*/
```

## Final Remarks

In short - `json.Decoder` is _not_ meant to be a standalone JSON unmarshal-er. Use `json.Unmarshal` for that. However, for streming JSON tasks it has a few nice features that are quite useful and assuming your input is indeed streaming json it does not _actually_ silently ignore invalid syntax.

In other words - `json.Decoder`'s behavior is not a bug, it's a feature!