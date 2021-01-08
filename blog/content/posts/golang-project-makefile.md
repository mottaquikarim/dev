---
title: "Using Makefile + Docker for Golang dev"
date: 2021-01-08T02:29:26Z
---

{{<toc>}}

(This post was inspired by this [article](https://leogtzr.medium.com/how-to-use-makefiles-for-your-golang-development-b4c438fe0bdd) on medium.)

---

For starters, I'd highly recommend reading the article I linked to _first_. Leo's points about _why_ he chooses Make resonate strongly with me.

In this post, I'll expand slightly on his Makefile and share how make targets can be leveraged with docker for golang development.

(Of course, we can apply this principle to dev with other langs too, but for now let's stick with go).

In particular, the `Makefile` I'll share can be used to quickly set up a golang pkg repo for dev, etc.

## TL;DR: the **Makefile**

```Makefile
# Definitions
ROOT                    := $(PWD)
GO_HTML_COV             := ./coverage.html
GO_TEST_OUTFILE         := ./c.out
GOLANG_DOCKER_IMAGE     := golang:1.15
GOLANG_DOCKER_CONTAINER := goesquerydsl-container

#   Format according to gofmt: https://github.com/cytopia/docker-gofmt
#   Usage:
#       make fmt
#       make fmt path=src/elastic/index_setup.go
fmt:
ifdef path
	docker run --rm -v ${ROOT}:/data cytopia/gofmt -s -w ${path}
else
	docker run --rm -v ${ROOT}:/data cytopia/gofmt -s -w .
endif

#   Deletes container if exists
#   Usage:
#       make clean
clean:
	docker rm -f ${GOLANG_DOCKER_CONTAINER} || true

#   Usage:
#       make test
test:
	docker run -w /app -v ${ROOT}:/app ${GOLANG_DOCKER_IMAGE} go test ./... -coverprofile=${GO_TEST_OUTFILE}
	docker run -w /app -v ${ROOT}:/app ${GOLANG_DOCKER_IMAGE} go tool cover -html=${GO_TEST_OUTFILE} -o ${GO_HTML_COV}

#   Usage:
#       make lint
lint:
	docker run --rm -v ${ROOT}:/data cytopia/golint .
```

## Why Docker?

I really, really like wrapping all of my dev work these days into containers. This makes it super easy for me to bootstrap my work anywhere - from a dev box or EC2 instance to my local machine.

With docker, I can defined custom images and other dependencies that will ensure that I (or, anyone really) can get the service or project running (ie: unit/integration tests run and system can be built) without worrying too much about anything except which make targets to run.

## Definitions

Let's begin by going over some defintions.

```Makefile
# Definitions
ROOT                    := $(PWD)
GO_HTML_COV             := ./coverage.html
GO_TEST_OUTFILE         := ./c.out
GOLANG_DOCKER_IMAGE     := golang:1.15
GOLANG_DOCKER_CONTAINER := goesquerydsl-container
```

The `walrus` operator is used to define default values for some variables we will be using in our targets.

**`ROOT`**: We usually place our `Makefile` in the folder root - as such, we define the `${ROOT}` dir to be current working dir

**`GO_HTML_COV`**: When running golang tests, it is useful to generate coverage data to better understand which parts of the codebase could use unit testing coverage. 

**`GO_TEST_OUTFILE`**: This file is lower level, GO_HTML_COV outputs HTML code that we can render in the browser. The GO_TEST_OUTFILE can be used to generate other types of coverage reports or as a way to public test coverage data to static code analysis tools such as [code climate](https://codeclimate.com/). **PS**: I write about getting started with golang and CC test coverage in [this post](./posts/integrating-code-climate-w/go-pkgs/)

**`GOLANG_DOCKER_IMAGE`**: this aligns with official golang docker image available on [dockerhub](https://hub.docker.com/_/golang). 

**`GOLANG_DOCKER_CONTAINER`**: This is a label for the container you will be running off of the golang docker image. I would pick something meaningful to your pkg itself. For instance, this example is derived from my [esquerydsl](https://github.com/mottaquikarim/esquerydsl) golang pkg and the naming structure reflects this. (Heads up, this current Makefile ex doesn't really use `GOLANG_DOCKER_CONTAINER` all that much but useful to have for more complex projects)

## make **clean**

Generally, we want the `clean` target to remove any output artifacts and the like. This one is super simple and it merely removes the docker container instance.

## make **fmt**

This target encapsulates the [`go fmt`](https://golang.org/cmd/gofmt/) command which will prettify your golang src as per the golang best practices. Mainly, tabs are true tabs and spaces are alinged. I usually run this target as part of my CI/CD pipeline as well.

```Makefile
#   Format according to gofmt: https://github.com/cytopia/docker-gofmt
#   Usage:
#       make fmt
#       make fmt path=src/elastic/index_setup.go
fmt:
ifdef path
    docker run --rm -v ${ROOT}:/data cytopia/gofmt -s -w ${path}
else
    docker run --rm -v ${ROOT}:/data cytopia/gofmt -s -w .
endif
```

To expound on the code itself:

**`ifdef path`** is a common way to check to see if the target was called with a named argument. If so, we can conditionally determine a different course of action for our target.

**`--rm`** ([docs](https://docs.docker.com/engine/reference/run/#clean-up---rm)) will remove the container once it has stopped running.

**`-v ${ROOT}:/data`** this will mount our current working dir (in host) to the container's filesystem in `/data`. This is a nice and quick way to share the contents of our src code with the container itself so that `go fmt` can be applied to our go files _and_ the effects of the fmt changes are **available outside** the container's `/data` folder.

**`cytopia/gofmt -s -w ${path}`** [`cytopia/gofmt`](https://hub.docker.com/r/cytopia/gofmt/) is a docker image that wraps the [`gofmt`](https://godoc.org/cmd/gofmt) command line utility. 

* **`-w`**: I usually run `gofmt` with `-w` to overwrite my files that are not fmt complaint vs having the reformatted output print to stdin
* **`-s`**: This tries to [simplify code](https://godoc.org/cmd/gofmt#hdr-The_simplify_command) if applicable. 

## make **lint**

```Makefile
#   Usage:
#       make lint
lint:
    docker run --rm -v ${ROOT}:/data cytopia/golint .
```

**golint** is a [linter](https://github.com/golang/lint) for golang src code. 

I typically run this and `fmt` together as a step in CI, like so:

```bash
make fmt lint
```

## make **test**

```Makefile
#   Usage:
#       make test
test:
    docker run \
        -w /app \
        -v ${ROOT}:/app \
        ${GOLANG_DOCKER_IMAGE} go test ./... \
            -coverprofile=${GO_TEST_OUTFILE}
    docker run \
        -w /app \
        -v ${ROOT}:/app \
        ${GOLANG_DOCKER_IMAGE} go tool \
            cover -html=${GO_TEST_OUTFILE} -o ${GO_HTML_COV}
```

(Heads up, the **`\`** is mainly to make the code a bit easier to format+read on this blog's design)

Here, we run `go test` within the golang docker image. If our package supported a specific version of docker, we would only have to update **`GOLANG_DOCKER_IMAGE`** and re-run.

Additionally, we take advantage of volume mounting here for two reasons:

1. Make the test coverage HTML and output files available to the host (so that we can view the stats in our browser, for instance)
2. By mounting our `src` into the container, we can run our tests within the docker container but _develop our code_ in our preferred code editor/environment on the host.


## BONUS: make **bash**

```Makefile
#   Usage:
#       make bash
bash:
    docker run -it \
        -w /app \
        -v ${ROOT}:/app \
        ${GOLANG_DOCKER_IMAGE} /bin/bash
```

**`-it`** this allows us to "log in" to our docker container, with our src code mounted into the `/app` dir. From here, we can run normal golang ops as normal (ie: `go test` or `go get`, etc).

I use this to directly run / test / debug stuff and I just enjoy having the flexibility and option to get into the container itself and futz around.

---

Ok and there you have it! Feel free to take this `Makefile` and use/abuse.

Having coding, fam.  
