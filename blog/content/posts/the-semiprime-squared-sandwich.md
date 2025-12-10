---
title: "The Semiprime Square Sandwich"
date: 2025-12-09T00:00:00Z
tags: ["math", "just for fun"]
katex: true
---

{{<toc>}}

---

**The BLUF:** 

Triples of consecutive semiprimes starting with a prime number squared (like \\(11^2\\) = 121, \\(11^2\\) + 1 = 122, \\(11^2\\) + 2 = 123) have been catalogued before, but their internal structure has not. This post proves that every such triple has the form \\((r^2, 2p, 3b)\\) where the auxiliary primes \\(p\\) and \\(b\\) satisfy the linear relation \\(3b = 2p + 1\\). From this single constraint, everything else follows: \\(p \equiv 1 \pmod{60}\\), \\(b \equiv 1\\) or \\(17 \pmod{24}\\), and \\(r \equiv 1, 11, 19,\\) or \\(29 \pmod{30}\\). The relation \\(3b = 2p + 1\\) in this context and the complete structural analysis that follows appear to be novel.

---

# Semiprimes and Sandwiches, Oh My!

A few years ago, around this time of year coincidentally, I wrote about [The Semiprime Sandwich]({{< relref "posts/the-semiprime-sandwich.md" >}}) – stretches of three consecutive integers \\([n-1, n, n+1]\\) that all happen to be **distinct semiprimes**. The first such example occurs at:

$$
33,\ 34,\ 35.
$$

I have not thought about semiprime sandwiches in a while (though I do think about sandwiches, the eating kind, perhaps a little too often).

Recently, I stumbled on a special case of the semiprime sandwich where **one of the three numbers is a perfect square** of a prime. It turns out that sandwiches in this configuration are completely classifiable with some light algebra and modular arithmetic. In this post, I walk through that analysis and land on a neat little theorem that captures every such triple.

---

# Square-Centered Semiprime Triples

We will focus on triples of consecutive integers

$$
(n,\ n+1,\ n+2)
$$

where all three numbers are **distinct semiprimes**, and the first number \\(n\\) is a perfect square.

Let me be precise about terminology:

> **semiprime**: a natural number that is the product of exactly two prime numbers (counting multiplicity).

So \\(6 = 2\cdot 3\\), \\(15 = 3\cdot 5\\), and \\(25 = 5^2\\) are all semiprimes.  
A **square semiprime** is one of the form \\(r^2\\) where \\(r\\) is prime.

By **distinct semiprimes**, I mean the three numbers have different prime factorizations. So \\((9, 10, 11)\\) would not count even if all three were semiprimes, because we want three genuinely different factorization patterns.

Assume we are in the square case and write

$$
n = r^2,
$$

so the triple becomes

$$
(r^2,\ r^2+1,\ r^2+2).
$$

Now we squeeze this configuration using nothing more than parity (even/odd) and divisibility by 3.

---

## Step 1: forcing the factor \\(2\\)

Among three consecutive integers, exactly one is even. (Refer to my original post for analysis proving this)


In our triple \\((r^2,\ r^2+1,\ r^2+2)\\), the middle term \\(r^2+1\\) is always even (odd square plus 1).

Because \\(r^2+1\\) is assumed to be a **distinct semiprime**, it must factor as

$$
r^2 + 1 = 2p
$$

for some prime \\(p\\). The 2 is forced by evenness; the primality of \\(p\\) is forced by the "exactly two prime factors (counting multiplicity)" requirement. If \\(p\\) were composite, \\(2p\\) would have at least three prime factors.

This already gives a nice symmetric picture:

$$
r^2 = 2p - 1,\qquad
r^2 + 1 = 2p,\qquad
r^2 + 2 = 2p + 1.
$$

So once we know \\(p\\), the three consecutive numbers are exactly \\(2p-1, 2p, 2p+1\\), with \\(r^2 = 2p-1\\) sitting one below the even semiprime \\(2p\\).

---

## Step 2: forcing the factor \\(3\\)

