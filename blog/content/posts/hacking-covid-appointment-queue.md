---
title: "Hacking the Covid Appointment Queue"
date: 2021-02-27T19:45:28Z
tags: ["just for fun", "chrome dev tools"]
---

{{<toc>}}

**TL;DR**: By examining the minified source code of the [Rite Aid Immunization Scheduler](https://www.riteaid.com/pharmacy/apt-scheduler) I was able to figure out a way to book vaccine appointments for my (eligible -- obviously) loved ones and family friends. In the end, my method successfully booked appointments for 8 individuals living in various parts of New Jersey.

## The Problem

A few close family members of mine have pre-existing conditions which make them eligible to get the COVID vaccine. I'm obviously concerned about their well being and have sought ways to snag them an appointment.

Enter [**Vaccine Finder**](https://vaccinefinder.org/search), a nifty site that aggregates locations near you that are administering vaccines _and_ happen to have vaccines in stock.

Perfect! This seemed to be the ideal solution. Except, whomp whomp, not really. For New Jersey at least, the research results takes the user to the respective landing pages of the vaccine providers - from my experience, these were mainly Rite Aid/CVS pharamacies:

![vaccine finder results](/dev/img/vaccinefinder.png)

The [CVS pharmacy vaccination portal](https://www.cvs.com/immunizations/covid-19-vaccine) was pretty disappointing - everything is always booked and there is much else you can really do beyond that.

![cvs results](/dev/img/cvs.png)

(PS: check out the CSV sidebar below for some commentary about the "feed" that is available here).

The [Rite Aid vaccination portal](https://www.riteaid.com/pharmacy/apt-scheduler) is a lot more interesting.

It starts us off with a handy form that checks to see if one qualifies for booking an appointment.

![rite aid](/dev/img/riteaid.png)

(PPS: check out sidebar#2 below for some commentary about the "rules engine" and determining if you qualify).

It's slick and doesn't even require a log in! So far, so good. Assuming you have a condition that qualifies you to book an appointment, you are led to the next screen / the beginning of your misery:

![rite aid screen](/dev/img/riteaidscreen1.png)

Ok great - let's pick a store and see where we end up.

![rite aid screen](/dev/img/riteaidscreen1_err1.png)

Whomp whomp, again!

A few issues:

* The list of stores generated are not stores with vaccines _available_...they're just stores that exist nearby.
* You have to **SELECT** each store, then click on **Next** to see if a slot may be available or not. More often than not, availability does not exist. So, as a "normal" user you have no choice but to click over and over again hoping for a hit.
* Now, assuming you've cleared this step and picked a store quickly enough, you get sent to the next "level" where you must choose from a dropdown _super quick_ for available time slots in the Morning, Afternoon or Evening. But! If someone else is on the same exact view and happens to pick the slot before you, you lose! There's no indication of this until _after_ you pick and then back you go to step 1. Do no pass Go. Do not collect $200.

Ok so anyways - at this point, this is the issue:

> The Rite Aid Immunization Scheduler is Good and Cool in that it exists (seriously!) but it is also Not Good and Unusable (TM) given that demand for the appointment slots are very, very high and the flow does not really account for this usecase.

So this begs the question: how do we fix this until a better experience is rolled out?

## Attempt 1: Find stores with Availability

My first attempt at trying to get around the UX frustrations was to just try and come up with a way to access the store availability data without having to click the damn buttons.

I figured that this data was being fetched on button click, so I peeked into the Network tab in Chrome's Dev tools and found calls similar to this (note the `storeNumber` at the end of the URL)

```bash
GET https://www.riteaid.com/services/ext/v2/vaccine/checkSlots?storeNumber=3697
```

which returned:

```javascript
{
  "Data": {
    "slots": {
      "1": false,
      "2": false
    }
  },
  "Status": "SUCCESS",
  "ErrCde": null,
  "ErrMsg": null,
  "ErrMsgDtl": null
}
```

I assumed (correctly, as it turned out) that if `.Data["slots"]["1"]` or `.Data["slots"]["2"]` were `true` then I'd be in business. So, all I had to do was put together a script that would hit the URL above with the storeNumber in question (there actually is an API call made to perform the geoquery search -- I include it in the script below).

I ended up writing a quick py script and running it in a [REPL](https://repl.it):

```python
import requests

def get_stores(zipcode = "XXXXX", radius = 10):
  url_base = "https://www.riteaid.com/services/ext/v2/stores/getStores"
  params = {
    "address": zipcode,
    "attrFilter": "PREF-112",
    "fetchMechanismVersion": "2",
    "radius": radius,
  }
  return requests.get(url_base, params=params)

def get_store(storenumber):
  url_base = "https://www.riteaid.com/services/ext/v2/vaccine/checkSlots"
  params = {
    "storeNumber": storenumber,
  }

  return requests.get(url_base, params=params)

def is_store_eligible(store):
  return sum([1 for slot in store['Data']['slots'].values() if slot]) > 0

for z in ["XXXXX", "YYYYY", "ZZZZZ"]:
  stores = get_stores(zipcode=z, radius=10).json()
  for item in stores['Data']['stores']:
    store = get_store(item['storeNumber']).json()
    if is_store_eligible(store):
      print(item['storeNumber'], z)
```

If all works well, the output looks something like:

```bash
12345 XXXXX
34531 YYYYY
```

where the first number is the store id and the second number is the zipcode. 

Now, this script worked great - I ran it continuously while sleeping for a few seconds in between invocations and it did reliably point me to stores where availability slots showed up!

But the problem was by the time I typed in the zip code in the search field, hit enter, scrolled down to the store number, selected the store and then clicked "next" (this figure is from above, reproduced to make my point):

![rite aid screen](/dev/img/riteaidscreen1_err1.png)

...either the slot would be gone **OR** I'd advance to the next screen where I'd have to play the game of clicking UI buttons some more and lose out on the appointment slot anyways. 🤦🤦🤦

Bummer. 

## Attempt 2: Running the API calls from within the browser.

Given this setback, my next thought was to try and run the API calls as I observed them in the Chrome Dev tools but with plain old javascript.

I wrote a quick POST request wrapper using the [fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) (GET was easy enough to do without having to write a func for it):

```javascript
async function postData(url = '', data = {}) {
    const formBody = [];
    for (let property in data) {
        const encodedKey = encodeURIComponent(property);
        const encodedValue = encodeURIComponent(data[property]);
        formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formBody
    });
    return response.json();
}
```

and then started replicating the API calls I was observing in the Network tab. Unfortunately, this didn't work very well.

In hindsight, I realize now the issue had to do priamrily with passing along fresh captcha tokens along with each call I was making (something that I missed initially while working on this but actually caught, fixed and implemented into my script later on). But at any rate, in the moment, I got stuck because _my_ POST requests were not working in the same was as the website's POST reuqests.

Unsure of how to go on, I did what appeared to be my one remaining option: I opened up the **Sources** tab in dev tools, prettified the javascript code and started reading.

## Attempt 3: Grokking, then directly calling, the source code

Reading the application's underlying JS code sucked because the source code was minified! (And therefore to some extent obfuscated)

![obfuscated](/dev/img/obfuscated_code.png)

Luckily, uncompressing it is easy (Chrome dev tools has a handy feature that prettifies the js code). Post prettification, we end up with:

![prettified](/dev/img/prettified.png)

This makes the code easier to read...but not by much.

I started making progress though by using the Network tab's stack trace feature (so handy!)

![network](/dev/img/network.png)

Each network call emitted by the browser displays a full trace of the code that was called to invoke the call itself. Given that user actions (such as clicking the "next" button) led to various network calls, I realized I could use the stack traces to find the areas of the javascript source responsible for emitting the calls. Then, I hoped, I could find some context as to why my POST requests were 400-ing when made directly from the console.

I picked the `fetchSlotDetails` line because it was a word that I understood in context of the application flow (ie: the function sounded like it had something to do with finding valid appointment slots). Clicking into it, I ended up here:

![source](/dev/img/source.png)

My biggest takeaway from this code snippet was on line **45916** (lol) -- **fetchSlotDetails** seemed to be a plain old property of a js object! (Or maybe part of the **prototype** object).

Cool. 

Maybe this is significant? Honestly, at this point I was mainly just exploring and trying to figure out the flow of the code + entry points to better grok how this thing works. I scrolled all the way up to find the object definition and stubmbled on this gem:

![global](/dev/img/global.png)

The key takeway (for me at least) was this:

```javascript
// ...
)(window, window.jQuery);
(function(c, a) {
// ...
    c.AddComponent("covidScheduler", {
        init: function(d) {
```

Based on the first two lines, it seemed strongly likely to me that `c` was actually just the **global** window object! If true, then `c.AddComponent` was simply the same as:

```javascript
window.AddComponent
```

meaning **AddComponent** (and as I later validated), **GetComponent** were **PART OF THE GLOBAL SCOPE**.

OMG!!

This was great news for me because **fetchSlotDetails** and in fact all the network call wrappers and DOM wrappers of this entire application were directly accesible via the Dev Tools console! Check it:

![console](/dev/img/console.png)

This was probably unintended by the original developers but it sure did make my life a hell of a lot easier moving forward. Because _most_ of the methods that powered this application were bound directly to the global namespace, it was pretty trivial to call the methods on these components with various `this` vars passed along using [bind](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this#the_bind_method) to them as needed for my usecase. I did still have to resort to a few fun hacks/tricks (like monkey patching certain methods in between steps and overwriting [**sessionStorage** tokens](https://stormpath.com/blog/where-to-store-your-jwts-cookies-vs-html5-web-storage#:~:text=JWT%20sessionStorage%20and%20localStorage%20Security,site%20scripting%20(XSS)%20attacks.) (fun fact: sessionStorage is always globally accessible!)) to circumvent cases where variables only accessible in the scope of the closure (but initially loaded from session storage if available)

By inspecting these methods and then eventually calling them, I was able to piece together the steps necessary to walk through the 7 (seven!!) step process of securing an appointment...programmatically! Using my technique, I was able to successfully book appointments for three family members + 4 family friends with pre-existing conditions. 

## Closing Thoughts

Some things never change.

Back in my javascript-ing days, we obsessed over writing IIFEs (Immediately Invoked Function expressions) precisely to prevent functionality like I discovered on this rite-aid site. That being said, I am a bit glad that the source code was so tightly bound to the global scope as it made my job of trying to procure appointment slots for my family members in need a hell of a lot easier.

I'm trying to not think too hard about the ethics of all this but I do hope that in the near future rite-aid/other vaccine appointment making sites improve their UX and client-side functionality to better reflect our current reality. 

## UPDATE 03/14/2021

Some folks have pointed out to me that the actual script/code is not available here. 

This is by design! 

Having reflected further about the implications of making my implementation public, I've come to the conclusion that it will perhaps do more harm than good. The major purpose of this write up was really to chronicle my problem solving approach and less significantly, showcase the awesome utility of the Chrome Dev Tools. 

I really wish there was a better way to get a hold of appointment slots - but opening up a side channel to circumvent a bad UX flow will only lead to further detrimental effects (greater strain on the Rite Aid Immunization Scheduler's APIs, folks charging to run the tool for the not-so-tech-savvy and/or people who are not eligible signing up just because they can). That's the last thing we need right now. 

I am however very much down to brainstorm / build something similar in principle to TurboVax. I highly admire the tool and am glad it exists but it is disappointing that the code is not available for forking / re-using. If anyone is down to collaborate, please get in touch!

### Video Walkthrough
Please find a video walkthrough of the extension working here:

{{< imgur id="4EOIEmY" >}}

_In this particular walkthrough, the script actually does find an appointment slot however due to a small bug in validating phone numbers the actual confirmation fails (thank god! as this was just an example and not meant to be "real")_

^ For fun, let's expound on what the phone number validation was about.

For whatever reason, the phone number that is input into the system by the user as part of the **contact info** stage is stored as: **(XXX) XXX-XXXX**. However, the appointment confirmation API endpoint raises a validation exception when it sees this, returning:

```javascript
{
  "Data": null,
  "Status": "ERROR",
  "ErrCde": "RA0001",
  "ErrMsg": "There was an error validating your entries. Please check and try again.",
  "ErrMsgDtl": {
    "patientDetails.phone": [
      "Please enter a ten digit phone number"
    ]
  }
}
```

My best guess is that the issue is on my end, I am likely failing to call a validation function on the phone number field. At any rate, the fix is easy - just updated that field and remove **(**, **)**, **-** characters. My initial approach was not very javascript-y (and I will not even share here).

A contact suggested the following:

```javascript
[...phone_str].filter(Number).join('')
```

This is super clever! `Number(N)` will return `NaN` if `N` is not `0-9`. `NaN` is falsey af so it gets filtered out of the final return value.

The _bug_ here though is that `Number(N)` where `N === 0` is **also** falsey, meaning any numberstrings that contain `0` **also** will be filtered out.

The workaround - while uglier - is as follows:

```javascript
[...phone_str].filter(n => !isNaN(Number(n))).join('')
```

This now explicitly filters out a possible char if it is indeed `NaN` and `NaN` **only**.

## Sidebar 1: CVS Feed

Interestingly, the dialog is generated with a single API call that looks like this:

```python
import requests

def get_cvs():
  url_base = "https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.NJ.json?vaccineinfo"
  headers = {
    "referer": "https://www.cvs.com/immunizations/covid-19-vaccine",
    # without this dude, it fails!
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
  }
  return requests.get(url_base, headers=headers)
```

The results are in pretty JSON format at least:

```javascript
{
  "responsePayloadData": {
    "currentTime": "2021-02-27T23:28:06.837",
    "data": {
      "NJ": [
        {
          "city": "BRIGANTINE",
          "state": "NJ",
          "status": "Fully Booked"
        },
        // ...
        {
          "city": "WILLINGBORO",
          "state": "NJ",
          "status": "Fully Booked"
        }
      ]
    },
    "isBookingCompleted": true
  },
  "responseMetaData": {
    "statusDesc": "Success",
    "conversationId": "Id-4c30be3e0bd44ed5af5505b861381edd",
    "refId": "Id-613a3b6078b5418650d72c1f",
    "operation": "getInventorybyCity",
    "version": "1.0.0",
    "statusCode": "0000"
  }
}
```

At any rate - useful for potentially _finding_ a store with availability (and maybe an alerting service?).

## Sidebar 2: Rite Aid Rules Engine

Determining eligibility (via the Rite Aid qualification page) was a bit murkey. To determine if various family members were eligible, I initially (painstakingly) filled out the form inputs plugging in various ailments to try and find the winning combination. (The reason a "winning combo" is needed even is that the choices presented do not clearly match the list of criteria presented on government websites. Plus there seems to be conditions presented in the UI that _may_ be valid in the future but aren't currently. In short, this is another example of a not-so-fun UX)

One particular family member of mine has a condition that according to a pharmacist we consulted in meatspace (like, IRL) was certainly valid but we were having trouble picking the matching condition from the UI dropdown.

To solve this, I looked under the hood on the [covid qualifier](https://www.riteaid.com/pharmacy/covid-qualifier) page and noted the following API call:

```bash
GET https://www.riteaid.com/content/dam/riteaid-web/covid-19/rule-engine.json
```

which returned something like:

```javascript
{
  "conditions": {
    "any": [
      {
        "all": [
          {
            "fact": "stateCode",
            "operator": "equal",
            "value": "NY"
          },
          {
            "fact": "age",
            "operator": "greaterThanInclusive",
            "value": "65"
          }
        ]
      },
      // ...
  }
}
```

Particularly, in NJ:

```javascript
{
  // ...
  {
    "all": [
      {
        "fact": "stateCode",
        "operator": "equal",
        "value": "NJ"
      },
      {
        "fact": "age",
        "operator": "greaterThanInclusive",
        "value": "18"
      },
      {
        "fact": "medicalConditionCode",
        "operator": "in",
        "value": [
          "Obesity",
          "Diabetes",
          "Heart Condition",
          "Sickle Cell Anemia",
          "Smoking",
          "Organ transplant",
          "Kidney Disease",
          "COPD",
          "Cancer",
          "Down Syndrome",
          "Pregnancy",
          "Weakened Immune System"
        ]
      }
    ]
  }
  // ...
}
```

which answered the question of "which option most accurately describes the condition and is also valid" pretty quickly.

(It also appears that booking appointments through rite aid is only valid in a handful of states and these states have various degrees of rules and regulations governing who can be vaccinated or not). 

The full JSON body for this API call as of 03/08/2021 is available [here](https://pastebin.com/Pq7sLWyN)