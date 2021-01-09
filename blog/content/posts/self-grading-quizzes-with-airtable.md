---
title: "Self Grading Quizzes With Airtable"
date: 2020-03-16T06:31:03Z
---

{{<toc>}}

This semester, I am teaching a course at Baruch University on Big Data Technologies. 

I resolved to administer a small quiz at the start of class to get a feel for how the class is doing overall in terms of comprehension of key materials. 

However, grading quizzes - especially at such a recurring cadence - will definitely be time consuming, even for a small class of say 15 people (my class has 47 students).

## Requirements

I wanted a system that would:

* Make it easy to create multi-question, *multiple choice* quizzes
* Make grading automatic
* Share individual grades automatically to students via email or some other manner
* Require minimal infrastructure and coding (ie: maybe a lambda function somewhere? ideally no code at all)

## TL;DR:

Using Airtable, there is a way to create multi-choice, self grading quizzes. I've created a set up that you can **find and replicate** here for your class's usecase:

* **[AIRTABLE BASE](https://airtable.com/shriZOQyCUScx3zCc)**
* **[QUIZ FORM](https://airtable.com/shr2hBhcm33iRV5jK)**

## Airtable based solution

Leveraging [Airtable](https://airtable.com/), I have come up with an approach that generally has worked for me thus far.

The key to this solution is to create a table that represents a quiz. Each row will include student name, email, created time, "questions", "checks" and a "grade".

The last two types of rows: "checks" and "grade" are both formula types.

Here's a screenshot:

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/0i10457qg9scp4dj756k.png)

The columns "1"..."5" represent questions and each are formatted to be "single select" types with 4 predefined selections.

### Formula Columns

To assert correctness, each "question" column has an accompanying "solution" column that asserts for correctness. 

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/8nopme8drybkye5vibnq.png)

As seen here, "Solution 1" is a formula `{1} = "C"` which is ensuring that the selection for column "1", if "C" is correct. This can be repeated with as many questions as necessary.

To compute grade, we simply find the average:

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/hynfw25jjyci1swotdy5.png)

The "code" for this formula:

```
({Solution 1} + {Solution 2} + {Solution 3} + {Solution 4} + {Solution 5})/5
```

Where the label inside each `{}` corresponds to the column name `Solution 1`...`Solution 5`.

That's it! That's the internals of the quiz. Now, per student who completes this quiz, a corresponding row will be created with a "creation time" (for future filtering if needed) and "checks" for each question submitted and a "grade" that computes average.

If needed that "grade" column can also be updated to weight individual questions differently as well. 👍

## Creating the quiz

For the "frontend", we need a form and the actual quiz questions! Airtable supports a concept of a "view" where it is possible to create a "form" that will populate the rows in the table.

Here's an example:

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/mbazzoh4y7bdcja75epp.png)

Essentially, each column from the table can be added (or removed!) as an input field. Also, it is possible to make certain fields required and to add arbitrary text (in my quiz, I even had a few coding questions). 

Additionally, this form is by default not shared:

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/aqczrffb7hkpr7q3yvfk.png)

but can be toggled to shareable via a private link at any time (so it is easy to "publish" and "unpublish" a quiz)

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/9mwb6oin87i21ol8jcxp.png)

## The Verdict

For a non-custom coded system, this works "well enough"; looking back to the requirements:

* ✅Make it easy to create multi-question, *multiple choice* quizzes
* ✅Make grading automatic
* ❌Share individual grades automatically to students via email or some other manner
* ✅Require minimal infrastructure and coding (ie: maybe a lambda function somewhere? ideally no code at all)

Some happy additional features:

* ✅Tables and views are easy to duplicate, meaning multiple quizzes can be easily supported
* ✅Publishing/unpublishing forms are actually super helpful
* ✅At the bottom of each column, airtable calculates some metrics such as class average, etc which can be read in real time as students complete quiz

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/f7eu9t5borc7108f243x.png)

There are some definite drawbacks here as well:

* ❌lack of fine tuned controls in terms of formatting the questions 
* ❌adding more than 4-5 questions becomes somewhat unreasonable due to the additional column that much be added
* ❌**RATE LIMITS**! If more that ~50 people open the form all at once (or refresh a lot), I've seen cases where the form is "disabled momentarily" (a few hours)
* ❌no automatic support for emailing grades to students


For that last item - I have come up with a (similarly codeless) solution! If there is sufficient interest (please let me know in the comments!) I will follow up this post with a tutorial for how I achieved near-real time email notification to students based on quiz submission 👍