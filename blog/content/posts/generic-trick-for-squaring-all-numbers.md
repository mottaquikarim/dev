---
title: "Generic Trick for Squaring All Numbers"
date: 2022-09-05T04:28:00Z
tags: ["math", "just for fun", "featured"]
katex: true
---

{{<toc>}}

# TL;DR: The Trick.

Let's first grok the trick just by pattern recognition.

## Example: **31^2=**

$$
\begin{aligned}
3\bold{1}^2 &= (\bold{3} * 10 + \bold{1}) \cr
\bold{3} * (3\bold{1} + \bold{1}) &= 96\text{\textunderscore} \cr
1^2 &= \space\space\space\space 1\cr
\hline
&= 961
\end{aligned}
$$

## Example: **54^2=**

$$
\begin{aligned}
5\bold{4}^2 &= (\bold{5} * 10 + \bold{4}) \cr
\bold{5} * (5\bold{4} + \bold{4}) &= 290\text{\textunderscore} \cr
4^2 &= \space\space\space\space 16\cr
\hline
&= 2916
\end{aligned}
$$

## Example: **79^2=**

$$
\begin{aligned}
7\bold{9}^2 &= (\bold{7} * 10 + \bold{9}) \cr
\bold{7} * (7\bold{9} + \bold{9}) &= 616\text{\textunderscore} \cr
9^2 &= \space\space\space\space 81\cr
\hline
&= 6241
\end{aligned}
$$

## Example: **106^2=**

$$
\begin{aligned}
10\bold{6}^2 &= (\bold{10} * 10 + \bold{6}) \cr
\bold{10} * (10\bold{6} + \bold{6}) &= 1120\text{\textunderscore} \cr
6^2 &= \space\space\space\space\space\space 36\cr
\hline
&= 11236
\end{aligned}
$$

# Proof.

Let's prove this result by using a similar approach that we took in ["Proving the Squaring Numbers Ending in 5 Trick"](/dev/posts/proving-the-squaring-numbers-ending-in-5-trick/). 

$$
\begin{aligned}
\text{Let: } a &= (10 * \bold{t} + \bold{n}) \space \text{where: }\bold{t} \geq 0, \bold{n} \geq 0 \cr
\text{Then: } a^2 &= (10 * \bold{t} + \bold{n})^2 \cr
&= (10 * \bold{t} + \bold{n}) (10 * \bold{t} + \bold{n}) \cr
\end{aligned}
$$


Let's expand this, using FOIL. Our objective is to isolate **a=(10t + n)** in our simplification process:

$$
\begin{aligned}
a^2 &= (10 * \bold{t} + \bold{n}) (10 * \bold{t} + \bold{n}) \cr
&= \bold{10} * 10 * t * t + \bold{10} * t * n + \bold{10} * t * n + n^2 \cr
&= 10 \Bigg[ 10 * \bold{t} * t + \bold{t} * n + \bold{t} * n \Bigg] + n^2 \cr
&= 10 \Bigg[ t \bigg[ \bold{10 * t + n} + n \bigg] \Bigg] + n^2 \cr
\text{Substitute: } a &= (10 * \bold{t} + \bold{n}) \cr
&= 10 \Bigg[ t \bigg[ \bold{a} + n \bigg] \Bigg] + n^2 \cr
\end{aligned}
$$

That last result:

$$
a^2 = 10 \Bigg[ t \bigg[ \bold{a} + n \bigg] \Bigg] + n^2
$$

Proves our observation. 

## Example: **31^2=**
Let's consider our first example: **31^2** as a gut check -- 

$$
\begin{aligned}
a &= 31 \cr
&= (10 * \bold{3} + \bold{1}) \cr
\text{Therefore: } \cr
t &= 3 \cr
n &= 1 \cr
\text{Substitute. } \cr
a^2 &= 10 \Bigg[ t \bigg[ \bold{a} + n \bigg] \Bigg] + n^2 \cr
&= 10 \Bigg[ \bold{3} \bigg[ \bold{31} + \bold{1} \bigg] \Bigg] + (1)^2 \cr
&= 10 \Bigg[ \bold{3} \bigg[ \bold{32} \bigg] \Bigg] + (1)^2 \cr
&= 10 \Bigg[ \bold{96} \Bigg] + (1)^2 \cr
&= 960 + 1 \cr
&= 961 \cr
\end{aligned}
$$

