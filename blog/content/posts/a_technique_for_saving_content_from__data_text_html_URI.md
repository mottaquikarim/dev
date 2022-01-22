---
title: "A technique for saving content from a `data:text/html` URI"
date: 2022-01-22T12:39:04Z
tags: ["javascript", "just for fun"]
---

{{<toc>}}

OMG! I finally got it. 🙌

**BLUF**

🙌 Turn your chrome tab into a "notepad" using: `data:text/html, <html contenteditable>` (copy and paste this into your URL bar to test it out)

🚨 But! If you hit back or refresh by accident, you lose your notes (this sucks)

✅ Using javsacript's clipboard functionality, I came up with a solution that updates the clipboard everytime you type in to the "notepad". 

👉 Click **[`TabNotes`](data:text/html,%3Chtml%20contenteditable%3E%3Cscript%3Evar%20sel%3Ddocument.getSelection%28%29%3Bdocument.querySelector%28%22html%22%29.addEventListener%28%22input%22%2Cfunction%28%29%7Bsaved%3D%5Bsel.focusNode%2Csel.focusOffset%5D%2Cdocument.execCommand%28%22selectall%22%29%2Cdocument.execCommand%28%22copy%22%29%2Cwindow.getSelection%28%29.removeAllRanges%28%29%2Cdocument.querySelector%28%22html%22%29.focus%28%29%2Csel.collapse%28saved%5B0%5D%2Csaved%5B1%5D%29%7D%29%3B%3C%2Fscript%3E)** to see this working in action. 👈

## Background.

