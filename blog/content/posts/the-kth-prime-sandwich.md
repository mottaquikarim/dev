---
title: "🍞 The K-Prime 🍞"
date: 2022-12-03T05:27:51Z
tags: ["math", "just for fun"]
katex: true
---

{{<toc>}}

# Hol up.

Remember this? 🍞 [The Semiprime]({{< relref "posts/the-semiprime-sandwich.md" >}}) 🍞

Towards the bottom, I made a bold claim!

> I don't know how to prove this yet (and I could be very wrong here!) but I would bet that the longest consecutive sequence of k-primes possible is always k+1. For instance, with primes, the longest consecutive sequence possible is 2, eg: \\([2,3]\\) since primes can be thought of as k-prime numbers where k=1. For semiprimes, eg: k-primes where \\(k==2\\), the longest consecutive sequence possible is 3, as shown here, etc. 

Let me expound. Suppose instead of considering semiprimes (or 2-primes), we considered 3-prime numbers. My conjecture was that we would expect to find some sequence of consecutive numbers of **max length** \\(4\\) (\\(k = 3, k+1 = 4\\)).

And more generally speaking, for a k-prime number, we could expect to find some sequence of consecutive numbers of **max len** \\(k+1\\).

Fam, I'm here today to tell you that I was very right in surmising that "I could be very wrong here!"...because I was! In this post, I'll show that:

> Given any class of k-prime numbers, the **longest length** sequence of consecutive numbers that are k-prime is **three**. We will call this the k-prime sandwich.

