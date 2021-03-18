---
title: "Grokking Builtin.all in Python"
date: 2021-03-16T22:26:46Z
tags: ["featured", "python"]
---

{{<toc>}}

A coworker shared this neat code snippet on slack:

```python
>>> all([0, 0, 0])
False
>>> all([1, 1, 1])
True
```

and mused to us all:

> this is annoying <br/> _-- venerated colleague, circa 2021_

Indeed he's right! It _is_ annoying. His note piqued my curiousity as to why/how this worked under the hood; in this post I take a dive into the guts of **[cpython](https://github.com/python/cpython)** searching for answers.

_(**EDIT**: heads up, I wrote a lot of words here. If you want the simpler walk through without the fancy code spelunking, click **[here](#tying-it-all-together-finally)** to skip to the final section)_

## First, a sensible alternative

Let's get a few things out of the way before we go on.

First and foremost - let's explain why, naively, `all([0,0,0])` returning `False` is in fact not _unexpected_.

In python, there is a concept of **truthy** and **falsy**. While there exists explicitly defined `True` and `False` values (of type _bool_ as it were), _non boolean_ types are also evaluated by python to **True** or **False** within boolean contexts. 

A "boolean context", fwiw, looks like this:

```python
some_value = "not a boolean, lol"
if some_value:
    pass

# or
while some_value:
    pass
```

In the example above, `some_value` is clearly a `str` yet when used in an if (or while!) statement block, it is evaluated as `True`!

In general, all values in python are "truthy" unless they aren't, in which case, they are "falsy". If you can imagine, there are only a few explicit values that are defined as "falsy", find them enumerated here:

```python
[] # empty list
{} # empty dict
() # empty tuple
set() # empty set
"" # empty string
range(0) # empty range
0 # int, 0
0.0 # float, 0
None # nonetype, obvi
False # boolean false
```
_(I had the hardest time finding a definitive list of these items on the interwebs. The closest I could find that seemed "official" was [this](https://docs.python.org/2.4/lib/truth.html) py2.4(!!) "Python Library Reference". The list above is from [this](https://www.freecodecamp.org/news/truthy-and-falsy-values-in-python/) freecodecamp article)_

Ok cool - so with this clarification, it is obvious why `all([0,0,0])` evals to `False`. `0` is falsy therefore it is at least plausible to surmise that there is a naive **if statement** somewhere that fails to account for this edge case.

Moreover, it stands to reason that all of the following will also probably eval to `False`:

```python
all([False, False, False])
all([{}, {}, {})
# .. etc, you get the idea
```

Ok great - having established this, let's take to the official python3 (at time of this writing) [docs](https://docs.python.org/3/library/functions.html?highlight=any#all):

> **all(iterable)**<br/>
Return True if all elements of the iterable are true (or if the iterable is empty).

The docs also present this "equivalent" implementation:

```python
def all(iterable):
    for element in iterable:
        if not element:
            return False
    return True
```

From the documentation, two things are obvious to me:

**1**: Using `all([0,0,0])` to determine if all members of an iterable are equal is kind of a bad usecase. The purpose of the `all` method is _only_ to determine if all the values in an iterable are truthy. That's it. Full stop.  (But also, like, **TIL**)

**2**: If you _do_ want to determine whether all the values in an iterable are indeed the same value, consider:

```python
len(set([0,0,0])) == 1
```

_(Note: this will **not** work for something like `[{}, {}, {}]` since dicts are not hashable. However, for basic usecases where we want to (safely!) determine if a list of primitive types are all the same, the approach is IMO "good enough")_

_(Note 2: if you **really** want to handle all cases, including unhashable types, consider the following:_

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

_... certainly not as compact but gets the job done!)_

## Venturing into the guts of CPython

Ok, now for the meat of this story.

Let me preface this by saying: I really enjoy venturing into source code to validate behavior that I am seeing. More often than not, this is fueled by (perhaps an unreasonable...) hope that _maybe_ I'll notice something undocumented or interesting that could be helpful immediately or sometime in the future.

For this specific case though, I was wondering how easy/hard it may be to submit a PR to rectify this behavior of `all` (spoiler: not all that straight forward and more importantly, definitely not _appropriate_ given the officially documented behavior we saw above)

Still, this was an interesting exercise and worth documenting for fun and profit (...mainly fun, though)

I started by searching for `all` within the `cpython` [repo](https://github.com/python/cpython). Generally Github's code searching functionality is pretty great - the main issue here was that `all` is fairly generic word that is used _often_ both in and outside of the code (like in documentation and such).

[This](https://stackoverflow.com/a/8608609) stackoverflow suggested that builtin funcs could be found in the `Object` folder:

> However, many of the built-in types can be found in the Objects [sub-directory of the Python source trunk](https://github.com/python/cpython/tree/master/Objects). For example, see [here](https://github.com/python/cpython/blob/master/Objects/enumobject.c) for the implementation of the enumerate class or [here](https://github.com/python/cpython/blob/master/Objects/listobject.c) for the implementation of the list type.

Once I started digging into the src code, I realized that there is a _lot_ of code (surprise, surprise) in the cpython codebase. So I cloned the entire project to my local machine and started grepping the heck out of...everything in the project folder.

```bash
➜  cpython git:(master) grep -r "any(" .
```

Running the ^ above (I figured `any`, a similar method to `all` might be a less frequently used token than `all`...) I ended up with a _ton_ of results. I manually scanned through each line item in the output (anyone have a better way to search for things like this? I couldn't think of anything useful but admittedly I didn't try too hard) I ended up here:

```bash
./Python/bltinmodule.c:builtin_any(PyObject *module, PyObject *iterable)
```

That looked interesting! Looking at the func definition (ok, one definition above `builtin_any` - as I mentioned, I looked for `any` but I wanted the src for `all`):

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

We found it! This is the actual implementation of the builtin `all` method!! 

Ok cool, so let's examine it. The most interesting to us are the lines from 340 onwards:

{{< highlight c "linenos=inline,linenostart=340" >}}
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
{{< / highlight >}}


This is the main loop that walks through each item in the iterable and applies a bunch of logic to validate if it is `true` or not. To understand what `true` means, we consider line **344**, which invokes the `PyObject_IsTrue` method. Using a similar approach to what I described earlier, I was able to track down the definition of the `PyObject_IsTrue` method, reproduced below:

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

So this method, as it turns out, isn't all that complex. It does a bunch of checks against `v` a generic type called `PyObject` that, recall from the previous `builtin_all` method, is `item` -- a member of our iterable passed in to `all`. 

Let's examine this `PyObject_IsTrue` method line by line:

First, we inspect this (**line 1386**):

```c
// ...
if (v == Py_True)
    return 1;
```

Recall that `v` for us is just `0`. So this condition does not match; `0` is not `True`. Onwards! 

The next two conditions (**lines 1388-1391**):

```c
// ...
if (v == Py_False)
    return 0;
if (v == Py_None)
    return 0;
```

also do not match. `v` is `0` not `False` nor `None`.

The next check is key (**lines 1392-1394**, for this exercise, at least).

```c
// ...
else if (Py_TYPE(v)->tp_as_number != NULL &&
            Py_TYPE(v)->tp_as_number->nb_bool != NULL)
    res = (*Py_TYPE(v)->tp_as_number->nb_bool)(v);
```


Woof. I'm not super familiar with C so this code block looks especially foreign to me. 

I tried figuring out what the definition of `Py_TYPE` might be -- but unfortunately didn't get too far in my grepping adventures. So, I turned again to the python docs (...by googling, of course).

The **[Type Objects](https://docs.python.org/3/c-api/typeobj.html)** documentation had a lot of good info that helped clear up exactly what this particular line means:

```c
Py_TYPE(v)->tp_as_number
```

Based on my interpretation of the documentation + the preamble from [this helpful blog post](https://tenthousandmeters.com/blog/python-behind-the-scenes-7-how-python-attributes-work/), all types in python are instances of the C struct `_typeobject` which determines how a type behaves. `tp_as_number` is a **member** (bascially an element in the struct) of the `_typeobject` struct. Only types that are _numerical_ or support numerical usage (ie: floats or bools since they can be used as 0/1, etc) have this member defined and **NOT** set to **NULL**.

To further clarify this, let's take another dive into the code. We begin by hunting down the definition of the `_typeobject`, which is graciously reproduced for our benefit in the **[Type Objects](https://docs.python.org/3/c-api/typeobj.html#pytypeobject-definition)** docs I mentioned above. I am re-producting it here for convenience but abridging all but the relevant members:


{{< highlight c "linenos=inline,linenostart=1" >}}
typedef struct _typeobject {
    // ... !!! removing since not needed for our analysis

    /* Method suites for standard classes */

    PyNumberMethods *tp_as_number;

    // ... !!! removing since not needed for our analysis

} PyTypeObject;
{{< / highlight >}}

_([Sauce](https://github.com/python/cpython/blob/63298930fb531ba2bb4f23bc3b915dbf1e17e9e1/Doc/includes/typestruct.h))_

The main hint here for me was `PyTypeObject`; by grepping the codebase for this token, I was able to locate the following `PyTypeObject`:

{{< highlight c "linenos=inline,linenostart=2778" >}}
PyTypeObject PyZip_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "zip",                              /* tp_name */
    sizeof(zipobject),                  /* tp_basicsize */
    0,                                  /* tp_itemsize */
    /* methods */
    (destructor)zip_dealloc,            /* tp_dealloc */
    0,                                  /* tp_vectorcall_offset */
    0,                                  /* tp_getattr */
    0,                                  /* tp_setattr */
    0,                                  /* tp_as_async */
    0,                                  /* tp_repr */
    0,                                  /* tp_as_number */
    0,                                  /* tp_as_sequence */
    0,                                  /* tp_as_mapping */
    0,                                  /* tp_hash */
    0,                                  /* tp_call */
    0,                                  /* tp_str */
    PyObject_GenericGetAttr,            /* tp_getattro */
    0,                                  /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC |
        Py_TPFLAGS_BASETYPE,            /* tp_flags */
    zip_doc,                            /* tp_doc */
    (traverseproc)zip_traverse,    /* tp_traverse */
    0,                                  /* tp_clear */
    0,                                  /* tp_richcompare */
    0,                                  /* tp_weaklistoffset */
    PyObject_SelfIter,                  /* tp_iter */
    (iternextfunc)zip_next,     /* tp_iternext */
    zip_methods,                        /* tp_methods */
    0,                                  /* tp_members */
    0,                                  /* tp_getset */
    0,                                  /* tp_base */
    0,                                  /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    0,                                  /* tp_init */
    PyType_GenericAlloc,                /* tp_alloc */
    zip_new,                            /* tp_new */
    PyObject_GC_Del,                    /* tp_free */
};
{{< / highlight >}}

_([Sauce](https://github.com/python/cpython/blob/9a9c11ad41d7887f3d6440e0f0e8966156d959b5/Python/bltinmodule.c#L2778))_


**Line 2790** is the line we care about: note how the value is set to `0` here. But what is `PyZip_Type` anyways? In that same file (but further down), we observe:


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

_([Sauce](https://github.com/python/cpython/blob/9a9c11ad41d7887f3d6440e0f0e8966156d959b5/Python/bltinmodule.c#L2917))_

This provides strong evidence that the python builtin definition for `zip()` (**line 2952**, above) is actually specified by `PyZip_Type`. As we know, we cannot use `zip()` in any numerical contexts which explains why `tp_as_number` is set to `0` (in C, `null` is a constant with value of **0** ([sauce](https://www.thoughtco.com/definition-of-null-958118#:~:text=Null%20is%20a%20built%2Din,pattern%20for%20a%20null%20pointer.))).

But let's be sure...consider (randomly picked) the `float` type -- from **line 2936**:

```c
SETBUILTIN("float",                 &PyFloat_Type);
```

If we were to peer into `PyFloat_Type`, we would expect to see `tp_as_number` defined - not as `0` - but as a [`PyNumberMethods` struct](https://github.com/python/cpython/blob/63298930fb531ba2bb4f23bc3b915dbf1e17e9e1/Doc/includes/typestruct.h#L18).

We locate `PyFloat_Type` and upon inspection:

{{< highlight c "linenos=inline,linenostart=1919" >}}
PyTypeObject PyFloat_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "float",
    sizeof(PyFloatObject),
    0,
    (destructor)float_dealloc,                  /* tp_dealloc */
    0,                                          /* tp_vectorcall_offset */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_as_async */
    (reprfunc)float_repr,                       /* tp_repr */
    &float_as_number,                           /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    (hashfunc)float_hash,                       /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,   /* tp_flags */
    float_new__doc__,                           /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    float_richcompare,                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    float_methods,                              /* tp_methods */
    0,                                          /* tp_members */
    float_getset,                               /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    0,                                          /* tp_init */
    0,                                          /* tp_alloc */
    float_new,                                  /* tp_new */
    .tp_vectorcall = (vectorcallfunc)float_vectorcall,
};
{{< / highlight >}}

_([Sauce](https://github.com/python/cpython/blob/fa7ce080175f65d678a7d5756c94f82887fc9803/Objects/floatobject.c#L1919))_

**Line number 1930**, happily, proves us right! `tp_as_number` is a pointer to `float_as_number`, which is defined right above:

{{< highlight c "linenos=inline,linenostart=1883" >}}
static PyNumberMethods float_as_number = {
    float_add,          /* nb_add */
    float_sub,          /* nb_subtract */
    float_mul,          /* nb_multiply */
    float_rem,          /* nb_remainder */
    float_divmod,       /* nb_divmod */
    float_pow,          /* nb_power */
    (unaryfunc)float_neg, /* nb_negative */
    float_float,        /* nb_positive */
    (unaryfunc)float_abs, /* nb_absolute */
    (inquiry)float_bool, /* nb_bool */
    0,                  /* nb_invert */
    0,                  /* nb_lshift */
    0,                  /* nb_rshift */
    0,                  /* nb_and */
    0,                  /* nb_xor */
    0,                  /* nb_or */
    float___trunc___impl, /* nb_int */
    0,                  /* nb_reserved */
    float_float,        /* nb_float */
    0,                  /* nb_inplace_add */
    0,                  /* nb_inplace_subtract */
    0,                  /* nb_inplace_multiply */
    0,                  /* nb_inplace_remainder */
    0,                  /* nb_inplace_power */
    0,                  /* nb_inplace_lshift */
    0,                  /* nb_inplace_rshift */
    0,                  /* nb_inplace_and */
    0,                  /* nb_inplace_xor */
    0,                  /* nb_inplace_or */
    float_floor_div,    /* nb_floor_divide */
    float_div,          /* nb_true_divide */
    0,                  /* nb_inplace_floor_divide */
    0,                  /* nb_inplace_true_divide */
};
{{< / highlight >}}

_([Sauce](https://github.com/python/cpython/blob/fa7ce080175f65d678a7d5756c94f82887fc9803/Objects/floatobject.c#L1883))_


Tada! Our assumptions are correct and indeed the check:

```c
// ...
else if (Py_TYPE(v)->tp_as_number != NULL && // ...
```

is mainly checking to ensure that `v`, our `item` in question, has numerical properties as defined by the `PyNumberMethods` struct. If so, we then go on to check and ensure that:

```c
Py_TYPE(v)->tp_as_number->nb_bool != NULL
```

which leads us to our second big question: what the hell is `nb_bool`??

To answer this question - thankfully - we don't need to look all that far. But before looking into the code, let's revisit out trusty docs one last time. The "Quick Reference" section ([here](https://docs.python.org/3/c-api/typeobj.html#quick-reference)) displays a bunch of "slots" that are defined in the `_typeobject` struct:

![tp slots](/dev/img/tp_slots.png)

Clicking on the [**sub-slots**](https://docs.python.org/3/c-api/typeobj.html#sub-slots) link under the **special methods/attrs** column for `tp_as_number` leads us to:

![sub slots](/dev/img/sub_slots.png)

Generally, these "subslots" display a variety of C struct elements and the corresponding python "special method" that it relates to. In particular and most useful to note is `nb_bool`, which relates to the python `__bool__` dunder method! So basically, 

```c
Py_TYPE(v)->tp_as_number->nb_bool != NULL
```

is simply checking to ensure that the `Py_TYPE` has a valid `__bool__` method defined!

With thiat, let's now look at **line 1893** from our `static PyNumberMethods float_as_number` definition, which illustrates that for `PyFloat_Type` at least, the `nb_bool` slot is defined as `float_bool`:

```c
// ...
(inquiry)float_bool, /* nb_bool */
```

and the definition of `float_bool` is available in the same **floatobject.c** file that defines `PyFloat_Type`:

```c
static int
float_bool(PyFloatObject *v)
{
    return v->ob_fval != 0.0;
}
```
_([Sauce](https://github.com/python/cpython/blob/145bf269df3530176f6ebeab1324890ef7070bf8/Objects/floatobject.c#L841))_

On initial glance, the utility of this method is obvious - return `True` if `ob_fval` is not `0.0`. Otherwise, return `False`.

But now on to a new question: what the heck is `v->ob_fval`?? If we were to guess, it is probably the actual _numerical_ value of our variable `v` of type `PyFloatObject` (like for instance the number `3.14159` that is stored as type float).

Confirming this is easy - just look at the header file for **floatobject.c**:

{{< highlight c "linenos=inline,linenostart=15" >}}
typedef struct {
    PyObject_HEAD
    double ob_fval;
} PyFloatObject;
{{< / highlight >}}
_([Sauce](https://github.com/python/cpython/blob/63298930fb531ba2bb4f23bc3b915dbf1e17e9e1/Include/floatobject.h#L15))_


This clearly demonstrates that `PyFloatObject` has a property called `ob_fval` which is of type `double`. In `float_bool(PyFloatObject *v)`, we compare this value against `0.0` to return a boolean that determines the **"truthy"** or **"falsy"** --ness of our value.

Moreover, it is clear that for other `Py_TYPE`**s** out there (like ints or bools for instance), we can repeat this exercise and end up again at _some_ function that represents `nb_bool` (corresponding to the `__bool__` dunder method) which defines the logic that determines if the underlying value is **"truthy"** or **"falsy"**. For example, for python's `range` builtin (defined as `PyRange_Type`), the `nb_bool` method is defined as:

{{< highlight c "linenos=inline,linenostart=680" >}}
static int
range_bool(rangeobject* self)
{
    return PyObject_IsTrue(self->length);
}
{{< / highlight >}}
_([Sauce](https://github.com/python/cpython/blob/145bf269df3530176f6ebeab1324890ef7070bf8/Objects/rangeobject.c#L680))_

In other words, it generally works the same way as `float_bool` does - a static method that returns an `int` is associated with the `nb_bool` slot but of course implementation details are determined by and specific to the characteristics of the type in question (`PyRange_Type`, `PyFloat_Type`, etc)

And SO, **finally**, we can fully parse our initial code block and explain what it is doing (in the context of `all([0,0,0])`):

```c
// ...
else if (Py_TYPE(v)->tp_as_number != NULL &&
            Py_TYPE(v)->tp_as_number->nb_bool != NULL)
    res = (*Py_TYPE(v)->tp_as_number->nb_bool)(v);
```

**1**: check to see if `v` has numerical methods defined

**2**: also ensure that a proper `__bool__` method is available for `v`

**FINALLY**: if **(1)** and **(2)** are both NOT **NULL**, then **call** the `__bool__` method on `v`, which will set `res` to be `1`, `0` or some numeric representation of error (in other words, `True` or `False`).

At this point, it becomes painfully obvious as to why we get the `False` return value that we have observed for our initial example of `all([0,0,0])`.

_(Note: I sneakily did not include the actual `nb_bool` implementation for the python `int` type, which is defined in the `PyLong_Type` struct. This is mainly because for ints at least, the definition/code path is a little less obvious (but works the same way in principle) so for the purposes of clarity I chose to go with `PyFloat_Type` which IMO is easier to follow)_


## Tying it all together, finally!

Still, for the sake of completeness, let's see this thought process through to completion. I'll walk through the code path and expound on what (I am fairly sure at this point) is happening at each step.

```python
all([0,0,0])
# ??? -- we want to replace this "???" with True or False
```

The builtin method `all` is defined here:

```c
#define BUILTIN_ALL_METHODDEF    \
    {"all", (PyCFunction)builtin_all, METH_O, builtin_all__doc__},
```
_([Sauce](https://github.com/python/cpython/blob/63298930fb531ba2bb4f23bc3b915dbf1e17e9e1/Python/clinic/bltinmodule.c.h#L22))_

this is how the method `builtin_all` in associated the the python func `all()`. Next, we end up in the function definition for `builtin_all`, reproducing here for convenience:

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

On **line 341**, we produce our first `item` -- `0` since our input into the original `all()` function was `[0,0,0]`.

On **line 344**, we invoke `PyObject_IsTrue` for `0`, which is a `PyLongObject` (int, basically).

Ok, so let's reproduce `PyObject_IsTrue` below (for convenience) and trace our `item` as it traverses the control flow structure:

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

Again, because `v` -- which is `item` -- is `0` and of type `PyLongObject`, we know that specifically, **lines 1392-1394** in the logic above apply:

```c
// ...
else if (Py_TYPE(v)->tp_as_number != NULL &&
            Py_TYPE(v)->tp_as_number->nb_bool != NULL)
    res = (*Py_TYPE(v)->tp_as_number->nb_bool)(v);
```

In this case, because our `item` is indeed `0`, we know that `res` is set to `0` as well. Then, we skip to the bottom of this method, **line 1404**:

```c
return (res > 0) ? 1 : Py_SAFE_DOWNCAST(res, Py_ssize_t, int);
```

`res` is set to `0` so the return value of this function is not `1` but instead the safely downcasted value of `0`. 

_(If you're interested, you can find the definition of `Py_SAFE_DOWNCAST` [here](https://github.com/python/cpython/blob/e43baaba73a8b169b2f910b80560e4492063ae65/Include/pyport.h#L418). Super interestingly, it turns out the this downcasting action isn't **actually** safe unless in **debug** mode, this [issue](https://python-bugs-list.python.narkive.com/J38UaM3H/issue19692-rename-py-safe-downcast) has proposed renaming the method since py3.4!)_

Ok! So `PyObject_IsTrue` as it is invoked in **line 344** in the `builtin_all` method has returned `0`. Therefore we now know that `cmp` in **line 344** is `0`:

{{< highlight c "linenos=inline,linenostart=340" >}}
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
{{< / highlight >}}

Therefore, the code skips to **line 350**, where we evaluate the condition where `cmp == 0` and return `Py_RETURN_FALSE`, a "safe" false return value.

And so, in conclusion, our intial call to `all`:

```python
all([0,0,0])
# False
```

returns **False** as displayed above.

Tada!

_(PS: wondering what the difference is between `Py_RETURN_FALSE` and `Py_False`? I was too! These [docs](https://docs.python.org/3/c-api/bool.html) were very helpful in clarifying)_

## Final remarks

So here's a fun question to ask: **why??**

As in - why do this, even? I came for the possibility/thrill of contributing to python (a lang I have used+abused for a very long time to make a living) but I stayed for the learnings and...possibly new ideas for contribution??

While I have definitely ventured into python source in the past, I usually stayed in python land and rarely looked into the C code. I wasn't planning to look as far/deep as I did tonight but I am glad that I did as I feel like I have a much better understanding of how at least some parts of python now work "under the hood".

I wrote this post for my own sake mainly but also in the hopes that perhaps others may find my spelunking useful/interesting and yes, perhaps even fun!

_(PS: I wrote a follow up post to the ideas presented here where I build python from source and implement an addition to the builtin modules (that are written in C). **[Find the post here!](/dev/posts/extending-pythons-builtin-c-modules/)**)


## Sidebar: WTF is tp_bool???

Ok this really bugged me for a while. I'm pretty sure I know what is going on but I'll start from the top.

As I poured over the python source code, I had built up a mental model of how the sub-slots generally worked. Let's go back to our friend, `PyNumberMethods float_as_number`:

```c
static PyNumberMethods float_as_number = {
    float_add,          /* nb_add */
    float_sub,          /* nb_subtract */
    float_mul,          /* nb_multiply */
    float_rem,          /* nb_remainder */
    float_divmod,       /* nb_divmod */
    float_pow,          /* nb_power */
    (unaryfunc)float_neg, /* nb_negative */
    float_float,        /* nb_positive */
    (unaryfunc)float_abs, /* nb_absolute */
    (inquiry)float_bool, /* nb_bool */
    0,                  /* nb_invert */
    0,                  /* nb_lshift */
    0,                  /* nb_rshift */
    0,                  /* nb_and */
    0,                  /* nb_xor */
    0,                  /* nb_or */
    float___trunc___impl, /* nb_int */
    0,                  /* nb_reserved */
    float_float,        /* nb_float */
    0,                  /* nb_inplace_add */
    0,                  /* nb_inplace_subtract */
    0,                  /* nb_inplace_multiply */
    0,                  /* nb_inplace_remainder */
    0,                  /* nb_inplace_power */
    0,                  /* nb_inplace_lshift */
    0,                  /* nb_inplace_rshift */
    0,                  /* nb_inplace_and */
    0,                  /* nb_inplace_xor */
    0,                  /* nb_inplace_or */
    float_floor_div,    /* nb_floor_divide */
    float_div,          /* nb_true_divide */
    0,                  /* nb_inplace_floor_divide */
    0,                  /* nb_inplace_true_divide */
};
```
_([Sauce](https://github.com/python/cpython/blob/145bf269df3530176f6ebeab1324890ef7070bf8/Objects/floatobject.c#L1892))_

Take note especially of:

```c
// ...
(inquiry)float_bool, /* nb_bool */
```

Now, consider the equivalent but for `PyNumberMethods long_as_number`:

```c
static PyNumberMethods long_as_number = {
    (binaryfunc)long_add,       /*nb_add*/
    (binaryfunc)long_sub,       /*nb_subtract*/
    (binaryfunc)long_mul,       /*nb_multiply*/
    long_mod,                   /*nb_remainder*/
    long_divmod,                /*nb_divmod*/
    long_pow,                   /*nb_power*/
    (unaryfunc)long_neg,        /*nb_negative*/
    long_long,                  /*tp_positive*/
    (unaryfunc)long_abs,        /*tp_absolute*/
    (inquiry)long_bool,         /*tp_bool*/
    (unaryfunc)long_invert,     /*nb_invert*/
    long_lshift,                /*nb_lshift*/
    long_rshift,                /*nb_rshift*/
    long_and,                   /*nb_and*/
    long_xor,                   /*nb_xor*/
    long_or,                    /*nb_or*/
    long_long,                  /*nb_int*/
    0,                          /*nb_reserved*/
    long_float,                 /*nb_float*/
    0,                          /* nb_inplace_add */
    0,                          /* nb_inplace_subtract */
    0,                          /* nb_inplace_multiply */
    0,                          /* nb_inplace_remainder */
    0,                          /* nb_inplace_power */
    0,                          /* nb_inplace_lshift */
    0,                          /* nb_inplace_rshift */
    0,                          /* nb_inplace_and */
    0,                          /* nb_inplace_xor */
    0,                          /* nb_inplace_or */
    long_div,                   /* nb_floor_divide */
    long_true_divide,           /* nb_true_divide */
    0,                          /* nb_inplace_floor_divide */
    0,                          /* nb_inplace_true_divide */
    long_long,                  /* nb_index */
};
```
_([Sauce](https://github.com/python/cpython/blob/145bf269df3530176f6ebeab1324890ef7070bf8/Objects/longobject.c#L5584))_

But note specifically:

```c
// ...
(inquiry)long_bool,         /*tp_bool*/
```

Wtf is `tp_bool`?! 

This is likely due to my own ignorance/tiredness but I searched frantically for some definition, _any definition_, of `tp_bool` in the source code. Nothing. Tried the docs. Nada.

Finally, I realized that I could probably just look at the `PyNumberMethods` definition which led me to:

```c
typedef struct {
    /* Number implementations must check *both*
       arguments for proper type and implement the necessary conversions
       in the slot functions themselves. */

    // ... SKIPPING non relevant lines

    inquiry nb_bool;

    // ... SKIPPING non relevant lines
    
} PyNumberMethods;
```
_([Sauce](https://github.com/python/cpython/blob/62078101ea1be5d2fc472a3f0d9d135e0bd5cd38/Include/cpython/object.h#L104))_

From this definition, it became clear that the `tp_bool` label is just a typo. Whomp, whomp.

Probably not important enough for a PR but man did it confuse me for a while!