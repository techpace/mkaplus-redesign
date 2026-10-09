---
title: "Why we built Legwork"
summary: "Frontier models spend too much effort on errands. Here's the split we made, and what we still haven't proven."
publishDate: "2026-10-08"
product: "legwork"
type: "build-note"
topics: ["ai-workflows"]
tags: ["research", "model-costs"]
status: "published"
---

Legwork started with a pattern that's easy to miss when you use AI every day. Ask Claude or ChatGPT a question about a large folder and it doesn't just think. It starts digging: search, open, read, search again. Dozens of rounds, each one resending everything it has read so far.

Your best model ends up spending its effort on errands. That's the problem we set out to fix.

## The errands add up

Searching a folder isn't hard work. It's a lot of small, repetitive work: find the files that might matter, open them, skim, decide what to read next. A frontier model can do all of that, but it's an expensive place to do it, and every round makes the conversation heavier, because the model carries everything it has read into the next step.

In our benchmark, 10 real questions about a 2,275-file manuscript, the reasoning model that did all the digging itself used 776 requests and 37.45M input tokens across 20 runs.

## Split the thinking from the digging

So we split the job. Claude or ChatGPT keeps the reasoning: it understands your question, weighs the evidence and writes the answer. The searching, reading and cross-checking goes to a worker, a low-cost model that does the legwork and comes back with a short report.

With that split, the same benchmark's reasoning model used 68 requests and 0.51M input tokens, 98.6% fewer, with the same average score in a blind review: 4.12 out of 5 in both modes. At list API rates, the total cost of those 20 runs went from $17.19 to $2.01.

## Bring your own worker

We don't pick the worker for you. You connect your own key with a low-cost model provider, or run a local model, and you pay that provider directly. MKA Plus never resells tokens.

That's partly about trust. You know which model read your documents, and if you'd rather keep document text on your own hardware, you can. It's also about honest numbers: worker cost depends on the model you choose, and you see that bill directly instead of finding it folded into ours.

## Every finding carries a source

A cheaper model doing the reading raises a fair question: can you trust what it found? Our benchmark says it isn't perfect. Two of the 20 delegated answers contained an inaccuracy; none of the answers where the reasoning model did everything itself did.

So the worker doesn't hand back a summary you have to take on faith. Every finding comes with the exact file and location it came from, so you or your AI can check it in seconds. The report also lists what the worker looked for and couldn't find. Gaps are stated, not filled in. And re-running the worker is cheap, so a doubtful finding is easy to check again.

<figure class="post-fig" style="padding:0;background:none;border:0">
  <article class="sheet" aria-label="Example worker report">
  <div class="sheet-head"><strong>Worker report</strong><span>example</span></div>
  <h4>Objective</h4>
  <p>Where does Mara first appear, and who introduces her?</p>
  <h4>Findings</h4>
  <ol>
    <li>Mara is first named in the harbour scene. <span class="cite">part-1/ch03.docx:112</span></li>
    <li>She is introduced by the narrator's sister, not by Daniel. <span class="cite">part-1/ch03.docx:118</span></li>
    <li>An earlier outline lists her under a different name. <span class="cite">notes/outline-v2.pdf · p.4</span></li>
  </ol>
  <h4>Evidence</h4>
  <blockquote>"…my sister waved her over from the harbour wall and said, this is Mara."</blockquote>
  <h4>Not found</h4>
  <p class="nf">No mention in part-2 drafts before chapter 9.</p>
</article>
  <figcaption class="fn">An example worker report: one finding per line, each with its source, and a list of what wasn't found.</figcaption>
</figure>

## What we haven't proven yet

Legwork isn't faster. In the benchmark, both modes took about the same total time. The saving is in the work your main model does, not in waiting time.

Our numbers come from one corpus, one reviewer, and a reasoning model driven through its API, not inside the Claude or ChatGPT apps. Testing inside the apps is in progress, and we'll publish those results here when we have them.

Setup is meant to be one step. When your early access spot opens, you get one connector URL to paste into Claude or ChatGPT, and the same workspace is shared across the apps you connect.

For the numbers in full, read [what our benchmark does and doesn't mean](/blog-legwork-benchmark-costs.html), or see [how Legwork works](/legwork.html). [Early access](/early-access.html) is open, and we read every request.
