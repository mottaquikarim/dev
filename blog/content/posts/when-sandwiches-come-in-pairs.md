---
title: "When Sandwiches Come in Pairs"
date: 2025-12-13T22:31:54Z
draft: true
tags: ["math", "just for fun"]
katex: true
---

{{<toc>}}

# Introduction

In [my previous post]({{< relref "posts/the-semiprime-squared-sandwich.md" >}}), I classified the structure of semiprime square sandwiches—triples of consecutive semiprimes \\((r^2, r^2+1, r^2+2)\\) where \\(r\\) is prime. The classification revealed tight constraints: the middle term is always \\(2p\\) with \\(p \equiv 1 \pmod{60}\\), the final term is always \\(3b\\) with \\(b \equiv 1\\) or \\(17 \pmod{24}\\), and the source prime \\(r\\) must satisfy \\(r \equiv 1, 11, 19, 29 \pmod{30}\\).

This post extends the analysis in two directions. First, I present quantitative heuristics predicting how many such triples exist up to a bound \\(N\\), verified computationally up to \\(10^{10}\\). Second, I investigate **twin valid primes**—twin prime pairs \\((r, r+2)\\) where *both* primes generate valid semiprime square sandwiches.

---

# Quantitative Heuristics: The Bateman-Horn Prediction

The classification theorem reduces the existence of square-centered semiprime triples to a simultaneous primality problem: find primes \\(r\\) such that both \\((r^2+1)/2\\) and \\((r^2+2)/3\\) are also prime. This connects our problem to the **Bateman-Horn conjecture**, a standard heuristic for counting primes in polynomial sequences.

## The Heuristic Framework

The Bateman-Horn conjecture predicts that for "nice" polynomial systems, the count of integers \\(n \leq N\\) satisfying multiple primality conditions follows:

$$
\pi(N) \sim C \cdot \frac{N}{(\log N)^k}
$$

where \\(k\\) is the number of independent primality conditions and \\(C\\) is a computable constant depending on local densities at each prime.

In our setting, we have three conditions:

1. \\(r\\) is prime
2. \\(p = (r^2 + 1)/2\\) is prime  
3. \\(b = (r^2 + 2)/3\\) is prime

Each condition contributes one factor of \\(\log N\\) to the denominator, suggesting:

$$
\pi(N) \sim C \cdot \frac{N}{(\log N)^3}
$$

## Empirical Verification

To test this prediction, I computed all valid source primes \\(r \leq 10^{10}\\). The results:

| \\(N\\) | Actual Count | \\(N/(\log N)^3\\) | Empirical \\(C\\) |
|---------|--------------|---------------------|-------------------|
| \\(10^4\\) | 35 | 12.8 | 2.73 |
| \\(10^5\\) | 160 | 65.5 | 2.44 |
| \\(10^6\\) | 759 | 379.2 | 2.00 |
| \\(10^7\\) | 4,668 | 2,388.1 | 1.95 |
| \\(10^8\\) | 30,319 | 15,998.6 | 1.90 |
| \\(10^9\\) | 204,439 | 112,363.5 | 1.82 |
| \\(10^{10}\\) | 1,456,226 | 819,130.2 | 1.78 |

The fit to the \\(N/(\log N)^3\\) form is excellent, but the empirical constant \\(C\\) is not constant—it decreases slowly with \\(N\\).

## The Converging Constant

Fitting the data to candidate models reveals that \\(C(N)\\) follows a logarithmic correction:

$$
C(N) \approx C_\infty + \frac{a}{(\log N)^2}
$$

The best fit gives:

$$
C(N) \approx 1.60 + \frac{100}{(\log N)^2}
$$

This predicts \\(C_\infty \approx 1.60\\) as \\(N \to \infty\\), though convergence is slow—even at \\(N = 10^{100}\\), the formula gives \\(C \approx 1.601\\).

| \\(N\\) | Actual \\(C\\) | Predicted \\(C\\) | Error |
|---------|----------------|-------------------|-------|
| \\(10^6\\) | 2.00 | 2.12 | −6% |
| \\(10^7\\) | 1.95 | 1.98 | −2% |
| \\(10^8\\) | 1.90 | 1.89 | +0.3% |
| \\(10^9\\) | 1.82 | 1.83 | −0.6% |
| \\(10^{10}\\) | 1.78 | 1.79 | −0.4% |

