---
title: "Safely Construct Elasticsearch Queries w/Golang"
date: 2020-12-16T14:28:28Z
tags: ['golang']
---

{{<toc>}}
**TL; DR**: ya boy wrote a golang elasticsearch query dsl utility. [Find it here!](https://github.com/mottaquikarim/esquerydsl)

---

## **The Why**

If you've used elasticsearch with golang, then you've probably used the [official elasticsearch go client](https://github.com/elastic/go-elasticsearch).

The es go client is exhaustive and generally, pretty great. However, it can be a bit...scary when having to deal with constructing search queries using the [elasticsearch query dsl](https://www.elastic.co/guide/en/elasticsearch/reference/7.10/query-dsl.html)

Take for instance the following (from [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html#query-filter-context-ex) in the docs):

```json
GET /_search
{
  "query": { 
    "bool": { 
      "must": [
        { "match": { "title":   "Search"        }},
        { "match": { "content": "Elasticsearch" }}
      ],
      "filter": [ 
        { "term":  { "status": "published" }},
        { "range": { "publish_date": { "gte": "2015-01-01" }}}
      ]
    }
  }
}
```

### **Using strings**

In my experience, the simplest/fastest way to construct this json string is with...well, a string:

```go
elasticQuery := `
{
  "query": { 
    "bool": { 
      "must": [
        { "match": { "title":   "Search"        }},
        { "match": { "content": "Elasticsearch" }}
      ],
      "filter": [ 
        { "term":  { "status": "published" }},
        { "range": { "publish_date": { "gte": "2015-01-01" }}}
      ]
    }
  }
}
`
```

If we need to inject variable values, we just use `fmt.Sprintf` and move on with our lives. The primary issue here is that validating/formatting these json strings require additional work and can be error prone (ie: fat-fingering an additional comma somewhere, etc).

### **Using (use-case specific) structs**

The _other_ approach would be to make everything hyper specific and create structs / custom marshal-ers that would generate the query DSL json format when `json.Marshal` is called (on said custom struct(s)). 

This approach requires creating custom structs and code for the sole purpose of building these queries. (This may work for certain usecases! But, it also means more code and therefore additional maintenance and more trouble translating to other projects).

### **What does Google say?**

The best "documentation"/support I could find through google-fu was [this article](https://kb.objectrocket.com/elasticsearch/how-to-construct-elasticsearch-queries-from-a-string-using-golang-550) that also just suggested building a json string and crossing your fingers.

(excerpt from the blog post above):

```golang
func constructQuery(q string, size int) *strings.Reader {

	// Build a query string from string passed to function
	var query = `{"query": {`

	// Concatenate query string with string passed to method call
	query = query + q

	// Use the strconv.Itoa() method to convert int to string
	query = query + `}, "size": ` + strconv.Itoa(size) + `}`
	fmt.Println("\nquery:", query)

	// Check for JSON errors
	isValid := json.Valid([]byte(query)) // returns bool

	// Default query is "{}" if JSON is invalid
	if isValid == false {
		fmt.Println("constructQuery() ERROR: query string not valid:", query)
		fmt.Println("Using default match_all query")
		query = "{}"
	} else {
		fmt.Println("constructQuery() valid JSON:", isValid)
	}

	// Build a new string from JSON query
	var b strings.Builder
	b.WriteString(query)

	// Instantiate a *strings.Reader object from string
	read := strings.NewReader(b.String())

	// Return a *strings.Reader object
	return read
}
```

Finally, there was [this issue](https://github.com/elastic/go-elasticsearch/issues/42) on the go elasticsearch client from 2019:

> This package is intentionally a low-level client, while olivere/elastic is a high-level client with extensions for building the requests and deserializing the responses. We are aiming for offering a more high-level API in the future, but — as I've indicated in other tickets — no sooner than a machine-readable, formal specification of the request and response bodies is available.

Moreover (and awesomely, that comment thread has a gem of a code snippet):

```golang
// BoolQuery Elastic bool query
type BoolQuery struct {
	Bool BoolQueryParams `json:"bool"`
}

// BoolQueryParams params for an Elastic bool query
type BoolQueryParams struct {
	Must               interface{} `json:"must,omitempty"`
	Should             interface{} `json:"should,omitempty"`
	Filter             interface{} `json:"filter,omitempty"`
	MinimumShouldMatch int         `json:"minimum_should_match,omitempty"`
}
```

that looks very similar to what I've ended up with (wish I had seen this first, heh) as I tackled this problem.

Regardless the main point is this:

> Currently there isn't an easy way to define query DSL json strings for use with the elasticsearch go client.

And - for good reason perhaps - the official client looks like it will not support such a feature anytime soon.

## **`package esquerydsl`**

For all these reasons, I decided to build a simple, dependency less (aside from go stdlib deps) utility that generically defines structs to build queryDSL json strings.

Here's an example ([playground](https://play.golang.org/p/tlSkQH1mUGy))

```golang
package main

import (
	"fmt"

	"github.com/mottaquikarim/esquerydsl"
)

func main() {
	_, body, _ := esquerydsl.GetQueryBlock(esquerydsl.QueryDoc{
		Index: "some_index",
		Sort:  []map[string]string{map[string]string{"id": "asc"}},
		And: []esquerydsl.QueryItem{
			esquerydsl.QueryItem{
				Field: "some_index_id",
				Value: "some-long-key-id-value",
				Type:  "match",
			},
		},
	})
	fmt.Println(body)
}
```

The output:

```json
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "some_index_id": "some-long-key-id-value"
          }
        }
      ]
    }
  },
  "sort": [
    {
      "id": "asc"
    }
  ]
}
```

(Find more examples in tests, including the initial queryDSL example referenced at the top of this post [here](https://github.com/mottaquikarim/esquerydsl/blob/master/esquerydsl_test.go#L26))

PRs welcome! Especially re: unittests such that documentation coverage is increased. If you use this lib and it is useful, do let me know please!

Happy querying, fam 👍

