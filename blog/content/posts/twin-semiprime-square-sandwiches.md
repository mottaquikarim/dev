---
title: "Twin Semiprime Square Sandwiches"
date: 2026-10-25T00:00:00Z
draft: false
tags: ["math", "just for fun"]
katex: true
images: ["images/a401114-cover.png"]
ogimagewidth: 1584
ogimageheight: 396
---

Fair warning, Dear Reader: this post is not (really) about sandwiches. Not the edible kind, at least.

---

BLUF: I contributed to math! My submission to the Online Encyclopedia of Integer Sequences (OEIS) is available here: [https://oeis.org/A401114](https://oeis.org/A401114).

---

{{<toc>}}

# Background

Years ago, after a conversation with my friend Chai, I noticed a pattern: the numbers 33, 34, and 35 form a sequence of consecutive semiprimes. I thought this was very neat and I wondered: what could be the longest possible length of such a sequence? ([original post]({{< relref "posts/the-semiprime-sandwich.md" >}})). In other words, I sought to answer the question: is it only 3? Infinity? Some other number? And why?

After some brief exploration looking into the properties of these sequences, I was able to prove that the longest possible chain of consecutive semiprimes is exactly 3. (And, that the first occurrence of this sequence is the pattern I had noticed before: 33, 34, 35).

For reasons still unclear to me, I thought this was a really cute finding, and I decided to name sequences of this nature "Semiprime Sandwiches". (Sometime earlier this year, when I had learned of the OEIS, I looked it up and it turns out the Semiprime Sandwiches have been listed since 2002, as OEIS: [A056809](https://oeis.org/A056809).)

At some point last year, I revisited my explorations in this area and I was able to make new progress in enumerating additional properties of Semiprime Sandwiches. Primarily, I was able to show that amongst the Semiprime Sandwiches, there exists a more interesting subset: Semiprime ***Square*** Sandwiches. ([post]({{< relref "posts/the-semiprime-squared-sandwich.md" >}})) I was able to show that these sequences are of the form \\({r^2, 2p, 3s}\\) (where \\(r\\), \\(p\\) and \\(s\\) are all prime) and that they adhere to a certain set of divisibility rules:

$$
\begin{aligned}
r &\equiv 1, 11, 19, \text{ or } 29 \pmod{30} \cr
p &\equiv 1 \pmod{60} \cr
s &\equiv 1 \text{ or } 17 \pmod{24}
\end{aligned}
$$

In plain English: \\(r\\) always leaves a remainder of 1, 11, 19 or 29 when divided by 30, \\(p\\) is always 1 more than a multiple of 60, and \\(s\\) is always 1 or 17 more than a multiple of 24. (This, as it turns out, was *also* already known and listed, OEIS: [A179502](https://oeis.org/A179502), submitted in 2011).

Ok so let's fast forward to this week - my trek into the office has become a legitimate odyssey by land (train) and by sea (ferry) thanks to the ongoing NJT Portal Bridge construction work (call me Taq-ysseus, tonight). So, in between agent turns, train delays and intermittent internet connectivity during my (much longer) commute, I started musing again about Semiprime Sandwiches. This turned out to be quite serendipitous, because I ended up stumbling upon an *even more* interesting (or perhaps, more *specific*) subset of the Semiprime Sandwich - what I am calling the Twin Semiprime Square Sandwich (or TS3 for short) - which has now been accepted to the OEIS as OEIS: [A401114](https://oeis.org/A401114).

The rest of this post will expound on the sequence, and put forth a few lemmas + 1 conjecture from my explorations this past month.

# OEIS: A401114

Let's start off by describing the observation that was accepted. (The comment I submitted as part of the submission is at the end of this section. I personally find that prose pretty hard to grok, so for my own sake (for when I revisit this work again, perhaps inevitably during the next NJT service outage event), I'm going to reproduce my initial logic and thinking first.)

## The basics

I want to start by establishing a few relevant properties of the Semiprime Square Sandwich (defined in [my previous post]({{< relref "posts/the-semiprime-squared-sandwich.md" >}})). The Semiprime Square Sandwich can be understood to be:

> A prime number \\(r\\) forms a Semiprime Square Sandwich if \\(r^2\\), \\({r^2 + 1}\\) and \\({r^2 + 2}\\) are all semiprimes. When that happens, \\({r^2 + 1 = 2p}\\) and \\({r^2 + 2 = 3s}\\), where \\(p\\) and \\(s\\) are both prime.

So let's break this down with a simple prime number, say 11. We know that \\({11^2 = 121}\\) is definitely a semiprime (it's \\({11 \times 11}\\), a product of exactly two primes).

Cool, now, as it turns out, 121, 122, 123 form a Semiprime Square Sandwich: 122 is a semiprime (\\({2 \times 61}\\)) and 123 is a semiprime (\\({3 \times 41}\\)). Now let's rewrite this in symbolic terms, suppose 121, which is \\({11 \times 11}\\), is written as \\(r^2\\), where \\({r = 11}\\). Then, we can rewrite 122 as \\(2p\\) where \\(p\\) is a prime and we can rewrite 123 as \\(3s\\), where \\(s\\) is a prime:

$$
\begin{aligned}
121 &= 11^2 = r^2 \cr
122 &= 2 \times 61 = 2p \cr
123 &= 3 \times 41 = 3s
\end{aligned}
$$

(PS: note that \\(r\\), which is 11, has a remainder of 11 when divided by 30, \\(p\\), which is 61, has a remainder of 1 when divided by 60 and \\(s\\), which is 41, has a remainder of 17 when divided by 24 - just as predicted by the divisibility rules for Semiprime Square Sandwiches I referenced earlier on in this post.)

## The question

Now suppose we ask the question: what if \\({r + 2}\\) was *also* a prime (NOTE: in the example above, where \\({r = 11}\\), this does happen to be the case since \\({r + 2}\\) is \\({11 + 2}\\), or 13). Could it be that \\({(r + 2)^2}\\), \\({(r + 2)^2 + 1}\\) and \\({(r + 2)^2 + 2}\\) ALSO form a Semiprime Square Sandwich?

And if it COULD be that this were true, then what are the properties/behavior of such instances of our sequence? How might we find them?

---

Algorithmically, we can hunt for such sequences to prove to ourselves that this does occur "in the wild" (which I did). And the primary finding from this search is that TS3s don't follow a formula, but they *do* follow certain divisibility rules.

The main rule I found (and show below) is that every TS3 number, \\(r\\), is one below a multiple of 30.

In other words, if \\(r\\) and \\({r + 2}\\) are your twin primes, both generating Semiprime Square Sandwiches, then it is guaranteed that

$$
r \equiv 29 \pmod{30}
$$

## Justification

Let's start with a real example: the first TS3 pair: 661949 and 661951. Notice that the number between them, 661950, is \\({30 \times 22065}\\) (so then \\(r\\), 661949, divided by 30 must leave a remainder of 29).

**Step 1: Every square sandwich ends in 1 or 9.** We know that \\(r\\), which is prime, must be odd. So, it follows that \\(r\\) must end in 1, 3, 7, or 9 (Why not 5? Because any number ending in 5 is divisible by 5, and therefore can't be prime). If \\(r\\) ends in 3 or 7, then \\(r^2\\) ends in 9 (no matter what the value of \\(r\\), squaring it means the last digit is squared, so \\({3 \times 3 = 9}\\), or \\({7 \times 7 = 49}\\)...which also ends in 9), so \\({r^2 + 1}\\) MUST end in 0. That makes

$$
p = \frac{r^2 + 1}{2}
$$

a multiple of 5, and since we know \\(p\\) is always bigger than 5 (since square sandwiches start from 11), it can't be prime. **So \\(r\\) can't end in 3 or 7.** And \\(r\\) is a prime bigger than 2, so it can't end in 0, 2, 4, 6 or 8 either. That leaves 1 and 9.

**Step 2: So the number between the twins ends in 0.** Both \\(r\\) and \\({r + 2}\\) must end in 1 or 9. If \\(r\\) ends in 1, then \\({r + 2}\\) ends in 3, which Step 1 rules out. So \\(r\\) ends in 9, \\({r + 2}\\) ends in 1, and \\({r + 1}\\) ends in 0. It's a multiple of 10. Check: 661949 ends in 9, 661951 ends in 1, 661950 ends in 0.

**Step 3: The number between any pair of twin primes is a multiple of 6.** Out of any three numbers in a row, one is a multiple of 3. It can't be \\(r\\) or \\({r + 2}\\), because those are prime. So it's \\({r + 1}\\). And \\({r + 1}\\) is even (it has to be, since \\(r\\) and \\({r + 2}\\) are primes and \\(r\\) can't be 2, so \\(r\\) and \\({r + 2}\\) must be odd). Therefore \\({r + 1}\\) is a multiple of 6.

**Step 4: Are we done? I think we're done.** \\({r + 1}\\) is a multiple of 10 and a multiple of 6, so it's a multiple of 30. (**PS**: Why 30? Because a number divisible by both \\({10 = 2 \times 5}\\) and \\({6 = 2 \times 3}\\) has to be divisible by their LCM:

$$
\text{lcm}(10, 6) = 2 \times 3 \times 5 = 30
$$

Thanks 3rd grade math!) That's what \\({r \equiv 29 \pmod{30}}\\) means: divide \\(r\\) by 30 and the remainder is 29. Check: \\({661950 = 30 \times 22065}\\) (so \\(r\\), 661949, divided by 30 will give us remainder 29).

## How this looks on the OEIS

And here is the comment that I submitted as part of the submission. Claude helped me take my overall argument (which I came up with mostly in my head while sitting, if I was lucky that day, on an immobile train in an internet dead zone somewhere in the swamps of Secaucus) and condense it into this format, which is in line with the terse style of commentary observed across the OEIS:

> For each term r, let R = r^2 and R' = (r+2)^2. Then R, R+1, R+2 are consecutive semiprimes, and R', R'+1, R'+2 are consecutive semiprimes.<br><br>
> Also, r, r+2, (R+1)/2, (R+2)/3, (R'+1)/2, (R'+2)/3 are all prime.<br><br>
> All terms in this sequence are congruent to 29 (mod 30), so r+1 is divisible by 30. Proof: r and r+2 are both terms of [A179502](https://oeis.org/A179502), so both are primes greater than 3. Since r is odd, R is odd, so R+1 is an even semiprime: R+1 = 2\*p with p prime. If r == 2 or 3 (mod 5), then R+1 is divisible by 5 (since 2^2+1 = 5 and 3^2+1 = 10), so p is divisible by 5, so p = 5 and r = 3, a contradiction. Thus r == 1 or 4 (mod 5), and by the same argument, r+2 == 1 or 4 (mod 5). If r == 1 (mod 5), then r+2 == 3 (mod 5), which contradicts r+2 == 1 or 4 (mod 5). So r == 4 (mod 5), and then r+2 == 1 (mod 5). Since r and r+2 are primes greater than 3, r+1 is divisible by 6. So r+1 is divisible by 30.

# So what about cousins and sexy primes?

Ok so once I had the twin prime argument all sorted out, the natural next question became: what about other gaps? Eg: a twin prime is a set of two numbers, \\(r\\) and \\({r + 2}\\), that we observed could *sometimes*, under the right divisibility circumstances, give us Twin Semiprime Square Sandwiches. We know that other gapped primes exist (eg: cousin primes, or primes \\(r\\) and \\({r + 4}\\) or "sexy" primes, \\(r\\) and \\({r + 6}\\)).

Ok so let's get on exploring. Remember from our proof above: given \\(r\\) is a prime number such that \\(r^2\\) is the first term in a Semiprime Square Sandwich, \\(r\\) must end in either 1 or 9. Since \\({r + 4}\\) then must end in either 5 (\\({1 + 4}\\)) (which can't work, since the only prime number ending in 5 is 5 itself) or \\({r + 4}\\) must end in 3 (\\({9 + 4 = 13}\\), ending in 3) (which can't work, because \\({r + 4}\\) does not end in 1 or 9 as established above), there exist no cousin primes where both cousins lead to Semiprime Square Sandwiches.

Let's try again, for sexy primes. \\({r + 6}\\) must end in either 7 or 5. Using similar logic as above, neither case works, therefore there exist no sexy primes where both numbers (...sexes?) lead to Semiprime Square Sandwiches.

# Is there any "gap" number, g, greater than 2, that satisfies our condition?

Let's see! We know our gap, \\(g\\), can either be even or odd. Suppose \\(g\\) is odd (so ending in 1, 3, 5, 7, 9). Since \\(r\\) must be odd, \\(r\\) + an odd \\(g\\) would be even. So \\({r + g}\\) would be even, which doesn't work.

Neat - let's look at \\(g\\) such that \\(g\\) is even. Here, \\({r + g}\\) would be odd, but remember, \\(r\\) must end in either 1 or 9. So we need to think of numbers that, when added to \\(r\\), would ALSO end in 1 or 9. Since there's a bounded set of endings for even numbers (0, 2, 4, 6, 8) we just have to test each with each possible ending of \\(r\\), to see if we get back to 1 or 9 endings for \\({r + g}\\).

So for example, if \\(r\\) ends in 1, \\({r + 0}\\) would end in 1 (trivial, ha). But \\({r + 2}\\) would end in 3. Which doesn't work. Same for 4 (ends in 5), 6 (ends in 7). 8 works though, ending in 9 which could be valid. So \\(g\\) *could* be a number ending in 8 (8, 18, 28, etc).

Now let's try for the case where \\(r\\) ends in 9. Similar idea, 2 works (\\({9 + 2 = 11}\\), which ends in 1). 4 doesn't, 6 doesn't, 8 doesn't.

| Last digit of \\(g\\) | \\(r\\) ends in 1 | \\(r\\) ends in 9 |
| --- | --- | --- |
| 0 | ends in 1 ✓ | ends in 9 ✓ |
| 2 | ends in 3 ✗ | ends in 1 ✓ |
| 4 | ends in 5 ✗ | ends in 3 ✗ |
| 6 | ends in 7 ✗ | ends in 5 ✗ |
| 8 | ends in 9 ✓ | ends in 7 ✗ |

So \\(g\\) such that \\(g\\) ends in 0, 2 or 8 (eg: 10, 20, 30..., or 2 (as we saw!), 12, 22..., or 8, 18, 28...) are all valid possibilities.

We don't know if this goes on forever, but a quick(ish) counting check shows the following:

| Gap \\(g\\) | Pairs with \\(r\\) below \\(10^8\\) | Smallest \\(r\\) |
| --- | --- | --- |
| 2 (twin) | 5 | 661949 |
| 4 (cousin) | 0 | none, proven |
| 6 (sexy) | 0 | none, proven |
| 8 | 39 | 300221 |
| 10 | 54 | 11959 |
| 12 | 20 | 186379 |
| 14 | 0 | none, proven |
| 16 | 0 | none, proven |
| 18 | 51 | 11 |
| 20 | 24 | 2283551 |

# What I know, and what I don't

So, two things I can say for sure about Twin Semiprime Square Sandwiches. First, every one of them starts one below a multiple of 30. Second, twins aren't the only option: two square sandwiches can only sit a gap \\(g\\) apart if \\(g\\) is even and ends in 0, 2 or 8. That rules out cousins, sexy primes and infinitely many other gaps for good.

What I can't say (yet) is whether TS3s go on forever. My conjecture is that they do: there are 182 of them below 10 billion, and nothing I've found stops them. But proving it is the same kind of problem as the twin prime conjecture, which has been open for over 170 years.

Next up: what happens if one sandwich can *build* the next one? I might have found another OEIS sequence. I call them "s-chains," and I'll provide a breakdown of the thinking assuming I can convince myself (and the OEIS editors) that this is worth a submission. Stay tuned!
