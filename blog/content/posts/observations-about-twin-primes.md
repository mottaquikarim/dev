---
title: "Observation About Twin Primes"
date: 2022-12-08T10:24:40Z
tags: ["math", "just for fun"]
katex: true
---

> A twin prime is a prime number that is either 2 less or 2 more than another prime number—for example, either member of the twin prime pair (41, 43). 

([source](https://en.wikipedia.org/wiki/Twin_prime))

So I realized something interesting the other day, given twin primes \\(p, p+2\\) and \\(q\\) the number occurring in between:

| p      	          | q               | p + 2          | is \\(q \\) a multiple of 6?  |
| -----------         | -----------     | -------------- | ----------------------------  |
| \\( 2  \\)          | \\( 3 \\)       | \\( 3n + 1 \\) | no                            |
| \\( 3  \\)          | \\( 4 \\)       | \\( 5 \\)      | no                            |
| \\( 5  \\)          | \\( 6 \\)       | \\( 7 \\)      | yes, \\( 6 * 1 \\)            |
| \\( 11 \\)          | \\( 12 \\)      | \\( 13 \\)     | yes, \\( 6 * 2 \\)            |
| \\( 17 \\)          | \\( 18 \\)      | \\( 19 \\)     | yes, \\( 6 * 3 \\)            |
| \\( 29 \\)          | \\( 30 \\)      | \\( 31 \\)     | yes, \\( 6 * 5 \\)            |
| \\( 41 \\)          | \\( 42 \\)      | \\( 43 \\)     | yes, \\( 6 * 7 \\)            |
| \\( 59 \\)          | \\( 60 \\)      | \\( 61 \\)     | yes, \\( 6 * 10 \\)           |
| \\( 71 \\)          | \\( 72 \\)      | \\( 73 \\)     | yes, \\( 6 * 12 \\)           |

Note that \\( q \\) is *always* divisible by \\( 6 \\)! As you can imagine, Dear Reader, I wondered if this held true generally. (And is it turns out, yes. It _does_!)

Let's convince ourselves of this.

First, let's remember that we only care about twin primes > 4. Then, as we showed in a previous post:

> Given any three consecutive numbers, exactly one number will be divisible by 3.

^ Just to rehash the above super quick, suppose we have some consecutive number sequence 

> \\( p, q, r, s \\) 

such that 

> \\( q = p + 1 \\), \\( r = p + 2 \\) and \\( s = p + 3 \\) 

Let's let \\( p \\) be divisble by \\( 3 \\), or in other words \\( p = 3n \\) where \\( n \\) is some natural number.

Now, we can represent \\( p, q, r, s \\) as \\( 3n, 3n + 1, 3n + 2, 3n + 3 \\).

Let's look at this set in groups of \\( 3 \\), eg:

* \\( \bold{3n, 3n+1, 3n+2}, 3n + 3\\) | here, \\( 3n \\) is clearly divisible by \\( 3 \\)
* \\( 3n, \bold{3n+1, 3n+2, 3n + 3}\\) | here, \\( 3n + 3 \\) is clearly divisible by \\( 3 \\)

(And of course, if \\( 3n \\) is in the middle of the set, so \\( 3n -1, 3n, 3n + 1 \\), we observe the same result).

All in all, let's move forward having convinced ourselves that given any set of three consecutive numbers one number will be a multiple of three. 

Now,

> Given a set of twin primes \\( p, p+2 \\) (such that \\( p \\) > 4), we know that there exists a **non prime** \\( p + 1 \\) in between _and_ that by definition \\( p \\) and \\( p + 2 \\) cannot be divisible by \\( 3 \\) (because they are prime). Therefore, \\( p + 1 \\) **must** be divisible by 3 (as per our conclusion above)

Also:

> Given a set of twin primes \\( p, p+2 \\) (such that \\( p \\) > 4), we know that both \\(p\\) _and_ \\(p+2\\) must be _odd_. Therefore, \\(p+1\\) **must** be even.

For this reason, we can conclude that:

* \\(p+1\\) is even (it is divisible by 2)
* \\(p+1\\) is divisible by 3

And so, \\(p+1\\) is also be divisible by \\(6\\). For this reason:

> Any number \\(q\\) occurring between twin primes \\(p\\) and \\(p+2\\) **must** be a multiple of \\(6\\).

Ta-da 🎉