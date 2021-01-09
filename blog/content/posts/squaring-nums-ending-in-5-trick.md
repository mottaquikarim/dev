---
title: "Why does (25)(25) = 2(2+1)(100)+25? An explanation"
date: 2017-10-15T05:05:47Z
katex: true
draft: true
---

<!-- https://katex.org/docs/supported.html#units -->
<!-- https://bluestnight.com/docs/midnight/users/shortcodes/math/ -->
<!-- https://eankeen.github.io/blog/posts/render-latex-with-katex-in-hugo-blog/ -->

{{<toc>}}


So here’s a neat trick. What’s a quick way to square numbers that end in — 5 in your head?

For example, what is **25\* 25**? (Plug into a calculator real quick). We expect our trick to give us: **625.**

Now, let’s explore **how** our “trick” (more of an algorithm, really) works:

First, we take the number in the tens place.
--------------------------------------------

$$ 2 $$



Add 1 to the number in the tens place.
--------------------------------------

$$2+1 = 3$$

Multiply our first number (2) by the second number (3).
-------------------------------------------------------

$$2\*3 = 6$$

Great! Almost there, hold **6** in the back of your head for a bit.

Take the number in the ones place (5) and square it.
----------------------------------------------------

$$5^2 = 5 \* 5 = 25$$

Take the (6) from our previous computation and concatenate with (25). Result will be (625).
-------------------------------------------------------------------------------------------

## Explanation

In computer science, _concatenate_ means to smoosh together. For example, if we _add_ **9** with **8**, we get **17**. But if we _concatenate_ **9** and **8**, we get **98**. I use the term concatenate above in the same spirit.

> To summarize then, the _trick_ is to concatenate **5 \* 5** (which is easy enough, just **25**) with the _product_ of the digit in tens place and its increment.

Cool! But here’s the million dollar question: **WHY?!**

Go ahead and try this out with any number that ends in — 5. It will **always** work. But **why** does it work???

I set out to find out, outlined below is my rationalization behind the mechanics of this rule.

Let’s begin by representing **25** slightly differently:

$$25 \* 25 = 625$$
$$(20 + 5)(20 + 5) = 625$$

(**_NOTE:_** Remember that 25 \* 25 = 625. Any and all operations we run on the left side of our equation should still evaluate to 625.)

This should look very similar to an elementary principle from middle school math:

$$(a + b)(a + b)$$

(in this case, _a_ = 20 and _b_ = 5)

