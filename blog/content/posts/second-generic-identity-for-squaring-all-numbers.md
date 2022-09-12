---
title: "Second Generic Identity for Squaring All Numbers"
date: 2022-09-12T00:48:23Z
tags: ["math", "just for fun"]
katex: true
---

{{<toc>}}

# Part 1: the Basic Trick

Let's begin with a very simplistic version of this trick. 

Consider:

$$
\begin{aligned}
11 ^ 2 &= ? \cr
&= 10 * 10 + 11 + 10 \cr
&= 100 + 21 \cr
&= 121
\end{aligned}
$$

In words:

> Suppose we have a number **N** to square. If we know the square of **N-1**, the square of **N** is simply **(N-1)(N-1)** _plus_ **N** _plus_ **N-1**.

How neat is that!

Let's prove it:

$$
\begin{aligned}
N^2 &= N * N \cr
&= \big([N-1]+1\big)\big([N-1]+1\big) \cr
&= [N-1]^2 + \big([N-1]+1\big) + \big([N-1]+1\big) + 1 \cr
&= [N-1]^2 + \big(N\big) + \big([N-1]+1\big) + 1 \cr
&= [N-1]^2 + \big(N\big) + \big(N\big) + 1 \cr
&= [N-1]^2 + \bold{\big(N\big)} + \bold{\big(N + 1\big)} \cr
\end{aligned}
$$

Ta da!

While this is a great insight, the utilitiy of this approach breaks down if we want to know the square of some number **N** but we do not know the square of **N-1**.

For instance, what if we wanted to compute **14^2** but did not know **13^2**? The question to ask now is:

> Can this be generalized further such that we can compute the square of _any_ number **N = 10t * n** (where **t** and **n** is a decomposed representation of the number, for instance if **N=15**, **t** is **1** and n is **5**) provided we know the square of **10t** (in this case, since **t=1**, **10t** would just be **10**)?


# Part 2: the Second Trick

Suppose we wanted to find **14^2** but did not know **13^2** of hand (but obviously **10^2** is **100**). Can we still find our answer? 

From our obervation above:

$$
\begin{aligned}
14^2 &= 13^2 + 13 + 14 \cr
&= \big(12^2 + 12 + 13 \big) + 13 + 14 \cr
&= 12^2 + \big(12 + 13 \big) + \big(13 + 14 \big)\cr
&= 11^2 + \big(11 + 12 \big) + \big(12 + 13 \big) + \big(13 + 14 \big)\cr
&= 10^2 + \big(\bold{10} + 11 \big) + \big(\bold{11} + 12 \big) + \big(\bold{12} + 13 \big) + \big(\bold{13} + 14 \big)\cr
&= 10^2 + \bold{\big(10 + 11 + 12 + 13\big)} + \big(11 + 12 + 13 + 14 \big) \cr
\end{aligned}
$$

This pattern looks interesting! Let's generalize it a bit:

$$
\begin{aligned}
\text{Let: } \cr
t &= 1 \cr
n &= 4 \cr
a &= 10t + n = 14 \cr
a - 1 &= 13 \cr
\end{aligned}
$$

From:

$$
\begin{aligned}
14^2 &= 10^2 + \bold{\big(10 + 11 + 12 + 13\big)} + \big(11 + 12 + 13 + 14 \big) \cr
\end{aligned}
$$

Notice that:

$$
\begin{aligned}
\big(10 + 11 + 12 + 13\big) &= \sum_{10}^{13} x_i \cr
\end{aligned}
$$

So:

$$
\begin{aligned}
\big(10 + 11 + 12 + 13\big) &= \cr
&= \big(10t + \cdots + (a-1)\big) \cr
&= \frac{4}{2}(10 + 13) \cr
&= \frac{n}{2}(10t + \big[ (a-1) \big]) \cr
\end{aligned}
$$

And:

$$
\begin{aligned}
\big(11 + 12 + 13 + 14\big) &= \sum_{11}^{14} x_i \cr
\end{aligned}
$$

So:

