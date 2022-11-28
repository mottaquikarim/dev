---
title: "Fourth Generic Trick for Squaring All Numbers"
date: 2022-11-28T06:22:00Z
tags: ["math", "just for fun", "featured"]
katex: true
---

{{<toc>}}

This approach my friends is _pretty damn cool_ 😎.

# Derivation

Let's get straight to the derivation here as IMO that is the best way to grok this problem. Suppose we have some number - let's say **82** - that we'd like to square.

Moreover, suppose there was a number _close_ to **82** that we knew how to square easily. In this case, let's go with **80** since \\( 80^2 = \bold{6400} \\) (and this is something we can easily compute mentally).

Now comes the fun part, let:

* \\( \bold{b} = 80 \\): the number that we can square easily
* \\( \bold{c} = 82 \\): the number that we wish to find the solution for

Also, lete there be some number \\( a \\) such that:

$$
a^2 + b^2 = c^2
$$

Ok, symbolically, we solve for \\(a\\) here easily enough:

$$
a^2 = c^2 - b^2
$$

By itself, this is not super useful. **However**, recall that the _difference_ of two squares can be simplied such that:

$$
c^2 - b^2 = (c+b)(c-b)
$$

Meaning:

$$
a^2 = (c+b)(c-b)
$$

Let's now substitute super quick with the example values we chose:

$$
\begin{aligned}
a^2  		&= (c+b)(c-b) \cr
 	 		&= (82+80)(82-80) \cr
 	 		&= (162)(2) \cr
\bold{a^2}  &= \bold{324} 
\end{aligned}
$$

Ok, so what? Well, if we add this back to \\( 80^2 \\):

$$
\begin{aligned}
a^2 + b^2 &= c^2 \cr
a^2  &= 324 \cr
b^2  &= 6400 \cr
324 + 6400 &= c^2 \cr
6724 	 &= (82)^2 \cr
\end{aligned}
$$

Tada! This approach is super neat because you can use _any_ square you know as a starting point!

For instance, suppose we wanted to find \\( 88^2 \\) and we wanted to start with \\( 90^2 \\) since we can compute the square in our head. Then:

$$
\begin{aligned}
a^2 + b^2 	&= c^2 \cr
c^2 		&= (88)^2 \cr
b^2  		&= (90)^2 \cr
	 		&= 8100 \cr
a^2  		&= (c+b)(c-b) \cr
			&= (88+90)(88-90) \cr
			&= (178)(-2) \cr
			&= -356 \cr
-356 + 8100 &= c^2 \cr
7744 	 &= (88)^2 \cr
\end{aligned}
$$

Ok, that one wasn't a great example for mental math (but kudos to you if you can quickly (and accurately!) subtract 356 from 8100 in your head!) but overall this principle works great! Let's try that same problem above but know our "known" starting point is \\( 85^2 \\) (which we can compute easily with the ending in 5 trick).

$$
\begin{aligned}
a^2 + b^2 	&= c^2 \cr
c^2 		&= (88)^2 \cr
b^2  		&= (85)^2 \cr
	 		&= 7225 \cr
a^2  		&= (c+b)(c-b) \cr
			&= (88+85)(88-85) \cr
			&= (173)(3) \cr
			&= 519 \cr
519 + 7225 &= c^2 \cr
7744 	 &= (88)^2 \cr
\end{aligned}
$$

(FWIW, \\( 519 + 7225 \\) _may_ some scary at first to perform mentally but I swear it isn't! Just add \\( 520 \\) to \\( 7200 \\) (that should be easy: \\( 7720 \\)) and then add back \\( 25 \\), so \\( 7745 \\) and then take away \\( 1 \\) which gets you \\( 7744\\) )

# Recap

Ok so let's recap this - given some number \\( n \\) you want to square:

1. Find a number _close by_ to \\( n \\) that you know how to square in your head (either because you have it memorized or because you have a trick that makes it significantly easier). Let's call this number \\( \bold{k} \\).
2. Compute \\( \big[ n+k \big]\big[ n-k \big] \\)
3. Add the result from (2) to \\( \bold{k}^2 \\)
4. ???
5. Profit!

I really like this one!
