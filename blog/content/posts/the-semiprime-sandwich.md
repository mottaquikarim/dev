---
title: "The Semiprime Sandwich"
date: 2022-11-20T21:29:05Z
tags: ["math", "just for fun"]
katex: true
---

{{<toc>}}

# Lol, wut?

I had the opportunity to catch up with my old friend, Chai, earlier this week. It has been a _while_ since we talked and the topic of aging and birthdays came up. 

Chai is turning 32, or \\(2^5\\) years old(!!), later on this year. This is the (reasonably speaking) penultimate \\(2^n\\)_th_ of age in most of our lives: while an uncomfortable thought, it is highly unlikely anyone reading this article in the year 2022 will live to the age of \\(2^7\\)). (BTW: Chai if you're reading this (_and_ Date.now() < 1670302800000): happy early birthday, fam! 🎉🎉) 

During that conversation, something occurred to me: the numbers \\([33, 34, 35]\\) are consecutive (distinct) semiprimes!

A quick refresher:

> **semiprime**: a natural number that is the product of exactly two prime numbers

And:

> **distinct semiprime**: a semiprime that is _not_ a perfect square (eg: 25 may count as a **semiprime** but it is not a **distinct** semiprime)

Observing that \\([33, 34, 35]\\) were _consecutive_ is pretty neat: it occurred to me that this particular set was _probably_ special (or at the very least, interesting _to me_).

After some reflection, I am certain that:

1. The **longest** possible chain of consecutive, distinct semiprimes is **three**. For fun, I will refer to this as a **🥪 semiprime sandwich 🥪** 
2. The first occurance of a **semiprime sandwich** starts at 33 (so 33, 34, 35 is the **first** semiprime sandwich). 

> (**SIDEBAR**| This my friends, makes the 30s a delightfully special decade of our lives - the next time we may hope to encounter a semiprime sandwich age range would be from age 93!)

(_FWIW_, this curious property is not present on the [wikipedia page on semiprimes](https://en.wikipedia.org/wiki/Semiprime), which leads me to believe that either this observation is obvious, inconsequential, or both. Still, it was fun to think about and for me at least, a source of delight during an otherwise stressful week. Anyways, onwards with this post!)

# Justification

Note, I am _not_ labeling this a proof because my reasoning below will be pretty informal. 

---

Suppose we have some number sequence \\(n-1\\), \\(n\\), and \\(n+1\\) such that they are all distinct semiprimes. (It goes without saying that they are all also consecutive).

We have two options to consider:

* \\(n\\) could be **odd**
* \\(n\\) could be **even**

## A (possible) semiprime 🍞\\(n\\)🍞 where \\(n\\) is odd.

If \\(n\\) is odd _and_ a semiprime, we know that its two prime factors must **also** be odd. (eg: if \\(n == 35\\) then its factors are \\(5\\) and \\(7\\)). 

Also, because \\(n\\) is **odd**, then \\(n-1\\) and \\(n+1\\) _must_ be **even**. Now semiprimes _can_ be even, if they are then \\(2\\) must be one of their prime factors. Because we are surmising \\([n-1, n, n+1]\\) are all distinct semiprimes, \\(n-1\\) and \\(n+1\\) must be **even** semiprimes. 

Note that:

> Given an **even** distinct semiprime, one factor must be \\(2\\) and the other (prime) factor **must** be **odd**.

^ The reason for this is because \\(2\\) is the only even prime number. Since we are considering only distinct semiprimes, the other prime factor for an even semiprime **cannot** be \\(2\\). Therefore, that prime factor **must** be odd. Suppose then that:

$$
\begin{aligned}
n - 1 &= 2 * k
\end{aligned}
$$

where \\(k\\) is an odd number. The _next_ even number, \\([n - 1] + 2\\), is expressed as:

$$
\begin{aligned}
[n - 1] + 2 &= [2 * k] + 2 \cr
&= 2\big([k] + 1\big) \cr
&= 2\big(k + 1\big) \cr
n + 1 &= 2\big(k + 1\big) \cr
\end{aligned}
$$

So! Now, we may now rewrite:

$$
\begin{aligned}
n - 1, n, n + 1
\end{aligned}
$$

as

$$
\begin{aligned}
2k, n, 2\big(k + 1\big)
\end{aligned}
$$

Given that **if** \\(2k\\) is semiprime, then \\(k\\) is **odd**, it is clear that \\(k+1\\) **must be even**. For this reason, \\(n+1\\) _cannot_ be a semiprime.

From the analysis above, we arrive at two conclusions:

> Given \\(n\\), an odd semiprime, _either_ \\(n-1\\) **or** \\(n+1\\) is a semiprime but **not** both.

In otherwords, an **odd** semiprime cannot be preceeded **and** succeeded by a semiprime.

Also, 

> The longest possible semiprime chain when \\(n\\) is an odd semiprime is **two**.

## A semiprime 🍞\\(n\\)🍞 where \\(n\\) is even.

If \\(n\\) is an _even_ semiprime, then \\(n-1\\) and \\(n+1\\) are both odd. So, it is _possible_ for one or both numbers (\\(n-1\\) and / or \\(n+1\\)) to be semiprime.

> **Quick intuition sidebar here**| suppose we have two numbers \\(a\\) and \\(b\\) that are consecutively odd such that \\(a < b \\) (in other words, \\(b = a + 2\\)). Suppose now that \\(b\\) ends in \\(5\\). Then it is possible that \\(b\\) is a distinct semiprime (\\(35, 55, 65\\) are just a few examples of this). **Also**, if \\(b\\) ends in \\(5\\), then \\(a\\) **must** end in \\(3\\) as per our defintion that \\(b = a + 2\\). It is possible then for \\(a\\) to be a distinct semiprime if \\(3\\) is be a factor of \\(a\\) and the second factor of \\(a\\) is be any prime number > \\(2\\), such as \\(11\\) or \\(31\\). In fact, we have an example of this phenomenon from our primary example: if \\(b == 35\\), then \\(a == 33\\), both numbers are distince semiprimes.

Moreover, supposing \\([n-1, n, n+1]\\) do indeed form a semiprime sandwich (giving us a consecutive semiprime chain length of **three**), we **know** that \\(n-2\\) and \\(n+2\\) could _not_ be distinct semiprimes because:

* \\(n\\) is an even distinct semiprime, so \\(n = 2*k \\) where \\(k\\) is odd (as per our reasoning in the previous section).
* \\(n-2\\) is also even but factors to \\(n-2 = 2*(k-1)\\).
 * So \\(k-1\\) must be even (since \\(k\\) is odd) and so it is not prime 
 * **pedantic note**| (unless \\(k-1 == 2\\) but that would make \\(n == 4\\) which is a semiprime but not a **distinct** semiprime)
* likewise, \\(n+2\\) is also even but factors to \\(n+2 = 2*(k+1)\\).
 * So \\(k+1\\) must be even and therefore not prime

In short, we must conclude that:

> **IF** \\(n\\) is an even distinct semiprime, then the longest possible chain of consecutive distinct semiprimes it _may_ fall within must be \\([n-1, n, n+1]\\), with a length of **3**.

Another interpretation of our analysis here is that a **semiprime sandwich** (consecutive distinct semiprimes of length **3**) _must_ have an **even** distinct semiprime as the middle component (or _meat_, if you will).

# \\(\big[33,34,35\big]\\) is the first semiprime 🥪

The easiest way I could think of to show this was by first enumerating the first few even semiprimes. This is simple to do by hand, let's take the first few primes:

$$
\begin{aligned}
k   &=[3,5,7,11,13,17] \cr
2*k &= [6,10,14,22,26,34] \cr
\end{aligned}
$$

_(We multiply by \\(2\\) because we know that a semiprime sandwich must have an **even** semiprime as the middle element)_

For each of the results above, look before and after and analyze if distinct semiprime or not, eg:

$$
\begin{aligned}
k   &= 6 \cr
k - 1 &= 5 \cr
k + 1 &= 7 \cr
\end{aligned}
$$

Since \\(5\\) is a prime number, we know that \\(\big[5, 6, 7\big]\\) is not a valid semiprime sandwich. For this analysis, \\(34\\) (and \\(33\\), \\(35\\)) emerge as the _first_ example of a semiprime sandwich.


# PS!

A random side note here: an "almost prime" or **k-prime** number is:

> A natural number with k prime factors. For example, semiprimes can be thought of as "almost prime" with k=2. To that end, a prime number is a k-prime where k=1

I don't know how to prove this yet (and I could be very wrong here!) but I would bet that the longest consecutive sequence of k-primes possible is always k+1. For instance, with primes, the longest consecutive sequence possible is 2, eg: \\([2,3]\\) since primes can be thought of as k-prime numbers where k=1. For semiprimes, eg: k-primes where \\(k==2\\), the longest consecutive sequence possible is 3, as shown here, etc. 

UPDATE/PS: I proved myself wrong! Read more [here]({{< relref "posts/the-kth-prime-sandwich.md" >}})