_(Let's note this as **Observation 1**)_

Then, I'll show that:

> Given any k-prime sandwich, one of the "bread slices" **must** be divisible by **three**.

_(Let's note this as **Observation 2**)_

# k-prime sandwiches have a max length \\(= 3\\)

We will begin by assuming there is some class of k-prime numbers such that the longest possible chain of consecutive occurances of k-prime numbers is \\(> 3\\). (....so...\\(4\\))

Also, we know that because two consecutive numbers must consist of one even and one odd member. So, let's let \\(p\\) represent the odd k-prime and \\(q\\) represent the even k-prime (basically \\(q = p + 1\\)).

> \\(q\\) therefore must decompose to: \\(q = 2 * f\_1 *  ... * f\_{k-1}\\) where \\(f\_{n}\\) represents the k prime factors of \\(q\\). <br/><br/>\\(2\\) must be a factor here since we can _only_ have an even k-prime if \\(2\\) is a prime factor of that k-prime.

_(**Why?** Because all primes are odd except for \\(2\\) and an even number **must** be the product of either all even factors or all odd factors and at least one even factor)_

Ok so with this in mind, let's consider some numbers \\(p, q, r, s\\) that are consecutive k-primes:

$$
\begin{aligned}
\text{let: } p &= a\_1 *  ... * a\_{k} \cr
\text{let: } q &= p + 1 \cr
               &= 2 * f\_1 *  ... * f\_{k-1} \cr
\text{let: } r &= p + 2 \cr
\text{let: } s &= p + 3 \cr
               &= q + 2 \cr
\end{aligned}
$$

We know that \\(q\\) must have \\(2\\) as at most one prime factor (because like the previous post on semiprime sandwiches, we are considering _distinct_ k-primes only). Let's express \\(s\\) in terms of \\(q\\):

$$
\begin{aligned}
q &= p + 1 \cr
  &= 2 * f\_1 *  ... * f\_{k-1} \cr
s &= q + 2 \cr
  &= 2 * f\_1 *  ... * f\_{k-1} + 2 \cr
  &= 2\bigg(f\_1 *  ... * f\_{k-1} + 1 \bigg) \cr
\end{aligned}
$$

Now the key part to consider is this: \\( s = q + 2 = 2\bigg(f\_1 *  ... * f\_{k-1} + 1 \bigg) \\). Because \\(f\_1, ... ,f\_{k-1}\\) are all prime, they must be **odd**. Therefore, the product of these factors: \\(f\_1 * ... * f\_{k-1}\\) must _also_ be **odd**. And thus, adding **one** to this product, \\(f\_1 * ... * f\_{k-1} + 1 \\) gives us an **even** number. Because \\(2\\) is the only even prime number, this means our sum:  \\(f\_1 * ... * f\_{k-1} + 1 \\) cannot be prime and therefore \\(s = q + 2 \\) **cannot be k-prime**.

> Therefore, we _cannot_ have any sequence of consecutive k-primes that have **more than 1** even k-prime member. The only possible set of consecutive numbers that have exactly **one** even **k-prime** is a sequence of **three** numbers \\(\big[p,q,r\big]\\) where \\(q\\) and only \\(q\\) is even and \\(q = p + 1 \\), \\(r = p + 2\\).

This demonstrates **Observation 1** and shows us that the 🍞 k-prime 🍞 has max length \\( = 3\\).

# In a 🍞 k-prime 🍞, either \\(p\\) or \\(r\\) is a multiple of 3.

This observation (**Observation 2**) comes from the understanding that our longest possible set of consecutive k-primes is 3. Suppose we have some set of numbers: \\(\big[p,q,r\big]\\). We know that \\(q\\) must be **even**. 

As we also know, sometimes a multiple of \\(3\\) can be even. Therefore, it is possible that:

$$
\begin{aligned}
q &= 3n \cr
\text{OR } q &= 3n + 2 \cr
\text{OR } q &= 3n + 4 \cr
\text{OR } q &= 3n + 6 \cr
\end{aligned}
$$

We stop at \\(q = 3n + 6\\) because:

$$
\begin{aligned}
q &= 3n \cr
q &= 3n + 6 \cr
  &= 3(n+2) \cr
\end{aligned}
$$

^ this is basically the next possible case where q is even and a multiple of 3.

For each of the cases above, let's rewrite our consecutive sequence \\(\big[p,q,r\big]\\) as:

| p      	         | q               | r              | multiple of 3 present? |
| -----------        | -----------     | -------------- | ---------------------- |
| \\( 3n - 1 \\)     | \\( 3n \\)      | \\( 3n + 1 \\) | yes, \\(q\\)           |
| \\( 3n + 1 \\)     | \\( 3n + 2 \\)  | \\( 3n + 3 \\) | yes, \\(r\\)           |
| \\( 3n + 3 \\)     | \\( 3n + 4 \\)  | \\( 3n + 5 \\) | yes, \\(p\\)           |
| \\( 3n + 5 \\)     | \\( 3n + 6 \\)  | \\( 3n + 7 \\) | yes, \\(q\\)           |

As we can see from the table: 

> For each possible combination of \\(\big[p,q,r\big]\\), we always have one element in the set that is divisible by 3.

Moreover, observe that:

> Since the only possible semiprime with 2 _and_ 3 as factors is **6**, for semiprime sandwiches only: there is exactly one element that is divisible by 2 and there is exactly one element that is divisible by 3.

# Generating k-primes

I noticed that there wasn't any resources (that I could easily find) listing k-primes. For this reason, I put together (a pretty inefficient) script to do exactly this:

```python
def generate_factorization(end: int, kprime: int):
  """
  Generate prime factorization for all numbers from 2 -> end
  kprime is used to determine if the number is a kth-prime
  based on the prime factors calculated
  """
  # store nums and factor pairs in a dict for future access
  nums = {}
  for k in range(2, end):
    ok = k
    p = 2
    factors = []
    while k >= p**2:
      if k % p == 0:
        factors.append(p)
        k = int(k / p)
      else:
        p += 1
    factors.append(k)
    nums[ok] = {
      "factors": factors,
      # we only care about distinct k-primes, so we want to ensure that
      # the only factors AND only distinct factors are kprime
      "distinctk": len(set(factors)) == kprime and len(factors) == kprime
    }

  return nums


def find_streaks(ks, streak_num):
  """
  Given a list of numbers, find a streak of len streak_num
  eg: [2,3,4,7,8,9], streak_num = 3
    => [[2,3,4], [7,8,9]]
  """
  streaks = []
  curr_streak = []

  for k in list(ks.keys()):
    if len(curr_streak) == 0:
      curr_streak.append(k)
      continue

    if k == curr_streak[-1] + 1:
      curr_streak.append(k)
    else:
      curr_streak = [k]

    if len(curr_streak) == streak_num:
      streaks.append(curr_streak)
      curr_streak = []

  return streaks
```

([REPL](https://replit.com/@mottaquikarim/LovingSteelProgramminglanguages#main.py))

## 🍞 semiprime 🍞 \\( < 1000 \\)

```python
ks = generate_factorization(1001, 2)
ks_ = {key: ks[key] for key in ks if ks[key]["distinctk"]}
streaks = find_streaks(ks_, 3)
for streak in streaks:
  print('-------')
  for it in streak:
    print(it, ks[it]["factors"])
  print('-------')
```

```text
-------
33 [3, 11]
34 [2, 17]
35 [5, 7]
-------
-------
85 [5, 17]
86 [2, 43]
87 [3, 29]
-------
-------
93 [3, 31]
94 [2, 47]
95 [5, 19]
-------
-------
141 [3, 47]
142 [2, 71]
143 [11, 13]
-------
-------
201 [3, 67]
202 [2, 101]
203 [7, 29]
-------
-------
213 [3, 71]
214 [2, 107]
215 [5, 43]
-------
-------
217 [7, 31]
218 [2, 109]
219 [3, 73]
-------
-------
301 [7, 43]
302 [2, 151]
303 [3, 101]
-------
-------
393 [3, 131]
394 [2, 197]
395 [5, 79]
-------
-------
445 [5, 89]
446 [2, 223]
447 [3, 149]
-------
-------
633 [3, 211]
634 [2, 317]
635 [5, 127]
-------
-------
697 [17, 41]
698 [2, 349]
699 [3, 233]
-------
-------
921 [3, 307]
922 [2, 461]
923 [13, 71]
-------
```

## 🍞 3-prime 🍞 \\( < 5000 \\)

```python
ks = generate_factorization(1001, 3)
ks_ = {key: ks[key] for key in ks if ks[key]["distinctk"]}
streaks = find_streaks(ks_, 3)
for streak in streaks:
  print('-------')
  for it in streak:
    print(it, ks[it]["factors"])
  print('-------')
```

```text
-------
1309 [7, 11, 17]
1310 [2, 5, 131]
1311 [3, 19, 23]
-------
-------
1885 [5, 13, 29]
1886 [2, 23, 41]
1887 [3, 17, 37]
-------
-------
2013 [3, 11, 61]
2014 [2, 19, 53]
2015 [5, 13, 31]
-------
-------
2665 [5, 13, 41]
2666 [2, 31, 43]
2667 [3, 7, 127]
-------
-------
3729 [3, 11, 113]
3730 [2, 5, 373]
3731 [7, 13, 41]
-------
```

## 🍞 4-prime 🍞 \\( < 500000 \\)

```python
ks = generate_factorization(500001, 4)
ks_ = {key: ks[key] for key in ks if ks[key]["distinctk"]}
streaks = find_streaks(ks_, 3)
for streak in streaks:
  print('-------')
  for it in streak:
    print(it, ks[it]["factors"])
  print('-------')
```

```text
-------
203433 [3, 19, 43, 83]
203434 [2, 7, 11, 1321]
203435 [5, 23, 29, 61]
-------
-------
214489 [11, 17, 31, 37]
214490 [2, 5, 89, 241]
214491 [3, 19, 53, 71]
-------
-------
225069 [3, 13, 29, 199]
225070 [2, 5, 71, 317]
225071 [7, 11, 37, 79]
-------
-------
258013 [7, 29, 31, 41]
258014 [2, 23, 71, 79]
258015 [3, 5, 103, 167]
-------
-------
294593 [13, 17, 31, 43]
294594 [2, 3, 37, 1327]
294595 [5, 7, 19, 443]
-------
-------
313053 [3, 13, 23, 349]
313054 [2, 7, 59, 379]
313055 [5, 17, 29, 127]
-------
-------
315721 [7, 23, 37, 53]
315722 [2, 11, 113, 127]
315723 [3, 19, 29, 191]
-------
-------
352885 [5, 13, 61, 89]
352886 [2, 17, 97, 107]
352887 [3, 19, 41, 151]
-------
-------
389389 [7, 11, 13, 389]
389390 [2, 5, 23, 1693]
389391 [3, 31, 53, 79]
-------
-------
409353 [3, 7, 101, 193]
409354 [2, 11, 23, 809]
409355 [5, 19, 31, 139]
-------
-------
418845 [3, 5, 7, 3989]
418846 [2, 17, 97, 127]
418847 [11, 13, 29, 101]
-------
-------
421629 [3, 13, 19, 569]
421630 [2, 5, 11, 3833]
421631 [7, 29, 31, 67]
-------
-------
452353 [11, 17, 41, 59]
452354 [2, 7, 79, 409]
452355 [3, 5, 53, 569]
-------
-------
464385 [3, 5, 83, 373]
464386 [2, 13, 53, 337]
464387 [7, 11, 37, 163]
-------
-------
478905 [3, 5, 7, 4561]
478906 [2, 23, 29, 359]
478907 [11, 13, 17, 197]
-------
-------
485133 [3, 11, 61, 241]
485134 [2, 13, 47, 397]
485135 [5, 7, 83, 167]
-------
```