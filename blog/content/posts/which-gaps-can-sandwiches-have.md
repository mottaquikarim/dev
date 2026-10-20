---
title: "Which Gaps Can Sandwiches Have?"
date: 2026-10-20T00:00:00Z
draft: true
tags: ["math", "just for fun"]
katex: true
---

{{<toc>}}

# Twins exist. What about cousins?

Quick recap. A [semiprime square sandwich]({{< relref "posts/the-semiprime-squared-sandwich.md" >}}) is a prime \\(r\\) where \\(r^2\\), \\(r^2+1\\) and \\(r^2+2\\) are all semiprimes. That happens exactly when \\(r > 5\\) is prime and both

$$
p = \frac{r^2+1}{2}, \qquad b = \frac{r^2+2}{3}
$$

are prime. These \\(r\\) values are [A179502](https://oeis.org/A179502) in the OEIS: 11, 29, 79, 271, 379, ...

In [the last post]({{< relref "posts/when-sandwiches-come-in-pairs.md" >}}) I looked at twin pairs, ie: \\(r\\) and \\(r+2\\) both in A179502. They exist (the first one is 661949) and I sent the list to the OEIS as [A401114](https://oeis.org/draft/A401114), which is still in editor review.

So the obvious next question: what about cousin pairs \\((r, r+4)\\)? Sexy pairs \\((r, r+6)\\)? More generally, for which gaps \\(g\\) can \\(r\\) and \\(r+g\\) both be terms?

---

# The data

I computed every term below \\(10^8\\). There are 30,319 of them, which matches the OEIS count. Then for each even gap I counted how many \\(r\\) have \\(r+g\\) as a term too:

| \\(g\\) | Pairs below \\(10^8\\) | First \\(r\\) |
|---------|------------------------|---------------|
| 2 | 5 | 661949 |
| 4 | 0 | |
| 6 | 0 | |
| 8 | 39 | 300221 |
| 10 | 54 | 11959 |
| 12 | 20 | 186379 |
| 14 | 0 | |
| 16 | 0 | |
| 18 | 51 | 11 |
| 20 | 24 | 2283551 |
| 22 | 11 | 7601119 |
| 24 | 0 | |
| 26 | 0 | |
| 28 | 34 | 5851 |
| 30 | 72 | 10069 |

(Fun one: the very first pair at \\(g = 18\\) is 11 and 29, the first two terms.)

The zeros are not random. Gaps 4, 6, 14, 16, 24, 26 never show up. Odd gaps are skipped in the table because they obviously can't work (more on that below). So what's going on?

---

# Finding the rule

## First try: divide by 3

My first instinct was to use 3, since 3 is baked into the structure. Take a cousin pair and look at the top term of the second sandwich:

$$
(r+4)^2 + 2 = r^2 + 8r + 18 = r(r+8) + 18.
$$

18 is a multiple of 3 and \\(r\\) is a prime bigger than 3, so this is divisible by 3 exactly when 3 divides \\(r+8\\). I was hoping that never happens. Then I tried \\(r = 97\\): \\(97 + 8 = 105 = 3 \cdot 35\\). Dead.

And in hindsight it had to be dead. For any prime \\(R > 3\\), \\(R^2 \equiv 1 \pmod 3\\), so \\(R^2 + 2\\) is always a multiple of 3. That's the whole reason the top term is \\(3b\\) in the first place. So 3 dividing something here doesn't block anything.

## Second try: last digits

So I just stared at the first few terms:

11, 29, 79, 271, 379, 461, 521, 631, 739, 881, 929, 1459

Every one ends in 1 or 9. That turns out to be the key.

**Lemma.** No term ends in 3 or 7.

If \\(r\\) ends in 3 or 7, then \\(r^2\\) ends in 9, so \\(r^2+1\\) ends in 0. That means 5 divides \\(r^2+1\\), and so 5 divides \\(p = (r^2+1)/2\\). But \\(p\\) is prime and bigger than 5, so that can't happen. (The only way out would be \\(r = 3\\), and 3 is not a term.)

Terms are primes bigger than 5, so they can't end in 5 or an even digit either. That leaves 1 and 9.

## Cousins (gap 4)

- If \\(r\\) ends in 1, then \\(r+4\\) ends in 5. Not prime.
- If \\(r\\) ends in 9, then \\(r+4\\) ends in 3. Not a term, by the lemma.

So no cousin pairs. Ever.

## Sexy (gap 6)

- If \\(r\\) ends in 1, then \\(r+6\\) ends in 7. Not a term.
- If \\(r\\) ends in 9, then \\(r+6\\) ends in 5. Not prime.

No sexy pairs either.

## Odd gaps

Every term is odd, so \\(r+g\\) is even when \\(g\\) is odd. Not prime.

## The general rule

Same idea for any gap. Both \\(r\\) and \\(r+g\\) have to end in 1 or 9, and \\(g\\) has to be even. The possible last-digit moves are 1 to 1, 9 to 9 (\\(g\\) ends in 0), 9 to 1 (\\(g\\) ends in 2), and 1 to 9 (\\(g\\) ends in 8). So:

> **Rule.** \\(r\\) and \\(r+g\\) can both be terms of A179502 only if \\(g\\) is even and \\(g\\) ends in 0, 2 or 8.

Check against the table: 2, 8, 10, 12, 18, 20, 22, 28, 30 all have pairs. 4, 6, 14, 16, 24, 26 have none. Exact match.

(This is the same thing as the mod 30 gap table in the last post, just easier to see. Last digits are mod 10, and mod 10 is where all the action is.)

---

# Can any other prime block a gap?

The rule says which gaps are ruled out. A fair question is whether some bigger prime rules out even more. It doesn't. Here's why, prime by prime.

**Primes \\(\ell \geq 11\\).** A large term \\(r\\) gets ruled out mod \\(\ell\\) only when \\(\ell\\) divides \\(r\\), \\(r^2+1\\), or \\(r^2+2\\). Each of the last two has at most 2 solutions mod \\(\ell\\), so that's at most 5 bad remainders. For a pair, \\(r\\) has to dodge its bad remainders and \\(r+g\\) has to dodge them too. That's at most 10 bad remainders for \\(r\\). Since \\(\ell \geq 11\\), there's always at least one left over, so \\(\ell\\) can't kill any gap on its own.

**\\(\ell = 7\\).** The squares mod 7 are 1, 2 and 4. Neither \\(-1 \equiv 6\\) nor \\(-2 \equiv 5\\) is on that list, so 7 never divides \\(r^2+1\\) or \\(r^2+2\\). Only \\(r \equiv 0\\) is bad. A pair rules out at most 2 of the 7 remainders.

**\\(\ell = 5\\).** This is the last-digit argument above. It's the one that actually does something.

**\\(\ell = 3\\).** The real condition from 3 is that \\(b = (r^2+2)/3\\) is not itself a multiple of 3, ie: 9 doesn't divide \\(r^2+2\\). Working mod 9, that forces

$$
r \equiv 1, 2, 7, 8 \pmod 9.
$$

The differences between those four numbers (mod 9) hit every remainder from 0 to 8. So for any \\(g\\), there's a way to place \\(r\\) and \\(r+g\\) that 3 is happy with. 3 blocks nothing.

**\\(\ell = 2\\).** Terms are odd. That's the "\\(g\\) is even" part.

I also checked all of this with a short Python script: for every prime up to 50 (using mod 9 for 3), it computes the allowed remainders and which gaps get blocked. Only 2 and 5 block anything, and the allowed gaps up to 3000 are exactly the even ones ending in 0, 2 or 8.

---

# A small bonus for the twins

The rule gives a quick proof of something from the last post. If \\((r, r+2)\\) is a twin pair:

- \\(r\\) can't end in 1, because then \\(r+2\\) ends in 3. So \\(r\\) ends in 9.
- \\(r\\) and \\(r+2\\) are both primes bigger than 3, so \\(r \equiv 2 \pmod 3\\).
- \\(r\\) is odd.

Put those together and \\(r \equiv 29 \pmod{30}\\). All 5 twin values below \\(10^8\\) (661949, 6142949, 8359919, 23304959, 68412959) fit.

---

# What's still open

The rule tells you which gaps are allowed. It does not tell you that every allowed gap has infinitely many pairs. For that you'd need infinitely many \\(r\\) where six numbers are prime at the same time: \\(r\\), \\(r+g\\), and the four \\(p\\)'s and \\(b\\)'s. That's the same kind of problem as the twin prime conjecture, and nobody knows how to prove those. The heuristics (Bateman-Horn, which I went through in [the last post]({{< relref "posts/when-sandwiches-come-in-pairs.md" >}})) say yes, there should be infinitely many for each allowed gap. The table above at least agrees so far.

So the honest summary: gaps 4 and 6 (and every gap ending in 4 or 6, and every odd gap) are impossible, and that's proven. Everything else is allowed, and probably happens forever, but that part is still a guess.
