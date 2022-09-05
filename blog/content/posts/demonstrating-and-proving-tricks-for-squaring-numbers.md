---
title: "Demonstrating a Trick for Squaring Numbers Ending in 6"
date: 2022-09-04T11:13:37Z
tags: ["math", "just for fun"]
katex: true
---

{{<toc>}}

<!--
Katex:
- https://katex.org/docs/supported.html#style-color-size-and-font
- https://katex.org/docs/support_table.html
-->

**NOTE**: This post builds on my post ["Proving the Squaring Numbers Ending in 5 Trick"](/dev/posts/proving-the-squaring-numbers-ending-in-5-trick/). I'll be heavily referencing it in this post.

# Methodology.

In my last post on this topic (referenced above), we proved that numbers ending in **--5** have a neat property, namely that if:

$$
\begin{aligned}
\text{Let: } \cr
a &= (10t + n) \cr
\text{Where: } \cr
n &= 5 \cr
\end{aligned}
$$

Then:

$$
\begin{aligned}
a^2 &= (10t + 5)(10t + 5) \cr
&= 10 * 10 * t * t + 10 * 5 * t + 10 * 5 * t + 5 * 5 \cr
&= \bold{10}\Bigg[ 10 * t * t + t * (5) + t * (5) \Bigg] + \bold{25} \cr
&= \bold{10}\Bigg[ \bold{(5)} * 2 * t * t + t * \bold{(5)} + t * \bold{(5)} \Bigg] + \bold{25} \cr 
&= \bold{10}\Bigg[ \bold{5}\bigg[  2 * t * t + t + t \bigg]  \Bigg] + \bold{25} \cr 
&= \bold{10}\Bigg[ \bold{5}\bigg[  2 * t * t + 2 * t \bigg]  \Bigg] + \bold{25} \cr
&= \bold{10}\Bigg[ \bold{5} * \bold{2 * t}\bigg[  t + 1 \bigg]  \Bigg] + \bold{25} \cr
&= \bold{10}\Bigg[ \bold{10} * \bold{t}\bigg[  t + 1 \bigg]  \Bigg] + \bold{25} \cr
&= \bold{100}\Bigg[ \bold{t}\bigg[  t + 1 \bigg]  \Bigg] + \bold{25} \cr
\end{aligned}
$$

Our result:

$$
\begin{aligned}
a^2 &= \bold{100}\Bigg[ \bold{t}\bigg[  t + 1 \bigg]  \Bigg] + \bold{25} \cr
\end{aligned}
$$

