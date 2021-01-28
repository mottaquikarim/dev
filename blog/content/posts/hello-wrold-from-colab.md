
---
title: "Hello, Wrold from Colab"
date: 2021-01-28T04:01:51Z
tags: ["meta", "python", "just for fun"]
---

{{<toc>}}

> Hello, Wrold, from Google Colab!!

_[Here](https://colab.research.google.com/drive/1K3xuq9Ipy_iUIX_NmH5j-CP4foIVklhA?usp=sharing) is the colab doc for those following along at home)_

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


