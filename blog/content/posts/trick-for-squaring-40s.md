---
title: "Trick for Squaring 40s (and 50s)"
date: 2022-11-20T22:36:58Z
katex: true
---

{{<toc>}}

# The Trick (I)

Here's a really cute trick for squaring numbers in the \\(40\\)s.

$$
\begin{aligned}
40^2 &= 1600 \cr
     &= [16] \text{ and } [00] \cr
41^2 &= 1681 \cr
	 &= [16] \text{ and } [81] \cr
	 &= [16 + 0] \text{ and } [9^2] \cr
42^2 &= 1764 \cr
	 &= [17] \text{ and } [64] \cr
	 &= [16 + 1] \text{ and } [8^2] \cr
	 &= [16 + \bold{1}] \text{ and } [(10-\bold{2})^2] \cr
43^2 &= 1849 \cr
	 &= [18] \text{ and } [49] \cr
	 &= [16 + \bold{2}] \text{ and } [(10-\bold{3})^2] \cr
44^2 &= 1936 \cr
	 &= [19] \text{ and } [36] \cr
	 &= [16 + \bold{3}] \text{ and } [(10-\bold{4})^2] \cr
45^2 &= 2025 \cr
	 &= [20] \text{ and } [25] \cr
	 &= [16 + \bold{4}] \text{ and } [(10-\bold{5})^2] \cr
\end{aligned}
$$

and so on! This goes all the way up to 50 and in fact, from 50 we get:

# The Trick (II)

$$
\begin{aligned}
50^2 &= 2500 \cr
     &= [25] \text{ and } [00] \cr
51^2 &= 2601 \cr
	 &= [26] \text{ and } [01] \cr
	 &= [25 + 1] \text{ and } [1^2] \cr
52^2 &= 2704 \cr
	 &= [27] \text{ and } [04] \cr
	 &= [25 + \bold{2}] \text{ and } [\bold{2}^2] \cr
53^2 &= 2809 \cr
	 &= [28] \text{ and } [09] \cr
	 &= [25 + \bold{3}] \text{ and } [\bold{3}^2] \cr
54^2 &= 2916 \cr
	 &= [29] \text{ and } [16] \cr
	 &= [25 + \bold{4}] \text{ and } [\bold{4}^2] \cr
55^2 &= 3025 \cr
	 &= [30] \text{ and } [25] \cr
	 &= [25 + \bold{5}] \text{ and } [\bold{5}^2] \cr
\end{aligned}
$$

This goes on too! In fact, we can go "backwards" (into the 30s) and "forwards" (into the 60s) but the trick becomes less useful since you have to know stuff like \\(13^2\\) and what not, which isn't nearly as fun/fast. 

My bet is it has to do with the \\(\bold{5}\\) in the \\(\bold{5}0\\)s. Looking at just two examples (\\(51\\) and \\(52\\)) we can see that:

$$
\begin{aligned}
51^2 &= (50+1)^2 \cr
	 &= (50^2 + 2*50 +1) \cr
     &= (50^2 + 2*50 +1) \cr
	 &= (5^2*10^2 + 2*50 + 1) \cr
     &= (5*5*10*10 + 2*5*10 + 1) \cr
     &= (5*5*10*10 + 2*5*5*2 + 1) \cr
     &= (100(5*5 + 1) + 1) \cr
     &= (100(25 + \bold{1}) + \bold{1}) \cr
\end{aligned}
$$

and likewise with \\(52^2\\):

$$
\begin{aligned}
51^2 &= (50+2)^2 \cr
	 &= (50^2 + 2*2*50 + 4) \cr
     &= (50^2 + 4*50 +4) \cr
	 &= (5^2*10^2 + 4*50 + 4) \cr
     &= (5*5*10*10 + 2*2*5*10 + 4) \cr
     &= (5*5*10*10 + 2*2*5*5*2 + 4) \cr
     &= (100(5*5 + 2) + 4) \cr
     &= (100(25 + \bold{2}) + \bold{2^2}) \cr
\end{aligned}
$$


etc. At some point later on I'll follow up with some justification for this.