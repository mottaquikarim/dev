---
title: "Fifth Generic Trick for Squaring All Numbers"
date: 2022-11-28T06:52:49Z
tags: ["math", "just for fun", "featured"]
katex: true
---

{{<toc>}}

Ok so for this one, no proof (at least not yet). But, we will demonstrate by example.

# Squaring \\( \bold{30} \\)s

Let's begin here.

| Number      		| Square |
| ----------- 		| ----------- |
| \\( 30^2 \\)      | \\(900\\)       |
| \\( 31^2 \\)      | \\(961\\)       |
| \\( 32^2 \\)      | \\(1024\\)       |
| \\( 33^2 \\)      | \\(1089\\)       |
| \\( 34^2 \\)      | \\(1156\\)       |
| \\( 35^2 \\)      | \\(1225\\)       |
| \\( 36^2 \\)      | \\(1296\\)       |
| \\( 39^2 \\)      | \\(1521\\)       |

So far, there's no _real_ pattern here. But! What if we decomposed our numbers a bit? eg:

| Number      		| Square           | Left             | Middle           | Right           |
| ----------- 		| -----------      | -----------      | -----------      | -----------     |
| \\( 30^2 \\)      | \\(900\\)        | _(blank)_        | _(blank)_        | _(blank)_       |
| \\( 31^2 \\)      | \\(961\\)        | \\( 9 \\)        | \\( 6 \\)        | \\( 1 \\)       |
| \\( 32^2 \\)      | \\(1024\\)       | \\( 9 \\)        | \\( 12 \\)       | \\( 4 \\)       |
| \\( 33^2 \\)      | \\(1089\\)       | \\( 9 \\)        | \\( 18 \\)       | \\( 9 \\)       |
| \\( 34^2 \\)      | \\(1156\\)       | \\( 9 \\)        | \\( 24 \\)       | \\( 16 \\)      |
| \\( 35^2 \\)      | \\(1225\\)       | \\( 9 \\)        | \\( 30 \\)       | \\( 24 \\)      |
| \\( 36^2 \\)      | \\(1296\\)       | \\( 9 \\)        | \\( 36 \\)       | \\( 36 \\)      |
| \\( 39^2 \\)      | \\(1521\\)       | \\( 9 \\)        | \\( 54 \\)       | \\( 81 \\)      |

Ok, bear with me here. The important parts are the `middle` and `right` columns. Suppose our number ( \\( 30, 31, 32, ..., 39 \\)) is expressed as: \\( 10a + n \\) where \\( a = 3 \\) and \\( n = 0,1,2,3...,9 \\)

Then, it is clear that:

* the **middle** column can be expressed as: \\( 2 * n * a \\)
* the **right** colume can be expressed as: \\( n^2 \\)

If we look specifically at:

| Number      		| Square           | Left             | Middle           | Right           |
| ----------- 		| -----------      | -----------      | -----------      | -----------     |
| \\( 31^2 \\)      | \\(961\\)        | \\( 9 \\)        | \\( 6 \\)        | \\( 1 \\)       |

we notice that this works itself out quite nicely! \\( 31^2 = 961 \\) and our **left**, **middle** and **right** columns concatenate to this value as well. Great! But what about the rest...?

As it turns out, they _also_ work provided we move any "extra" digit over. For instance, consider:

| Number      		| Square           | Left             | Middle           | Right           |
| ----------- 		| -----------      | -----------      | -----------      | -----------     |
| \\( 32^2 \\)      | \\(1024\\)       | \\( 9 \\)        | \\( 12 \\)       | \\( 4 \\)       |

Here, **middle** is \\( 12 \\). If we "carry" the \\(1\\) from \\(12\\) over to the **left** column, we end up with:

| Number      		| Square           | Left             | Middle           | Right           |
| ----------- 		| -----------      | -----------      | -----------      | -----------     |
| \\( 32^2 \\)      | \\(1024\\)       | \\( 10 \\)        | \\( 2 \\)       | \\( 4 \\)       |

As we can clearly see, this results in \\( 1024 \\) which is in fact \\( 32^2 \\). This principle applies across the board, for instance, consider:

| Number      		| Square           | Left             | Middle           | Right           |
| ----------- 		| -----------      | -----------      | -----------      | -----------     |
| \\( 36^2 \\)      | \\(1296\\)       | \\( 9 \\)        | \\( 36 \\)       | \\( 36 \\)      |

Here, we first carry over the \\( 3 \\) in **right** over to **middle**.

| Number      		| Square           | Left             | Middle           | Right           |
| ----------- 		| -----------      | -----------      | -----------      | -----------     |
| \\( 36^2 \\)      | \\(1296\\)       | \\( 9 \\)        | \\( 39 \\)       | \\( 6 \\)       |

Then, we do it again, carrying over \\( 3 \\) in **middle** to **left**:

| Number      		| Square           | Left             | Middle           | Right           |
| ----------- 		| -----------      | -----------      | -----------      | -----------     |
| \\( 36^2 \\)      | \\(1296\\)       | \\( 12 \\)        | \\( 9 \\)       | \\( 6 \\)       |

As we can clearly see, this results in \\( 1296 \\) which is in fact \\( 36^2 \\).


# Generically

Ok so let's generalize this (we already kinda did). Given some number \\( 10a + n \\) where \\( a, n \\) are natural numbers:

| Number      			 | Left               | Middle            | Right           |
| ----------- 			 | -----------        | -----------       | -----------     |
| \\( (10a+n)^2 \\)      | \\( a^2 \\)        | \\( 2an \\)       | \\( n^2 \\)     |

And then ofc, we have to carry over any values in **middle** and **right** that are not digits.

# Ex: \\(\bold{78}^2\\)

Here:

* \\( a = 7 \\)
* \\( n = 8 \\)

| Number      		| Square           | Left             	| Middle           | Right           |
| ----------- 		| -----------      | -----------      	| -----------      | -----------     |
| \\( 78^2 \\)      | \\(6084\\)       | \\( 49 \\)        	| \\( 112 \\)      | \\( 64 \\)      |

We first carry over from the **right**

| Number      		| Square           | Left             	| Middle           | Right          |
| ----------- 		| -----------      | -----------      	| -----------      | -----------    |
| \\( 78^2 \\)      | \\(6084\\)       | \\( 49 \\)        	| \\( 118 \\)      | \\( 4 \\)      |

Ok and now we do so again from **middle**:

| Number      		| Square           | Left             	| Middle           | Right          |
| ----------- 		| -----------      | -----------      	| -----------      | -----------    |
| \\( 78^2 \\)      | \\(6084\\)       | \\( 60 \\)        	| \\( 8 \\)        | \\( 4 \\)      |

Tada! Again, doesn't work _great_ for larger numbers but for squaring anything in the \\( 20 \\)s and \\( 30 \\)s, this is probably a very quick solution for solving mentally.