$$
\begin{aligned}
\big(11 + 12 + 13 + 14\big) &= \cr
&= \big(\big[ 10t + 1 \big] + \cdots + a\big) \cr
&= \frac{4}{2}(11 + 14) \cr
&= \frac{n}{2}(\big[ (10t + 1) \big]+ a) \cr
\end{aligned}
$$


Let's substitute:

$$
\begin{aligned}
14^2 &= 10^2 + \bold{\big(10 + 11 + 12 + 13\big)} + \big(11 + 12 + 13 + 14 \big) \cr
14^2 &= 100t^2 + \frac{n}{2}\big[ 10t + (a-1) \big] + \frac{n}{2}\big[ (10t + 1) + a \big] \cr
\end{aligned}
$$

Simplify:

$$
\begin{aligned}
14^2 &= 100t^2 + \frac{n}{2}\big[ 10t + a \big] - \bold{\frac{n}{2}} + \frac{n}{2}\big[ (10t + a \big] + \bold{\frac{n}{2}}\cr
\end{aligned}
$$

Rearrange:

$$
\begin{aligned}
14^2 &= 100t^2 + \frac{n}{2}\big[ 10t + a \big] + \frac{n}{2}\big[ (10t + a \big] - \bold{\frac{n}{2}} + \bold{\frac{n}{2}}\cr
\end{aligned}
$$

Combine:

$$
\begin{aligned}
14^2 &= 100t^2 + \frac{n}{2}\big[ 10t + a \big] + \frac{n}{2}\big[ (10t + a \big]\cr
\end{aligned}
$$

And finally...

>
$$
\begin{aligned}
(10t + n)^2 &= 100t^2 + n\big[ 10t + a \big]\cr
\end{aligned}
$$

Ta da!



# Examples

Lete's see if this works!

## Example: **31^2=**

$$
\begin{aligned}
\text{Let: } \cr
t &= 3 \cr
n &= 1\cr
a &= 10t + n = 31 \cr
a - 1 &= 10 \cr
\text{With: } \cr
(10t + n)^2 &= 100t^2 + n\big[ 10t + a \big]\cr 
\text{Then: } \cr
31^2 &= 100(3)^2 + (1)\big[ 10(3) + 31 \big]\cr
&= 100(3)^2 + \big[ 30 + 31 \big]\cr
&= 900 + \big[ 61 \big]\cr
&= 961 \cr
\end{aligned}
$$

## Example: **39^2=**

$$
\begin{aligned}
\text{Let: } \cr
t &= 3 \cr
n &= 9\cr
a &= 10t + n = 39 \cr
a - 1 &= 38 \cr
\text{With: } \cr
(10t + n)^2 &= 100t^2 + n\big[ 10t + a \big]\cr 
\text{Then: } \cr
39^2 &= 100(3)^2 + (9)\big[ 10(3) + 39 \big]\cr
&= 100(3)^2 + 9\big[ 30 + 39 \big]\cr
&= 900 + 9\big[ 69 \big]\cr
&= 900 + \big[ 630 - 9 \big]\cr
&= 900 + \big[ 521 \big]\cr
&= 1521 \cr
\end{aligned}
$$

^ Note, this isn't as fun for numbers where **n** > 5. However, we can easily also solve this as:

$$
\begin{aligned}
39^2 &= 40^2 - 40 - 39\cr
&= 1600 - 79\cr
&= 1521\cr
\end{aligned}
$$

# Reflections.

This one is pretty neat too, though I still contend that this solution,

>
$$
\begin{aligned}
(10t + n)^2 &= 100t^2 + n\big[ 10t + a \big]\cr
\end{aligned}
$$


is not as pretty as:

>
$$
a^2 = 10 \Bigg[ t \bigg[ \bold{a} + n \bigg] \Bigg] + n^2
$$

(From: ["Generic Trick for Squaring All Numbers"](/dev/posts/generic-trick-for-squaring-all-numbers/). )

But there you have it! _Two_ approaches for squaring numbers without having to do the actual "math" of squaring stuff.

