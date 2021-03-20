---
title: "Hacking Python With Spells From Harry Potter"
date: 2021-03-20T18:19:39Z
tags: ["python", "just for fun"]
---

{{<toc>}}

![hp py](/dev/img/hp_py.png)

This post is intended to be a follow-up/continuation of my discussion around [cpython](https://github.com/python/cpython) and grokking (generally speaking) how the language works "under the hood".

_(For better context, I'd recommend first reading the previous post(s) in this series:_

1. ["Grokking Builtin.all in Python"](/dev/posts/grokking-builtin.all-in-python/)
2. ["Extending Python's Builtin C Modules"](/dev/posts/extending-pythons-builtin-c-modules/)

(That being said, this post is relatively stand alone and you can just probably make do ok reading this without looking at the previous parts).

## Why tho?

In this post, I will describe how I extended cpython once again, this time aliasing three python syntax elements to three Harry Potter spells:

* **lumos** (aliasing **type()**)
* **accio** (aliasing **import**)
* **avadakedavra** (aliasing **del**)

Years ago - around 2014 probably - my buddy and (current) rustacean [Apoorv Kothari](https://github.com/rust-lang/rust/pulls?utf8=%E2%9C%93&q=is%3Apr+author%3Atoidiu+) mentioned a meet up he went to where someone decided to swap out python's `import` keyword with `accio`.

There was no real rhyme or reason for doing this - but, it did lead to a deep dive of python internals and made for a fun story to tell.

Given my recent exploration of cpython, I thought it would be fun to see how far I could take this concept myself. My goal was to support `accio` as an alias for `import` but along the way (as I learned more about how parsing works in cpython), I thought to also alias `lumos(...)` for `type(...)` (a quick win) and `avadakedavra` for `del` (pretty easy once I figured out `accio`). 

I hope to follow up with one last post...at some point where I will also add a custom operator (perhaps `!` for `not` or `~=` for regex (thanks to [Phil Eaton](https://notes.eatonphil.com/) for the idea, though he may get to this before me)) and define a custom type (like `float` or something). In my follow up I hope to dive deeper into the specifics of the [new PEG parser for CPython (PEP617)](https://www.python.org/dev/peps/pep-0617/).

For the purposes of this post however, I'd like to primarily share the steps required to achieve the three aliases in question (without going too deeply into _how_ the parser itself works). Let's start with `lumos`, by far the simplest of the three.

## type -> lumos

To implement `lumos`, I started at `./Python/clinic/bltinmodule.c.h` _([sauce](https://github.com/python/cpython/blob/9a9c11ad41d7887f3d6440e0f0e8966156d959b5/Python/clinic/bltinmodule.c.h))_. (Recall from the previous post that this is the file where we ultimately defined `samesame`, a custom function added to python's list of **builtin**s).

I was hoping to find something similar to:

```c
PyDoc_STRVAR(builtin_any__doc__,
"any($module, iterable, /)\n"
"--\n"
"\n"
"Return True if bool(x) is True for any x in the iterable.\n"
"\n"
"If the iterable is empty, return False.");

#define BUILTIN_ANY_METHODDEF    \
    {"any", (PyCFunction)builtin_any, METH_O, builtin_any__doc__},
```

Which would help me pinpoint the definition of the _actual_ `type(...)` implementation. Then, I was going to just add another line similar to:

```c
#define BUILTIN_ANY_METHODDEF    \
    {"any", (PyCFunction)builtin_any, METH_O, builtin_any__doc__},
```

for my alias.

I couldn't find anything in that header file though, so I fell back to my tried and true _grep the entire codebase_ for **type** approach. This also sucked! (Way too much info). But, I refined my search and grepped for:

```bash
grep -rI "\"type\"" ./Python
```

which was super helpful as it pinpointed the line where **"type"** is associated to the underlying c-method. What I was searching for was infact in [`./Python/bltinmodule.c`](https://github.com/python/cpython/blob/9a9c11ad41d7887f3d6440e0f0e8966156d959b5/Python/bltinmodule.c#L2951) (**line 2951**, reproducing entire block below for convenience):

{{< highlight c "linenos=inline,linenostart=2917" >}}
#define SETBUILTIN(NAME, OBJECT) \
    if (PyDict_SetItemString(dict, NAME, (PyObject *)OBJECT) < 0)       \
        return NULL;                                                    \
    ADD_TO_ALL(OBJECT)

    SETBUILTIN("None",                  Py_None);
    SETBUILTIN("Ellipsis",              Py_Ellipsis);
    SETBUILTIN("NotImplemented",        Py_NotImplemented);
    SETBUILTIN("False",                 Py_False);
    SETBUILTIN("True",                  Py_True);
    SETBUILTIN("bool",                  &PyBool_Type);
    SETBUILTIN("memoryview",        &PyMemoryView_Type);
    SETBUILTIN("bytearray",             &PyByteArray_Type);
    SETBUILTIN("bytes",                 &PyBytes_Type);
    SETBUILTIN("classmethod",           &PyClassMethod_Type);
    SETBUILTIN("complex",               &PyComplex_Type);
    SETBUILTIN("dict",                  &PyDict_Type);
    SETBUILTIN("enumerate",             &PyEnum_Type);
    SETBUILTIN("filter",                &PyFilter_Type);
    SETBUILTIN("float",                 &PyFloat_Type);
    SETBUILTIN("frozenset",             &PyFrozenSet_Type);
    SETBUILTIN("property",              &PyProperty_Type);
    SETBUILTIN("int",                   &PyLong_Type);
    SETBUILTIN("list",                  &PyList_Type);
    SETBUILTIN("map",                   &PyMap_Type);
    SETBUILTIN("object",                &PyBaseObject_Type);
    SETBUILTIN("range",                 &PyRange_Type);
    SETBUILTIN("reversed",              &PyReversed_Type);
    SETBUILTIN("set",                   &PySet_Type);
    SETBUILTIN("slice",                 &PySlice_Type);
    SETBUILTIN("staticmethod",          &PyStaticMethod_Type);
    SETBUILTIN("str",                   &PyUnicode_Type);
    SETBUILTIN("super",                 &PySuper_Type);
    SETBUILTIN("tuple",                 &PyTuple_Type);
    SETBUILTIN("type",                  &PyType_Type);
    SETBUILTIN("zip",                   &PyZip_Type);
    debug = PyBool_FromLong(config->optimization_level == 0);
    if (PyDict_SetItemString(dict, "__debug__", debug) < 0) {
        Py_DECREF(debug);
        return NULL;
    }
    Py_DECREF(debug);

    return mod;
#undef ADD_TO_ALL
#undef SETBUILTIN
{{< / highlight >}}

Interestingly, `type` is defined as `PyType_Type`(a `PyObject`, similar to floats, etc - [sauce](https://github.com/python/cpython/blob/c9bc290dd6e3994a4ead2a224178bcba86f0c0e4/Objects/typeobject.c)) and not as a `builtin__type` as I would have expected (similar to `all(..)` for instance).

Regardless - having tracked down the location of this definition, it was very easy to "implement" support for `lumos`, just add the following:

{{< highlight c "linenos=inline,linenostart=2950" >}}
// ... 
SETBUILTIN("type",                  &PyType_Type);
SETBUILTIN("lumos",                  &PyType_Type);
{{< / highlight >}}

rebuild + run:

```bash
docker build -t pydev:1.0 .
docker run -it pydev:1.0 ./python
```
_(Check out ["Step 2: Dockerizing the build process"](http://localhost:1313/dev/posts/extending-pythons-builtin-c-modules/#step-2-dockerizing-the-build-process) from the last post in this series for more info.)_

and then test:

```bash
>>> lumos(15)
<class 'int'>
```

Tada!

_([Here's the PR](https://github.com/mottaquikarim/cpython/pull/2) of these changes.)_


## del -> avadakedavra

Next up we have the gruesome `avadakedavra` implementation. This one is interesting in that to achieve this change, we must actually modify the _grammar_ that defines python. 

I went down the wrong path _hard_ by applying my previous strategy of grepping the entire project. There is actually a _LOT_ of places where the token **del** is used but as it turns out - most of the code is generated!

I eventually ended up stumbling back on to the Python Developer Guide, which has a handy [Changing Cpython's Grammar](https://devguide.python.org/grammar/#) post delineating how to _properly_ make changes to the grammar definitions.

THe Changing Cpython's Grammar post suggests starting from the `./Grammar/python.gram` file; peering into that file we note that `del` is defined on **line 73**:


{{< highlight text "linenos=inline,hl_lines=73,linenostart=66" >}}
simple_stmt[stmt_ty] (memo):
    | assignment
    | e=star_expressions { _Py_Expr(e, EXTRA) }
    | &'return' return_stmt
    | &('import' | 'from') import_stmt
    | &'raise' raise_stmt
    | 'pass' { _Py_Pass(EXTRA) }
    | &'del' del_stmt
    | &'yield' yield_stmt
    | &'assert' assert_stmt
    | 'break' { _Py_Break(EXTRA) }
    | 'continue' { _Py_Continue(EXTRA) }
    | &'global' global_stmt
    | &'nonlocal' nonlocal_stmt
{{< / highlight >}}

_([Sauce](https://github.com/python/cpython/blob/9a9c11ad41d7887f3d6440e0f0e8966156d959b5/Grammar/python.gram#L66))_

Additionally, the `del_stmt` is defined further down in the same file:

{{< highlight text "linenos=inline,hl_lines=73,linenostart=132" >}}
del_stmt[stmt_ty]:
    | 'del' a=del_targets &(';' | NEWLINE) { _Py_Delete(a, EXTRA) }
    | invalid_del_stmt
{{< / highlight >}}

_([Sauce](https://github.com/python/cpython/blob/9a9c11ad41d7887f3d6440e0f0e8966156d959b5/Grammar/python.gram#L132))_

And finally, `invalid_del_stmt` is defined again further down in the same file: 

{{< highlight text "linenos=inline,hl_lines=73,linenostart=797" >}}
invalid_del_stmt:
    | 'del' a=star_expressions {
        RAISE_SYNTAX_ERROR_INVALID_TARGET(DEL_TARGETS, a) }
{{< / highlight >}}

_([Sauce](https://github.com/python/cpython/blob/9a9c11ad41d7887f3d6440e0f0e8966156d959b5/Grammar/python.gram#L797))_

Since we only want to _alias_ `avadakedavra`, we can take a shortcut and _only_ add `stmt` definitions that actuall refer to the **del** token itself.

As such, we must add an `avadakedavra_stmt` and `invalid_avadakedavra_stmt` since both blocks refer directly to the **del** keyword. However, we leave `del_targets` (**line 133**) alone since we require `avadakedavra` to work exactly in the same way as `del` works.

Adding the updates (summarized below), we end up with:

```text
simple_stmt[stmt_ty] (memo):
    # ... other statements
    | &'del' del_stmt
    | &'avadakedavra' avadakedavra_stmt
    # ... other statements

# ... more definitions

avadakedavra_stmt[stmt_ty]:
    | 'avadakedavra' a=del_targets &(';' | NEWLINE) { _Py_Delete(a, EXTRA) }
    | invalid_avadakedavra_stmt

# ... more definitions

invalid_avadakedavra_stmt:
    | 'avadakedavra' a=star_expressions {
        RAISE_SYNTAX_ERROR_INVALID_TARGET(DEL_TARGETS, a) }
```
_([Sauce](https://github.com/mottaquikarim/cpython/pull/3/files#diff-2973ca53337859793077e9bdc1a1623063379f0fdfcb788836fd82ebb66b763b))_


According to the docs, we must now run `make regen-pegen`, which will regenerate `./Parser/parser.c` and allow our dev-python build to recognize the new token we just defined.

In order to run that make target, we actually need python3.9 installed. The docker image we have defined actually does not have python installed _at all_. Instead of modifying it, I just ran the make command within the `python:3.9` base image, as follows:

```bash
docker run -it -v ${PWD}:/app -w /app python:3.9 make regen-pegen
```

Here, I volume mount the source into the container running our `python:3.9` image and run the make target. This allows the regenerated **parser.c** file to be available to our host machine - meaning rebuilding our original `pydev` image will generate the binary with the grammar changes we defined.

So, all together these three lines should do it (note the comments for additional clarification):

```bash
# make regen-pegen to generate parser.c
docker run -it -v ${PWD}:/app -w /app python:3.9 make regen-pegen
# rebuild image with the new parser.c
docker build -t pydev:1.0 .
# run our dev build with support for avadakedavra!
docker run -it pydev:1.0 ./python
```

With all said and done, we now observe that we can use `avadakedavra` in place of `del`!!

```python
>>> unfortunate_characters = {"Hedwig": True, "Mad-Eye Moody": True,}
>>> avadakedavra unfortunate_characters["Hedwig"]
>>> unfortunate_characters
{'Mad-Eye Moody': True}
>>> avadakedavra unfortunate_characters
>>> unfortunate_characters
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'unfortunate_characters' is not defined
>>>
```

Tada!

_([Here's the PR](https://github.com/mottaquikarim/cpython/pull/3) of these changes.)_


## import -> accio

Last but not least - let's repeat our process to define `accio`, which behaves exactly like `import`. At first glance, this _feels_ more complex since import can be used in a multitude of ways:

```python
import random
from random import randint, randrange
from math import *
```

Still, I decided to start the simplest way possible: by repeating the steps from the previous section (del -> avadakedavra). I figured if it failed, the error messages might provide meaningful hints as to how to proceed further along. 

So, again in `./Grammar/python.gram`, we make the following changes:

```text
simple_stmt[stmt_ty] (memo):
    # ... other statements
    | &('import' | 'from') import_stmt
    | &('accio' | 'from') accio_stmt
    # ... other statements

# ... more definitions

accio_stmt[stmt_ty]: accio_name | accio_from
accio_name[stmt_ty]: 'accio' a=dotted_as_names { _Py_Import(a, EXTRA) }
# note below: the ('.' | '...') is necessary because '...' is tokenized as ELLIPSIS
accio_from[stmt_ty]:
    | 'from' a=('.' | '...')* b=dotted_name 'accio' c=import_from_targets {
        _Py_ImportFrom(b->v.Name.id, c, _PyPegen_seq_count_dots(a), EXTRA) }
    | 'from' a=('.' | '...')+ 'accio' b=import_from_targets {
        _Py_ImportFrom(NULL, b, _PyPegen_seq_count_dots(a), EXTRA) }

# ... more definitions

```
_([Sauce](https://github.com/mottaquikarim/cpython/pull/4/files#diff-2973ca53337859793077e9bdc1a1623063379f0fdfcb788836fd82ebb66b763b))_

We only make necessary changes which in this case translates to updating the `accio_name` and `accio_from` stmts. Once completed, we re-run the `regen-pegen` make target and build, resulting in:

```python
>>> accio random
>>> random.randint(1,5)
4
>>> from random accio randint, randrange
>>> randint(1,5)
2
>>> randrange(5)
4
>>> from math accio *
>>> ceil(4.2)
5
>>>
```

Tada!

_([Here's the PR](https://github.com/mottaquikarim/cpython/pull/4) of these changes.)_

## Final Remarks

While this was certainly a _magical_ experience, the truth of the matter is until recently the inner workings of python - to me at least - certainly _were_ magical. I could tell you _very accurately_ what outputs to expect based on inputs provided but could not tell you for the life of me _how_ these outputs were actually computed. (This is essentially the definition of the word magic, right?)

Having gone deeper into the internals of cpython at least, I now feel like I have a better sense of the _how_, which has been very fascinating to discover. There's definitely still much left to learn / grok and I'm unsure just how much deeper I'll take this. But, at the very least I hope my explorations here (especially the docker stuff!) can help make it easier for you, dear reader, to conduct similar exercises of your own for your own understanding and benefit. 

Happy hacking, fam.