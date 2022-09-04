---
title: "Proving the Squaring Numbers Ending in 5 Trick"
date: 2022-09-04T00:46:49Z
tags: ["math", "just for fun"]
katex: true
---

{{<toc>}}

So here’s a neat trick. What’s a quick way to square numbers that end in — 5 in your head?

For example, what is $$25*25 = ?$$

(Plug into a calculator real quick). We expect our trick to help up compute the solution, 625, _quickly_.

Ok, let’s break down the approach.

## Example: what is **25**^2?.

First, let's re-write our number (25) in a slightly different but equivalent manner:

$$
\begin{aligned}
25^2 &= (20 + 5)^2 \cr
&= (\bold{2} * 10 + \bold{5} * 1)^2 \cr
\end{aligned}
$$

Here, we have decomposed the number **25**, as we can see:

* **2** is in the **tens** place
* **5** is in the **ones** place

To quickly arrive at the square of **25**, we:

### 1. Let **t=** the the number in the **tens** place, **2**. Let **p=** **t+1**, or **3**.


$$
\begin{aligned}
\bold{Let: } \cr
t &= 2 \cr
p &= t + 1 \cr
\bold{Then: } \cr
p &= (2) + 1 \cr
p &=3
\end{aligned}
$$

### 2. Now, let **k=** **t * p**, or **6**.

Next, we multiply **t** and **p** together:

$$
\begin{aligned}
k &= t * p \cr
&= 2 * 3 \cr
&= 6  \cr
\end{aligned}
$$


### 3. Take **k**, or **6** and put it in front of **25**, which gives us **625**. Done!

For the last part, _concatente_ **k** and **25** to arrive at our answer -- **625**.

Tada!

## But WHY tho??

This method works - for _all_ numbers ending in **5** that we would like to square. We will prove this below.


Suppose we have some number **a** that ends in **5**. We may represent **a** as:


$$
\begin{aligned}
\text{Let } \cr
a &= (10 * \bold{t} + 1 * \bold{n}) \cr
\text{Then } \cr
a^2 &= (10 * \bold{t} + 1 * \bold{n}) * (10 * \bold{t} + 1 * \bold{n}) \cr
&= (10t +n)(10t + n)
\end{aligned}
$$


**NOTE**: we assume here that **t** is an integer greater than or equal to **0**.

Now, we can expand this number sentence by FOIL, but we will not immediately simplify the terms:

$$
\begin{aligned}
a^2 &= (10t +n)(10t + n) \cr
&= 10 * 10 * t * t + 10 * t * n + 10 * t * n + n * n 
\end{aligned}
$$

Remember, we _only_ care about numbers ending in **--5**, so **n=5**. Let's substitue:

$$
\begin{aligned}
n &= 5 \cr
a^2 &= 10 * 10 * t * t + 10 * t * (5) + 10 * t * (5) + (5) * (5) \cr
&=  10 * 10 * t * t + 10 * t * (5) + 10 * t * (5) + \bold{25} \cr
\end{aligned}
$$

As we can clearly see: the mystery of why the square of any number ends in **25** is (kinda) solved. Onwards!

We will now group our terms like so:

$$
\begin{aligned}
a^2 &= \Bigg[ 10 * 10 * t * t + 10 * t * (5) + 10 * t * (5) \Bigg] + \bold{25} \cr
&= \Bigg[ \bold{10} * 10 * t * t + \bold{10} * t * (5) + \bold{10} * t * (5) \Bigg] + \bold{25}
\end{aligned}
$$

Let's pull out the **10**:

$$
\begin{aligned}
a^2 &= \bold{10}\Bigg[ 10 * t * t + t * (5) + t * (5) \Bigg] + \bold{25}
\end{aligned}
$$

Ok cool, next -- we will factor the terms _inside_ the large brackets:

$$
\begin{aligned}
a^2 &= \bold{10}\Bigg[ 10 * t * t + t * (5) + t * (5) \Bigg] + \bold{25} \cr
&= \bold{10}\Bigg[ \bold{(5)} * 2 * t * t + t * \bold{(5)} + t * \bold{(5)} \Bigg] + \bold{25} \cr 
&= \bold{10}\Bigg[ \bold{5}\bigg[  2 * t * t + t + t \bigg]  \Bigg] + \bold{25} \cr 
&= \bold{10}\Bigg[ \bold{5}\bigg[  2 * t * t + 2 * t \bigg]  \Bigg] + \bold{25} \cr
&= \bold{10}\Bigg[ \bold{5} * \bold{2 * t}\bigg[  t + 1 \bigg]  \Bigg] + \bold{25} \cr
&= \bold{10}\Bigg[ \bold{10} * \bold{t}\bigg[  t + 1 \bigg]  \Bigg] + \bold{25} \cr
&= \bold{100}\Bigg[ \bold{t}\bigg[  t + 1 \bigg]  \Bigg] + \bold{25} \cr
\end{aligned}
$$

