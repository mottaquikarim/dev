---
title: "Generate Lambda Layer Artifacts w/Docker"
date: 2020-12-22T16:41:25Z
tags: ["serverless", "docker"]
---

{{<toc>}}
This post (and accompanying code) was inspired by [this](https://towardsdatascience.com/how-to-install-python-packages-for-aws-lambda-layer-74e193c76a91) tutorial and a need to easily generate lambda layer artifacts for a grad course I teach at Baruch University.

**[Github](https://github.com/mottaquikarim/pkglambdalayer)**

**TL;DR**: Generate a lambda layer artifact for python using this:

```bash
➜  cat >> requirements.txt
requests==2.24.0
➜  docker run -v $PWD:/data mottaquikarim/pkglambdalayer:latest
```

On completion, expect the following:
```bash
➜  ls -ahl
total 1792
drwxr-xr-x   5 tkarim  staff   160B Dec 21 08:36 .
drwxr-xr-x  23 tkarim  staff   736B Dec 21 08:31 ..
drwxr-xr-x  13 tkarim  staff   416B Dec 21 08:36 pkg
-rw-r--r--   1 tkarim  staff   879K Dec 21 08:36 pkg.zip
-rw-r--r--   1 tkarim  staff    17B Dec 21 08:36 requirements.txt
```

**pkg.zip** can be uploaded into your own Lambda Layer using the AWS Console 👍👍

## **The Backstory**

I teach a course at Baruch University where I introduce folks to various AWS technologies in the context of "Big Data" processing.

So of course, Lambdas are a topic I cover. In order to keep the course load from being _too_ technical, I try to lean hard on AWS console whenever possible vs going too deeply into the infra-as-code  approach.

As such, most of our explorations in Lambda-land are done through the AWS Lambda UI.

## **The Problem**

> You can't _actually_ load in dependencies into the AWS Lambda UI!

While I totally understand perhaps _why_ this is so, it definitely throws a bit of a curveball in my class as I want folks to write useful lambda funcs but without having to delve too deeply into the packaging process.

## **Lambda Layers and Docker**

I found Lambda Layers to be an acceptable compromise - last semester I just generated a single artifact similar to above which I shared via Google Drive and had folks go through the motions of uploading and leveraging the dependencies. 

This process seemed to be a good candidate for automation so as a first step, I packaged it into a docker image. Folks in my class have basic working knowledge of pulling / running docker images so next semester I hope to leverage this without having to pre-gen a single build artifact on my own.

Plus, this will empower folks in class to perhaps do more with lambda if it is easier to create various combinations of dependencies in thier layers.

I figured maybe this would be interesting/useful to others so I wrapped into a [Github repo](https://github.com/mottaquikarim/pkglambdalayer) and am publishing/sharing. 