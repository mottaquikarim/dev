---
title: "Hacking the Covid Appointment Queue"
date: 2021-02-27T19:45:28Z
---

{{<toc>}}

> **TL;DR**: Alright ya got me - this story is not about "hacking". Instead, it's really just about some...optimizations I made to the [Rite Aid vaccinate appointment signup](https://www.riteaid.com/pharmacy/apt-scheduler) UX flow using javascript, Chrome devtools and approximately one sleepless night.

Buckle up fam, this will be a deep dive.

## The Problem

A few dear family members of mine have pre-existing conditions which make them eligible to get the COVID vaccine. I'm obviously concerned about their well being and have sought ways to snag them an appointment.

Enter [**Vaccine Finder**](https://vaccinefinder.org/search), a nifty site that aggregates locations near you that are administering vaccines _and_ happen to have vaccines in stock.

Perfect! This seemed to be the ideal solution. Except, whomp whomp, not really. For New Jersey at least, the research results takes the user to the respective landing pages of the vaccine providers - from my experience, these were mainly Rite Aid/CVS pharamacies:

![vaccine finder results](/dev/img/vaccinefinder.png)

The [CVS pharmacy vaccination portal](https://www.cvs.com/immunizations/covid-19-vaccine) was pretty disappointing - everything is always booked and there is much else you can really do beyond that.

![cvs results](/dev/img/cvs.png)

(PS: check out the CSV sidebar below for some commentary about the "feed" that is available here).

The [Rite Aid vaccination portal](https://www.riteaid.com/pharmacy/apt-scheduler) is a lot more interesting.

It starts us off with a handy form that checks to see if one qualifies for booking an appointment.

![rite aid](/dev/img/riteaid.png)

It's slick and doesn't even require a log in! So far, so good. Assuming you have a condition that qualifies you to book an appointment, you are lead to the next screen / the beginning of your misery:

![rite aid screen](/dev/img/riteaidscreen1.png)

Ok great - let's pick a store and see where we end up.

![rite aid screen](/dev/img/riteaidscreen1_err1.png)

Whomp whomp.

A few issues:

* The list of stores generated are not stores with vaccines _available_...they're just stores that exist nearby.
* You have to **SELECT** each store, then click on **Next** to see if a slot may be available or not. More often than not, availability does not exist. So, as a "normal" user you have no choice but to click over and over again hoping for a hit.
* The list displaying the store options are in a fixed height window with an overflow. **WTF!** This means as you are picking stores from top to bottom, stressed af, you have now ALSO scroll down as you get further into your list / desperation!

As a fun sidenote (no picture displayed because OMG is it annoying af): even if you make it past this step, the _next_ step displays an arbitrary/borderline unusable calendar view and the ability to "choose" slots that come back with a "Sorry, someone just reserved this slot" so often I legitimately thought there was a system error on their end for a good while.

Ok so anyways - at this point, this is the issue:

> The Rite Aid Immunization Scheduler is Good and Cool in that it exists but basically is unusable given that demand for the appointment slots are very, very high. 

## Attempt 1: Find stores with Availability

My first attempt at trying to get around the UX frustrations was to just try and come up with a way to access the store availability data without having to click the damn button.

I figured that this data was being fetched on button click, so I peeked into the Network tab in Chrome's Dev tools and found calls similar to this

```bash
GET https://www.riteaid.com/services/ext/v2/vaccine/checkSlots?storeNumber=3697
```

which seemed to return:

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

I assumed (correctly, as it turned out) that if `.Data.slots["1"]` or `.Data.slots["2"]` were `true`, then I'd be in business. So, all I had to do was put together a script that would hit the URL above with the store ID in question (there actually is an API call made to perform the geoquery search -- I include it in the script below).

I ended up writing a quick py script:

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

Now, this script worked great - I ran it continuously while sleeping for a few seconds in between invocations and it did seem to reliably point me to stores that availability slots show up!

But, the problem way, by the time I typed in the zip code in the search back, scrolled down to the store number, "selected" the store and then clicked "next" (this figure is from above, reproduced to make my point):

![rite aid screen](/dev/img/riteaidscreen1_err1.png)

...either the slot would be gone **OR** I'd advance to the next screen where I'd have to play the game of clicking UI buttons some more and lose out on the appointment slot anyways.

Bummer. 

## Attempt 2: Running code in the browser

At this point, I realized that my best bet was to write logic - in js - that I could run in the webpage itself through the Console in Chrome's Dev tools.

The initial idea was to simply run the same network commands, but using javascript's `fetch` API to push an appointment all the way through.

In order figure out what the network commands to call are, I had to look at the js source of the app itself.

This...sucked 

## CVS Sidebar

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

At any rate - useful for potentially _finding_ a store with availability (and maybe an alerting service?) but not uch else. Bummer.