The agreement is excellent for \\(N \geq 10^7\\).

**Prediction formula:**

$$
\pi(N) \approx \left(1.60 + \frac{100}{(\log N)^2}\right) \cdot \frac{N}{(\log N)^3}
$$

## Verification of Modular Constraints

All 1,456,226 computed triples (up to \\(10^{10}\\)) satisfy the predicted constraints with **zero violations**:

**Source prime \\(r \pmod{30}\\)** (sampled):

| Residue | Percentage |
|---------|------------|
| 1 | 24.6% |
| 11 | 25.4% |
| 19 | 25.0% |
| 29 | 25.0% |

The four valid residue classes are populated almost perfectly uniformly.

**Middle prime \\(p \pmod{60}\\)** (sampled):

| Residue | Percentage |
|---------|------------|
| 1 | 100% |

Every sampled middle prime satisfies \\(p \equiv 1 \pmod{60}\\), exactly as predicted.

**Top prime \\(b \pmod{24}\\)** (sampled):

| Residue | Percentage |
|---------|------------|
| 1 | 49.7% |
| 17 | 50.3% |

Both predicted classes appear with remarkably even frequency.

## Gap Statistics

The gaps between consecutive valid \\(r\\) values grow with \\(N\\):

| \\(N\\) | Min Gap | Max Gap | Median Gap |
|---------|---------|---------|------------|
| \\(10^7\\) | 18 | 19,680 | 1,432 |
| \\(10^8\\) | 2 | 38,942 | 2,240 |
| \\(10^9\\) | 2 | 66,908 | 3,330 |
| \\(10^{10}\\) | 2 | 100,380 | 4,692 |

The minimum gap of 2 corresponds to twin valid primes, discussed below.

---

# Twin Valid Primes

Now for the main event. Given the classification of valid source primes, a natural question arises: can consecutive primes *both* generate valid sandwiches?

Specifically, if \\((r, r+2)\\) are twin primes, can both \\(r\\) and \\(r+2\\) produce semiprime square sandwiches?

## The Algebraic Constraint

For both \\(r\\) and \\(r+2\\) to be valid source primes, both must lie in the set \\(\\{1, 11, 19, 29\\} \pmod{30}\\).

Twin primes differ by 2, so we need residue classes \\(a\\) and \\(a+2\\) (mod 30) that are both valid. Checking all possibilities:

- \\(1 + 2 = 3 \not\in \\{1, 11, 19, 29\\}\\) ✗
- \\(11 + 2 = 13 \not\in \\{1, 11, 19, 29\\}\\) ✗
- \\(19 + 2 = 21 \not\in \\{1, 11, 19, 29\\}\\) ✗
- \\(29 + 2 = 31 \equiv 1 \pmod{30}\\) ✓

**Only one transition works:** \\(29 \to 1\\).

> **Theorem (Twin Valid Prime Constraint).** If twin primes \\((r, r+2)\\) both generate valid semiprime square sandwiches, then necessarily \\(r \equiv 29 \pmod{30}\\) and \\(r+2 \equiv 1 \pmod{30}\\).

This is remarkably restrictive. Not only must \\((r, r+2)\\) be twin primes, but \\(r\\) must land in a specific residue class.

## Computational Search

Searching up to \\(10^{10}\\), I found exactly **182 twin valid prime pairs**:

| \\(r\\) | \\(r+2\\) | \\(r \bmod 30\\) | \\((r+2) \bmod 30\\) |
|---------|-----------|------------------|----------------------|
| 661,949 | 661,951 | 29 | 1 |
| 6,142,949 | 6,142,951 | 29 | 1 |
| 8,359,919 | 8,359,921 | 29 | 1 |
| 23,304,959 | 23,304,961 | 29 | 1 |
| 68,412,959 | 68,412,961 | 29 | 1 |
| 100,319,039 | 100,319,041 | 29 | 1 |
| 118,243,259 | 118,243,261 | 29 | 1 |
| 123,338,879 | 123,338,881 | 29 | 1 |
| 149,016,059 | 149,016,061 | 29 | 1 |
| 204,394,049 | 204,394,051 | 29 | 1 |
| ... | ... | ... | ... |

Every single pair has the predicted structure: \\(r \equiv 29 \pmod{30}\\).

## Twin Valid Prime Density

The growth of twin valid primes:

