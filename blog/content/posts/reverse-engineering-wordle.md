---
title: "Reverse Engineering Wordle"
date: 2022-01-24T12:24:16Z
tags: ["featured", "javascript", "just for fun", "chrome dev tools"]
---

{{<toc>}}

**BLUF**

👀 I looked into + grokked [Wordle's](https://www.powerlanguage.co.uk/wordle/) javascript source code

🐱💻 Then, I managed to come up with a workaround that enables loading **any** _previous_ word of the day puzzle

🙌 I wrote a little tool to load the original Wordle site but with my "hack" injected allowing anyone to play any past word of the day puzzle. I call it: **[Wordle Time Machine](https://mottaquikarim.github.io/wordle_timemachine/)** 🎉

## Background.

Ok let's get a few things out of the way first:

* Yes, all the words (past and future) are available in the source (nothing too fancy here)
* No, the purpose of this post is not to expose any of the upcoming solutions. But! Be warned fam, some of the techniques described here _can_ be used to cheat (but where's the fun in that, right?)

I really like this game and primarily found myself wanting to play more. In particular, I wanted to play  previous words of the day since I only discovered Wordle fairly recently.

## Requirements.

Here are the requirements I set for myself:

* enable playing past words
* don't actually recreate any parts of the game itself (eg: don't copy/paste the source code and modify - a viable option but again, no fun in that)
* no chrome extension type stuff (I want to play on mobile)

## Aside.

Btdubs fam -- did you know that the game state is saved in [Local Storage](https://developer.mozilla.org/en-US/docs/Web/API/Storage)?

If we run the following in Chrome's "console" in the Web Dev Tools:

```javascript
localStorage.getItem("gameState")
```

we observe:

```json
{
  "boardState": [
    "",
    "",
    "",
    "",
    "",
    ""
  ],
  "evaluations": [
    null,
    null,
    null,
    null,
    null,
    null
  ],
  "rowIndex": 0,
  "solution": "😜",
  "gameStatus": "IN_PROGRESS",
  "lastPlayedTs": null,
  "lastCompletedTs": null,
  "restoringFromLocalStorage": null,
  "hardMode": false
}
```

Note the `solution` field -- this will store the answer for the word of the day. (This has nothing to do with my solution).

The reason I bring this up is because if we really _wanted_, we _could_ build a version of my Wordle tool that allows folks to inject their own "word of the day" to challenge friends with custom words. The only requirement would be the word must be a part of the "acceptable words" list bundled into Wordle's src.

## Experimentation.

> NOTE: all of this exploration was done on script version [main.e65ce0a5.js](https://www.powerlanguage.co.uk/wordle/main.e65ce0a5.js). My guess is if there are code changes, that hash value will likely update.

Anyways, I digress. I started my experimentation by looking at the Network tab as I input my guesses into the app on Chrome.

I noted that there were no network requests being sent which made me realize the solution must be bundled into the HTML/js code.

Looking into the js source (which was minified -- thankfully CHrome supports prettification as part of dev tools 🙏), I stumbled on to the famous list of solutions:

```javascript
 var La = [/* SOLUTIONS */]
     , Ta = [/* ACCEPTABLE WORDS */]
```

Searching the codebase for `La` led to interesting results:

```javascript
var Ha = new Date(2021,5,19,0,0,0,0);
function Na(e, a) {
    var s = new Date(e)
      , t = new Date(a).setHours(0, 0, 0, 0) - s.setHours(0, 0, 0, 0);
    return Math.round(t / 864e5)
}
function Da(e) {
    var a, s = Ga(e);
    return a = s % La.length,
    La[a]
}
function Ga(e) {
    return Na(Ha, e)
}
```

In particular, function `Da` appears to return a word from `La`. Before going down further, let's see how `Da` is used (...by, you guessed it: searching the codebase for `Da` invocations!):

```javascript
e.today = new Date; // <- important!
var o = za();
return e.lastPlayedTs = o.lastPlayedTs,
!e.lastPlayedTs || Na(new Date(e.lastPlayedTs), e.today) >= 1 ? (e.boardState = new Array(6).fill(""),
e.evaluations = new Array(6).fill(null),
e.solution = Da(e.today), // <- important!
```

Ok so let's summarize what is going on here:

* `Da` returns `La[a]`; presumably `a` is an index and `La[a]` therefore is the word of the day
* `e.solution` is storing the return value of `Da`, meaning this is likely going to store the actual answer of the day
* `e.today` is just `new Date` (look at the first line above), eg: today's date

There are a few other interesting bits here but this is all we really need to craft our solution.

First thing I did was ensure that `Da`/`e.solution` were not available globally. (They are not -- interestingly, `window.wordle` is exposed. I went down this path a bit but I didn't make much progress because the game system uses `customElements` ([sauce](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements)))

My next approach (and bear with me here) was to [monkeypatch](https://dev.to/napoleon039/monkey-patching-what-is-it-and-should-you-be-using-it-50db) the `Date` class itself, given that 

* `e.today` appears to be the entry point to this functionality
* there's no other way to access `e.solution` (without like, recreating the entire `game-app` which I wasn't prepared to do)
* `Date` itself is available globally so this is a viable entrypoint

Here's what my solution looked like:

```javascript
// Don't try this at home kids, this hack is dirty
// basically overwrite Date object to trick the src code to 
// pick the appropriate solution for that date
(function() {
    const today = new Date()
    var OriginalDate = Date
    Date = OriginalDate;
    Date.prototype = OriginalDate.prototype;
    Date = function() { 
        if (arguments.length == 1 
                && window.overrideDate == true 
                && arguments[0].getFullYear
                && arguments[0].getMonth
                && arguments[0].getDate
                && arguments[0].getFullYear() == today.getFullYear() 
                && arguments[0].getMonth() == today.getMonth()
                && arguments[0].getDate() == today.getDate()) {
            return new OriginalDate(year,month,date,0,0,0,0)
        }
        else return new OriginalDate(...arguments)
    };
    // lol, `Date.now` is not part of the prototype
    for (let prop of Object.getOwnPropertyNames(OriginalDate)) {
        Date[prop] = OriginalDate[prop]
    }
    console.log(Date.now, OriginalDate["now"])
    console.log(Object.getOwnPropertyNames(Date), Object.getOwnPropertyNames(OriginalDate))
})();
window.overrideDate = true;
```

A few key notes:

* `Date` is used everywhere in the codebase
* I noted that (luckily?) `Da`'s usage of `Date` is actually a date object (remember: `e.today = new Date`); all other Date uses are either in timestamps or the longer form year/month/day instantiation
* ^ this is **mad lucky**! I took advantage of this luck to craft a new Date constructor that returns `new OriginalDate(year, month...)` where `year`, `month`, etc are inputs to a function that inits all of this madness

This approeach worked! 🎉

## Output Artifact.

Next challenge: how the hell do I run this before the game logic is exectuted? (In other words: the game code execs immediately, monkey patching the Date afterwards does nothing because game has already "started" and state is set).

I went down multiple paths for this one, ultimately to no avail. (Tried exotic stuff like `newWin = window.open("about:blank")` and then wrote directly to `newWin` with `document.write(...)` and whatnot).

Eventually, I settled on a particularly egreious solution: fetch the HTML content of the original app, walk the nodes and load all the scripts _after_ running my Date hack.

WARNING: this code is pretty cringe -- pls don't judge:

```javascript
// everything else is purely in the service of loading the src code
fetch("https://x6ca288in5.execute-api.us-east-1.amazonaws.com/default/get_wordle")
    .then(resp => resp.text()).then(html => {
    // Convert the HTML string into a document object
    var parser = new DOMParser();
    var doc = parser.parseFromString(html, 'text/html');
    console.log(html)

    document.querySelector('head').innerHTML = doc.head.innerHTML;
    document.querySelector('body').innerHTML = doc.body.innerHTML;
    loaders = []
    document.querySelectorAll("body > script").forEach(scr => {
        // very gross, inserting HTML does not actually run the scripts, so we resort to dirty tricks
        if (scr.getAttribute('src') && scr.getAttribute('src').indexOf('main') != -1) {
            console.log(scr.getAttribute('src').indexOf('www.powerlanguage.co.uk/wordle/') == -1)
            console.log(scr.getAttribute('src'))
            newScr = document.createElement('script')
            newScr.type  = "text/javascript";
            newScr.src = scr.getAttribute('src')
            if (scr.getAttribute('src').indexOf('www.powerlanguage.co.uk/wordle/') == -1) {
                loaders.push("https://x6ca288in5.execute-api.us-east-1.amazonaws.com/default/get_wordle?script=" + scr.getAttribute('src'))
                console.log(loaders)
                return
            }
            document.body.appendChild(newScr);
            return;
        }
        newScr = document.createElement('script')
        newScr.text = scr.text
        document.body.appendChild(newScr);
    })
    return loaders
})
.then(urls => {
    console.log('here', loaders)
    urls.forEach(url => {
        console.log(url)
        fetch(url)
        .then(resp => resp.text())
        .then(js => {
            console.log(js)
            newScr = document.createElement('script')
            newScr.type  = "text/javascript";
            newScr.text = js
            document.body.appendChild(newScr);
        })
    })
})
.catch(console.log)
```

The TL;DR here is that we insert the HTML head/body tags from Wordle's source, then walk the script tags. We do a hacky thing to detect for `main.*.js` type script srcs and then load them invidually (because for whatever reason, loading a script tag as part of `*.innerHTML += <code>` doesn't actually exectute the script (so we need to create a _new_ script element to run the code).

Oh and to make everything even more fun, `fetch`-ing the actual HTML/js content does not work (for good reason!). So I put together a quick proxy lambda that just `requests.get()`s the sources (this is so lame, tho).

Ok so that finally did work (but like, everything sucks just a little bit 😭) and I was ready for the easy part: making the dates selectable.

I chose to run with a simple datepicker (thank god for `input type="date"` 🙏) and called it a day. I wrapped the thing into GH pages and fired it up on my phone. It worked! I ended up playing ~5 games from June 19 2021 onwards _and_ decided to play Jan 24th's word about 1/2 an hour before midnight (eg: it wasn't "released" yet).

All in all, I'm happy with how this turned out (tho am still really surprised the hack worked!) and I hope others get to enjoy this as well before the js src inevitably changes.

On the bright side, I did download the state of the Wordle's src as it stands today so if things do change in the future I can probably still support this functionality by hosting the current src indefinitely.

Happy Wordle-ing! 🎉

## Update(s).

I've been tinkering with the game source code for the past week or so and have learned a lot more about how the app works in general. I've applied my learned to two new variants:

* [Wordle Time Machine v2](https://mottaquikarim.github.io/wordle_timemachine/v2.html?d=2021-06-19)
* [Wordle with Friends](https://mottaquikarim.github.io/wordle_with_friends/)

Enjoy!
