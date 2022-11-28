---
title: "Generating Pythagorean Triples"
date: 2022-11-28T07:18:09Z
tags: ["math", "just for fun"]
katex: true
---

{{<toc>}}

# Background

The pythagorean theorem states that given any right triangle with legs \\(a \\), \\(b\\) and hypotenuse \\(c\\):

$$
a^2 + b^2 = c^2
$$

(For those who are curious to learn more, [please check out wikipedia](https://en.wikipedia.org/wiki/Pythagorean_theorem))

A pythagorean triple is a set of three natural numbers (\\(a,b,c\\)) such that \\( a^2 + b^2 = c^2 \\). We express such a triple as \\( \big( a,b,c \big) \\) with the understanding that \\( c \\) is the hypotenuse. Because we are only interested in natural number solutions, the equation \\( a^2 + b^2 = c^2 \\) is an example of a [nonlinear diophantine equation](https://en.wikipedia.org/wiki/Diophantine_equation).

FWIW, I have been fascinated by diophantine equatiosn lately, primarily thanks to my recent re-learning of the [taxicab number](https://en.wikipedia.org/wiki/Taxicab_number), fabled to have been derived from a conversation between Hardy and Ramanujan himself:

> I remember once going to see him [Ramanujan] when he was lying ill at Putney. I had ridden in taxi-cab No. 1729, and remarked that the number seemed to be rather a dull one, and that I hoped it was not an unfavourable omen. "No," he replied, "it is a very interesting number; it is the smallest number expressible as the sum of two [positive] cubes in two different ways.

(^ excerpt from wikipedia).

It is worth noting that generating pythagorean triples appears to be a solved problem. Here's a whole list of algorithms for [generating pythagorean triples](https://en.wikipedia.org/wiki/Formulas_for_generating_Pythagorean_triples#Euclid's,_Pythagoras',_and_Plato's_formulas).

In this post, I will put forth what I _think_ is an original approach to generating pythagorean triples (eg: at least it isn't explicitly described in the wiki post I referenced). 

# My Algorithm 

Let's begin with a quick observation. Here are some initial/obvious pythagorean triples:

* \\( 3, 4, 5 \\)
* \\( 5, 12, 13 \\)
* \\( 7, 24, 25 \\)
* \\( 9, 40, 41 \\)

A very curious observation here is that the \\( a \\) values are all odd and crucially, the \\( b \\) and \\( c \\) values are **consecutive**. A second observation here is that the **sum** of \\(b + c \\) is equal to \\( a^2 \\).

For instance:

* \\( 3^2 = 9 \\) and \\( 4 + 5 = 9 \\)
* \\( 5^2 = 25 \\) and \\( 12 + 13 = 25 \\)
* \\( 7^2 = 49 \\) and \\( 24 + 25 = 49 \\)
* \\( 9^2 = 81 \\) and \\( 40 + 41 = 81 \\)

Another way to look at this is like so:

$$
\begin{aligned}
a^2 + b^2 &= c^2 \cr
a^2 &= c^2 - b^2 \cr
\end{aligned}
$$

Now remember, we can express the square of any number \\( n \\) as the sum of the square of the previous number (\\( n - 1 \\), let's call it \\(k\\)) and \\(n + k \\). In other words:

$$
\begin{aligned}
n^2 &= k^2 + n + k \cr
\bold{\text{Let: }} k &= n - 1 \cr
n^2 &= (n-1)^2 + n + n-1 \cr
n^2 &= n^2 - 2n + 1 + n + n-1 \cr
n^2 &= n^2 - 2n + 1 + 2n -1 \cr
n^2 &= n^2 \cr
\end{aligned}
$$

^ This looks dumb but minimally shows that:

> the square of any number \\(n\\) can be expressed as the square of the _previous_ number plus \\(n\\) plus the _previous_ number.
> Or: 
> \\( n^2 = (n-1)^2 + n + (n-1) \\)

Another way to look at this is:

> The difference between some number \\(n^2\\) and \\((n-1)^2\\) is just the sum of those two numbers. Or:
> <br/>\\( n^2 - (n-1)^2 = n + (n-1) \\)

Ok going back to our diophantine equation:

$$
\begin{aligned}
a^2 + b^2 &= c^2 \cr
a^2 &= c^2 - b^2 \cr
\end{aligned}
$$

> If we could find some numbers \\(b\\) and \\(c\\) such that \\(b+c = a^2 \\) for each \\(a\\), we have found a set of valid solutions to this equation. 

For simplicity, let's start with the case that we observed above: \\(b\\) and \\(c\\) are consecutive. Let's let \\(c = b+1 \\).

There are two cases to consider:

* \\(a\\) is **even**
* \\(a\\) is **odd**

## \\(a\\) is **even**

If \\(a\\) is **even**, then \\(a^2\\) must also be even. (**WHY?**: An even times an even number is always even).

So, we want to find \\(a^2 = b + c \\) where \\(c = b + 1 \\).

Therefore: \\(\\) or

$$
\begin{aligned}
a^2 &= b + b + 1 \cr
    &= 2b + 1 \cr
\end{aligned}
$$ 

Since we are considering only **even** values of \\(a\\) here, \\(a^2\\) is **even** and so:

$$
\begin{aligned}
2b + 1 &= a^2 \cr
2b 	   &= a^2 - 1 \cr
\end{aligned}
$$ 

> Since \\(a^2\\) is even, \\(a^2-1\\) **must** be odd. Thus, there are no solutions for **even** values of \\(a\\) where we have a consecutive values \\(b,c\\) that add up to \\(a^2\\)

(FWIW: this doesn't mean there are no pythagorean triples with even legs (obviously since we noted a few examples to start off with here), it just means that with this approach as it stands so far we cannot find any.)

## \\(a\\) is **odd**

If \\(a\\) is **odd**, then \\(a^2\\) must also be odd. (**WHY?**: An odd times an odd number is always odd). Revisiting our equation:

$$
\begin{aligned}
a^2 &= b + b + 1 \cr
    &= 2b + 1 \cr
a^2 - 1 &= 2b \cr
\end{aligned}
$$ 

> Because we know \\(a^2\\) is odd, \\(a^2-1\\) **must** be even. And since \\(a^2-1\\) is even, \\(\frac{a^2-1}{2}\\) **must also** be even. Therefore there is _always_ some number \\(b\\) (and \\(c = b+1\\)) such that \\(a^2 = b + c \\).

Put another way:

> For all odd values of \\(a\\) in the pythagorean triple \\(a,b,c\\) we are guaranteed natural numbers \\(b\\) and \\(c\\) such that \\(a^2+b^2 = c^2\\).

### Implication

Ok let's put this to the test. Say \\(a = 13 \\). Then we know that:

$$
\begin{aligned}
a^2 &= b + b + 1 \cr
    &= 2b + 1 \cr
13^2 - 1 &= 2b \cr
169 - 1 &= 2b \cr
168 &= 2b \cr
84 &= \bold{b} \cr
85 &= b + 1 \cr
85 &= \bold{c} \cr
\end{aligned}
$$

And so, \\(13,84,85\\) is a pythagorean triple.

> Heads up: with this approach, we also arrive at exclusively primitive pythagorean triples (eg: \\(a,b,c\\) are coprime - they have no common divisor larger than 1). I don't know how to prove this yet so I'll leave it as just an observation.

We can do this all day, actually.

> Using the \\(a^2 = 2b+1\\) formula, we can generate at least one pythagorean triple solution for **all odd numbers**.

## Finding more possible solutions

Let's revisit our slightly modified version of the equation:

$$
\begin{aligned}
a^2 &= c^2 - b^2 \cr
\end{aligned}
$$

We have considered the cause where \\(c = b + 1 \\). But, this is but one possible condition, for instance it is possible to have an \\(a\\) such that \\(a^2 = b+c \\) where \\(c = b +2 \\) or \\(c = b + 3\\), etc. To explore this usecase, let's slightly modify our equation again:

$$
\begin{aligned}
a^2 &= c^2 - b^2 \cr
	&= (c+b)(c-b) \cr
\end{aligned}
$$

If \\(c = b + 1 \\), then:

$$
\begin{aligned}
a^2 &= c^2 - b^2 \cr
	&= (c+b)(c-b) \cr
\text{Let: } c &= b + 1 \cr
	&= ((b+1)+b)((b+1)-b) \cr
	&= (2b+1)(1) \cr
	&= (2b+1) \cr
\end{aligned}
$$

^ This of course brings us back to the formula derived in the previous section. **BUT**: this approach is easier to grok (and minimally easier to type!), allowing us to extend out reach, like so:

$$
\begin{aligned}
a^2 &= c^2 - b^2 \cr
	&= (c+b)(c-b) \cr
\text{Let: } c &= b + \bold{2} \cr
	&= ((b+\bold{2})+b)((b+\bold{2})-b) \cr
	&= (2b+2)(2) \cr
	&= (4b+4) \cr
\end{aligned}
$$

or:

$$
\begin{aligned}
a^2 &= c^2 - b^2 \cr
	&= (c+b)(c-b) \cr
\text{Let: } c &= b + \bold{3} \cr
	&= ((b+\bold{3})+b)((b+\bold{3})-b) \cr
	&= (2b+3)(3) \cr
	&= (6b+9) \cr
\end{aligned}
$$

Let's get this in tabular form:

| \\(c = \\)      		| \\(a^2 = \\) |
| ----------- 			| -----------  |
| \\( b+1 \\)      		| \\(2b+1\\)   |
| \\( b+2 \\)      		| \\(4b+4\\)   |
| \\( b+3 \\)      		| \\(6b+9\\)   |
| \\( b+4 \\)      		| \\(8b+16\\)  |
| \\( b+5 \\)      		| \\(10b+25\\) |
| \\( b+n \\)      		| \\(2nb+n^2\\)|

Also worth observing that run out of possible solutions when \\(n^2 >= a^2\\). (For example, when \\(a = 13 \\), the largest \\(n\\) that may provide us with a solution is \\(n = 12 \\))

### Testing

Let's test this by looking for triples from \\(a = 3 \\) to \\(a = 9 \\). It looks like we expect only the following (source (don't judge me) [here](https://www.avc.edu/sites/default/files/studentservices/lc/math/pythagorean_triples.pdf)):

| Row       | Triple       |
| -----------  | -----------  |
| 1  | \\(3,4,5\\) |
| 2  | \\(5, 12, 13\\) |
| 3  | \\(6,8,10\\) |
| 4  | \\(7,24,25\\) |
| 5  | \\(8,15,17\\) |
| 6  | \\(9,12,15\\) |
| 7  | \\(9,40,41\\) |


#### \\(a = 3 \\) 

| \\(c = \\)      		| \\(a^2 = \\) | Compute      	| Triple       |
| ----------- 			| -----------  | -----------  	| -----------  |
| \\( b+1 \\)      		| \\(2b+1\\)   | \\(2b+1 = 9\\) | \\(3,4,5\\)      |
| \\( b+2 \\)      		| \\(4b+4\\)   | \\(4b+4 = 9\\) | (none)       |
| \\( b+3 \\)      		| \\(6b+9\\)   | \\(n^2 >= 9\\) | STOP         |

**FOUND(Row)?**: 1


#### \\(a = 4 \\)

| \\(c = \\)      		| \\(a^2 = \\) | Compute      	| Triple       |
| ----------- 			| -----------  | -----------  	| -----------  |
| \\( b+1 \\)      		| \\(2b+1\\)   | \\(2b+1 = 16\\) | (none)     |
| \\( b+2 \\)      		| \\(4b+4\\)   | \\(4b+4 = 16\\) | \\(3,4,5\\)       |
| \\( b+3 \\)      		| \\(6b+9\\)   | \\(6b+9 = 16\\) | (none)         |
| \\( b+4 \\)      		| \\(8b+16\\)   | \\(n^2 >= 16\\) | STOP         |

**FOUND(Row)?**: 1, 1 (AGAIN)

#### \\(a = 5 \\)

| \\(c = \\)      		| \\(a^2 = \\) | Compute      	| Triple       |
| ----------- 			| -----------  | -----------  	| -----------  |
| \\( b+1 \\)      		| \\(2b+1\\)   | \\(2b+1 = 25\\) | \\(5,12,13\\)     |
| \\( b+2 \\)      		| \\(4b+4\\)   | \\(4b+4 = 25\\) | (none)      |
| \\( b+3 \\)      		| \\(6b+9\\)   | \\(6b+9 = 25\\) | (none)         |
| \\( b+4 \\)      		| \\(8b+16\\)   | \\(8b+16 = 25\\) | (none)         |
| \\( b+5 \\)      		| \\(10b+25\\)   | \\(n^2 >= 25\\) | STOP         |

**FOUND(Row)?**: 1, 2

#### \\(a = 6 \\)

| \\(c = \\)      		| \\(a^2 = \\) | Compute      	| Triple       |
| ----------- 			| -----------  | -----------  	| -----------  |
| \\( b+1 \\)      		| \\(2b+1\\)   | \\(2b+1 = 36\\) | (none)     |
| \\( b+2 \\)      		| \\(4b+4\\)   | \\(4b+4 = 36\\) | \\(6,8,10\\)      |
| \\( b+3 \\)      		| \\(6b+9\\)   | \\(6b+9 = 36\\) | (none)         |
| \\( b+4 \\)      		| \\(8b+16\\)   | \\(8b+16 = 36\\) | (none)         |
| \\( b+5 \\)      		| \\(10b+25\\)   | \\(10b+25 = 36\\) | (none)         |
| \\( b+6 \\)      		| \\(12b+36\\)   | \\(n^2 >= 36\\) | STOP         |

**FOUND(Row)?**: 1, 2, 3


#### \\(a = 7 \\)

| \\(c = \\)      		| \\(a^2 = \\) | Compute      	| Triple       |
| ----------- 			| -----------  | -----------  	| -----------  |
| \\( b+1 \\)      		| \\(2b+1\\)   | \\(2b+1 = 49\\) | \\(7,24,25\\)     |
| \\( b+2 \\)      		| \\(4b+4\\)   | \\(4b+4 = 49\\) | (none)       |
| \\( b+3 \\)      		| \\(6b+9\\)   | \\(6b+9 = 49\\) | (none)         |
| \\( b+4 \\)      		| \\(8b+16\\)   | \\(8b+16 = 49\\) | (none)         |
| \\( b+5 \\)      		| \\(10b+25\\)   | \\(10b+25 = 49\\) | (none)         |
| \\( b+6 \\)      		| \\(12b+36\\)   | \\(12b+36 = 49\\) | (none)         |
| \\( b+7 \\)      		| \\(14b+49\\)   | \\(n^2 >= 49\\) | STOP         |

**FOUND(Row)?**: 1, 2, 3, 4

#### \\(a = 8 \\)


| \\(c = \\)      		| \\(a^2 = \\) | Compute      	| Triple       |
| ----------- 			| -----------  | -----------  	| -----------  |
| \\( b+1 \\)      		| \\(2b+1\\)   | \\(2b+1 = 64\\) | (none)      |
| \\( b+2 \\)      		| \\(4b+4\\)   | \\(4b+4 = 64\\) | \\(8, 15, 17\\)       |
| \\( b+3 \\)      		| \\(6b+9\\)   | \\(6b+9 = 64\\) | (none)         |
| \\( b+4 \\)      		| \\(8b+16\\)   | \\(8b+16 = 64\\) | \\(6,8,10\\)         |
| \\( b+5 \\)      		| \\(10b+25\\)   | \\(10b+25 = 64\\) | (none)         |
| \\( b+6 \\)      		| \\(12b+36\\)   | \\(12b+36 = 64\\) | (none)         |
| \\( b+7 \\)      		| \\(14b+49\\)   | \\(14b+49 = 64\\) | (none)         |
| \\( b+8 \\)      		| \\(16b+64\\)   | \\(n^2 >= 64\\) | STOP         |

**FOUND(Row)?**: 1, 2, 3, 4, 5, 3 (AGAIN)

#### \\(a = 9 \\)

| \\(c = \\)      		| \\(a^2 = \\) | Compute      	| Triple       |
| ----------- 			| -----------  | -----------  	| -----------  |
| \\( b+1 \\)      		| \\(2b+1\\)   | \\(2b+1 = 81\\) | \\(9,40,41\\)      |
| \\( b+2 \\)      		| \\(4b+4\\)   | \\(4b+4 = 81\\) | (none)        |
| \\( b+3 \\)      		| \\(6b+9\\)   | \\(6b+9 = 81\\) | \\(9, 12, 15\\)         |
| \\( b+4 \\)      		| \\(8b+16\\)   | \\(8b+16 = 81\\) | (none)         |
| \\( b+5 \\)      		| \\(10b+25\\)   | \\(10b+25 = 81\\) | (none)         |
| \\( b+6 \\)      		| \\(12b+36\\)   | \\(12b+36 = 81\\) | (none)         |
| \\( b+7 \\)      		| \\(14b+49\\)   | \\(14b+49 = 81\\) | (none)         |
| \\( b+8 \\)      		| \\(16b+64\\)   | \\(16b+64 = 81\\) | (none)         |
| \\( b+9 \\)      		| \\(18b+81\\)   | \\(n^2 >= 81\\) | STOP        |

**FOUND(Row)?**: 1, 2, 3, 4, 5, 7, 6

^ That's all of them!

#### Results

It looks like the algorithm worked! By walking down from \\(a = 3 \\) to \\(a = 9 \\), we were able to identify _all_ pythagorean triples (primitive or not). Also, we seem to have stumbled on the same triple a few times along the way.

For what it's worth, we can always filter out the non primitive triples from this approach by analyzing \\(c\\), which in a primitive triple will always be odd (Shanks, 1993, p. 141 - reference [here](https://mathworld.wolfram.com/PythagoreanTriple.html#:~:text=Shanks))

# Commentary

This is really cool! I appreciate the simplicity of this approach in that we can find all possible triples simply by incrementing \\(a\\) starting at \\(a = 3\\). Moreover, it appears that my approach solves an issue with **Euclid's formula**:

> Despite generating all primitive triples, Euclid's formula does not produce all triples—for example, (9, 12, 15) cannot be generated using integer m and n.

(^ wiki, [here](https://en.wikipedia.org/wiki/Pythagorean_triple#Generating_a_triple))

While there are solutions put forth to remedy this, the approach listed here does not need any additional tweaks to render all triples.

At some point, I'd like to implement this algorithm in code to generate the first 100 or 1000 primes and also, I'd like to explore any possible optimizations here (for instance, I have a gut feeling that stopping when \\(n^2 >= a\\) might be sufficient instead of going all the way out to \\(n^2 >= a^2\\) but I have no way to really tell further exploration.)