| \\(N\\) | Valid \\(r\\) | Twin Pairs | Twins per 1000 Valid |
|---------|---------------|------------|----------------------|
| \\(10^7\\) | 4,668 | 3 | 0.64 |
| \\(10^8\\) | 30,319 | 5 | 0.16 |
| \\(10^9\\) | 204,439 | 39 | 0.19 |
| \\(10^{10}\\) | 1,456,226 | 182 | 0.12 |

Twin valid primes are getting *relatively* rarer—they grow slower than the total count. This makes sense: twin valid primes require *six* simultaneous primality conditions, while ordinary valid primes require only three.

## The Six-Prime Constellation

For each twin valid prime pair, we get a constellation of six related primes:

1. \\(r\\) — the first source prime
2. \\(r + 2\\) — the twin source prime
3. \\(p_1 = (r^2 + 1)/2\\) — middle prime for first sandwich
4. \\(p_2 = ((r+2)^2 + 1)/2\\) — middle prime for second sandwich
5. \\(b_1 = (r^2 + 2)/3\\) — top prime for first sandwich
6. \\(b_2 = ((r+2)^2 + 2)/3\\) — top prime for second sandwich

These six primes satisfy polynomial relationships. From the algebra:

$$
p_2 - p_1 = \frac{(r+2)^2 + 1}{2} - \frac{r^2 + 1}{2} = \frac{4r + 4}{2} = 2(r+1)
$$

$$
b_2 - b_1 = \frac{(r+2)^2 + 2}{3} - \frac{r^2 + 2}{3} = \frac{4r + 4}{3} = \frac{4(r+1)}{3}
$$

Since \\(r \equiv 29 \pmod{30}\\), we have \\(r + 1 \equiv 0 \pmod{30}\\), giving:

$$
p_2 - p_1 \equiv 0 \pmod{60}, \qquad b_2 - b_1 \equiv 0 \pmod{40}
$$

**Verification with \\(r = 661949\\):**

- \\(p_1 = (661949^2 + 1)/2 = 219088239301\\)
- \\(p_2 = (661951^2 + 1)/2 = 219089563201\\)
- \\(p_2 - p_1 = 1323900 = 60 \times 22065\\) ✓

- \\(b_1 = (661949^2 + 2)/3 = 146058826201\\)
- \\(b_2 = (661951^2 + 2)/3 = 146059708801\\)
- \\(b_2 - b_1 = 882600 = 40 \times 22065\\) ✓

The gap between consecutive \\(p\\) values is exactly \\(\frac{3}{2}\\) times the gap between consecutive \\(b\\) values.

---

# Forbidden Gaps: Cousin and Sexy Primes Cannot Both Be Valid

The twin prime analysis reveals a broader phenomenon: **most prime gap types cannot produce valid pairs**.

For two primes \\(r\\) and \\(r + k\\) to both generate valid sandwiches, we need:
- \\(r \equiv a \pmod{30}\\) for some \\(a \in \\{1, 11, 19, 29\\}\\)
- \\(r + k \equiv b \pmod{30}\\) for some \\(b \in \\{1, 11, 19, 29\\}\\)

This means \\(k \equiv b - a \pmod{30}\\) for valid residues \\(a, b\\).

Computing all possible differences:

| Gap \\(k \pmod{30}\\) | Valid Transition(s) | Common Name |
|-----------------------|---------------------|-------------|
| 2 | \\(29 \to 1\\) | Twin primes |
| 8 | \\(11 \to 19\\) | Octo primes |
| 10 | \\(1 \to 11\\), \\(19 \to 29\\) | — |
| 12 | \\(19 \to 1\\), \\(29 \to 11\\) | — |
| 18 | \\(1 \to 19\\), \\(11 \to 29\\) | — |
| 20 | \\(11 \to 1\\), \\(29 \to 19\\) | — |
| 22 | \\(19 \to 11\\) | — |
| 28 | \\(1 \to 29\\) | — |

**Gaps 4 and 6 are impossible.**

For gap 4 (cousin primes):
- \\(1 + 4 = 5 \not\in \\{1, 11, 19, 29\\}\\)
- \\(11 + 4 = 15 \not\in \\{1, 11, 19, 29\\}\\)
- \\(19 + 4 = 23 \not\in \\{1, 11, 19, 29\\}\\)
- \\(29 + 4 = 33 \equiv 3 \not\in \\{1, 11, 19, 29\\}\\)

