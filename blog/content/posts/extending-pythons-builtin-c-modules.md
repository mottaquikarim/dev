---
title: "Extending Pythons Builtin C Modules"
date: 2021-03-17T20:58:20Z
tags: ["featured", "python"]
---

{{<toc>}}

This post is intended to be a follow-up/continuation of my discussion around [cpython](https://github.com/python/cpython) and grokking (generally speaking) how `all(...)` works.

_(For better context, I'd recommend first reading the previous post in this series, ["Grokking Builtin.all in Python"](/dev/posts/grokking-builtin.all-in-python/))_

Having understood how the `builtin_all` method behaves, we now turn our attention to how we might be able to either "hack" `builtin_all` to accommodate our intended use case (for no reason except for our own education) or more generally speaking, how we might define a new method that specifically checks to see if _all_ items in the iterable are equivalent.

Effectively, we want to implement this logic (from the previous post):

```python
inp = [{},{},{}]
samesame = True
for it in inp:
  samesame = inp[0] == it
  if not samesame:
    break
# samesame will be False is all items in inp are not the same val
print(samesame) # True
```

but now formalized as a method in python's `bltinmodule.c` lib such that calling our method from python itself gives us:

```python
samesame([0,0,0]) # True
samesame([1,0,0]) # False
samesame([0,1,0]) # False
samesame([0,0.0,0]) # False
samesame([]) # True
samesame([{},{},{}]) # True
samesame([{},{},set()]) # False
```

Ok? 

**Ok.**

Let's do this!

## Step 1: Building CPython

Our first step is to actually build cpython locally so that we can make changes to the C source code and observe it in action.

To begin, I followed the steps provided [here](https://devguide.python.org/setup/#unix), as written in the Python Developer's Guide which defines the steps necessary for building python from the C source code.

While they have exhaustive documentation about how to get the codebase working in various environments and a bunch of caveats for install dependencies, etc - I chose to try to find the simplest way forward I possibly could.

To that end, I only needed to run the following two commands:

```bash
./configure --with-pydebug
```

and then:

```bash
make -s -j2
```

Initially I ran this directly on my local machine...which worked! And I saw that a `python.exe` file (yes, on a mac) was created in my current working directory. Running `./python.exe` resulted in the following:

```bash
Python 3.10.0a6+ (heads/master-dirty:6086ae7, Mar 17 2021, 19:52:03) [GCC 4.9.4] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Particularly, the `Python 3.10.0a6+ (heads/master-dirty:6086ae7` label demonstrates that a "dev" build of python was successfully created and is now runnable via the `./python.exe` binary!

## Step 2: Dockerizing the build process

Let's step back for a few moments.

The first thing I _actually_ did before even looking up the dev guide docs was to try and find a docker image that builds cpython's master branch. Disappointingly, I didn't find anything useful. So, I wrote one (see the Dockerfile below) in the hopes that it will make it easier for others (and of course by others I also include future-Taq) in playing around and/or dev-ing from the source.

```Dockerfile
FROM gcc:latest

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN ./configure --with-pydebug && make clean && make -s -j2
```

The first few lines are just our plain old docker usuals - build this image from the `gcc:latest` [base image](https://hub.docker.com/_/gcc), move the cpython source into container, set working dir, etc.

The last line builds python from source _initially_ (when image is created). Subsequent runs (once we've made changes to the source itself) only need `make clean && make -s -j2`. (We only need to re-run `./configure` if new dependencies must be linked as part of our dev cycle. Also, it is strongly recommended that we always build with `--with-pydebug` flag enabled).

_(**TODO**: for a future iteration: it would be great to configure some form of watcher (such as [CompileDaemon](https://github.com/githubnemo/CompileDaemon) in golang or [chokidar](https://github.com/paulmillr/chokidar) in npm) to rerun make as files are changed during development. At that point, I would be comfortable packaging this up as a cpython dev image on dockerhub)_

Once the Dockerfile is good and written (I stuck it directly into the top level of the `cpython` repo), we build the image:

```bash
docker build -t pydev:1.0 .
```

which will install dependencies and run `./configure`, etc etc. Then, we run the container:

```bash
docker run -it -v ${PWD}/Python:/usr/src/app/Python pydev:1.0 /bin/bash
```

In this mode, we launch the container in interactive mode allowing us to "manually" run the `make clean && make -s -j2` commands after changing source code as needed. 

By mounting the `Python` folder from our host machine into the container, we can make code changes in our IDE of choice (_outside_ the container) but still retain the ability to test the effects of our changes _inside_ the docker container. (Win-win!)

Alternatively, we can also run something like this:

```bash
docker run \
    -it \
    -v ${PWD}/Python:/usr/src/app/Python pydev:1.0 \
        bash -c "make clean && make -s -j2 && ./python"
```
_(indented for readability)_

In this setup, we make changes to our source (for the purposes of this post, all changes will be made to the `./Python` folder) then run the make command to rebuild source and then run the generated python binary (which puts us into the py REPL).

Unfortunately, this needs to be run "manually" everytime we want to debug changes (at least for now, without the file watcher idea in place). There is a lot of opportunities for improvement here but at the very least with the addition of this docker workflow we have a stable way to make changes to the source, mount these changes to our container and run python interactively (in the REPL shell) to test these changes.

Onwards!

## Step 3: Lightly dipping our toes into C-land

I'm no C aficionado - so, I began by _lightly_ making small incremental changes to the codebase. I made a change, rebuilt the source via the docker run command above, tested and then repeated the whole process all over again.

To start, I wanted to just prove to myself that I _could_ make visible changes and get the output I expected.

I began with the `builtin_all` method - reproduced below:

{{< highlight c "linenos=inline,linenostart=319" >}}
/*[clinic input]
all as builtin_all
    iterable: object
    /
Return True if bool(x) is True for all values x in the iterable.
If the iterable is empty, return True.
[clinic start generated code]*/

static PyObject *
builtin_all(PyObject *module, PyObject *iterable)
/*[clinic end generated code: output=ca2a7127276f79b3 input=1a7c5d1bc3438a21]*/
{
    PyObject *it, *item;
    PyObject *(*iternext)(PyObject *);
    int cmp;

    it = PyObject_GetIter(iterable);
    if (it == NULL)
        return NULL;
    iternext = *Py_TYPE(it)->tp_iternext;

    for (;;) {
        item = iternext(it);
        if (item == NULL)
            break;
        cmp = PyObject_IsTrue(item);
        Py_DECREF(item);
        if (cmp < 0) {
            Py_DECREF(it);
            return NULL;
        }
        if (cmp == 0) {
            Py_DECREF(it);
            Py_RETURN_FALSE;
        }
    }
    Py_DECREF(it);
    if (PyErr_Occurred()) {
        if (PyErr_ExceptionMatches(PyExc_StopIteration))
            PyErr_Clear();
        else
            return NULL;
    }
    Py_RETURN_TRUE;
}
{{< / highlight >}}

_([Sauce](https://github.com/python/cpython/blob/9a9c11ad41d7887f3d6440e0f0e8966156d959b5/Python/bltinmodule.c#L319))_

But! I changed **line 352** as follows:

{{< highlight c "linenos=inline,linenostart=319" >}}
/*[clinic input]
all as builtin_all
    iterable: object
    /
Return True if bool(x) is True for all values x in the iterable.
If the iterable is empty, return True.
[clinic start generated code]*/

static PyObject *
builtin_all(PyObject *module, PyObject *iterable)
/*[clinic end generated code: output=ca2a7127276f79b3 input=1a7c5d1bc3438a21]*/
{
    PyObject *it, *item;
    PyObject *(*iternext)(PyObject *);
    int cmp;

    it = PyObject_GetIter(iterable);
    if (it == NULL)
        return NULL;
    iternext = *Py_TYPE(it)->tp_iternext;

    for (;;) {
        item = iternext(it);
        if (item == NULL)
            break;
        cmp = PyObject_IsTrue(item);
        Py_DECREF(item);
        if (cmp < 0) {
            Py_DECREF(it);
            return NULL;
        }
        if (cmp == 0) {
            Py_DECREF(it);
            Py_RETURN_TRUE; // Py_RETURN_FALSE;
            // ^ THIS IS DIFFERENT NOW!
            // Expectation: return `True` if 
            // PyObject_IsTrue(item) evaluates to false
        }
    }
    Py_DECREF(it);
    if (PyErr_Occurred()) {
        if (PyErr_ExceptionMatches(PyExc_StopIteration))
            PyErr_Clear();
        else
            return NULL;
    }
    Py_RETURN_TRUE;
}
{{< / highlight >}}

_([Sauce](https://github.com/python/cpython/blob/9a9c11ad41d7887f3d6440e0f0e8966156d959b5/Python/bltinmodule.c#L319))_

With this change, my expectation is that running the following:

```python
all([0,0,0])
```

will return `True` instead of `False` as expected. And sure enough:

```bash
➜  cpython git:(master) ✗ docker run \
    -it \
    -v ${PWD}/Python:/usr/src/app/Python pydev:1.0 \
        bash -c "make clean && make -s -j2 && ./python"
# ... skipping output for the sake of brevity ... 

Python 3.10.0a6+ (heads/master-dirty:6086ae7, Mar 18 2021, 04:33:26) [GCC 4.9.4] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> all([0,0,0])
True
>>>
```

Tada! Progress!

## Step 4: Implementing a custom builtin method

So finally, having proven to ourselves that we can:

* build python from source
* make changes to the source and 
* observe the effects of our changes to the binary produced 

-- let's make our _actual_ change.

Again, I am no C expert so I chose to make the core implementation of my custom method, which I am calling `builtin_samesame` (dedicated to my former esteemed colleague and friend [Omid](https://www.linkedin.com/in/omid-hosseinmardi-4a9966a7/) who commonly used this refrain during our pair programming sessions at PX), as similar as possible to `builtin_all`.

Let's start off by viewing the implementation:

{{< highlight c "linenos=inline" >}}
static PyObject *
builtin_samesame(PyObject *module, PyObject *iterable)
/*[clinic end generated code: output=ca2a7127276f79b3 input=1a7c5d1bc3438a21]*/
{
    PyObject *it, *item, *firstitem;
    PyObject *(*iternext)(PyObject *);

    it = PyObject_GetIter(iterable);
    if (it == NULL)
        return NULL;
    iternext = *Py_TYPE(it)->tp_iternext;

    firstitem = iternext(it);
    if (firstitem == NULL) {
        Py_DECREF(it);
        Py_RETURN_TRUE;
    }

    for (;;) {
        item = iternext(it);
        if (item == NULL)
            break;
        if (Py_TYPE(firstitem)->tp_richcompare != NULL) {
            PyObject *res;
            res = (*Py_TYPE(firstitem)->tp_richcompare)(firstitem, item, Py_NE);
            if (res != Py_False) {
                Py_DECREF(firstitem);
                Py_DECREF(item);
                Py_DECREF(res);
                Py_DECREF(it);
                Py_RETURN_FALSE;
            }
            Py_DECREF(res);
        }
        else if (item != firstitem) {
            Py_DECREF(firstitem);
            Py_DECREF(item);
            Py_DECREF(it);
            Py_RETURN_FALSE;
        }
    }
    Py_DECREF(firstitem);
    Py_DECREF(it);
    if (PyErr_Occurred()) {
        if (PyErr_ExceptionMatches(PyExc_StopIteration))
            PyErr_Clear();
        else
            return NULL;
    }
    Py_RETURN_TRUE;
}
{{< / highlight >}}

This _does_ look pretty hardcore but I swear it isn't! The main differences between `builtin_samesame` and `builtin_all` are on **lines 5, 13-17, 23-42**. Let's break each of these three regions down to better grok what is going on.

**LINE 5**
{{< highlight c "linenos=inline,linenostart=5" >}}
PyObject *it, *item, *firstitem;
{{< / highlight >}}

This one is simple - we just declare an additional PyObject type, `*firstitem`. The idea is if any of the remaining items in our list is NOT equal to `*firstitem`, we can return false immediately as we are done.

**LINES 13-17**
{{< highlight c "linenos=inline,linenostart=13" >}}
firstitem = iternext(it);
if (firstitem == NULL) {
    Py_DECREF(it);
    Py_RETURN_TRUE;
}
{{< / highlight >}}

Here, we grab the first item in our iterable. If it is **NULL**, then there is nothing to do. By definition (of our own choosing, ha) we return `True`.

The meaning of `Py_DECREF` is available [here](https://docs.python.org/3/c-api/refcounting.html#c.Py_DECREF) in the docs. Basically, we decrement the reference count for a not-NULL object. Once the reference count hits 0, the object is deallocated from memory (if NULL though, we end up seg faulting, ha). Because this check is explicitly for `firstitem` being NULL, there is no need to decrement the ref count for `firstitem`.

**LINES 23-42**

{{< highlight c "linenos=inline,linenostart=23" >}}
// ...
    if (Py_TYPE(firstitem)->tp_richcompare != NULL) {
        PyObject *res;
        res = (*Py_TYPE(firstitem)->tp_richcompare)(firstitem, item, Py_NE);
        if (res != Py_False) {
            Py_DECREF(firstitem);
            Py_DECREF(item);
            Py_DECREF(res);
            Py_DECREF(it);
            Py_RETURN_FALSE;
        }
        Py_DECREF(res);
    }
    else if (item != firstitem) {
        Py_DECREF(firstitem);
        Py_DECREF(item);
        Py_DECREF(it);
        Py_RETURN_FALSE;
    }
}
Py_DECREF(firstitem);
{{< / highlight >}}

This logic performs the bulk of the work. (It could also definitely use some TLC but for now, I'll comment specifically on how it works as is).

Let's get that `else if` out of the way first, as it is simpler:

```c
// ...
else if (item != firstitem) {
    Py_DECREF(firstitem);
    Py_DECREF(item);
    Py_DECREF(it);
    Py_RETURN_FALSE;
}
```

This performs the basic `!=` check which ought to be well defined for primitive types. With this code block, cases such as:

```python
all([0,0,0])
all([True, False, True])
```

are all covered.

The first half of that conditional block is more interesting:

```c
if (Py_TYPE(firstitem)->tp_richcompare != NULL) {
    PyObject *res;
    res = (*Py_TYPE(firstitem)->tp_richcompare)(firstitem, item, Py_NE);
    if (res != Py_False) {
        Py_DECREF(firstitem);
        Py_DECREF(item);
        Py_DECREF(res);
        Py_DECREF(it);
        Py_RETURN_FALSE;
    }
    Py_DECREF(res);
}
```

After looking through the handy **[Type Objects](https://docs.python.org/3/c-api/typeobj.html#c.PyTypeObject.tp_richcompare)** documentation, I was able to pinpoint `tp_richcompare` as the method that manages dunder methods such as `__eq__`, `__ne__`, etc. (This provides support for comparing non primitive types such as `{}` or `set()`, etc)

The docs also tells us what the function signature looks like for `tp_richcompare`:

```c
PyObject *tp_richcompare(PyObject *self, PyObject *other, int op);
```

It also provides a handy table describing the constant definitions and their corresponding comparisons:

| Constant | Comparison |
|----------|------------|
| Py_LT    | <          |
| Py_LE    | <=         |
| Py_EQ    | ==         |
| Py_NE    | !=         |
| Py_GT    | >          |
| Py_GE    | >=         |

Moreover, from looking at the `Objects/dictobject.c` implentation of `tp_richcompare`, it was easy to see:

{{< highlight c "linenos=inline,linenostart=2958" >}}
static PyObject *
dict_richcompare(PyObject *v, PyObject *w, int op)
{
    int cmp;
    PyObject *res;

    if (!PyDict_Check(v) || !PyDict_Check(w)) {
        res = Py_NotImplemented;
    }
    else if (op == Py_EQ || op == Py_NE) {
        cmp = dict_equal((PyDictObject *)v, (PyDictObject *)w);
        if (cmp < 0)
            return NULL;
        res = (cmp == (op == Py_EQ)) ? Py_True : Py_False;
    }
    else
        res = Py_NotImplemented;
    Py_INCREF(res);
    return res;
}
{{< / highlight >}}

_([Sauce](https://github.com/python/cpython/blob/226a012d1cd61f42ecd3056c554922f359a1a35d/Objects/dictobject.c#L2958))_

that this method is **static** and essentially the same beast as `tp_as_number` (a topic of discussion from **Part I** ). As such, I drew on inspiration from the `PyObject_IsTrue` method we discussed in **Part I**(reproduced below for convenience) to figure out how to call `tp_richcompare`.

{{< highlight c "linenos=inline,linenostart=1379" >}}
/* Test a value used as condition, e.g., in a while or if statement.
   Return -1 if an error occurred */

int
PyObject_IsTrue(PyObject *v)
{
    Py_ssize_t res;
    if (v == Py_True)
        return 1;
    if (v == Py_False)
        return 0;
    if (v == Py_None)
        return 0;
    else if (Py_TYPE(v)->tp_as_number != NULL &&
             Py_TYPE(v)->tp_as_number->nb_bool != NULL)
        res = (*Py_TYPE(v)->tp_as_number->nb_bool)(v);
    else if (Py_TYPE(v)->tp_as_mapping != NULL &&
             Py_TYPE(v)->tp_as_mapping->mp_length != NULL)
        res = (*Py_TYPE(v)->tp_as_mapping->mp_length)(v);
    else if (Py_TYPE(v)->tp_as_sequence != NULL &&
             Py_TYPE(v)->tp_as_sequence->sq_length != NULL)
        res = (*Py_TYPE(v)->tp_as_sequence->sq_length)(v);
    else
        return 1;
    /* if it is negative, it should be either -1 or -2 */
    return (res > 0) ? 1 : Py_SAFE_DOWNCAST(res, Py_ssize_t, int);
}
{{< / highlight >}}

_([Sauce](https://github.com/python/cpython/blob/9a9c11ad41d7887f3d6440e0f0e8966156d959b5/Objects/object.c#L1379))_


Basically, just emulate **line 1394** but for `tp_richcompare` and pass in the required arguments as per the method signature we observed above.

Let's reproduce our conditional block one more time for convenience:

```c
if (Py_TYPE(firstitem)->tp_richcompare != NULL) {
    PyObject *res;
    res = (*Py_TYPE(firstitem)->tp_richcompare)(firstitem, item, Py_NE);
    if (res != Py_False) {
        Py_DECREF(firstitem);
        Py_DECREF(item);
        Py_DECREF(res);
        Py_DECREF(it);
        Py_RETURN_FALSE;
    }
    Py_DECREF(res);
}
```

All this line is doing:

```c
res = (*Py_TYPE(firstitem)->tp_richcompare)(firstitem, item, Py_NE);
```

is invoking `tp_richcompare` on our `firstitem` (remember this is a static method so we pass in firstitem, item and the **op** constant, in this case `Py_NE`) and based on the return value we choose to either stop in our tracks or continue on with the loop.

(NOTE: the way I implemented this is confusing af. The reason why we check for `res != Py_False` is because we are running `tp_richcompare` with `op = Py_NE`. So, if **firstitem != item** is **False** that means the two items _are_ equal and we can move on. For all other cases (if they are false OR if there is an error), we want to stop the loop. I know, I know, this is poorly written code - but it works and I'm feeling lazy 😎)

There's a ton of `Py_DECREF`s all over the place mainly because I don't know enough C to come up with a way to make that easier to manage. A problem for next time!

Ok so let's put a bow on this -- in conclusion, our `builtin_samesame` method (reproduced a final time below):

{{< highlight c "linenos=inline" >}}
static PyObject *
builtin_samesame(PyObject *module, PyObject *iterable)
/*[clinic end generated code: output=ca2a7127276f79b3 input=1a7c5d1bc3438a21]*/
{
    PyObject *it, *item, *firstitem;
    PyObject *(*iternext)(PyObject *);

    it = PyObject_GetIter(iterable);
    if (it == NULL)
        return NULL;
    iternext = *Py_TYPE(it)->tp_iternext;

    firstitem = iternext(it);
    if (firstitem == NULL) {
        Py_DECREF(it);
        Py_RETURN_TRUE;
    }

    for (;;) {
        item = iternext(it);
        if (item == NULL)
            break;
        if (Py_TYPE(firstitem)->tp_richcompare != NULL) {
            PyObject *res;
            res = (*Py_TYPE(firstitem)->tp_richcompare)(firstitem, item, Py_NE);
            if (res != Py_False) {
                Py_DECREF(firstitem);
                Py_DECREF(item);
                Py_DECREF(res);
                Py_DECREF(it);
                Py_RETURN_FALSE;
            }
            Py_DECREF(res);
        }
        else if (item != firstitem) {
            Py_DECREF(firstitem);
            Py_DECREF(item);
            Py_DECREF(it);
            Py_RETURN_FALSE;
        }
    }
    Py_DECREF(firstitem);
    Py_DECREF(it);
    if (PyErr_Occurred()) {
        if (PyErr_ExceptionMatches(PyExc_StopIteration))
            PyErr_Clear();
        else
            return NULL;
    }
    Py_RETURN_TRUE;
}
{{< / highlight >}}

Ought to provide support for our original impression of what `all(..)` does - that is, return `True` if all items in the iterable passed in are the same.

To actually test this guy out though, we have a few more changes left to make. 

First, in `bltinmodule.c`'s header file (`./Python/clinic/bltinmodule.c.h`), we add the following definition:

```c
PyDoc_STRVAR(builtin_samesame__doc__,
"samesame($module, iterable, /)\n"
"--\n"
"\n"
"Return True if all values x in the iterable are equal.\n"
"\n"
"If the iterable is empty, return True.");

#define BUILTIN_SAMESAME_METHODDEF    \
    {"samesame", (PyCFunction)builtin_samesame, METH_O, builtin_samesame__doc__},
```

This is crucial as it associates the python method name **"samesame"** with the `builtin_samesame` function. Also, we have the ability to provide some documentation as well which is manifested using: `help(samesame)`:

```python
>>> help(samesame)
Help on built-in function samesame in module builtins:

samesame(iterable, /)
    Return True if all values x in the iterable are equal.

    If the iterable is empty, return True.

>>>
```

Meanwhile, back at the ranch (in the `bltinmodule.c` file), we add our final change (note **line 2893**):


{{< highlight c "linenos=inline,linenostart=2887" >}}
static PyMethodDef builtin_methods[] = {
    {"__build_class__", (PyCFunction)(void(*)(void))builtin___build_class__,
     METH_FASTCALL | METH_KEYWORDS, build_class_doc},
    {"__import__",      (PyCFunction)(void(*)(void))builtin___import__, METH_VARARGS | METH_KEYWORDS, import_doc},
    BUILTIN_ABS_METHODDEF
    BUILTIN_ALL_METHODDEF
    BUILTIN_SAMESAME_METHODDEF
    BUILTIN_ANY_METHODDEF
    BUILTIN_ASCII_METHODDEF
    BUILTIN_BIN_METHODDEF
    {"breakpoint",      (PyCFunction)(void(*)(void))builtin_breakpoint, METH_FASTCALL | METH_KEYWORDS, breakpoint_doc},
    BUILTIN_CALLABLE_METHODDEF
    BUILTIN_CHR_METHODDEF
    BUILTIN_COMPILE_METHODDEF
    BUILTIN_DELATTR_METHODDEF
    {"dir",             builtin_dir,        METH_VARARGS, dir_doc},
    BUILTIN_DIVMOD_METHODDEF
    BUILTIN_EVAL_METHODDEF
    BUILTIN_EXEC_METHODDEF
    BUILTIN_FORMAT_METHODDEF
    {"getattr",         (PyCFunction)(void(*)(void))builtin_getattr, METH_FASTCALL, getattr_doc},
    BUILTIN_GLOBALS_METHODDEF
    BUILTIN_HASATTR_METHODDEF
    BUILTIN_HASH_METHODDEF
    BUILTIN_HEX_METHODDEF
    BUILTIN_ID_METHODDEF
    BUILTIN_INPUT_METHODDEF
    BUILTIN_ISINSTANCE_METHODDEF
    BUILTIN_ISSUBCLASS_METHODDEF
    {"iter",            (PyCFunction)(void(*)(void))builtin_iter,       METH_FASTCALL, iter_doc},
    BUILTIN_LEN_METHODDEF
    BUILTIN_LOCALS_METHODDEF
    {"max",             (PyCFunction)(void(*)(void))builtin_max,        METH_VARARGS | METH_KEYWORDS, max_doc},
    {"min",             (PyCFunction)(void(*)(void))builtin_min,        METH_VARARGS | METH_KEYWORDS, min_doc},
    {"next",            (PyCFunction)(void(*)(void))builtin_next,       METH_FASTCALL, next_doc},
    BUILTIN_OCT_METHODDEF
    BUILTIN_ORD_METHODDEF
    BUILTIN_POW_METHODDEF
    {"print",           (PyCFunction)(void(*)(void))builtin_print,      METH_FASTCALL | METH_KEYWORDS, print_doc},
    BUILTIN_REPR_METHODDEF
    BUILTIN_ROUND_METHODDEF
    BUILTIN_SETATTR_METHODDEF
    BUILTIN_SORTED_METHODDEF
    BUILTIN_SUM_METHODDEF
    {"vars",            builtin_vars,       METH_VARARGS, vars_doc},
    {NULL,              NULL},
};
{{< / highlight >}}

And with this, we are in business! Re-run docker and check it:

```python
>>> samesame([0,0,0])
True
>>> samesame([1,0,0])
False
>>> samesame([0,1,0])
False
>>> samesame([0,0.0,0])
False
>>> samesame([])
True
>>> samesame([{},{},{}])
True
>>> samesame([{},{},set()])
False
>>>
```

Tada!

## Final Remarks

Ok cool - so now, there's a path forward for developing with changes to the Python lang itself and then testing the changes for correctness and viability.

I should mention that I am not suggesting that `samesame` ought to be added to the Python API. This was more of an exercise of determining _how might we do such a thing_ if we wanted to or needed to.

I'm particularly excited about the Dockerfile and would like to follow up...at some point, with a more mature version of it. While it is super tempting to go further messing around with python internals I'll probably leave things here for now at least. At some point (per suggestion from another esteemed colleague), I'd certainly like to take a stab at creating a custom python type (this is more aligned with the content from Part I) just to see what that's like.

**[Please find MR of the changes discussed here](https://github.com/mottaquikarim/cpython/pull/1)**