On **May 13, 2016** I posted this article -- [A technique for saving content from a data:text/html, URI](https://taqkarim.medium.com/a-technique-for-saving-content-from-a-data-text-html-uri-10f045a8876d) -- on Medium:

> TL; DR: I put together a script that lets you save the notes you write in your browser-scratchpad. 

To be frank, my solution sucked. For good reason, the `data:text/html` in browser URI trick disallowed a lot of the common browser APIs that would allow local caching (eg: localStorage, etc).

My solution was dirty (I expound in decent detail on my Medium article) and I never actually ended up using it. But - `data:text/html, <html contenteditable>` is quite useful and I use it _often_ to jot down meeting notes or off the record points during 1:1s (that I don't want tracked in say Gdocs)

And this morning, while shaving, a thought occurred to me: 

> Why not save the text to the clipboard?

!! I can't believe I didn't think of this before!

## Experimentation.

I gotta admit fam, this got me pretty fired up. I started looking into what kinds of options we have currently to handle copy/pasta type operations in javascript.

Disappointingly, the `navigator.clipboard` [API](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/clipboard) is only available [in secure contexts](https://developer.mozilla.org/en-US/docs/Web/API/Clipboard). This means attempting to access the Clipboard API returns an error. whomp whomp.

As it turns out though, `document.execCommand` (soon to be deprecated, unfortunately) [API](https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand#commands) still works!

(NB: this idea occurred to me too late, it seems. I have a `PS!` in the end of this post with a compromise solution)

The main draw back with `document.execCommand('copy')` is that it only operates over selected text.

My naive attempt was to grab text input (using contenteditable's `input` event), write it to an invisible textarea (css `visibility: hidden` ftw!) and quickly run the copy execCommand:

### Naive attempt: URI
```html
data:text/html, <html><div contenteditable></div><textarea style="visibility: visible"></textarea></html>
```
Note: `visibility` is NOT hidden for the sake of demonstration purposes

### Naive attempt: js implementation

```javascript
let timeout;
document.querySelector('div').addEventListener('input', function() {
    clearTimeout(timeout)
    div = this
    text = document.querySelector('textarea')
    timeout = setTimeout(_ => {
        text.innerHTML = div.innerHTML;
        text.focus()
        text.select()
        document.execCommand('copy')
        div.focus()
    }, 1000) 
})
```

<video draggable="false" controls="" playsinline="" autoplay="" loop="" class="" style="width: 100%; height: auto; border: 1px solid black;">
  <source type="video/mp4" src="/dev/img/naive_attempt_1.mp4">
</video>
<select onchange="document.querySelector('video').playbackRate = Number(this.value)">
  <option value="1.0">Default (1.0)</option>
  <option value="0.50">Slower (0.5)</option>
  <option value="0.10">Slowest (0.1)</option>
</select>


### Naive attempt: remarks

This implementation sets a simple cancellable timer (to ensure that we only perform this copy work _after_ user has stopped typing). We read the contents of our content editable, stick it into the textarea (which we can programmatically select) and then run our exec command.

This ends up working pretty well!

But we can do better. The main tradeoffs here are:

* The actual uri requires more HTML / css. (The end result has a ton of js in there too so this shouldn't matter but still, I wanted to arrive at a solution ideally with a single element (the `<html contenteditable`)
* Focusing on the textarea means we lose access to our cursor position in the actual content -- this sucks! I wanted to find a better approach


### Refined attempt: URI

```html
data:text/html, <html contenteditable>
```

### Refined attempt: js implementation

```javascript
const sel = document.getSelection();
document.querySelector('html').addEventListener('input', function() {
    saved = [ sel.focusNode, sel.focusOffset ];
    document.execCommand('selectall')
    document.execCommand('copy')
    window.getSelection().removeAllRanges();
    document.querySelector('html').focus()
    sel.collapse(saved[0], saved[1]);
})
```

<video draggable="false" controls="" playsinline="" autoplay="" loop="" class="" style="width: 100%; height: auto; border: 1px solid black;">
  <source type="video/mp4" src="/dev/img/refined_attempt_1.mp4">
</video>
<select onchange="document.querySelector('video').playbackRate = Number(this.value)">
  <option value="1.0">Default (1.0)</option>
  <option value="0.50">Slower (0.5)</option>
  <option value="0.10">Slowest (0.1)</option>
</select>

### Refined attempt: remarks

I was able to find a solution to saving the cursor position by googling. (I've worked with contenteditables + ranges in the past and I still have nightmares -- as such I resolved to try and lean on the collective expertise of the internet to find a solution).

I looked through the implementation on [this codepen](https://codepen.io/kmessner/pen/oXgRrG) and pulled out the relevant bits for my solution (the `focusNode`/ `focusOffset` trick from above)

With this in place I was off to the races -- my new soluton works as follows:

1. on input event, let's save the cursor offset
2. this lets us momentarily select the entire text content _in the contenteditable_ itself
3. because text is selected, we can copy
4. to reset, we remove the selection and focus into the contenteditable once more
5. finally, we restore the cursor position

This works really well and the overall code is only a few lines long (thank _god_)

Ta da!

## Output Artifact.

I ran the js code in a minifier (this [one](https://jscompress.com/)) which resulted in:

```javascript
var sel=document.getSelection();document.querySelector("html").addEventListener("input",function(){saved=[sel.focusNode,sel.focusOffset],document.execCommand("selectall"),document.execCommand("copy"),window.getSelection().removeAllRanges(),document.querySelector("html").focus(),sel.collapse(saved[0],saved[1])});
```

Now, in order to use this functionality all we need to do is copy/paste the following into a URL bar:

```html
data:text/html, <html contenteditable><script>var sel=document.getSelection();document.querySelector("html").addEventListener("input",function(){saved=[sel.focusNode,sel.focusOffset],document.execCommand("selectall"),document.execCommand("copy"),window.getSelection().removeAllRanges(),document.querySelector("html").focus(),sel.collapse(saved[0],saved[1])});</script>
```

And everything we type into the "scratchpad" will automatically be saved to our clipboard!

(You can drag this link: **[`TabNotes`](data:text/html,%3Chtml%20contenteditable%3E%3Cscript%3Evar%20sel%3Ddocument.getSelection%28%29%3Bdocument.querySelector%28%22html%22%29.addEventListener%28%22input%22%2Cfunction%28%29%7Bsaved%3D%5Bsel.focusNode%2Csel.focusOffset%5D%2Cdocument.execCommand%28%22selectall%22%29%2Cdocument.execCommand%28%22copy%22%29%2Cwindow.getSelection%28%29.removeAllRanges%28%29%2Cdocument.querySelector%28%22html%22%29.focus%28%29%2Csel.collapse%28saved%5B0%5D%2Csaved%5B1%5D%29%7D%29%3B%3C%2Fscript%3E)** to your bookmark bar as well to use now).

## PS!

So what happens once the `execCommand` is fully deprecated? Idk, fam. But while experimenting, I did play with this solution:

```javascript
window.addEventListener('beforeunload', function (e) {
    e.preventDefault();
    e.returnValue = '';
    alert()
})
```

This prompts an alert message which can be used to prevent data loss. Compressing and adding to our URI we get:

```html
data:text/html, <html contenteditable><script>window.addEventListener("beforeunload",function(e){e.preventDefault(),e.returnValue="",alert()});</script>
```

<video draggable="false" controls="" playsinline="" autoplay="" loop="" class="" style="width: 100%; height: auto; border: 1px solid black;">
  <source type="video/mp4" src="/dev/img/ps_1.mp4">
</video>
<select onchange="document.querySelector('video').playbackRate = Number(this.value)">
  <option value="1.0">Default (1.0)</option>
  <option value="0.50">Slower (0.5)</option>
  <option value="0.10">Slowest (0.1)</option>
</select>

(You can drag this link: **[`TabNotes: alert`](data:text/html,%3Chtml%20contenteditable%3E%3Cscript%3Ewindow.addEventListener%28%22beforeunload%22%2Cfunction%28e%29%7Be.preventDefault%28%29%2Ce.returnValue%3D%22%22%2Calert%28%29%7D%29%3B%3C%2Fscript%3E)** to your bookmark bar as well to use now).

