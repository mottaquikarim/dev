
---
title: "Hello, Wrold from Colab"
date: 2021-01-28T04:01:51Z
tags: ["meta", "python", "just for fun"]
---

{{<toc>}}

> Hello, Wrold, from Google Colab!!

[Here](https://colab.research.google.com/drive/1K3xuq9Ipy_iUIX_NmH5j-CP4foIVklhA?usp=sharing) is the colab doc for those following along at home).

## What?

This is a post composed in Google Colab as a demonstration of feasibility that blog posts can be generated from a colab notebook.

In fact, any `ipynb` file is fair game - just drop it in to a particular folder and on build, it will be converted to a markdown file, "sanitized" and then available as a normal post on Hugo.

## Why?

No reason! "Just because".

Admittedly, it probably isn't a great idea to load data from two sources (as raw markdown and also available randomly as python notebooks).

Really, this is mainly a thought experiment. I've dabbled in static site generation from python notebooks before and will probably do so again.

On the plus side, composing python related posts got a heck of a lot easier since Python Notebooks can/will provide the ability to add code cells and output "for free".

Also, it _is_ kinda nice to have a web interface for composing stuff without having to go to terminal. Still, this particular approach is certifiably insane and there are definitely...easier options. Still! This is a fun thought experiment/demo! 

## How?

A more detailed post to follow shortly but for now:

- Write post in colab
- Use colab's "save to github" feature to push to the correct repo and sub folder
- Set up github workflow to process .ipynb files
- on save to github, workflow triggers script that used `jupytext` to convert into markdown and moves to huge content folder
- wait for normal deploy process to take effect
- ???
- profit.



Stay tuned fam, more details to follow.





## PS: want to load some py code? Why not!

Cool bit is on colab at least, you can control which cells show output vs not.

Let's start by importing a bunch of stuff.


```python id="LbrvGJGrwwlw"
import pandas as pd
!pip install yfinance
import yfinance as yf
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
```


Ok, now time to grab a ticker and view it


```python id="gCodbM66xNJO"
gme = yf.Ticker("GME")
```


Turn it into a df and plot? Sure!


```python colab={"base_uri": "https://localhost:8080/", "height": 228} id="hyp-jqjxxQs6" outputId="029b05b3-02ba-41a9-c3bd-4fdd6a1a909b"
hist = gme.history(period="5d").head()
hist
```

```python colab={"base_uri": "https://localhost:8080/", "height": 350} id="lgt-hrO7yEIg" outputId="373ce288-cfa2-432d-a642-f587e89e4c44"
# make pretty
BrBG = sns.color_palette('BrBG') # pre-existing palette
cpal = ['dodgerblue', '#2ecc71', '#bb64ed', '#ffd13b', 'xkcd:tangerine', '#fa62b7']
sns.set_style('whitegrid')

fig, ax = plt.subplots(figsize=(18, 5))
# Line graph
sns.lineplot(x='Date', y='High', data=hist, ci=None, ax=ax)
# Add a title
plt.title('GME stonks')
 
# Customize y-axis label
plt.ylabel('Highs')
plt.show()
```