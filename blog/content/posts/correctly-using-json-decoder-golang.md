---
title: "You might not be using json.Decoder correctly in golang"
date: 2021-01-24T04:01:51Z
---

{{<toc>}}

TL;DR: prevailing "secondary source" wisdom (ie: blog posts) about `json.Decoder` don't demonstrate the proper way to use it.

---

This post is a follow up to my (kinda lengthy) [deep dive]({{<ref "posts/is-json-decoder-broken-in-golang.md">}} "deep dive") into what I _thought_ was a bug in golang's `json.Decoder` pkg.

Instead, I realized that generally speaking, `json.Decoder` can be misunderstood - which _may_ lead to unintended consequences. In this post, I will demonstrate a safer pattern that ought to be used instead of the prevailing wisdom.

## Googling: **"json.decoder example golang"**

I ran a few google searches queries using some permutation of the following:

> json.decoder example golang

The results were your standard mix of documentation from `golang.org`, blog posts on `medium.com`/random mom&pop devsites (like this one!), and a few `stackoverflow` threads.

![Google Search](/dev/img/google-json-decoder.png)

Fortunately, results from `golang.org` are highly ranked - while it may be a bit harder to parse through golang's src code, the documentation is fairly thorough and more importantly: **correct**. _(Personally, I would have preferred some additional context in the docs expounding on some of the gotchas I discuss on my other post but I digress)_

Some of the threads I observed in Stack Overflow that referenced `json.Decoder` pulled directly from the docs (and therefore were also correct). Other's (probably) pulled from medium/other blog post sites similar to the ones I found googling around and were inaccurate/advocating incorrect usage.