Another way to look at this:

$$
\begin{aligned}
3\bold{1}^2 &= (\bold{3} * 10 + \bold{1}) \cr
t \bigg[ \bold{a} + n \bigg] &= \bold{3} * (3\bold{1} + \bold{1}) = 96\text{\textunderscore} \cr
n^2 &= 1^2 \space\space\space\space\space\space\space\space\space\space\space\space\space\space\space\space\space = \space\space\space\space 1\cr
\hline
&= \space\space\space\space\space\space\space\space\space\space\space\space\space\space\space\space\space\space\space\space\space\space\space\space\space\space 961
\end{aligned}
$$

# Reflections.

IMO, this representation of our **a^2** identity:

$$
a^2 = 10 \Bigg[ t \bigg[ \bold{a} + n \bigg] \Bigg] + n^2
$$

is **very nice to look at** 😍😍.

Practically speaking, it may not be simple (nor would it be fast) to compute **7 * 88** (to square **79**, for example) mentally. But knowing that the squaring of a number (a 2 digit by 2 digit operation) can be simplified to a simpler computation (a 1 digit by 2 digit operation, where the two factors being multiplied are determined by the actual number itself) is (to me at least) **just super neat**, man. 


**NOTE FOR MY FUTURE SELF**:
I ascertained this result by noticing that:

$$
\begin{aligned}
3^2 &= \space\space\space\space\bold{0}9 \cr
13^2 &= \space\space\bold{16}9 \cr
23^2 &= \space\space\bold{52}9 \cr
33^2 &= \bold{108}9
\end{aligned}
$$

The terms that are _not_ **9**, I realized, were the sum of an arithmetic sequence where **d=20** and the initial value was **16**. In other words:

$$
\begin{aligned}
\text{Let: } d &= 20 \cr
16 &= 0 + 16 + 0 * d \cr
52 &= 16 + 16 + 1 * d \cr
108 &= 52 + 16 + 2 * d \cr
\end{aligned}
$$

Because I knew **d**, the first term (**16**) and how many terms there would be in the sequence (3 terms if squaring **33**, 2 terms if squaring **23**, etc) I realized I could rewrite the numbers above as:

$$
\begin{aligned}
\text{Sum of arithmetic seq: } S &= \dfrac{n}{2}\bigg(a_{0} + a_n \bigg) \cr
52 &= \dfrac{2}{2}\bigg(a_0 + a_1 \bigg) \cr
&= \dfrac{2}{2}\bigg(a_0 + \big[ a_0 + 1 * d \big] \bigg) \cr
&= \dfrac{2}{2}\bigg(16 + \big[ 16 + 1 * d \big] \bigg) \cr
&= \dfrac{2}{2}\bigg(16 + \big[ 16 + 20 \big] \bigg) \cr
&= \dfrac{2}{2}\bigg(16 + \big[ 36 \big] \bigg) \cr
&= \bigg(16 + \big[ 36 \big] \bigg) \cr
&= 2\bigg( \bold{26} \bigg) \cr
108 &= \dfrac{3}{2}\bigg(a_0 + a_2 \bigg) \cr
&= \dfrac{3}{2}\bigg(a_0 + \big[ a_0 + 2 * d \big] \bigg) \cr
&= \dfrac{3}{2}\bigg(16 + \big[ 16 + 2 * d \big] \bigg) \cr
&= \dfrac{3}{2}\bigg(16 + \big[ 16 + 2 * \bold{20} \big] \bigg) \cr
&= \dfrac{3}{2}\bigg(16 + \big[ 16 + 40 \big] \bigg) \cr
&= \dfrac{3}{2}\bigg(16 + \big[ 56 \big] \bigg) \cr
&= 3\bigg(8 + \big[ 28 \big] \bigg) \cr
&= 3\bigg( \bold{36} \bigg) \cr
&= \bold{108} \cr
\end{aligned}
$$

At this point, I noticed the pattern where:

$$
\begin{aligned}
52 &= 2\bigg( \bold{26} \bigg) \cr
&= 2(23 + 3) \cr
108 &= 3\bigg( \bold{36} \bigg) \cr
&= 3(33 + 3) \cr
\end{aligned}
$$

which strongly hinted that I might be able to isolate this form from expanding out **a^2** where **a=(10t+n)**.