Among any three consecutive integers, exactly one is divisible by 3.

Look again at

$$
r^2 = 2p - 1,\quad
r^2 + 1 = 2p,\quad
r^2 + 2 = 2p + 1.
$$

If \\(r\\) is a prime different from 3, then \\(r\\) is \\(1\\) or \\(2\\) modulo 3, and in either case \\(r^2 \\equiv 1 \pmod{3}\\). That means \\(r^2\\) is **not** divisible by 3.

The middle term \\(r^2+1 = 2p\\) is divisible by 2, but not by 3 (otherwise both \\(r^2\\) and \\(r^2+1\\) would be multiples of 3, which cannot happen with consecutive integers). So the only candidate in the triple that can be divisible by 3 is the top term \\(r^2+2\\).

Thus we must have

$$
r^2 + 2 = 3b
$$

for some integer \\(b\\). Because \\(r^2+2\\) is assumed to be a distinct semiprime, \\(b\\) must be prime: if \\(b\\) factored further as \\(b = cd\\), then \\(3b = 3cd\\) would have at least three prime factors (counting multiplicity).

Notice that this equation is the same as

$$
2p + 1 = 3b,
$$

since \\(r^2 + 2 = (2p - 1) + 2 = 2p + 1\\).

So \\(p\\), \\(b\\), and \\(r\\) are tied together by the small system

$$
r^2 = 2p - 1, \qquad 2p + 1 = 3b.
$$

Solving for \\(p\\) and \\(b\\) in terms of \\(r\\) gives

$$
p = \frac{r^2 + 1}{2},\qquad b = \frac{r^2 + 2}{3}.
$$

There is no freedom here: once you pick \\(r\\), the potential primes \\(p\\) and \\(b\\) are forced.

---

## Summary of the structure

Every square-centered triple of consecutive semiprimes must look like

$$
(r^2,\ r^2+1,\ r^2+2) = (r^2,\ 2p,\ 3b),
$$

where \\(r\\) is a prime and

$$
p = \frac{r^2 + 1}{2},\qquad
b = \frac{r^2 + 2}{3}
$$

are also primes.

Conversely, if you start with a prime \\(r\\) for which \\((r^2+1)/2\\) and \\((r^2+2)/3\\) both happen to be prime, then \\(r^2\\), \\(r^2+1\\), and \\(r^2+2\\) are automatically semiprimes and give you such a triple.

That is the whole classification, which we can now package into a theorem.

---

# Theorem (Square-Centered Semiprime Triples)

> **Theorem.**  
> A triple of consecutive integers  
> $$
> (n,\ n+1,\ n+2)
> $$
> consists entirely of **distinct semiprimes** and has its **first term equal to a perfect square**  
> if and only if it can be written in the form  
> $$
> (r^2,\ r^2+1,\ r^2+2)
> $$
> where \\(r\\) is prime and
> $$
> r^2 + 1 = 2p,\qquad r^2 + 2 = 3b
> $$
> for some primes \\(p\\) and \\(b\\).

Equivalently, every such triple is exactly of the form

$$
(r^2,\ 2p,\ 3b)
$$

with

$$
p = \frac{r^2 + 1}{2},\qquad
b = \frac{r^2 + 2}{3}.
$$

That is the classification. The rest of the post is about what this tells us about the primes \\(p\\) and \\(b\\).

---

# Why small primes fail

Before diving into consequences, it is worth seeing why we have to wait until \\(r = 11\\) for the first example. The classification says: pick a prime \\(r\\), compute \\((r^2+1)/2\\) and \\((r^2+2)/3\\), and check if both are prime. Most small primes fail this test.

**\\(r = 3\\):** We get \\(r^2 + 1 = 10 = 2 \cdot 5\\) and \\(r^2 + 2 = 11\\). So far so good, but \\(r^2 = 9 = 3^2\\) means the triple is \\((9, 10, 11)\\). The problem: 11 is prime, not a semiprime. No good.

**\\(r = 5\\):** We get \\(r^2 + 2 = 27 = 3^3\\). That is three prime factors, not two. No good.