For gap 6 (sexy primes):
- \\(1 + 6 = 7 \not\in \\{1, 11, 19, 29\\}\\)
- \\(11 + 6 = 17 \not\in \\{1, 11, 19, 29\\}\\)
- \\(19 + 6 = 25 \not\in \\{1, 11, 19, 29\\}\\)
- \\(29 + 6 = 35 \equiv 5 \not\in \\{1, 11, 19, 29\\}\\)

> **Theorem (Forbidden Gaps).** If primes \\(r\\) and \\(r+k\\) both generate valid semiprime square sandwiches with \\(0 < k < 30\\), then \\(k \in \\{2, 8, 10, 12, 18, 20, 22, 28\\}\\). In particular, **cousin primes (gap 4) and sexy primes (gap 6) cannot both generate valid sandwiches.**

The mod 30 constraint creates "forbidden zones" in the gap spectrum.

## Octo Valid Primes: The Next Smallest Gap

After twin primes (gap 2), the next possible gap is 8. This requires \\(r \equiv 11 \pmod{30}\\) and \\(r + 8 \equiv 19 \pmod{30}\\).

For \\((r, r+8)\\) to both be valid, we need:

1. \\(r\\) and \\(r+8\\) both prime
2. \\((r^2+1)/2\\) and \\(((r+8)^2+1)/2\\) both prime
3. \\((r^2+2)/3\\) and \\(((r+8)^2+2)/3\\) both prime

The relationship between auxiliary primes:

$$
p_2 - p_1 = \frac{(r+8)^2 - r^2}{2} = \frac{16r + 64}{2} = 8(r + 4)
$$

$$
b_2 - b_1 = \frac{(r+8)^2 - r^2}{3} = \frac{16r + 64}{3} = \frac{16(r + 4)}{3}
$$

For \\(b_2 - b_1\\) to be an integer, we need \\(r + 4 \equiv 0 \pmod{3}\\). Since \\(r \equiv 11 \pmod{30}\\) and \\(11 \equiv 2 \pmod{3}\\), we have \\(r + 4 \equiv 2 + 1 \equiv 0 \pmod{3}\\). ✓

This is automatically satisfied by the residue constraint.

---

# Heuristic for Twin Valid Prime Density

For twin valid primes specifically, we need six independent primality conditions:

1. \\(r\\) is prime (with \\(r \equiv 29 \pmod{30}\\))
2. \\(r + 2\\) is prime
3. \\((r^2 + 1)/2\\) is prime
4. \\(((r+2)^2 + 1)/2\\) is prime
5. \\((r^2 + 2)/3\\) is prime
6. \\(((r+2)^2 + 2)/3\\) is prime

By Bateman-Horn, we expect:

$$
\pi_{\text{twin}}(N) \sim C_{\text{twin}} \cdot \frac{N}{(\log N)^6}
$$

Testing against the data:

| \\(N\\) | Twin Pairs | \\(N/(\log N)^6\\) | Empirical \\(C_{\text{twin}}\\) |
|---------|------------|---------------------|--------------------------------|
| \\(10^8\\) | 5 | 2.56 | 1.95 |
| \\(10^9\\) | 39 | 12.63 | 3.09 |
| \\(10^{10}\\) | 182 | 67.10 | 2.71 |

The constant has significant variance at these scales—not surprising given the small counts. Taking \\(C_{\text{twin}} \approx 3\\) as a rough estimate:

**Prediction for \\(10^{12}\\):**

$$
\pi_{\text{twin}}(10^{12}) \approx 3 \cdot \frac{10^{12}}{(\log 10^{12})^6} \approx 3 \cdot 2247 \approx 6700 \text{ pairs}
$$

---

# The Structure of Twin Sandwich Pairs

When \\((r, r+2)\\) are twin valid primes, the two sandwiches have a beautiful relationship.

The first sandwich:

$$
(r^2, \; 2p_1, \; 3b_1)
$$

The second sandwich:

$$
((r+2)^2, \; 2p_2, \; 3b_2)
$$

The gap between the starting squares:

$$
(r+2)^2 - r^2 = 4r + 4
$$

