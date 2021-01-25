---
title: "Integrating Code Climate w/go pkgs"
date: 2021-01-01T14:28:32Z
tags: ["golang"]
---

{{<toc>}}

TL; DR: When integrating golang code coverage with Code Climate, be sure to set the `--prefix` arg (set it to your pkg github prefix, ie: "github.com/mottaquikarim/esquerydsl") in the `after-build` stage in order for your src code to be recognized by the test reporter.

If ^^ that didn't make sense, read on below for the full background 👍

---

I've recently published a golang pkg, called [esquerydsl](https://github.com/mottaquikarim/esquerydsl), which facillitates safe construction of elasticsearch queries in golang.

In order to ensure future stability, I wanted to integrate [Code Climate](https://codeclimate.com/) for tracking maintainability and test coverage.

I've used CC before on python projects but never for go and while integrating, I ran into a gotcha that I thought I ought to document / share.

## Step 0: Write and run some tests!

I won't expound on the actual source code and instead focus on how to run and export test + results to code climate.

Running tests in go is super easy:

```bash
go test ./...
```

I prefer to work in docker so I usually run the above as:

```bash
docker run -w /app -v ${PWD}:/app golang:1.15 go test ./...
```
(All examples here on out will be run in docker)

Let's break this down before continuing:

* `docker run`: within a docker container, let's run some stuff
* `-w /app`: our "working directory" will be the `app` folder
* `-v ${PWD}:/app`: we volume mount our current working directory into the "working directory" in the container. This is a nice trick for quickly running tests on source code you are writing during dev
* `golang:1.15`: the image we want to run - in this case, golang v1.15
* `go test ./...`: finally, the command we want to run in our docker container - which is of course our go test command

### Track code coverage

Tracking code coverage in golang is also super easy. We just need to add a single arg to your `go test` command:

```bash
-coverprofile=c.out
```
The `-coverprofile` arg tells go where to publish the test coverage results, which can be parsed later on to help visualize your source code's coverage results.

Putting it all together:
```bash
docker run -w /app -v ${PWD}:/app golang:1.15 go test ./... -coverprofile=c.out
```

Now, there is a file called `c.out` which is available in your current working directory that encodes your line-by-line test coverage data. Great! All we have to do now is upload this to code climate and we are golden.

### Sidebar: generating code coverage results as HTML

This is a proper tangent, so feel free to ignore. 

---

I find it super useful to understand/view which lines I missed in my unit tests. While line by line test coverage does not necessarily guarantee stability, I find it to be a useful benchmark for knowing when to _stop_ writing unit tests (somewhere around 90+% is my 👍 point)

To visualize this in go, run the following after your tests:

```bash
docker run -w /app -v ${PWD}:/app golang:1.15 go tool cover -html=c.out -o coverage.html
```

`coverage.html` can be opened in your browser to walk through your src code and it will visually indicate which lines have been covered by your tests and which lines have been missed.

### Getting started with CodeClimate

I'm going to skip this because otherwise this post will get _long_. My assumption is folks reading this already have a CC Quality account and have a (golang!) repo set up for usage.

## Step 1: Downloading the test reporter

Download and run the Code Climate test reporter. Of course, we want to do this in our docker container (there are plenty of examples available on how to do this "bare" around the internet). For me, this entailed:

```bash
# 1. download CC test reported
CC_URL=https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64
docker run -w /app -v ${PWD}:/app golang:1.15 \
	/bin/bash -c \
	"curl -L ${CC_URL} > ./cc-test-reporter"
	
# 2. update perms
docker run -w /app -v ${PWD}:/app golang:1.15 chmod +x ./cc-test-reporter

# 3. run before build
docker run -w /app -v ${PWD}:/app \
	-e CC_TEST_REPORTER_ID=${CC_TEST_REPORTER_ID} \
	golang:1.15 ./cc-test-reporter before-build
```

The three main parts here:

1. We need to download the test reporter, which is available to `curl` via the `CC_URL`. I run this in two steps in a single docker `run` command which is why I have the `/bin/bash -c "...steps to run..."` line (you can do it in two lines if needed as well)
2. Update perms to make this download executable. Notice that I run `chmod` on the renamed file `cc-test-reporter` (you can call this whatever you want) within the container itself.
3. Finally, run `before-build` which sets up the test reporter to send the coverage data. The `CC_TEST_REPORTER_ID` is significant - this is how CC authenticates your repo's code coverage as really from you. I have it as an envvar since it should not be committed to code anywhere

## Step 2: Running the tests with code coverage

This step is easy, basically Step 0:

```bash
docker run -w /app -v ${PWD}:/app golang:1.15 go test ./... -coverprofile=c.out
```

## Step 3: Running the after build

This is where I ran into my issue. The easy / documented step is this:

```
# upload data to CC
docker run -w /app -v ${PWD}:/app \
	-e CC_TEST_REPORTER_ID=${CC_TEST_REPORTER_ID} \
	golang:1.15 ./cc-test-reporter after-build
```

This is pretty standard at this point: we run the `cc-test-reporter` with the `after-build` arg as directed by CodeClimate. And, we pass along the `CC_TEST_REPORTER_ID` to property identify ourselves. However, the kicker is the command above _alone_ will not work!

When I ran the line above for my `esquerydsl` package (heads up, I temporarily added the `--debug` flag too), I ended up with the following output:

```bash
time="2020-12-31T19:52:57Z" level=error msg="failed to read file github.com/mottaquikarim/esquerydsl/esquerydsl.go\nopen github.com/mottaquikarim/esquerydsl/esquerydsl.go: no such file or directory"
Error: open github.com/mottaquikarim/esquerydsl/esquerydsl.go: no such file or directory
```

To fix, it looks like the `--prefix` is required, as follows:

```bash
docker run -w /app -v ${PWD}:/app \
	-e CC_TEST_REPORTER_ID=${CC_TEST_REPORTER_ID} \
	golang:1.15 ./cc-test-reporter after-build --prefix=github.com/mottaquikarim/esquerydsl
```

Note the `--prefix=github.com/mottaquikarim/esquerydsl`. The _full_ package prefix url is needed for this to work. Once I added this arg, I was able to upload code coverage stats for my pkg just fine. (Check it out [here](https://codeclimate.com/github/mottaquikarim/esquerydsl)).

## The Code

I have this thing tied up in a neat bow at this point and thought I'd share. I use make targets to handle running this in Github Actions. I'll share the recipes below in the hopes maybe it can help someone else in the future.

### `Makefile`

```Makefile
# Definitions
ROOT                    := $(PWD)
GO_HTML_COV             := ./coverage.html
GO_TEST_OUTFILE         := ./c.out
GOLANG_DOCKER_IMAGE     := golang:1.15
GOLANG_DOCKER_CONTAINER := goesquerydsl-container
CC_TEST_REPORTER_ID	:= ${CC_TEST_REPORTER_ID}
CC_PREFIX		:= github.com/mottaquikarim/esquerydsl

#   Usage:
#       make test
test:
	docker run -w /app -v ${ROOT}:/app ${GOLANG_DOCKER_IMAGE} go test ./... -coverprofile=${GO_TEST_OUTFILE}
	docker run -w /app -v ${ROOT}:/app ${GOLANG_DOCKER_IMAGE} go tool cover -html=${GO_TEST_OUTFILE} -o ${GO_HTML_COV}

# custom logic for code climate, gross but necessary
_before-cc:
	# download CC test reported
	docker run -w /app -v ${ROOT}:/app ${GOLANG_DOCKER_IMAGE} \
		/bin/bash -c \
		"curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter"
	
	# update perms
	docker run -w /app -v ${ROOT}:/app ${GOLANG_DOCKER_IMAGE} chmod +x ./cc-test-reporter

	# run before build
	docker run -w /app -v ${ROOT}:/app \
		 -e CC_TEST_REPORTER_ID=${CC_TEST_REPORTER_ID} \
		${GOLANG_DOCKER_IMAGE} ./cc-test-reporter before-build

_after-cc:
	# handle custom prefix
	$(eval PREFIX=${CC_PREFIX})
ifdef prefix
	$(eval PREFIX=${prefix})
endif
	# upload data to CC
	docker run -w /app -v ${ROOT}:/app \
		-e CC_TEST_REPORTER_ID=${CC_TEST_REPORTER_ID} \
		${GOLANG_DOCKER_IMAGE} ./cc-test-reporter after-build --prefix ${PREFIX}

# this runs tests with cc reporting built in
test-ci: _before-cc test _after-cc
```

### `Github Action`

I saved this file in: `.github/workflows/run-build.yml` and in my repo secrets, I saved my `CC_TEST_REPORTER_ID` so that I can export it as envvar on build time.

```yml
name: Build Status

on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout master
      uses: actions/checkout@v2

    - name: Run unit tests
      run: |
        make clean test-ci
      env:
        CC_TEST_REPORTER_ID: ${{ secrets.CC_TEST_REPORTER_ID }}
```

Note that running `make test-ci` will run tests with the codeclimate reporter running and `make test` just runs normal unit tests for dev/debugging.

The results of the configs above should be viewable in the following:

* [Github Action run ex](https://github.com/mottaquikarim/esquerydsl/runs/1631500119?check_suite_focus=true)
* [README ex](https://github.com/mottaquikarim/esquerydsl)

Happy coding!