**\\(r = 7\\):** We get \\(r^2 + 1 = 50 = 2 \cdot 25 = 2 \cdot 5^2\\). That is three prime factors (counting multiplicity). No good.

**\\(r = 11\\):** Finally, \\(r^2 = 121\\), \\(r^2 + 1 = 122 = 2 \cdot 61\\), and \\(r^2 + 2 = 123 = 3 \cdot 41\\). All three are semiprimes with distinct factorizations. Success!

So the small primes fail for different reasons—sometimes the middle term has too many factors, sometimes the top term does, sometimes one of them is actually prime. The conditions are stringent enough that valid triples are rare.

---

# Some interesting consequences

Now that we know every square-centered triple comes from a prime \\(r\\) via

$$
(r^2,\ 2p,\ 3b),\quad
p = \frac{r^2+1}{2},\quad
b = \frac{r^2+2}{3},
$$

we can ask: **where do these primes actually live in the integers?**

Three simple facts emerge. First, the "middle" prime \\(p\\) always leaves remainder 1 when divided by 60. Second, the "top" prime \\(b\\) can only leave remainder 1 or 17 when divided by 24. Third, the source prime \\(r\\) can only leave remainder 1, 11, 19, or 29 when divided by 30.

Let's walk through each fact in more detail below.

---

## 1. The center prime is always \\(1 \pmod{60}\\)

We start from

$$
p = \frac{r^2+1}{2},
$$

with \\(r\\) an odd prime not equal to 3 or 5. Our goal is to pin down \\(p\\) modulo 60. Since \\(60 = 4 \times 3 \times 5\\), we can work modulo each factor separately and combine the results at the end using the Chinese Remainder Theorem.

### Working modulo 8 (and hence modulo 4)

Any odd integer can be written as \\(2k+1\\) for some integer \\(k\\). Squaring gives

$$
(2k+1)^2 = 4k^2 + 4k + 1 = 4k(k+1) + 1.
$$

Since one of \\(k\\) or \\(k+1\\) is even, \\(k(k+1)\\) is always even, so \\(4k(k+1)\\) is divisible by 8. Therefore

$$
r^2 \equiv 1 \pmod{8}
$$

for any odd \\(r\\).

This means

$$
r^2 + 1 \equiv 2 \pmod{8},
$$

and dividing by 2 gives

$$
p = \frac{r^2+1}{2} \equiv 1 \pmod{4}.
$$

### Working modulo 3

For a prime \\(r \neq 3\\), we have

$$
r \equiv 1 \text{ or } 2 \pmod{3}.
$$

Squaring either case:

- if \\(r \equiv 1\\), then \\(r^2 \equiv 1\\);
- if \\(r \equiv 2\\), then \\(r^2 \equiv 4 \equiv 1 \pmod{3}\\).

So always

$$
r^2 \equiv 1 \pmod{3}.
$$

Then

$$
r^2 + 1 \equiv 1 + 1 \equiv 2 \pmod{3}.
$$

Now 2 has an inverse modulo 3, namely 2 again, because \\(2\cdot 2 = 4 \equiv 1 \pmod{3}\\). So we can "divide by 2" by multiplying by 2:

$$
p = \frac{r^2+1}{2} \equiv 2 \cdot 2 \equiv 4 \equiv 1 \pmod{3}.
$$

So \\(p\\) leaves remainder 1 when divided by 3.

### Working modulo 5

For a prime \\(r \neq 5\\), the possibilities modulo 5 are

$$
r \equiv 1,2,3,\text{ or }4 \pmod{5}.
$$

Squaring each: \\(1^2 \equiv 1\\), and \\(4^2 = 16 \equiv 1\\), and \\(2^2 = 4\\), and \\(3^2 = 9 \equiv 4 \pmod{5}\\).

So \\(r^2\\) is either \\(1\\) or \\(4\\) modulo 5.

**Case 1: \\(r^2 \equiv 1 \pmod{5}\\).**  
Then