demonstrates _why_ [the trick](/dev/posts/proving-the-squaring-numbers-ending-in-5-trick/#example-what-is-25-2) works. 

Let's review it here once more for funsies though. We write our number in this form: 

$$
\begin{aligned}
a^2 &= (10t + n)(10t + n) \cr
\bold{Let: } \cr
n &= 5 \cr
\bold{So: } \cr
a^2 &= (10t + 5)(10t + 5) \cr
\end{aligned}
$$

So, we can interpret **t** as the numerical value _not_ in the ones place (I say this because if **a = 105**, we let **t=10**, not **0**). Our formula:

$$
\begin{aligned}
a^2 &= \bold{100}\Bigg[ \bold{t}\bigg[  t + 1 \bigg]  \Bigg] + \bold{25} \cr
\end{aligned}
$$

lets us wave our hands a bit like so:

$$
\begin{aligned}
\bold{Let: } \cr 
a &= 25 \cr
\bold{So: } \cr 
t &= 2 \cr
n &= 5 \cr
\end{aligned}
$$

1. Take **t**, add **1** to it (so **t + 1 = 2 +1 = 3**).
2. Multiply the result from (1) with **t** (so **2 * 3 = 6**)
3. Concatenate with **25**, which gives us a grand total of: **625**.

Step (3) is the hand-wavey part and it only works because our **t[t+1]** term is multiplied by **100**, enabling us to "concatenate" without worry.

And more importantly, **n=5** is _crucial_ here because we are able to factor:

$$
\begin{aligned}
a^2 &= (10t + 5)(10t + 5) \cr
&= 10 * 10 * t * t + 10 * 5 * t + 10 * 5 * t + 5 * 5 \cr
\end{aligned}
$$

to a representation like:

$$
\begin{aligned}
a^2 &= \bold{100}\Bigg[ \bold{t}\bigg[  t + 1 \bigg]  \Bigg] + \bold{25} \cr
\end{aligned}
$$

**_because_** the value in our ones place (**n=5**) is a multiple of _10_, which allows us to pull out the **5** from:

$$
\begin{aligned}
&= \bold{10}\Bigg[ \bold{(5)} * 2 * t * t + t * \bold{(5)} + t * \bold{(5)} \Bigg] + \bold{25} \cr 
\end{aligned}
$$

into:

$$
\begin{aligned}
&= \bold{10}\Bigg[ \bold{5} * \bold{2 * t}\bigg[  t + 1 \bigg]  \Bigg] + \bold{25} \cr
\end{aligned}
$$

So: That **5** is important!

And, while working on this post, it occurred to me that we can represent _any_ whole number (eg: **n=1**, **n=2**, etc) in terms of **5** (for instance **n=6** could be represented as **n=5+1**). For this reason, I believe we can find similar (but less pretty) tricks for _any_ whole number.

In the rest of this (admittely long post), I will work backwards from the proof to the trick for numbers where **n=1**, **n=2**, etc.

# Numbers where **n=6** (eg: **16**, **26**, etc).

## Proof.

$$
\begin{aligned}
\text{Let: } \cr
a &= (10t + n) \cr
\text{Where: } \cr
n &= 6 \cr
\end{aligned}
$$

Then:

$$
\begin{aligned}
a^2 &= (10t + \bold{6})(10t + \bold{6}) \cr
&= 10 * 10 * t * t + 10 * \bold{6} * t + 10 * \bold{6} * t + \bold{6} * \bold{6} \cr
\end{aligned}
$$

We may represent **6** as **6 = 5 + 1**. (Note, we just multiply the last term, **6 * 6**, for the sake of simplicity). Substituting:

$$
\begin{aligned}
a^2 &= (10t + \bold{6})(10t + \bold{6}) \cr
&= 10 * 10 * t * t + 10 * \bold{6} * t + 10 * \bold{6} * t + \bold{6} * \bold{6} \cr
&= 10 * 10 * t * t + 10 * (\bold{5 + 1}) * t + 10 * (\bold{5 + 1}) * t + 36 \cr
\end{aligned}
$$

Let's now simplify this number sentence, our goal is to get it to look as close as possible to our **t(t+1)** formula:

$$
\begin{aligned}
a^2 &= 10 * 10 * t * t + 10 * (\bold{5 + 1}) * t + 10 * (\bold{5 + 1}) * t + 36 \cr
&= 10 * 10 * t * t + 10 * \bold{5} * t + 10 * \bold{1} * t + 10 * \bold{5} * t + 10 * \bold{1} * t + 36 \cr
&= \bigg[10 * 10 * t * t + 10 * \bold{5} * t + 10 * \bold{5} * t \bigg] + 10 * \bold{1} * t + 10 * \bold{1} * t + 36 \cr
\end{aligned}
$$

Note that the last representation above (in square brackets) looks just like the result we were working with when proving the **n=5** trick. Let's complete our simplification:

$$
\begin{aligned}
a^2 &= \bigg[10 * 10 * t * t + 10 * \bold{5} * t + 10 * \bold{5} * t \bigg] + 10 * \bold{1} * t + 10 * \bold{1} * t + 36 \cr
&= 10 \Bigg[ 10 * t * t + \bold{5} * t + \bold{5} * t \Bigg] + 10t + 10t + 36 \cr
&= 10 \Bigg[ 5 \bigg[ 2 * t * t + t + t \bigg] \Bigg] + 20t + 36 \cr
&= 10 \Bigg[ 5 \bigg[ 2 * t * t + 2 * t \bigg] \Bigg] + 20t + 36 \cr
&= \bold{10}\Bigg[ \bold{5} * \bold{2 * t}\bigg[  t + 1 \bigg]  \Bigg] + 20t + 36 \cr
&= \bold{10}\Bigg[ \bold{10} * \bold{t}\bigg[  t + 1 \bigg]  \Bigg] + 20t + 36 \cr
&= \bold{100}\Bigg[ \bold{t}\bigg[  t + 1 \bigg]  \Bigg] +  20t + 36 \cr
\end{aligned}
$$

Tada! We have now shown that the square of numbers where **n=6** look _just like_ the square of numbers where **n=5** but with the **25** replaced by **20t + 36**. This is a pretty cool result in and of itself -- for example what is **26^2**? 

Easy, 

1. **t(t+1)** is **6**, 
2. **20t + 36** is **40 + 36** or **76** 

So the result is: **676**. But, we can do better. (Why? Because **20t + 36** may get annoying when **t=12** let's say)


Let's start with the last line from above and simplify the last two terms:

$$
\begin{aligned}
a ^ 2 &= \bold{100}\Bigg[ \bold{t}\bigg[  t + 1 \bigg]  \Bigg] +  20t + 36 \cr
&= \bold{100}\Bigg[ \bold{t}\bigg[  t + 1 \bigg]  \Bigg] +  20t + 30 + 6 \cr
&= \bold{100}\Bigg[ \bold{t}\bigg[  t + 1 \bigg]  \Bigg] +  10 * \bold{2} * t + 10 * \bold{3} + 6 \cr
&= \bold{100}\Bigg[ \bold{t}\bigg[  t + 1 \bigg]  \Bigg] +  10 \Bigg[ \bold{2}t + \bold{3} \Bigg] + 6 \cr
\end{aligned}
$$

Now _this_ is pretty cool. Let's try this again for **26^2**:

1. **t(t+1)** is **6**,
2. **2t + 3** is **7**,
3. We can _concatenate_ here because **6** is in the _hundreds_ place, **7** is in the _tens_ place and the last **6** is in the _ones_ place.

So the result is **676** (but without having to add two two-digit numbers together). Another way to think about this:

$$
\begin{aligned}
t\big[t + 1 \big] &= 600 \cr
2t + 3 &= \space\space 70 \cr
6 &= \space\space\space\space 6 \cr
\hline \cr
&= 676
\end{aligned}
$$

Basically, ignore the **0**s and we can easily synthesize the solution.

## Example: What is 36^2?

Let's put this to the test with an example.

### 1. Let **t=** the number in the **tens** place, **3**. Let **p= t+1**, or **4**

$$
\begin{aligned}
t &= \bold{3} \cr
p &= t + 1 \cr
&= 3 + 1 \cr
&= \bold{4}
\end{aligned}
$$

### 2. Now let **k= t * p**, or **12**.

$$
\begin{aligned}
k &= t * p \cr
&= t\big[t + 1\big] \cr
&= 3 \big[4\big] \cr
&= \bold{12}
\end{aligned}
$$

### 3. Next let **m= 2t * 3**, or **9**.

$$
\begin{aligned}
m &= 2t * 3 \cr
&= 2 * \bold{3} + 3 \cr
&= 6 + 3 \cr
&= \bold{9}
\end{aligned}
$$

### 4. Finally, combine **k** (12), **m** (9) and **6** to get: **1296**. Done!

$$
\begin{aligned}
t\big[t + 1 \big] &= 1200 \cr
2t + 3 &= \space\space\space\space 90 \cr
6 &= \space\space\space\space\space\space 6 \cr
\hline \cr
&= 1296
\end{aligned}
$$

We lucked out here because **m** is just **9**, so we concatenate to get **1296**. 

## Some quick examples.

Let's put this to the test!

### 6^2 = 36

$$
\begin{aligned}
\text{Let: } \cr
t &= 0 \cr
n &= 6 \cr
t\big[t + 1 \big] &= \space\space\space\space\space\space 0 \cr
2t + 3 &= \space\space\space\space 30 \cr
6 &= \space\space\space\space\space\space 6 \cr
\hline \cr
&= \space\space\space\space\space\space 36
\end{aligned}
$$


### 86^2 = 7396

$$
\begin{aligned}
\text{Let: } \cr
t &= 8 \cr
n &= 6 \cr
t\big[t + 1 \big] &= 7200 \cr
2t + 3 &= \space\space 190 \cr
6 &= \space\space\space\space\space\space 6 \cr
\hline \cr
&= 7396
\end{aligned}
$$

**NOTE**: for numbers where **2t+3** > 10, we can just add the number in the _tens_ place (like **1** in the case of **19** above) to the _ones_ place digit of **t(t+1)** (like **2** in the case of **72** above). So, the computation becomes something like:

$$
\begin{aligned}
t\big[t + 1 \big] &= 7\bold{2} \cr
2t + 3 &=\space\space \bold{1}9 \cr 
6 &= \space\space\space\space\space\space 6 \cr
\hline \cr
&= 7\bold{3}96
\end{aligned}
$$

(Note the bolds; personally I find this a bit easier when computing mentally).

## Final comments.

While this outcome isn't _as pretty_ as the **n=5** observation, IMO it is pretty _awesome_ that we can use the technique demonstrated above to find tricks for basically all whole numbers. For the rest of this post, I will be leveraging this approach to highlight tricks for the rest of our set of **n=[1,2,...]** (with some tricks being better/easier than others).

