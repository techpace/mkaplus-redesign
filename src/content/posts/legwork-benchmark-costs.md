---
title: "98.6% fewer tokens. Here's what that number does and doesn't mean."
summary: "What our Legwork benchmark measured, what it costs in dollars, and what it doesn't show."
publishDate: "2026-10-08"
product: "legwork"
type: "benchmark"
topics: ["performance", "ai-workflows"]
tags: ["model-costs", "evaluation"]
status: "published"
---

When we tell people Legwork cut our reasoning model's input tokens by 98.6%, the first question is usually "on what?" Fair question. Here's the short version, and the parts we'd rather you hear from us than discover yourself.

## The setup

On 5 October we took a real working corpus: a 2,275-file Vietnamese novel manuscript and its notes, about 35 MB of text. The author gave us 10 questions they actually ask day to day. Each question ran twice in two modes. In one, the reasoning model did all the searching and reading itself. In the other, it handed the digging to a Legwork worker and worked from the report. That's 40 runs, each with a 10-minute budget, and the author reviewed all 40 answers blind.

<figure class="post-fig">
  <div class="modes" role="img" aria-label="The two modes. Does it all: the reasoning model searches and reads every file itself, then writes the answer. With Legwork: the reasoning model hands the digging to a Legwork worker, which searches, reads and cross-checks, and returns a short sourced report; the reasoning model then writes the answer.">
    <div class="mode">
      <span class="tag">Mode 1 · Does it all</span>
      <div class="mode-flow">
        <div class="node ai"><span class="who">Reasoning model</span><h3>Searches and reads every file itself</h3></div>
        <span class="to" aria-hidden="true">→</span>
        <div class="node ai"><span class="who">Reasoning model</span><h3>Writes the answer</h3></div>
      </div>
    </div>
    <div class="mode">
      <span class="tag">Mode 2 · With Legwork</span>
      <div class="mode-flow">
        <div class="node ai"><span class="who">Reasoning model</span><h3>Hands off the digging</h3></div>
        <span class="to" aria-hidden="true">→</span>
        <div class="node worker"><span class="who">Legwork worker</span><h3>Searches, reads, cross-checks</h3></div>
        <span class="to" aria-hidden="true">→</span>
        <div class="node docs"><span class="who">Report</span><h3>Short, with sources</h3></div>
        <span class="to" aria-hidden="true">→</span>
        <div class="node ai"><span class="who">Reasoning model</span><h3>Writes the answer</h3></div>
      </div>
    </div>
  </div>
  <figcaption class="fn">The two modes we compared. Each of the 10 questions ran twice in each mode.</figcaption>
</figure>

## What moved

Across 20 runs per mode, the reasoning model's input went from 37.45M tokens to 0.51M, and its requests from 776 to 68. Even counting only tokens that weren't cache hits, input dropped 88.4%. The average review score was identical, 4.12 out of 5 in both modes, and the delegated answer was preferred in 6 of 10 questions.

<figure class="post-fig">
  <div class="bars">
    <div class="metric"><div class="metric-head"><h3>Reasoning-model input tokens</h3><span class="delta">−98.6%</span></div><div class="row"><span class="lab">Does it all</span><div class="track"><div class="fill" style="width:100.00%"></div></div><span class="val">37.45M</span></div><div class="row"><span class="lab">With Legwork</span><div class="track"><div class="fill lw" style="width:1.36%"></div></div><span class="val">0.51M</span></div></div>
    <div class="metric"><div class="metric-head"><h3>Reasoning-model requests</h3><span class="delta">−91%</span></div><div class="row"><span class="lab">Does it all</span><div class="track"><div class="fill" style="width:100.00%"></div></div><span class="val">776</span></div><div class="row"><span class="lab">With Legwork</span><div class="track"><div class="fill lw" style="width:8.76%"></div></div><span class="val">68</span></div></div>
  </div>
  <figcaption class="fn">Totals over 20 runs per mode. Bars to scale.</figcaption>
</figure>

## What it costs

We priced the measured tokens at list API rates as of 8 October 2026. The reasoning model was Qwen3.8-Max ($2 per 1M input tokens, $0.25 cached, $6 output, Alibaba Cloud Singapore). The worker was Agnes 3.0 Flash ($0.05 input, $0.005 cached, $0.15 output).

Doing all the digging itself, Qwen3.8-Max cost $17.19 across 20 runs, about $0.86 per question. With Legwork, its share fell to $1.40. The worker read 43.1M tokens of prompt to do the digging, mostly cache hits, wrote 0.35M, and added $0.61. That's $2.01 in total, about $0.10 per question, or 88% less.

<figure class="post-fig">
  <div class="bars">
    <div class="metric"><div class="metric-head"><h3>Total cost, 20 runs</h3><span class="delta">−88%</span></div><div class="row"><span class="lab">Does it all</span><div class="track"><div class="fill" style="width:100.00%"></div></div><span class="val">$17.19</span></div><div class="row"><span class="lab">With Legwork</span><div class="track stacked"><div class="fill seg" style="width:8.14%"></div><div class="fill lw seg" style="width:3.55%"></div></div><span class="val">$2.01</span></div></div>
  </div>
  <div class="legend"><span><i></i>Reasoning model (Qwen3.8-Max)</span><span><i class="lw"></i>Worker (Agnes 3.0 Flash)</span></div>
  <figcaption class="fn">At list API rates as of 8 October 2026. With Legwork: $1.40 reasoning model + $0.61 worker. Bars to scale.</figcaption>
</figure>

<div class="table-wrap">
  <table>
    <thead><tr><th>At list API rates</th><th class="num">Reasoning model</th><th class="num">Worker</th><th class="num">Total</th><th class="num">Per question</th></tr></thead>
    <tbody>
      <tr><td>Does it all</td><td class="num">$17.19</td><td class="num">$0</td><td class="num">$17.19</td><td class="num">$0.86</td></tr>
      <tr><td>With Legwork</td><td class="num">$1.40</td><td class="num">$0.61</td><td class="num"><strong>$2.01</strong></td><td class="num"><strong>$0.10</strong></td></tr>
    </tbody>
  </table>
</div>

Two honest footnotes. Money falls less than tokens (88% versus 98.6%) because most of the "does it all" input was cache hits, which are cheap. And the "does it all" figure is a floor: 16 of its 20 runs hit the 10-minute budget before finishing.

## What didn't move

It wasn't faster: both modes took about the same total time. The work didn't vanish either. The worker read about 8.2 MB and returned 0.68 MB of reports, so the reading still happened, just on a low-cost model you choose instead of your main one.

## Where it was worse

Two of the 20 delegated answers contained an inaccuracy; none of the "does it all" answers did. That's the reason every Legwork finding carries an exact source. You can check a claim in seconds, and re-running the worker is cheap.

## What we haven't tested yet

This was one corpus with one reviewer, and the reasoning model was driven through its API, not inside the Claude or ChatGPT apps. Testing inside the apps is in progress, and we'll publish those numbers here when we have them.

If you want every table, the [full methodology](/legwork-benchmark.html) is public.