$$
r^2 + 1 \equiv 2 \pmod{5}.
$$

The inverse of 2 modulo 5 is 3, because \\(2\cdot 3 = 6 \equiv 1 \pmod{5}\\). So

$$
p = \frac{r^2+1}{2} \equiv 2\cdot 3 \equiv 6 \equiv 1 \pmod{5}.
$$

**Case 2: \\(r^2 \equiv 4 \pmod{5}\\).**  
Then

$$
r^2 + 1 \equiv 4 + 1 \equiv 5 \equiv 0 \pmod{5}.
$$

So \\(p = (r^2+1)/2\\) would be divisible by 5. The only way a prime is divisible by 5 is if it equals 5 itself. That would give

$$
p = 5 = \frac{r^2+1}{2} \Rightarrow r^2 = 9 \Rightarrow r = 3,
$$

but \\(r = 3\\) fails to produce a valid triple (as we saw above: 11 is prime, not a semiprime).

So in all valid cases we must actually be in Case 1, and therefore

$$
p \equiv 1 \pmod{5}.
$$

### Putting the congruences together

We now know

$$
p \equiv 1 \pmod{4},\qquad
p \equiv 1 \pmod{3},\qquad
p \equiv 1 \pmod{5}.
$$

The least common multiple of 4, 3, and 5 is 60, and the only residue class modulo 60 that is 1 modulo all three is \\(1\\) itself. So

$$
p \equiv 1 \pmod{60}.
$$

Check against the actual examples. For \\(r = 11\\), we get \\(p = (121+1)/2 = 61\\), and indeed \\(61 = 60\cdot 1 + 1\\). For \\(r = 29\\), we get \\(p = (841+1)/2 = 421\\), and \\(421 = 60\cdot 7 + 1\\).

So the middle primes always sit in the "\\(60k+1\\)" lane of the number line.

---

## 2. The top prime and quadratic residues

Now look at the top semiprime:

$$
r^2 + 2 = 3b.
$$

Rewriting this as a congruence modulo \\(b\\) gives

$$
r^2 \equiv -2 \pmod{b}.
$$

This has a standard interpretation in number theory, and it connects our little puzzle to a classical result.

### Quick definition: quadratic residue

Fix a positive integer \\(m\\).  
An integer \\(a\\) is called a **quadratic residue modulo \\(m\\)** if there exists some integer \\(x\\) such that

$$
x^2 \equiv a \pmod{m}.
$$

You can think of this as: "\\(a\\) is a perfect square when you do arithmetic mod \\(m\\)."

If no such \\(x\\) exists, then \\(a\\) is called a **quadratic non-residue modulo \\(m\\)**.

**A concrete example.** Let us work modulo 7. I want to know: which numbers are "squares" in mod 7 arithmetic?

To find out, I just try squaring everything. There are only six nonzero residue classes to check: \\(1^2 = 1\\), and \\(2^2 = 4\\), and \\(3^2 = 9 \equiv 2\\), and \\(4^2 = 16 \equiv 2\\), and \\(5^2 = 25 \equiv 4\\), and \\(6^2 = 36 \equiv 1\\). 

So the only outputs we ever see are 1, 2, and 4. These are the quadratic residues modulo 7. The numbers 3, 5, and 6 never appear as outputs—no matter what integer you square, the result will never be congruent to 3, 5, or 6 modulo 7. These are the quadratic non-residues.

Now suppose I ask: is \\(-1\\) a quadratic residue mod 7? That is, does \\(x^2 \equiv -1 \pmod 7\\) have a solution? Since \\(-1 \equiv 6 \pmod 7\\), I am really asking if 6 is a quadratic residue. We just saw it is not—6 never shows up when we square things mod 7. So \\(-1\\) is a quadratic non-residue modulo 7.

**Back to our problem.** Recall that the top semiprime in our triple satisfies \\(r^2 + 2 = 3b\\). Rearranging, we get \\(r^2 = 3b - 2\\). Now reduce both sides modulo \\(b\\): the right side becomes \\(3b - 2 \equiv -2 \pmod b\\), so we have