For \\(r = 661949\\):
- First sandwich: \\((438176478601, \; 438176478602, \; 438176478603)\\)
- Second sandwich: \\((438179126401, \; 438179126402, \; 438179126403)\\)
- Gap between sandwiches: \\(438179126401 - 438176478601 = 2647800 = 4 \times 661950\\)

The sandwiches are separated by \\(4(r+1)\\)—close enough to be "neighboring" but not overlapping.

---

# Summary

| Result | Statement |
|--------|-----------|
| **Asymptotic count** | \\(\pi(N) \sim C(N) \cdot N/(\log N)^3\\) with \\(C(N) \to 1.60\\) |
| **Valid r up to \\(10^{10}\\)** | 1,456,226 |
| **Modular constraints** | \\(r \equiv 1, 11, 19, 29 \pmod{30}\\); verified with 0 violations |
| **Twin valid primes** | Require \\(r \equiv 29 \pmod{30}\\); 182 pairs up to \\(10^{10}\\) |
| **Forbidden gaps** | Gaps 4 and 6 impossible; smallest valid gaps are 2 and 8 |
| **Twin count heuristic** | \\(\pi_{\text{twin}}(N) \sim C \cdot N/(\log N)^6\\), \\(C \approx 3\\) |

---

# OEIS Sequences

Based on this analysis, I propose three new sequences:

## A-number (TBD): Valid Sandwich Primes

**Definition:** Primes \\(r\\) such that \\(r^2\\), \\(r^2+1\\), and \\(r^2+2\\) are consecutive semiprimes.

**Data:** 11, 29, 79, 271, 379, 461, 521, 631, 739, 881, 929, 1459, 1531, 1709, 2161, 2239, 2341, 2729, 3049, 3491, ...

**Comments:**
- Equivalently, primes \\(r > 3\\) such that \\((r^2+1)/2\\) and \\((r^2+2)/3\\) are both prime.
- All terms satisfy \\(r \equiv 1, 11, 19,\\) or \\(29 \pmod{30}\\).
- The middle term is \\(2p\\) where \\(p \equiv 1 \pmod{60}\\).
- The final term is \\(3b\\) where \\(b \equiv 1\\) or \\(17 \pmod{24}\\).
- The auxiliary primes satisfy \\(3b = 2p + 1\\).
- Asymptotically, \\(\pi(N) \sim 1.6 \cdot N/(\log N)^3\\).

## A-number (TBD): Twin Valid Sandwich Primes

**Definition:** Primes \\(r\\) such that both \\(r\\) and \\(r+2\\) generate valid semiprime square sandwiches.

**Data:** 661949, 6142949, 8359919, 23304959, 68412959, 100319039, 118243259, 123338879, 149016059, 204394049, ...

**Comments:**
- All terms satisfy \\(r \equiv 29 \pmod{30}\\).
- Subset of A001359 (lesser of twin primes).
- Cousin primes (gap 4) and sexy primes (gap 6) cannot both be valid sandwich primes.
- 182 terms below \\(10^{10}\\).

## A-number (TBD): Squares Starting Twin Valid Sandwiches

**Definition:** \\(r^2\\) where \\(r\\) and \\(r+2\\) are twin valid sandwich primes.

**Data:** 438176478601, 37736002324601, 69887806326561, 543120067418681, 4680332772466681, ...

---

# Open Questions

1. **Are there infinitely many valid sandwich primes?** The Bateman-Horn heuristic suggests yes, but a proof is beyond current methods.

2. **Are there infinitely many twin valid prime pairs?** Even harder—requires six simultaneous primality conditions.

3. **Do octo valid primes (gap 8) exist?** Computationally tractable to search.

4. **What is the exact asymptotic constant?** The empirical \\(C_\infty \approx 1.60\\) could potentially be derived from first principles, though the calculation is subtle.

---

# Final Thoughts

The semiprime square sandwich began as a curious observation about \\(11^2 = 121\\). The classification theorem revealed unexpected structure: the linear relation \\(3b = 2p + 1\\), the tight modular constraints, the connection to quadratic residues.

The twin valid prime extension shows this structure has depth. The constraint \\(r \equiv 29 \pmod{30}\\) for twin pairs, the forbidden gaps at 4 and 6, the six-prime constellation—none of this was obvious from staring at examples.

What makes recreational mathematics worthwhile is precisely this: you start with a pattern, and the pattern has *reasons*. The reasons connect to real mathematics. And sometimes, the reasons raise questions that nobody has answered yet.