For example, on Medium, et al - I saw a wide array of posts (such as [this](https://medium.com/what-i-talk-about-when-i-talk-about-technology/go-code-snippet-json-encoder-and-json-decoder-818f81864614), [this](https://itnext.io/welcome-to-just-enough-go-7dbef7e30188), [this](https://stackoverflow.com/q/28814366) or [this](https://medium.com/rungo/working-with-json-in-go-7e3a37c5a07b)) that suggested using `json.Decoder` in some way, shape, or form similarly to this:

```golang
func main() {
    jsonData := `{
"email":"abhirockzz@gmail.com",
"username":"abhirockzz",
"blogs":[
	{"name":"devto","url":"https://dev.to/abhirockzz/"},
	{"name":"medium","url":"https://medium.com/@abhishek1987/"}
]}`
    
    jsonDataReader := strings.NewReader(jsonData)
    decoder := json.NewDecoder(jsonDataReader)
    var profile Profile
    err := decoder.Decode(&profile)
    if err != nil {
        panic(err)
    }
    // ...
}
```
_(Example pulled from [Tutorial: How to work with JSON data in Go](https://itnext.io/welcome-to-just-enough-go-7dbef7e30188))_

## The Problem

On the surfact, this code looks sound. I forklifted the src into [go playground](https://play.golang.org/p/qy-7BIx_FlA) and ran it. 

```golang
package main

import (
	"encoding/json"
	"strings"
)

func main() {
    jsonData := `{
"email":"abhirockzz@gmail.com",
"username":"abhirockzz",
"blogs":[
	{"name":"devto","url":"https://dev.to/abhirockzz/"},
	{"name":"medium","url":"https://medium.com/@abhishek1987/"}
]}`
    
    jsonDataReader := strings.NewReader(jsonData)
    decoder := json.NewDecoder(jsonDataReader)
    var profile map[string]interface{}
    err := decoder.Decode(&profile)
    if err != nil {
        panic(err)
    }
    // ...
}
```
_(Note, changed `profile` to `map[string]interface{}` to make the code run)_

...It works! Great. But, what happens if we fubar the JSON string?


```golang
package main

import (
	"encoding/json"
	"strings"
)

func main() {
    jsonData := `{
"email":"abhirockzz@gmail.com",
"username":"abhirockzz",
"blogs":[
	{"name":"devto","url":"https://dev.to/abhirockzz/"},
	{"name":"medium","url":"https://medium.com/@abhishek1987/"}
]}THIS IS INTENTIONALLY MALFORMED NOW`
    
    jsonDataReader := strings.NewReader(jsonData)
    decoder := json.NewDecoder(jsonDataReader)
    var profile map[string]interface{}
    err := decoder.Decode(&profile)
    if err != nil {
        panic(err)
    }
    // ...
}
```
_([playground](https://play.golang.org/p/MyM1A8Y51Jc))_

...It works!

Wait...**WTF?!**. 

This code should _not_ work at all! Our JSON string is clearly malformed and we expect - based on the logic - the code to panic.

This is the entire issue in a nutshell. I expound in detail in my other post but in one (kinda long) sentence:

>  `json.Decoder.Decode` was implemented for parsing _streaming_ JSON data, meaning it will **always** traverse the JSON string until it finds a satisfactory, closing bracket (I use the term _satisfactory_ here because it does use a stack to keep track of inner brackets).

So, in order to detect the malformed json, we must actually run this logic in a loop - like so:

```golang
package main

import (
	"encoding/json"
	"io"
	"strings"
)

func main() {
	jsonData := `{
"email":"abhirockzz@gmail.com",
"username":"abhirockzz",
"blogs":[
	{"name":"devto","url":"https://dev.to/abhirockzz/"},
	{"name":"medium","url":"https://medium.com/@abhishek1987/"}
]}THIS IS INTENTIONALLY MALFORMED NOW`

	jsonDataReader := strings.NewReader(jsonData)
	decoder := json.NewDecoder(jsonDataReader)
	var profile map[string]interface{}
	for {
		err := decoder.Decode(&profile)
		if err != nil {
			panic(err)
		}
		if err == io.EOF {
			break
		}
	}

	// ...
}

```
_([playground](https://play.golang.org/p/TqIiLzNdtpi))_


Note the key diff here:

```golang
var profile map[string]interface{}
for {
	err := decoder.Decode(&profile)
	if err != nil {
		panic(err)
	}
	if err == io.EOF {
		break
	}
}
// ...
```

## The Fix

From the golang docs, this example says it best:

```golang
// This example uses a Decoder to decode a stream of distinct JSON values.
func ExampleDecoder() {
	const jsonStream = `
	{"Name": "Ed", "Text": "Knock knock."}
	{"Name": "Sam", "Text": "Who's there?"}
	{"Name": "Ed", "Text": "Go fmt."}
	{"Name": "Sam", "Text": "Go fmt who?"}
	{"Name": "Ed", "Text": "Go fmt yourself!"}
`
	type Message struct {
		Name, Text string
	}
	dec := json.NewDecoder(strings.NewReader(jsonStream))
	for {
		var m Message
		if err := dec.Decode(&m); err == io.EOF {
			break
		} else if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("%s: %s\n", m.Name, m.Text)
	}
	// Output:
	// Ed: Knock knock.
	// Sam: Who's there?
	// Ed: Go fmt.
	// Sam: Go fmt who?
	// Ed: Go fmt yourself!
}
```
_([sauce](https://golang.org/src/encoding/json/example_test.go#L57))_

In this usage, we create a new `json.Decoder` instance from the `NewDecoder` method and then continually loop and try to decode a chunk of our JSON string until we detect the end of the string (sucessfully breaking out of the loop) or an error.

I would take this a step further and only prefer to use `json.Decoder` when I am specifically working with streaming JSON data.

At any rate, this the The Way. Please keep this in mind going forward should you choose to use `json.Decoder` for your JSON string parsing needs.

## A few notes

* A big caveat I'd like to point out is that I did not perform any rigorous analysis of golang examples in the wild when I was inspired to write this post. My analysis comes largely from anecdotal examples I observed while researching my other deep dive article about the nature of `json.scanner` and `json.Decoder.Decode`.
* I certianly am not being critical of the medium/mom&pop blogs I linked to earlier, instead I am merely pointing out that it is _very_ easy to assume that the trivial usage of `json.Decoder.Decode` presented on those posts is generally correct when in actuality this is not the case.
* I think someone (maybe me? perhaps you?) ought to open a PR against godocs to clarify gotchas/differences between `json.Decoder` usage vs `json.Unmarshal`