$$
r^2 \equiv -2 \pmod{b}.
$$

This equation says: when we square \\(r\\) and divide by \\(b\\), the remainder is \\(b - 2\\). In other words, \\(-2\\) is a quadratic residue modulo \\(b\\), and \\(r\\) is the witness that proves it.

Let us verify with our first example. For \\(r = 11\\), we computed \\(b = 41\\). Is \\(-2\\) a quadratic residue mod 41? We need to check if some integer squared gives remainder \\(41 - 2 = 39\\) when divided by 41. And indeed: \\(11^2 = 121\\), and \\(121 = 2 \times 41 + 39\\), so the remainder is 39. That means \\(11^2 \equiv 39 \equiv -2 \pmod{41}\\). The prime \\(r = 11\\) is itself the witness.

This flips our perspective. We started by asking "which primes \\(r\\) produce valid triples?" But now we can also ask "which primes \\(b\\) can appear at the top of a valid triple?" The answer: exactly those primes \\(b\\) for which \\(-2\\) happens to be a quadratic residue.

### What does this say about \\(b\\)?

Here is where classical number theory hands us a gift. There is a result from quadratic reciprocity that tells us exactly which primes have the property that \\(-2\\) is a quadratic residue:

> For an odd prime \\(q\\), the number \\(-2\\) is a quadratic residue modulo \\(q\\) if and only if
> $$
> q \equiv 1 \text{ or } 3 \pmod{8}.
> $$

So any \\(b\\) that appears here must satisfy

$$
b \equiv 1 \text{ or } 3 \pmod{8}.
$$

We also know some extra things about \\(b\\) from the basic structure. First, \\(b\\) is not divisible by 3. Why? Because \\(b\\) is prime, and \\(b \neq 3\\). (If \\(b = 3\\), then \\(3b = 9 = r^2 + 2\\), which would require \\(r^2 = 7\\)—but 7 is not a perfect square.)

We can also pin down \\(b\\) modulo 8. In section 1, we showed that any odd number squared is congruent to 1 modulo 8. Since \\(r\\) is an odd prime, \\(r^2 \equiv 1 \pmod{8}\\), so \\(r^2 + 2 \equiv 3 \pmod{8}\\). This means \\(3b \equiv 3 \pmod 8\\). What value of \\(b\\) makes this true? We need \\(3b\\) to leave remainder 3 when divided by 8. Testing: \\(3 \times 1 = 3\\), so \\(b \equiv 1 \pmod 8\\) works. 

Now we combine our two facts about \\(b\\): it leaves remainder 1 when divided by 8, and it is not divisible by 3. To capture both constraints at once, we work modulo 24 (since \\(24 = 8 \times 3\\)).

Within each cycle of 24 integers, which ones are congruent to 1 modulo 8? Those are 1, 9, and 17. Of these three, 9 is divisible by 3, so we exclude it. That leaves just 1 and 17. So \\(b\\) must satisfy

$$
b \equiv 1 \text{ or } 17 \pmod{24}.
$$

### Why this restriction matters

This is a pretty sharp filter. Out of every 24 consecutive integers, only those in two residue classes—1 and 17—can even be candidates for \\(b\\). That is 2 out of 24, or about 8% of integers. And of course, \\(b\\) also has to be prime on top of that.

For our theorem, this gives us a necessary condition: if you hand me a supposed square-centered semiprime triple and claim the top term is \\(3b\\), I can immediately check whether \\(b \equiv 1\\) or \\(17 \pmod{24}\\). If not, the triple is impossible.

Combined with the constraint on \\(p\\) (that \\(p \equiv 1 \pmod{60}\\)), we now have a fairly complete picture of what valid triples look like. The bottom is \\(r^2\\) for some prime \\(r\\). The middle is \\(2p\\) where \\(p\\) lives in the \\(60k + 1\\) lane. The top is \\(3b\\) where \\(b\\) lives in one of the two lanes \\(24k + 1\\) or \\(24k + 17\\). These constraints are all necessary, and together with the primality requirements, they are sufficient.

