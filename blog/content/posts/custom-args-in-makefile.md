---
title: "Custom Args in Makefile"
date: 2021-01-03T00:59:04Z
---

{{<toc>}}


TL;DR: use `$(eval ARGS=${ARGS} [some additional arg])` within a make target to build custom argument sequences for commands wrapped by make targets - like `make test`

I expound further on the usecase and methodology below 👇

---

I like to wrap common tasks, such as running unit tests, around a make target.

This way, I can minimize the length of the command I need to run (ie: `make test` vs `go test ./... -race -coverprofile=c.out`)

However, as a project grows, it becomes necessary or just preferable to support a variety of permutations of the above. 

(Note: I am not advocating that one _ought_ to use make targets in this manner, just that if this route is chosen, there are patterns available to simplify things a bit).

## Without Makefile targets
For the sake of go, here are a few potential tests I'd like to be able to run:

### Run tests w/race conditions check

[Info](https://golang.org/doc/articles/race_detector.html)

```bash
go test ./... -race
```

### Run tests in "short" mode

[Info](https://golang.org/pkg/testing/#Short)

```bash
go test ./... -short
```
### Run tests w/verbose results in terminal

```bash
go test ./... -v
```

### Run tests for a specific package

```bash
go test ./my_awesome_pkg/...
```

### Run a specific test func in a specific package

```bash
go test ./my_awesome_pkg/... -r=TestFoobar
```

## Consolidating functionality within single Make target

Of course, the main issue that comes up here is: what if we wanted to mix and match some of these opts? (For instance, we might want to run tests on a specific package with verbose test output with race condition checks enabled.)

Again, assuming we'd like to reuse the `make test` interface, our make target can get really messy really quickly:

```Makefile
#   Usage:
#       make test-dev
#       make test-dev package=my_awesome_pkg
test:
ifdef package 
	go test -v ./${package}/... -coverprofile=c.out
else
	go test ./... -coverprofile=c.out
endif
```

In this example, we only support two use cases, run all tests in a single package and run all tests in all packages in current working directory. Even so, as you can probably see, it is easy to miss stuff (for instance, package tests have the verbose flag) and repetition can start to seep in (note the -coverprofile arg in both conditions).

An alternative (and personally, preferable approach might be):

```Makefile
#   Usage:
# 		make test norace=1
# 			Expl: run WITHOUT race conditions
# 		make test ftest=1
# 			Explt: run WITH "ftests", long lived non unit tests
# 		make test v=1
# 			Explt: run in verbose mode
# 		make test package=my_awesome_pkg
# 			Explt: run tests in a single package only
# 			NOTE: if omitted, will run ALL tests
# 		make test package=my_awesome_pkg func=TestViews
# 			Explt: run a single test func (needs package as well)
test:
	$(eval ARGS=)
# by default, run with race conditions
ifndef norace
	$(eval ARGS=${ARGS} -race)
endif
# by default, run in "short" mode
ifndef ftest
	$(eval ARGS=${ARGS} -short)
endif
ifdef v
	$(eval ARGS=${ARGS} -v)
endif
# if package provided, run the package
ifdef package
	$(eval ARGS=${ARGS} ./${package}/...)
else
	$(eval ARGS=${ARGS} ./...)
endif
# if func provided, run the func only
ifdef func
	$(eval ARGS=${ARGS} -run=${func})
endif
	go test ${ARGS} -coverprofile=c.out
```

In this approach, we use `$(eval ARGS=${ARGS} [append an arg]` to build the actual args for our `go test` invocation based on make target args.

What's nice about this technique is we can choose to make certain things default vs non default by leveraging make's `ifdef` and `ifndef` (if not defined) conditionals.

The last line is the actual test invocation and if we wanted to, we could always echo `${ARGS}` right before for debugging purposes, etc.

### Run tests w/race conditions check

```bash
go test ./... -race

# w/Make target
make test

# explicitly opt out of using the -race flag
make test norace=1
```

### Run tests in "short" mode

```bash
go test ./... -short

# w/Make target
make test ftest=1
```
> Note, using the targets you can abstract away the underlying go test CLI flags to something that is more contextually relevant to you, in this case mapping "ftests" to mean "short" mode.

### Run tests w/verbose results in terminal

```bash
go test ./... -v

# w/Make target
make test v=1
```

If you wanted to tack on a few functionalities into the same invocation, you can do so by:

```bash
make test v=1 ftest=1
```

This will run your tests in "verbose" mode and it will _not_ skip the "slower" tests that may reach out to a db or some other dependency.

### Run tests for a specific package

```bash
go test ./my_awesome_pkg/...

# w/Make target
make test package=my_awesome_pkg
```

### Run a specific test func in a specific package

```bash
go test ./my_awesome_pkg/... -r=TestFoobar

# w/Make target
make test package=my_awesome_pkg func=TestViews
```

As an additional exercise, consider adding functionality that may take multiple func args and run the tests for those args _only_.


## Final Remarks

I really like this approach and have started using it in a lot of my makefile target patterns where I leverage `make test` for dev-ing or ci related tasks. While I've walked through a golang based usecase, this pattern can be used for more or less any make target usage (though personally, I really only use this for running tests during dev/ci).