Let's look at that last representation once again:

$$
a^2 = \bold{100}\Bigg[ \bold{t}\bigg[  t + 1 \bigg]  \Bigg] + \bold{25}
$$

Recall that **t** is the number in our **tens** place and this result demonstrates that the square of **a** (where **a** ends with **5**) is _always_ equal to the number in the **tens** place, times the number in the **tens** place plus 1. Because this value, **t(t+1)** is multiplied by 100, we are guaranteed that this number will always end in **25**.

Donezo!

## Some quick examples.

Let's put this to the test!

### **5^2** = **25**

$$
\begin{aligned}
a &= 5 \cr
a &= (10 * \bold{t} + 1 * \bold{n}) \cr
t &= 0 \cr
n &= 5 \cr
a^2 &= \bold{100}\Bigg[ \bold{t}\bigg[  t + 1 \bigg]  \Bigg] + \bold{25} \cr
5^2 &= \bold{100}\Bigg[ \bold{0}\bigg[  0 + 1 \bigg]  \Bigg] + \bold{25} \cr
25 &= \bold{100}\Bigg[ 0  \Bigg] + \bold{25} \cr
&= 0 + \bold{25} \cr
&= 25
\end{aligned}
$$

### **55^2** = **3025**

$$
\begin{aligned}
a &= 55 \cr
a &= (10 * \bold{t} + 1 * \bold{n}) \cr
t &= 5 \cr
n &= 5 \cr
a^2 &= \bold{100}\Bigg[ \bold{t}\bigg[  t + 1 \bigg]  \Bigg] + \bold{25} \cr
55^2 &= \bold{100}\Bigg[ \bold{5}\bigg[  5 + 1 \bigg]  \Bigg] + \bold{25} \cr
55^2 &= \bold{100}\Bigg[ \bold{5}\bigg[  6 \bigg]  \Bigg] + \bold{25} \cr
3025 &= \bold{100}\Bigg[ 30  \Bigg] + \bold{25} \cr
&= 3000 + \bold{25} \cr
&= 3025
\end{aligned}
$$

### **105^2** = **11025**

$$
\begin{aligned}
a &= 105 \cr
a &= (10 * \bold{t} + 1 * \bold{n}) \cr
t &= 10 \cr
n &= 5 \cr
a^2 &= \bold{100}\Bigg[ \bold{t}\bigg[  t + 1 \bigg]  \Bigg] + \bold{25} \cr
105^2 &= \bold{100}\Bigg[ \bold{10}\bigg[  10 + 1 \bigg]  \Bigg] + \bold{25} \cr
105^2 &= \bold{100}\Bigg[ \bold{10}\bigg[  11 \bigg]  \Bigg] + \bold{25} \cr
11025 &= \bold{100}\Bigg[ 110  \Bigg] + \bold{25} \cr
&= 11000 + \bold{25} \cr
&= 11025
\end{aligned}
$$

## A beautiful outcome.

Honestly, this observation strikes me as exceedingly _pretty_. We are only able to end up with the **t(t+1)** result _because_ **n=5**. With **n=5**, we are able to factor out our number sentence from above (reproduced below for convenience):

$$
\begin{aligned}
a^2 &= \bold{10}\Bigg[ 10 * t * t + t * (5) + t * (5) \Bigg] + \bold{25} \cr
&= \bold{10}\Bigg[ \bold{(5)} * 2 * t * t + t * \bold{(5)} + t * \bold{(5)} \Bigg] + \bold{25} \cr 
&= \bold{10}\Bigg[ \bold{5}\bigg[  2 * t * t + t + t \bigg]  \Bigg] + \bold{25} \cr 
\end{aligned}
$$

**t(t+1)** is _only_ possible_because_ **n** was 5 . For instance, if **n** was **6**, we would end up with:

$$
\begin{aligned}
a^2 &= \bold{10}\Bigg[ 10 * t * t + t * (6) + t * (6) \Bigg] + \bold{36} \cr
&= \bold{10}\Bigg[ \bold{(5)} * 2 * t * t + t * \bold{(6)} + t * \bold{(6)} \Bigg] + \bold{36} \cr 
&= \bold{10}\Bigg[ \bold{(5)} * 2 * t * t + \bold{12} * t \Bigg] + \bold{36} \cr 
\end{aligned}
$$

With **n=6** (as an example), we end up with terms that are cannot be easily simplified, which is why (AFAIK) no _simple_ solution for squaring numbers that _don't_ end in **5** exists in the same way. _(Heads up, I **did** find some interesting results for a more general case; will share that methodology in a future post)_.

In short:

> It’s just a happy coincidence! 🎉 🎈🎊 🙌