So far, all the data points hit the \\(17 \pmod{24}\\) lane.

---

## 3. The source prime lives in four residue classes

We have derived constraints on the auxiliary primes \\(p\\) and \\(b\\). But what about the source prime \\(r\\) itself? It turns out the constraints on \\(p\\) propagate back to \\(r\\).

We know \\(p\\) leaves remainder 1 when divided by 60. Since \\(p = (r^2 + 1)/2\\), this tells us something about \\(r^2\\). Rearranging: \\(r^2 + 1 = 2p\\). If \\(p\\) leaves remainder 1 when divided by 60, then \\(2p\\) leaves remainder 2 when divided by 120. So \\(r^2 + 1\\) leaves remainder 2 when divided by 120, which means \\(r^2\\) leaves remainder 1 when divided by 120.

What does this tell us about \\(r\\)? Let's break it down. Since \\(120 = 8 \times 3 \times 5\\), we can check each factor separately.

**Modulo 8:** In section 1, we showed that any odd number squared leaves remainder 1 when divided by 8. Every prime except 2 is odd, so this is automatically satisfied.

**Modulo 3:** If \\(r\\) is not divisible by 3, then \\(r\\) leaves remainder 1 or 2 when divided by 3. Either way, \\(r^2\\) leaves remainder 1. (Check: \\(1^2 = 1\\) and \\(2^2 = 4 \equiv 1 \pmod 3\\).) Every prime except 3 satisfies this, so this is also automatic.

**Modulo 5:** We need \\(r^2\\) to leave remainder 1 when divided by 5. Let's check each possibility. If \\(r\\) leaves remainder 1, then \\(r^2\\) leaves remainder 1. If \\(r\\) leaves remainder 2, then \\(r^2 = 4\\). If \\(r\\) leaves remainder 3, then \\(r^2 = 9 \equiv 4\\). If \\(r\\) leaves remainder 4, then \\(r^2 = 16 \equiv 1\\). So \\(r^2 \equiv 1 \pmod 5\\) only when \\(r \equiv 1\\) or \\(4 \pmod 5\\).

The first two constraints are automatic for any prime greater than 3. The modulo 5 constraint is the only real filter: \\(r\\) must leave remainder 1 or 4 when divided by 5.

To see which primes pass this filter, we work modulo 30. Here's why.

Any prime greater than 5 has three properties: it's odd (not divisible by 2), not divisible by 3, and not divisible by 5. So if we list the numbers from 1 to 30 and cross out the ones that are even, divisible by 3, or divisible by 5, we get the only possible remainders a prime can leave when divided by 30:

1, 7, 11, 13, 17, 19, 23, 29.

That's eight possibilities. Now we check which of these eight satisfy our constraint \\(r \equiv 1\\) or \\(4 \pmod 5\\):

Now we check each of these eight classes against our constraint \\(r \equiv 1\\) or \\(4 \pmod 5\\):

Now we check each of these eight classes against our constraint \(r \equiv 1 \text{ or } 4 \pmod 5\):

| Prime \(r\) | \(r \bmod 5\) | OK? |
|-------------|---------------|-----|
| 1           | 1             | ✓   |
| 7           | 2             | ×   |
| 11          | 1             | ✓   |
| 13          | 3             | ×   |
| 17          | 2             | ×   |
| 19          | 4             | ✓   |
| 23          | 3             | ×   |
| 29          | 4             | ✓   |


Four pass, four fail. So **only primes \\(r \equiv 1, 11, 19,\\) or \\(29 \pmod{30}\\)** can produce valid triples.

Let us verify against our examples. We have \\(r = 11 \equiv 11 \pmod{30}\\) and \\(r = 29 \equiv 29 \pmod{30}\\). Both land in the valid set.

