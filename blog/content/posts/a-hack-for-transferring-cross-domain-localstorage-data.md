---
title: "A Hack for Transferring Cross Domain Localstorage Data"
date: 2022-02-02T08:24:42Z
tags: ["javascript", "just for fun", "chrome dev tools"]
---

{{<toc>}}

**BLUF**

🎉 Wordle [has been purchased by the NYTimes!](https://www.nytco.com/press/wordle-new-york-times-games/) 

🐱‍💻 I wanted to cache the game in its current state, so I downloaded source and uploaded to my own server: [Wordle Classic](https://mottaquikarim.github.io/wordle_classic/)

🤔 But! I wanted to transfer my streaks data to my new hosted app

💡 Thanks to `javascript:` and a small code addition to Wordle Classic, I was able to transfer my streaks without having to open up Chrome's Dev Console

I expound further in this post.

## Background.

With the purchase of the Wordle game by the Times, I expect a whole slew of new features and code changes as the experience is integrated with the Times ecosystem.

In order to maintain functionality of my [hacks]({{< ref "/posts/reverse-engineering-wordle" >}}) ([Wordle Time Machine](https://mottaquikarim.github.io/wordle_timemachine/v2.html?d=2021-06-19) and [Wordle with Friends](https://mottaquikarim.github.io/wordle_with_friends/)), I decided to `File > Save Page As` on the original https://www.powerlanguage.co.uk/wordle/ app (in Chrome on my desktop) and host it myself on Github Pages.

This way, my hacks would remain functional even after the NYTimes devs make changes to the game in the future.

But having completed this work, it occurred to me that it _would_ be neat to try and consider transferring the statistics data stored in the original Wordle app in my the "Wordle Classic" copy.

## Requirements.

Now, the naive approach here would be to just open up dev console in Chrome (on the original Wordle app) and do the following:

```javascript
const stats = window.localStorage.getItem("statistics")
```

Then, we can copy/pasta the output in to the dev console of the "Wordle Classic" copy:

```javascript
window.localStorage.setItem("statistics", "<JSON OUTPUT FROM ABOVE>")
```

🎂

The key issue with this approach is that for mobile usecases (which is how I've been playing the game anyways), this is more or less not possible. (Ok, I _guess_ we could connect the phone to safari dev tools and mess around there, but I wanted to avoid this).

So as a fun thought experiment I decided to consider:

> Is it possible at all to "transfer" localstorage data from one domain to another _without_ having to resort to dev tools?

In particular, I wanted to:

* avoid having to open up console at all
* achieve the transfer ideally by mainly avoiding having to install stuff (like extensions and whatnot)

## Experimentation.

I have to say, I got lucky again. I played around with the basic initial ideas around iframes and window.postMessage, etc. Ofc (and for good reason!) most cross site shenanigans with js were forbidden by the browser.

Ok, cool. So then, I thought: maybe using the `javascript:` prefix in the URL bar could help me figure out next steps?

I started off with a naive `javascript:alert()`. 

As expected, this created an alert modal _but did not reload the page_. This was surprising (to me at least) but also the **key insight** I needed for my technique.

If `javascript:<some arbitrary code here>` runs within the context of the loaded page, surely this means I would have access to localStorage when I run something like: 

```javscript
javascript:console.log(window.localStorage.getItem("statistics"))
```
...right? As it turns out -- right indeed!

I was able to confirm that running the code snippet above _would_ in fact provide access to the localStorage data accessible to the www.powerlanguage.co.uk domain.

![screenshot](/dev/img/example-screenshot-javascript-alert.png)

**!!**

Sweet -- we are halfway there.

## Output Artifact.

Now, the only work left was to actually send this data over to the "Wordle Classic" copy. This turned out to be pretty easy -- I modified my `javascript:` snippet above as follows:

```javascript
javascript:window.location.href = 
	"https://mottaquikarim.github.io/wordle_classic/?statistics=" 
	+ encodeURIComponent(localStorage.getItem("statistics"))
```
(Note: formatted weirdly because I couldn't figure out how to enable word-wrapping in my Hugo syntax highlighter 😅)

The new snippet _reads_ the contents of the original Wordle's `statistics` localStorage item and navigates us to the "Wordle Classic" copy, "saving" the state as a query param. On the "Wordle Classic" side of things, I added the following script tag:

```html
<script>
  if (location.search !== "") {
    const [key,val] = location.search.slice(1).split("=")
    if (key === "statistics") {
      localStorage.setItem(key, decodeURIComponent(val))
      alert(`successfully updated ${key}`)
    }
  }
</script>
```

And donezo! I was able to successfully transfer my "statistics" from the https://www.powerlanguage.co.uk domain to my https://mottaquikarim.github.io domain. Here's the flow in screenshots:

### 1. Load "Wordle Classic" copy domain, demonstrating no stats.

![screenshot](/dev/img/step_1_show_statistics.png)

Note that the stats dialog shows **0s only**

### 2. Paste the `javascript:` snippet.

![screenshot](/dev/img/step_2_show_javascript_hack.png)

Note that the localStorage view has a `statistics` item (which is incidentally missing from (1) where we are looking at the https://mottaquikarim.github.io domain)

### 3. Hit "Enter", which will redirect us to the "Wordle Classic" domain

![screenshot](/dev/img/step_3_show_alert_and_page_reload.png)

Note the URL change and as per the javascript snippet above, we see an alert indicating that the `setItem` method ran successfully.

### 4. Stats dialog in "Wordle Classic" reflects transferred state 🎉 

![screenshot](/dev/img/step_4_show_transferred_game_state.png)

Note the localStorage view has a `statistics` item, it should be the same as the item in step (2).

Ta da!

## **Aside:** Considerations for Mobile.

Going back to the original premise -- I wanted to migrate my stats on mobile,specifically.

On chrome moblie, this was easy enough. I ran the `javascript:` snippet and it worked as expected (heads up: pasting the snippet to the URL bar removes the `javascript:` prefix, you'll have to add that back in otherwise the page redirects to a google search results view).

For safari though, I ran into this:

<img style="width: 50%; height: auto; margin: 0 auto;" src="/dev/img/step_2_mobile.JPG">

Womp womp.

To solve this problem, I took advantage of Safari's bookmarking feature. To begin, I created a simple bookmark, calling it `JS RUNNER`.

<img style="width: 50%; height: auto; margin: 0 auto;" src="/dev/img/step_3_mobile.JPG">

Then, I navigated to this bookmark and edited it.
<img style="width: 48%; height: auto; margin: 0 auto;" src="/dev/img/step_4_mobile.JPG">
<img style="width: 48%; height: auto; margin: 0 auto;" src="/dev/img/step_6_mobile.JPG">

In the edit view, I updated the bookmark URL with my `javascript:` snippet
<img style="width: 50%; height: auto; margin: 0 auto;" src="/dev/img/step_7_mobile.JPG">

After saving this change, I was able to run the `javascript:` code on safari as well, successfully transferring my stats over from the original app to my copy 🎉

<img style="width: 48%; height: auto; margin: 0 auto;" src="/dev/img/step_8_mobile.JPG">
<img style="width: 48%; height: auto; margin: 0 auto;" src="/dev/img/step_9_mobile.JPG">


## **Aside 2:** Transferring from Homescreen App.

One big drawback of my technique is afaik, there is no way to actually transfer this data if you've saved the game as part of your "homescreen". Apple seems to discourage this behavior anyways (the act of adding to Homescreen is buried within the "share" modal under bookmarks, add to favorites, etc)

Importantly, it appears that once you _do_ add to homescreen, iOS minimally spawns a new instance of LocalStorage that is distinct from the Safari instance. Because of this, it does appear to be impossible (at least from my understanding today) to transfer localstorage data from the homescreen without a code change to the original app itself.
