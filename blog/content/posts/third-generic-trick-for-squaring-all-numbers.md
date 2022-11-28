---
title: "Third Generic Trick for Squaring All Numbers"
date: 2022-11-28T05:35:45Z
tags: ["math", "just for fun"]
katex: true
---

{{<toc>}}

# TL;DR: The Trick.

## \\(\bold{56}^2\\)

$$
\begin{aligned}
(56)^2 &= (\bold{55} + 1)^2 \cr
	 	 &= 3025 + \bold{2}(55) + 1 \cr
	 	 &= 3025 + 110 + 1 \cr
	 	 &= 3136
\end{aligned}
$$

Note that:

* \\(55^2\\) can be computed [using the ending in 5 trick]({{< relref "posts/proving-the-squaring-numbers-ending-in-5-trick.md" >}})
* the really important part here is the \\(\bold{2}*55\\) bit
* this applies generally but becomes less useful the further we get from a number ending in 5.


## \\(\bold{57}^2\\)
$$
\begin{aligned}
(57)^2 &= (\bold{55} + 2)^2 \cr
	 	 &= 3025 + \bold{4}(55) + 4 \cr
	 	 &= 3025 + 220 + 4 \cr
	 	 &= 3249
\end{aligned}
$$

Note that:

* since we are **2** away from \\(55\\) here, we multiply by **4**.

## \\(\bold{58}^2\\)
$$
\begin{aligned}
(58)^2 &= (\bold{55} + 3)^2 \cr
	 	 &= 3025 + \bold{6}(55) + 9 \cr
	 	 &= 3025 + 330 + 9 \cr
	 	 &= 3364
\end{aligned}
$$

Note that:

* since we are **3** away from \\(55\\) here, we multiply by **9**.

## \\(\bold{54}^2\\)
$$
\begin{aligned}
(54)^2 &= (\bold{55} - 1)^2 \cr
	 	 &= 3025 - \bold{2}(55) + 1 \cr
	 	 &= 3025 - 110 + 1 \cr
	 	 &= 2916
\end{aligned}
$$

Note that:

* since we are **-1** away from \\(55\\) here, we multiply by **-2**.

# Demonstrating why this works

Let's start with a very simple example and then we can expound from there. Say we have a number that ends in \\(6\\), such as \\(46\\) or \\(56\\).

## Applying to numbers ending in \\( \bold{6} \\) only.

We can express this number as:

$$
10a + 6
$$

where \\(a\\) represents the digit in the **tens place**. Now, as we know, we have a [shortcut for figuring out how to square numbers ending in 5]({{< relref "posts/proving-the-squaring-numbers-ending-in-5-trick.md" >}}). Let's try to use that knowledge as a starting point here. Let's rewrite our number as:

$$
\begin{aligned}
10a + 6 &= \bigg[\big( 10a + 5 \big) + 1 \bigg] \cr
\end{aligned}
$$

Ok! This is cool, because we can now express \\( (10a + 6)^2 \\) as:

$$
\begin{aligned}
(10a + 6)^2 &= \bigg[\big( 10a + 5 \big) + 1 \bigg]^2 \cr
		    &= \big( 10a + 5 \big)^2 + 2(1)\big( 10a + 5 \big) + 1 \cr
\end{aligned}
$$

Now remember, \\( 10a + 5 \\) is the number we know how to square quickly/easily. So, our problem now simplifies to:

1. First, apply the trick for squaring the number ending in 5
2. Then, double the number ending in 5
3. Finally, add the result from (1) to the result from (2) and then add our third piece, the \\( \bold{1} \\) to the sum. This gives us our solution/trick for squaring **all numbers ending in 6**.

## Generic solution

Instead of numbers ending in \\(6\\) let's now consider any number \\(n\\) such that \\( 0 < n < 10 \\). Now we can express our number as:

$$
10a + n
$$

We still want to decompose our number, \\( 10a + n \\) into some form such that we have a number ending in **5**. Let there be some number \\(k\\) such that \\( n = 5 + k \\). Then:

$$
\begin{aligned}
10a + n &= \bigg[\big( 10a + 5 \big) + k \bigg] \cr
\end{aligned}
$$

We're in business! Note that if we were considering a number ending in **6**, then \\(k = 1\\) as we saw in the previous section. Let's simplify:

$$
\begin{aligned}
(10a + n)^2 &= \bigg[\big( 10a + 5 \big) + k \bigg]^2 \cr
		    &= \big( 10a + 5 \big)^2 + 2(k)\big( 10a + 5 \big) + k^2 \cr
\end{aligned}
$$

Tada! While it doesn't look like much, this actually brings us to the examples we saw earlier. Let's try one of our examples again, but now with our formula applied.

### \\(\bold{56}^2\\)

$$
\begin{aligned}
(10a + n)^2 &= \big( 10a + 5 \big)^2 + 2(k)\big( 10a + 5 \big) + k^2 \cr
\end{aligned}
$$

Here, \\( a = 5 \\), \\( n = 6 \\) and \\( k = 1 \\). Substitute:

$$
\begin{aligned}
(10a + n)^2 	&= \big( 10a + 5 \big)^2 + 2(k)\big( 10a + 5 \big) + k^2 \cr
(10(5) + 6)^2 	&= \big( 10(5) + 5 \big)^2 + 2(1)\big( 10(5) + 5 \big) + (1)^2 \cr
				&= \big( 55 \big)^2 + 2(1)\big( 55 \big) + (1)^2 \cr
\end{aligned}
$$

This may looks weird / difficult but it's actually really easy to compute mentally since the ending in 5 trick is so simple. The real drawback to this solution is honestly the middle term, as our number ends in a digit further away from 5, the cognitive load for computing 2 times that number or 4 times that number starts to get more difficult.

Thankfully, there are better solutions to this (that I have stumbled on). More on those in subsequent posts.