Now, [FOIL](https://en.wikipedia.org/wiki/FOIL_method) gives us a way to expand the number sentence above:

$$(a + b)(a + b) \newline \thickspace
	= a\*a + ab + ab + b\*b \newline \thickspace
	= a^2 + ab + ab + b^2$$

And since our decomposition of **25** is essentially _a + b_, we can apply the same approach to our number sentence (with the caveat that we will **not** evaluate the products of the numbers, nor will we sum them):

$$(20 + 5)(20 + 5) \newline \thickspace 
	= 625$$

$$20\*20 + 20\*5 + 5\*20 + 5\*5 \newline \thickspace 
	= 625$$

It is natural to want to evaluate the number sentence right there (mainly because we are easily able to). **But!** To achieve what we seek (an explanation for _why_ the algorithm we explored above works) we will abstain from evaluation and instead rely on strategically **factoring**.

$$(20 + 5)(20 + 5) = 625$$ 

Expand.

$$20\*20 + 20\*5 + 5\*20 + 5\*5 = 625$$

Rearrange.

$$\(20\*20\) + \(20\*5\) + \(20\*5\) + \(5\*5\) = 625$$

Factor.

$$\(2\*10\*20\) + \(2\*10\*5\) + \(2\*10\*5\) + \(5\*5\) = 625$$

Note the number sentence above once more, particularly realize that the first three terms all share a common \\(2\*10\\) multiplier. This means we can pull out the shared \\(2\*10\\)  terms from the first three numbers, like so:


$$2\*10\*\(20 + 5 + 5\) + 5\*5 = 625$$

It is interesting to note that just pulled out **2**, which is the number from the **tens place** in **25**. We will revisit the significance of that later on. For now, let’s trudge forward by adding the \\(5+5\\) term.

$$2\*10\(20 + 10\) + 5\*5 = 625$$

Notice now that our \\(20 + 10\\) term can be rewritten as follows:

$$\(20 + 10\) =  \newline
	\(2 \* 10 \+ 1 \* 10\) = 10\(2 \+ 1\)$$

Let’s substitute this back into our calculation:

```
(20 + 5)(20 + 5) = 625  
**20**\*20 + **20**\*5 + 5\***20** + 5\*5 = 625  
**2\*10**\*20 + **2\*10**\*5 + 5\***2\*10** + 5\*5 = 625  
**2\*10**(20 + 5 + 5) + 5\*5 = 625  
**2\*10**(20 + 10) + 5\*5 = 625\--------- ^ FROM PREVIOUS BLOCK**2\*10\***10(2 + 1) + 5\*5 = 625
```

**Now**, we are cooking. Let’s rearrange our last number sentence:

```
**2\*10\***10(2 + 1) + 5\*5 = 625  
**2\*(2+1)**\*10\*10 + 5\*5 = // possible by commutative property of  
                      // multiplication
```

That first term, _2\*(2+1)_, is our holy grail. It reflects what our “trick” posited above: we can take the digit in the tens place **_(2)_**, add one to it **_(2+1)_**, multiply by the digit itself to arrive at **6 = 2\*_(2+1)_**, the first component of our solution! Essentially, the factoring exercise shows us _where_ the **6,** or the **12** (if we try to compute _35 \* 35_), etc comes from.

Before making any conclusions, let’s try it with a few other numbers to validate the analysis above:

35 \* 35 = 1225
---------------

```
35 \* 35 = 1225  
(30 + 5)(30 + 5) = 1225  
**30**\*30 + 3**0**\*5 + 5\*3**0** + 5\*5 = 1225  
**3\*10**\*30 + **3\*10**\*5 + 5\***3\*10** + 5\*5 = 1225  
**3\*10**(30 + 5 + 5) + 5\*5 = 1225  
**3\*10**(30 + 10) + 5\*5 = 1225\---------3\*10\*10**(3 + 1)** + **25** = 1225  
**3(3 + 1)**\*10\*10 + **25** = 1225
```

75 \* 75 = 5625
---------------

```
75 \* 75 = 5625  
(70 + 5)(70 + 5) = 5625  
**70**\*70 + 7**0**\*5 + 5\*7**0** + 5\*5 = 5625  
**7\*10**\*70 + 7**\*10**\*5 + 5\*7**\*10** + 5\*5 = 5625  
**7\*10**(70 + 5 + 5) + 5\*5 = 5625  
**7\*10**(70 + 10) + 5\*5 = 5625\---------7\*10\*10**(7 + 1)** + **25** = 5625  
**7(7 + 1)**\*10\*10 + **25** = 5625
```

Ok, so it _seems_ to be working. The real key to understanding why this always works is the number sentence below:

```
**7\*10**(70 + 5 + 5) + 5\*5 = 5625
```

Generally, when we expand any number that ends in — 5 in the manner that we have above, we get something like:

```
25 \* 25 = (20 + 5)(20 + 5)  
35 \* 35 = (30 + 5)(30 + 5)  
75 \* 75 = (70 + 5)(70 + 5)
```

When the expanded sentence gets **FOILed**, we end up with an intermediary term that looks like this (bold for emphasis):

```
7\*10(70 + **5 + 5**) + 5\*5 = 5625
```

That _5 + 5_ term always shows up when squaring numbers that end in 5 (and if we were trying to compute 76 \* 76, it would be _6 + 6_, etc). And _because_ **_5 + 5_** adds to **_10_** — always, we will _always_ arrive at the last sentence below:

```
7\*10(70 + **5 + 5**) + 5\*5 = 5625  
7\*10(70 + **10**) + 5\*5 = 5625  
7\*10\*10**(7 + 1)** + **25** = 5625  
**7(7 + 1)**\*10\*10 + **25** = 5625
```

And that’s **_why_**  squaring any number ending in — 5 will result in a solution that can be computed by the algorithm above.

> It’s just a happy coincidence! _🎉 🎈🎊 🙌_

(This is also why this trick seems to **only** work with numbers that end in 5).

(PS: although I didn’t state explicitly, this trick should work for numbers > 100 as well but our **_p_** value would be > 10 which makes the “mental” part of this trick a bit more involved!)

I attempted an [inductive proof](https://en.wikipedia.org/wiki/Mathematical_induction#Description) of the concept above, written below with very little annotation.

```
For any number:10p + q,let p = any natural number  
    q = 5then,(10p + 5)(10p + 5) = p(p+1)\*100 + 25Proof:Let p = 1. Then:  
(10p + 5)(10p + 5) =   
(10 + 5)(10 + 5) =   
10\*10 + 5\*10 + 5\*10 + 25 =   
10(10 + 5 + 5) + 25 =  
10(10 + 10) + 25 =   
1\*(10 + 10)\*10 + 25 =  
1\*(10\*(1 + 1))\*10 + 25 =  
1\*(1 + 1)\*10\*10 + 25 = p(p + 1)\*10\*10 + 25  
Since p = 1Let p = k. Then:  
(10p + 5)(10p + 5) =  
(10k + 5)(10k + 5) =   
10k \* 10k + 5\*10k + 5\*10k + 25 =  
10k(10k +5 + 5) + 25 =   
k(10k + 10)\*10 + 25 =   
k(10(k+1))\*10 + 25 =  
k(k+1)\*10\*10 + 25 = p(p + 1)\*10\*10 + 25  
Since p = 1Let p = k+1. Then:  
(10p + 5)(10p + 5) =  
(10(k+1) + 5)(10(k+1) + 5) =  
Let M = k + 1  
(10M + 5)(10M + 5) =  
10M\*10M + 5\*10M + 5\*10M + 25 =  
10M(10M +5 + 5) + 25 =   
M(10M + 10)\*10 + 25 =   
M(10(M+1))\*10 + 25 =  
M(M+1)\*10\*10 + 25 = p(p + 1)\*10\*10 + 25  
Since p = k + 1 = M
```

