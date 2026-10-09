---
title: "What Legwork won't read, and what it writes down"
summary: "How our next release handles sensitive files, keys and the audit trail, including the limits. Built and tested, not live yet."
publishDate: "2026-10-08"
product: "legwork"
type: "engineering"
topics: ["privacy", "security"]
tags: ["audit-log", "document-access"]
status: "published"
---

<div class="note-box"><strong>Not live yet.</strong> Everything on this page is built and tested, but it isn't serving real users today. It comes with our next public release. We're writing about it now because how a tool treats your files should be clear before you hand them over.</div>

When you point a research worker at a folder, two questions matter as much as the answers it gives back: what will it refuse to read, and what record does it keep? Here's how Legwork handles both, including the parts that are deliberately blunt.

## Files it won't read

Any file whose name matches `*secret*` or `*credential*` is hard-denied. The worker never reads it, and the report lists it as excluded, so you can see what was skipped instead of wondering.

We'll be candid about this rule. It's based on file names, and it's deliberately strict. That means it can skip an innocent file, a chapter called `secret-garden.md`, for example, and it can't catch a sensitive file with an ordinary name.

It's a temporary rule, and we'll refine it. Until then, the obvious habit is the safest one: keep keys and passwords out of the folders you point Legwork at.

## One job, one container

Each research job runs its worker in an isolated Docker container, started from a pinned image. One job's worker doesn't share a running environment with another's, and the image it runs is a fixed, known version rather than whatever happened to be installed that day.

This is about isolating each job's worker. Where workspaces are stored, how long data is kept and how each customer's workspace is isolated will be published on [Your documents and keys](/legwork-privacy.html) before early access opens, as that page says.

## Keys you can revoke

The API keys that give access to Legwork are stored only as sha256 hashes, so the stored value can't be turned back into a working key. Keys can be revoked. Right now, a revocation takes effect after a server restart.

## What it writes down

Every job gets a trace, and every call gets a line in a ledger. Each tool call is recorded with its arguments, with secrets redacted, and the size of its result. The ledger never stores your file content or the report text.

It also splits every MCP response into substantive bytes and control bytes: the part that carries the content, and the protocol around it. That split is what lets a token-savings claim be audited from the record instead of taken on trust.

<figure class="post-fig" style="padding:0;background:none;border:0">
  <div class="pillars two" style="margin-top:0">
    <div class="pillar"><h3>Recorded for every job</h3><ul>
      <li>Every tool call the worker makes</li>
      <li>Its arguments, with secrets redacted</li>
      <li>The size of each result</li>
      <li>Substantive vs control bytes in each MCP response</li></ul></div>
    <div class="pillar"><h3>Never recorded</h3><ul>
      <li>The content of your files</li>
      <li>The text of the report</li>
      <li>Secrets passed in arguments</li></ul></div>
  </div>
  <figcaption class="fn">What the per-job trace and per-call ledger keep. Built and tested, not live yet.</figcaption>
</figure>

## Cancel and restarts

You can cancel a job, and it stops reliably. If the server restarts while jobs are running, those jobs are clearly marked and cleaned up, not left half-finished in the background. A lock stops two servers from running on the same state at once.

## What stays the same

None of this changes who reads what. The worker model you connect reads the parts of your documents it searches. Your AI app, Claude or ChatGPT, receives the worker's short report, not your whole files. You bring your own key or a local model, and MKA Plus never resells tokens.

To recap the status: the name rule, per-job containers, hashed keys, the trace and ledger, and the cancel and restart handling are built and tested, and they come with our next public release. They aren't live today.

For the bigger picture, read [why we built Legwork](/blog-why-we-built-legwork.html). Questions about any of this: **hello@mkaplus.com**.