This constraint is quite restrictive. Among the first several primes greater than 5, we have: 7 (out), 11 (in), 13 (out), 17 (out), 19 (in), 23 (out), 29 (in), 31 (in), 37 (out), 41 (in), 43 (out), 47 (out), 53 (out), 59 (in), 61 (in)... Only about half the primes even have a chance of being \\(r\\), and then the primality conditions on \\(p\\) and \\(b\\) filter further.

---

# Examples

It is worth looking at the first few concrete triples to see the structure in action.

Take \\(r = 11\\). Then

$$
r^2 = 121,\quad
p = \frac{121+1}{2} = 61,\quad
b = \frac{121+2}{3} = 41.
$$

All three numbers \\(r, p, b\\) are prime, and the triple is

$$
(121,\ 122,\ 123) = (11^2,\ 2\cdot 61,\ 3\cdot 41).
$$

Now take \\(r = 29\\). Then

$$
r^2 = 841,\quad
p = \frac{841+1}{2} = 421,\quad
b = \frac{841+2}{3} = 281,
$$

again all prime, giving the triple

$$
(841,\ 842,\ 843) = (29^2,\ 2\cdot 421,\ 3\cdot 281).
$$

In both cases, you can see: the bottom is a square of a prime, the middle is \\(2p\\) with \\(p \equiv 1 \pmod{60}\\), and the top is \\(3b\\) with \\(b \equiv 1\\) or \\(17 \pmod{24}\\).

---

# Final thoughts

This result sits in an interesting middle ground. The basic phenomenon—that there exist triples of consecutive semiprimes starting with a prime square—is already catalogued in the OEIS as sequence [A179502](https://oeis.org/A179502), and a comment on [A039833](https://oeis.org/A039833) notes the 2p-1, 2p, 2p+1 structure for general semiprime sandwiches.

**What appears to be new is the complete structure that emerges when you restrict to the square-centered case.** The key insight is the relation

$$
3b = 2p + 1,
$$

which ties the two auxiliary primes together. This relation is forced by the square constraint: for any prime \\(r \neq 3\\), we have \\(r^2 \equiv 1 \pmod 3\\), so \\(r^2 + 2 \equiv 0 \pmod 3\\). The semiprime requirement then demands \\(r^2 + 2 = 3b\\) for some prime \\(b\\). Since \\(r^2 + 2 = 2p + 1\\), we get the relation.

This does not appear in the general semiprime sandwich literature because the third term of a general sandwich need not be divisible by 3. For instance, the first sandwich (33, 34, 35) = (3·11, 2·17, 5·7) has third term 5·7, not 3·(prime).

From \\(3b = 2p + 1\\) everything else follows: the constraint \\(p \equiv 1 \pmod{60}\\), the constraint \\(b \equiv 1\\) or \\(17 \pmod{24}\\), and the constraint \\(r \equiv 1, 11, 19,\\) or \\(29 \pmod{30}\\). All three are derived in detail above.

The relation also gives an alternative way to search for these triples. Instead of iterating over primes \\(r\\) and checking two conditions, you can iterate over primes \\(p \equiv 1 \pmod{60}\\) and check: (1) is \\(2p - 1\\) a perfect square of a prime? (2) is \\((2p+1)/3\\) prime? If both, you have found a triple.

**Is this important?** Not in the sense of unlocking new theorems or settling old conjectures. But it is genuinely non-trivial—the argument uses real ideas (parity, divisibility, quadratic reciprocity) and lands on constraints that are not at all obvious from staring at examples. The tight linear coupling \\(3b = 2p + 1\\) is the kind of structure that feels like it should have been noticed before, and yet I cannot find it anywhere.

One question I cannot answer: **are there infinitely many such triples?** The classification reduces this to asking whether there are infinitely many primes \\(r \equiv 1, 11, 19, 29 \pmod{30}\\) such that both \\((r^2+1)/2\\) and \\((r^2+2)/3\\) are also prime. This connects to notoriously hard problems about the simultaneous distribution of primes in polynomial sequences. I do not know the answer, and I suspect nobody does.

If someone points me at prior work that already established the \\(3b = 2p + 1\\) relation or its consequences, I will update this post accordingly.