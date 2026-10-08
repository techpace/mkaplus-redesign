"""Generates the static MKA Plus site into website/. Output is plain HTML; the script is a one-off authoring aid."""
import pathlib, sys

OUT = pathlib.Path(sys.argv[1])
BASE = "https://www.mkaplus.com/"

NAV = [("legwork.html", "Legwork"), ("marshal.html", "Marshal"), ("services.html", "Services"),
       ("about.html", "About"), ("contact.html", "Contact")]


def nav_list(active):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return '<ul class="nav-links">' + "".join(items) + "</ul>"


def page(fname, title, desc, body, active=None, forms=False):
    canonical = BASE if fname == "index.html" else BASE + fname
    script = '\n<script src="assets/forms.js" defer></script>' if forms else ""
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="assets/favicon-32.png" type="image/png" sizes="32x32">
<link rel="icon" href="assets/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..800&amp;family=Schibsted+Grotesk:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="MKA Plus"><img src="assets/logo.webp" alt="MKA Plus" width="800" height="129"></a>
    <nav class="desktop-nav" aria-label="Main">{nav_list(active)}</nav>
    <div class="nav-right">
      <a class="btn primary" href="early-access.html">Get early access</a>
      <details class="menu"><summary aria-label="Open menu">Menu</summary><nav aria-label="Main (mobile)">{nav_list(active)}</nav></details>
    </div>
  </div>
</header>

<main>
{body.strip()}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="stack" style="gap:10px">
      <a class="logo" href="index.html" aria-label="MKA Plus"><img src="assets/logo.webp" alt="MKA Plus" width="800" height="129"></a>
      <p>36/70/4 D2 Street, Ward 25, Binh Thanh District, HCMC, Vietnam</p>
      <p>Tel +84 28 3620 5400 · hello@mkaplus.com</p>
    </div>
    <ul>
      <li><a href="legwork.html">Legwork</a></li>
      <li><a href="legwork-benchmark.html">Benchmark</a></li>
      <li><a href="marshal.html">Marshal</a></li>
      <li><a href="services.html">Managed IT services</a></li>
    </ul>
    <ul>
      <li><a href="about.html">About</a></li>
      <li><a href="contact.html">Contact</a></li>
      <li><a href="privacy.html">Privacy</a></li>
      <li><a href="terms.html">Terms</a></li>
    </ul>
    <p class="legal">© 2026 MKA Plus. All rights reserved.</p>
  </div>
</footer>{script}
</body>
</html>
"""
    (OUT / fname).write_text(html, encoding="utf-8")


# ---------------------------------------------------------------- shared blocks
FLOW = """
<div class="flow-row" aria-label="How a question flows through Legwork">
  <div class="node ai">
    <span class="who">Your AI</span>
    <h3>Thinks</h3>
    <ul><li>Understands your question</li><li>Weighs the evidence</li><li>Writes the answer</li></ul>
  </div>
  <div class="link">
    <div class="arrow"><span>objective</span><i></i></div>
    <div class="arrow back"><i></i><span>short report + sources</span></div>
  </div>
  <div class="node worker">
    <span class="who">Legwork worker · model you choose</span>
    <h3>Does the legwork</h3>
    <ul><li>Searches every file</li><li>Reads what matters</li><li>Cross-checks, cites <span class="cite">ch03.docx:112</span></li></ul>
  </div>
  <div class="link">
    <div class="arrow"><span>search · read</span><i></i></div>
  </div>
  <div class="node docs">
    <span class="who">Your documents</span>
    <h3>Stay where they are</h3>
    <ul><li>Word, PDF, sheets, slides</li><li>Markdown, notes, text</li><li>One workspace across apps</li></ul>
  </div>
</div>
"""

BARS = """
<div class="bars">
  <div class="metric">
    <div class="metric-head"><h3>Input tokens</h3><span class="delta">−98.6%</span></div>
    <div class="row"><span class="lab">Does it all</span><div class="track"><div class="fill" style="width:100%"></div></div><span class="val">37.45M</span></div>
    <div class="row"><span class="lab">With Legwork</span><div class="track"><div class="fill lw" style="width:1.36%"></div></div><span class="val">0.51M</span></div>
  </div>
  <div class="metric">
    <div class="metric-head"><h3>Requests</h3><span class="delta">−91%</span></div>
    <div class="row"><span class="lab">Does it all</span><div class="track"><div class="fill" style="width:100%"></div></div><span class="val">776</span></div>
    <div class="row"><span class="lab">With Legwork</span><div class="track"><div class="fill lw" style="width:8.76%"></div></div><span class="val">68</span></div>
  </div>
  <div class="quality">
    <span class="big">Same quality</span>
    <p class="muted">Equal average score in a blind review. The delegated answer was preferred in 6 of 10 questions.</p>
  </div>
</div>
"""

BENCH_NOTE = ("10 real questions over a 2,275-file manuscript, 40 runs. Totals for the reasoning model over 20 runs per mode. "
              "The reasoning model was driven through its API; tests inside the Claude and ChatGPT apps are in progress.")

PILLARS = """
<div class="pillars">
  <div class="pillar"><h3>Thinking stays with your AI</h3><p>The model you trust makes the judgment calls.</p></div>
  <div class="pillar"><h3>Every finding has a source</h3><p>The exact file and location for every claim, so you can check it in seconds.</p></div>
  <div class="pillar"><h3>Bring your own worker</h3><p>Any low-cost worker model you pick, or a local one. You pay the provider directly; we never resell tokens.</p></div>
  <div class="pillar"><h3>One workspace, many apps</h3><p>The same files and history in Claude and ChatGPT.</p></div>
  <div class="pillar"><h3>Setup in one URL</h3><p>Built for people who don't want to configure agents.</p></div>
  <div class="pillar"><h3>Works with every document</h3><p>Word, PDF, spreadsheets, slides, notes. No conversion needed.</p></div>
</div>
"""

REPORT = """
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
"""

MKA_BAND = """
<section>
  <div class="wrap split">
    <h2>Built by MKA Plus.</h2>
    <div class="stack-lg">
      <p style="font-size:1.1rem;max-width:36em">MKA Plus has run managed IT for organizations for more than 10 years. The same team that keeps networks and systems running now builds and deploys AI products, and stays on to support them.</p>
      <div class="actions"><a class="btn" href="services.html">Our IT services</a><a class="btn" href="about.html">About us</a></div>
    </div>
  </div>
</section>
"""

# ---------------------------------------------------------------- pages
HOME = f"""
<section class="hero gridbg">
  <div class="wrap">
    <div class="top">
      <span class="tag">Legwork · research worker for Claude and ChatGPT</span>
      <h1>Keep your AI for thinking. Hand off the digging.</h1>
      <p class="lede">Claude or ChatGPT stays in charge of the reasoning. Searching, reading and cross-checking your documents goes to a low-cost worker model you choose. It reports back in a few paragraphs, with the exact source for every finding.</p>
      <p class="stat">Internal benchmark: reasoning-model input tokens <b>−98.6%</b>, same answer quality. <a href="#proof">See the numbers ↓</a></p>
      <div class="actions"><a class="btn primary" href="early-access.html">Get early access</a><a class="btn" href="#how">See how it works</a></div>
    </div>
    {FLOW}
  </div>
</section>

<section>
  <div class="wrap">
    <div class="stack narrow">
      <span class="tag">The problem</span>
      <h2>Your best model spends its effort on errands.</h2>
      <p class="muted" style="font-size:1.12rem">Ask your AI a question about a large folder and it starts digging: search, open, read, search again. Dozens of rounds, each one resending everything it has read so far.</p>
    </div>
  </div>
</section>

<section class="surface" id="proof">
  <div class="wrap split">
    <div class="stack">
      <span class="tag">Internal benchmark</span>
      <h2>Same answers. A fraction of the work on your main model.</h2>
      <p class="fn">{BENCH_NOTE} <a href="legwork-benchmark.html">Full methodology →</a></p>
    </div>
    {BARS}
  </div>
</section>

<section id="how">
  <div class="wrap">
    <span class="tag">How it works</span>
    <h2 style="margin-top:12px">Three steps, no agents to configure.</h2>
    <div class="steps">
      <div class="step"><span class="k">1</span><h3>Connect</h3><p class="muted">Paste one connector URL into Claude or ChatGPT.</p></div>
      <div class="step"><span class="k">2</span><h3>Point it at your documents</h3><p class="muted">Any format you work with. Your workspace stays put between sessions and is shared across the AI apps you connect.</p></div>
      <div class="step"><span class="k">3</span><h3>Ask as usual</h3><p class="muted">Your AI hands the digging to the worker, gets back a short sourced report, then does the thinking.</p></div>
    </div>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <span class="tag">Why Legwork</span>
    {PILLARS}
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <span class="tag">Who it's for</span>
    <div class="rows">
      <div><h3>Writers</h3><p>Ask about your manuscript like you'd ask an assistant who has read every chapter.</p></div>
      <div><h3>Marketing &amp; content</h3><p>Find what you already wrote and what the brand guide says before you write the next piece.</p></div>
      <div><h3>Researchers &amp; analysts</h3><p>Cross-check dozens of documents. What wasn't found is listed too.</p></div>
      <div><h3>Developers</h3><p>Remote MCP backend. Bring your own key, pick your worker model.</p></div>
    </div>
  </div>
</section>

<section class="band" id="marshal">
  <div class="wrap split even">
    <div class="stack-lg">
      <span class="tag" style="color:var(--accent)">For organizations · Marshal</span>
      <h2>Your people adopt AI one by one. Marshal lets IT see and govern all of it.</h2>
      <p class="muted">Route, approve and account for every AI request. Approvals, quotas and audit, deployed in your own environment.</p>
      <div class="actions"><a class="btn" href="marshal.html">Explore Marshal</a></div>
    </div>
    <div class="qs" aria-label="Questions Marshal answers">
      <div class="q"><b>CIO / IT</b><span>Which providers and models are in use, by which projects?</span></div>
      <div class="q"><b>FinOps</b><span>What does it cost, by department, against quota and budget?</span></div>
      <div class="q"><b>Security / Audit</b><span>Who requested, who approved, when, and what was used under that key?</span></div>
      <div class="q"><b>Department heads</b><span>What is my team using, and is it within what we approved?</span></div>
    </div>
  </div>
</section>
{MKA_BAND}
"""

LEGWORK = f"""
<section class="hero gridbg">
  <div class="wrap">
    <div class="top">
      <span class="status">Early access</span>
      <h1>Your AI does the thinking. Legwork does the legwork.</h1>
      <p class="lede">A research worker for Claude and ChatGPT. Your AI keeps the reasoning. Legwork's worker searches, reads and cross-checks your documents, then hands back a short report with sources.</p>
      <div class="actions"><a class="btn primary" href="early-access.html">Get early access</a><a class="btn" href="legwork-benchmark.html">See the benchmark</a></div>
    </div>
    {FLOW}
  </div>
</section>

<section>
  <div class="wrap split">
    <div class="stack">
      <span class="tag">What comes back</span>
      <h2>A short report you can check.</h2>
      <p class="muted">Your AI doesn't get a pile of raw files. It gets a few paragraphs with a fixed shape:</p>
      <div class="rows" style="margin-top:8px">
        <div><h3>Findings</h3><p>One fact per line, each with the file and location it came from.</p></div>
        <div><h3>Evidence</h3><p>Short quotes, so the claim can be checked without opening the file.</p></div>
        <div><h3>Not found</h3><p>What the worker looked for and couldn't find. Gaps are stated, not filled in.</p></div>
      </div>
    </div>
    {REPORT}
  </div>
</section>

<section class="surface">
  <div class="wrap">
    <span class="tag">Who it's for</span>
    <h2 style="margin-top:12px">Built for people who work with a lot of documents.</h2>
    <div class="rows">
      <div><h3>Writers &amp; novelists</h3><p>Ask about your manuscript like you'd ask an assistant who has read every chapter. Get the answer with the chapter and line. Our benchmark ran on a real 2,275-file manuscript.</p></div>
      <div><h3>Marketing &amp; content creators</h3><p>Find what you already wrote, what you already promised, and what the brand guide says, with sources, before you write the next piece.</p></div>
      <div><h3>Researchers &amp; analysts</h3><p>Cross-check dozens of documents. Every finding comes with the exact place it came from, and what wasn't found is listed too.</p></div>
      <div><h3>Developers &amp; power users</h3><p>A remote MCP backend. Bring your own key and pick your worker model.</p></div>
      <div><h3>Teams<span class="note">Coming</span></h3><p>Shared workspaces and skills, with one budget per team.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="tag">Why Legwork</span>
    {PILLARS}
  </div>
</section>

<section class="band">
  <div class="wrap split">
    <div class="stack">
      <span class="tag">Your keys, your choice</span>
      <h2>We never resell model usage.</h2>
    </div>
    <div class="stack">
      <p class="muted" style="font-size:1.08rem">Connect your own account with a low-cost model provider, or run a local model. You pay the provider directly, and you see which worker model read your documents. <a href="legwork-privacy.html">How your data is handled →</a></p>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="tag">What to expect</span>
    <h2 style="margin-top:12px">Where Legwork helps, and where it doesn't.</h2>
    <div class="pillars">
      <div class="pillar"><h3>It isn't faster</h3><p>Delegated answers take about as long. The saving is in the work your main model does, not in waiting time.</p></div>
      <div class="pillar"><h3>Answers vary more between runs</h3><p>That's why every finding carries a source, and why re-running the worker is cheap.</p></div>
      <div class="pillar"><h3>Results so far are internal</h3><p>We'll publish results from inside the Claude and ChatGPT apps when that testing is done.</p></div>
    </div>
  </div>
</section>

<section class="surface">
  <div class="wrap split">
    <div class="stack">
      <span class="tag">Get started</span>
      <h2>Early access is open for individuals and small teams.</h2>
    </div>
    <div class="stack">
      <p class="muted">Tell us what you work on and which AI app you use. We'll email you when your spot opens.</p>
      <div class="actions"><a class="btn primary" href="early-access.html">Get early access</a></div>
    </div>
  </div>
</section>
"""

BENCH = f"""
<section class="page-hero">
  <div class="wrap stack-lg">
    <a class="crumb" href="legwork.html">← Legwork</a>
    <h1 class="sm">Legwork benchmark</h1>
    <p class="lede">How much work moves off your main model when it delegates the digging, and what happens to answer quality. Internal test, run 5 October 2026, reviewed 6 October 2026.</p>
  </div>
</section>

<section>
  <div class="wrap split">
    <div class="stack">
      <span class="tag">What we tested</span>
      <h2>Real questions, real documents.</h2>
    </div>
    <div class="rows" style="margin-top:0">
      <div><h3>Documents</h3><p>A 2,275-file Vietnamese-language novel manuscript and its notes, about 35 MB of text.</p></div>
      <div><h3>Questions</h3><p>10 questions the author actually asks day to day about the manuscript.</p></div>
      <div><h3>Two modes</h3><p>The reasoning model does all the searching and reading itself, or it delegates the digging to a Legwork worker and works from the report.</p></div>
      <div><h3>Runs</h3><p>Each question twice in each mode: 40 runs. Each run had a 10-minute budget.</p></div>
      <div><h3>Quality review</h3><p>All 40 answers reviewed blind by the manuscript's author, who knows the material best.</p></div>
    </div>
  </div>
</section>

<section class="surface">
  <div class="wrap split">
    <div class="stack">
      <span class="tag">Reasoning-model workload</span>
      <h2>Results</h2>
      <p class="fn">Totals over 20 runs per mode.</p>
    </div>
    {BARS}
  </div>
  <div class="wrap" style="margin-top:48px">
    <div class="table-wrap">
      <table>
        <thead><tr><th>Reasoning model</th><th class="num">Does it all</th><th class="num">With Legwork</th><th class="num">Change</th></tr></thead>
        <tbody>
          <tr><td>Requests</td><td class="num">776</td><td class="num">68</td><td class="num"><strong>−91%</strong></td></tr>
          <tr><td>Input tokens</td><td class="num">37,452,931</td><td class="num">510,012</td><td class="num"><strong>−98.6%</strong></td></tr>
          <tr><td>Input tokens, not cached</td><td class="num">3,060,099</td><td class="num">354,364</td><td class="num"><strong>−88.4%</strong></td></tr>
          <tr><td>Output tokens</td><td class="num">411,559</td><td class="num">107,971</td><td class="num"><strong>−74%</strong></td></tr>
          <tr><td>Tool results read into its context</td><td class="num">4.35 MB</td><td class="num">0.68 MB</td><td class="num"><strong>−84%</strong></td></tr>
          <tr><td>Total time</td><td class="num">12,827 s</td><td class="num">12,733 s</td><td class="num">about the same</td></tr>
        </tbody>
      </table>
    </div>
    <p class="fn" style="margin-top:14px">In the "does it all" mode, 16 of 20 runs were still investigating when the 10-minute budget ran out, so its figures are a lower bound. Most of its input was cache hits, which providers usually bill at a lower rate; the not-cached row shows that view.</p>
  </div>
</section>

<section>
  <div class="wrap split">
    <div class="stack">
      <span class="tag">Answer quality</span>
      <h2>Same average, more variation.</h2>
    </div>
    <div class="stack-lg">
      <div class="table-wrap">
        <table>
          <thead><tr><th>Blind review</th><th class="num">Does it all</th><th class="num">With Legwork</th></tr></thead>
          <tbody>
            <tr><td>Average score (1–5)</td><td class="num">4.12</td><td class="num">4.12</td></tr>
            <tr><td>Questions where this answer was preferred</td><td class="num">4 of 10</td><td class="num">6 of 10</td></tr>
            <tr><td>Answers with an inaccuracy</td><td class="num">0 of 20</td><td class="num">2 of 20</td></tr>
            <tr><td>Answers with a minor omission</td><td class="num">1 of 20</td><td class="num">2 of 20</td></tr>
          </tbody>
        </table>
      </div>
      <p class="fn">One question had a best answer in each mode and is counted for both; one had no clear favourite. Every question got a usable answer in both modes. Both inaccuracies were in delegated runs, which is why Legwork reports carry a source for every finding and make re-running the worker cheap.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap split">
    <div class="stack">
      <span class="tag">Limits</span>
      <h2>What this test doesn't show.</h2>
    </div>
    <div class="prose">
      <ul>
        <li><strong>Not measured inside the Claude or ChatGPT apps.</strong> The reasoning model was driven through its API. Testing inside the apps is in progress.</li>
        <li><strong>Not a speed gain.</strong> Both modes used about the same time.</li>
        <li><strong>The work moves; it doesn't vanish.</strong> The worker read about 8.2 MB and returned 0.68 MB of reports. That work lands on a low-cost model you choose instead of your main one.</li>
        <li><strong>Worker cost depends on your choice of model.</strong> We don't name models here because you pick your own, and results will vary with that choice.</li>
        <li><strong>One corpus, one reviewer.</strong> The questions were hard, real ones. Everyday questions may be lighter; we haven't measured that yet.</li>
      </ul>
    </div>
  </div>
</section>
"""

PRIV_LW = """
<section class="page-hero">
  <div class="wrap stack-lg">
    <a class="crumb" href="legwork.html">← Legwork</a>
    <h1 class="sm">Your documents and keys</h1>
    <p class="lede">Who reads what when you use Legwork, and who pays for it.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="prose">
      <h2>Who reads your documents</h2>
      <p>The worker model you connect reads the parts of your documents it searches. Your AI app, Claude or ChatGPT, receives the worker's short report, not your whole files.</p>
      <p>Legwork shows you which worker model handled each task, so you always know where your text went.</p>

      <h2>Your keys</h2>
      <p>You connect your own account with a model provider, or a model you run yourself. You pay that provider directly. MKA Plus never resells or marks up model usage.</p>

      <h2>Running a local model</h2>
      <p>If you'd rather keep document text on your own hardware, connect a local model as the worker.</p>

      <h2>Before early access opens</h2>
      <div class="note-box">We will publish here where workspaces are stored, how long data is kept, and how each customer's workspace is isolated. Early access starts only after that is published.</div>

      <p>Questions? Email <strong>hello@mkaplus.com</strong>.</p>
    </div>
  </div>
</section>
"""


def form_page_intro(back_href, back_label, title, lede):
    crumb = f'<a class="crumb" href="{back_href}">← {back_label}</a>' if back_href else ""
    return f"""
<section class="page-hero">
  <div class="wrap stack-lg">
    {crumb}
    <h1 class="sm">{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>
"""


EARLY = form_page_intro("legwork.html", "Legwork", "Get early access to Legwork",
                        "Tell us a little about your work. We read every request and reply by email when your spot opens.") + """
<section>
  <div class="wrap split">
    <div class="stack-lg">
      <span class="tag">What happens next</span>
      <div class="rows" style="margin-top:0">
        <div><h3>1. You send this form</h3><p>It opens your email app with the details filled in.</p></div>
        <div><h3>2. We reply</h3><p>We confirm we got it and may ask a question about your documents.</p></div>
        <div><h3>3. You connect</h3><p>When your spot opens, you get a connector URL to paste into Claude or ChatGPT.</p></div>
      </div>
    </div>
    <form class="form" data-subject="Legwork early access request" novalidate>
      <div class="two-col">
        <div class="field"><label for="ea-name">Name</label><input id="ea-name" name="name" data-label="Name" required autocomplete="name"></div>
        <div class="field"><label for="ea-email">Email</label><input id="ea-email" name="email" data-label="Email" type="email" required autocomplete="email"></div>
      </div>
      <div class="field"><label for="ea-role">What do you do?</label>
        <select id="ea-role" name="role" data-label="Role" required>
          <option value="">Choose one</option><option>Writer</option><option>Marketing or content</option>
          <option>Researcher or analyst</option><option>Developer</option><option>Other</option>
        </select></div>
      <fieldset class="field"><legend>Which AI app do you use?</legend>
        <div class="checks">
          <label><input type="checkbox" id="ea-app-claude" name="app" value="Claude" data-label="AI app"> Claude</label>
          <label><input type="checkbox" id="ea-app-chatgpt" name="app" value="ChatGPT"> ChatGPT</label>
          <label><input type="checkbox" id="ea-app-other" name="app" value="Other"> Other</label>
        </div></fieldset>
      <fieldset class="field"><legend>What kind of documents?</legend>
        <div class="checks">
          <label><input type="checkbox" id="ea-doc-word" name="docs" value="Word" data-label="Documents"> Word</label>
          <label><input type="checkbox" id="ea-doc-pdf" name="docs" value="PDF"> PDF</label>
          <label><input type="checkbox" id="ea-doc-sheets" name="docs" value="Spreadsheets"> Spreadsheets</label>
          <label><input type="checkbox" id="ea-doc-slides" name="docs" value="Slides"> Slides</label>
          <label><input type="checkbox" id="ea-doc-md" name="docs" value="Markdown or notes"> Markdown or notes</label>
        </div></fieldset>
      <div class="field"><label for="ea-size">Roughly how many files?</label>
        <select id="ea-size" name="size" data-label="Number of files">
          <option value="">Choose one</option><option>Under 100</option><option>100 to 1,000</option><option>1,000 to 10,000</option><option>More than 10,000</option>
        </select></div>
      <div class="field"><label for="ea-notes">Anything else?</label><textarea id="ea-notes" name="notes" data-label="Notes" placeholder="What would you ask about your documents?"></textarea></div>
      <div class="actions"><button class="btn primary" type="submit">Request early access</button></div>
      <p class="form-result" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
"""

MARSHAL = """
<section class="hero gridbg">
  <div class="wrap">
    <div class="top">
      <span class="status">Pilot phase</span>
      <h1>Route, approve and account for every AI request.</h1>
      <p class="lede">Know who uses which AI, for what, and at what cost. Marshal is a private control plane for enterprise AI: approved access, scoped keys, quotas, and reports your CIO, FinOps and auditors can rely on, deployed in your data center or VPC.</p>
      <div class="actions"><a class="btn primary" href="marshal-pilot.html">Talk to us about a pilot</a></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="stack narrow">
      <span class="tag">The problem</span>
      <h2>AI use grows from the bottom up.</h2>
      <p class="muted" style="font-size:1.12rem">Personal accounts, shared keys, tools nobody registered. When finance asks what it costs, or audit asks who approved it, there's no single answer.</p>
    </div>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <span class="tag">What Marshal does</span>
    <div class="pillars two">
      <div class="pillar"><h3>Access with approval chains</h3><ul>
        <li>Staff request a model and a quota.</li>
        <li>The request goes through your approval chain: as many levels as your organization needs, in your order.</li>
        <li>Once approved, a scoped key is issued with quota and expiry.</li>
        <li>Every step is recorded.</li></ul></div>
      <div class="pillar"><h3>Usage intelligence</h3><ul>
        <li>Usage by project, department, provider and model: tokens, cost, latency.</li>
        <li>Work versus personal or unclassified use.</li>
        <li>Reports for management, FinOps, security and audit.</li></ul></div>
      <div class="pillar"><h3>Policy that fails closed</h3><ul>
        <li>Requests outside the allowed provider, model, region or quota are denied, with a clear reason.</li>
        <li>No silent fallback to something unapproved.</li></ul></div>
      <div class="pillar"><h3>Private by default</h3><ul>
        <li>Runs in your environment.</li>
        <li>Provider keys stay in your secret store; applications never see them.</li>
        <li>Prompts and responses are not stored unless your policy says so.</li></ul></div>
    </div>
  </div>
</section>

<section class="surface">
  <div class="wrap split even">
    <div class="stack-lg">
      <span class="tag">One request, start to finish</span>
      <h2>From request to key, on the record.</h2>
      <p class="muted">The same object that was requested and approved is the one that gets metered and reported. So "who approved this" and "what was used under it" have one answer.</p>
    </div>
    <div class="stack">
      <ul class="chain" aria-label="Example approval chain">
        <li><span class="dot"></span><span>Access requested: model + monthly quota</span><span class="ok">submitted</span></li>
        <li><span class="dot"></span><span>Team manager</span><span class="ok">approved</span></li>
        <li><span class="dot"></span><span>IT security</span><span class="ok">approved</span></li>
        <li><span class="dot"></span><span>FinOps</span><span class="ok">approved</span></li>
        <li><span class="dot"></span><span>Scoped key issued, with quota and expiry</span><span class="ok">recorded</span></li>
      </ul>
      <ul class="chain" aria-label="Example denied request">
        <li class="deny"><span class="dot"></span><span>Later request uses a model outside the approval</span><span class="ok">denied · reason logged</span></li>
      </ul>
      <p class="fn">Example. Levels and order are set by your organization.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap split even">
    <div class="stack-lg">
      <span class="tag">Reports</span>
      <h2>Answers for each person who asks.</h2>
      <p class="muted">Reports use metadata and aggregates, so they don't need copies of sensitive content.</p>
    </div>
    <div class="qs" aria-label="Questions Marshal answers">
      <div class="q"><b>CIO / IT</b><span>Which providers, connections and models are in use, by which projects?</span></div>
      <div class="q"><b>FinOps</b><span>What does it cost, by department and project, against quota and budget?</span></div>
      <div class="q"><b>Security / Audit</b><span>Who requested, who approved, when, and what was used under that key?</span></div>
      <div class="q"><b>Department heads</b><span>What is my team using, and is it within what we approved?</span></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap split">
    <div class="stack">
      <span class="tag">Marshal + Legwork</span>
      <h2>Bottom-up use, top-down view.</h2>
    </div>
    <p class="muted" style="font-size:1.08rem">Employees use Legwork to get more from the AI they already have. Marshal shows IT what it's used for and what it saves.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="pillars two" style="margin-top:0">
      <div class="pillar"><h3>Fits how your organization approves things</h3><p>Approval chains with as many levels as your process needs, in your order. Reports shaped to your departments and projects. Our implementation team configures it with you, without custom code forks.</p></div>
      <div class="pillar"><h3>Designed for standard interfaces</h3><p>Built around OpenAI- and Anthropic-compatible APIs, MCP and OpenTelemetry, so it governs the tools you already run instead of replacing them.</p></div>
    </div>
  </div>
</section>

<section class="surface">
  <div class="wrap split">
    <div class="stack">
      <span class="tag">Pilot phase</span>
      <h2>Start with a pilot in your environment.</h2>
    </div>
    <div class="stack">
      <p class="muted">A time-boxed pilot with acceptance criteria agreed up front. We run a small number at a time.</p>
      <div class="actions"><a class="btn primary" href="marshal-pilot.html">Talk to us about a pilot</a></div>
    </div>
  </div>
</section>
"""

PILOT = form_page_intro("marshal.html", "Marshal", "Lighthouse pilot program",
                        "A time-boxed Marshal pilot in your environment, with a clear path to production.") + """
<section>
  <div class="wrap split">
    <div class="stack-lg">
      <span class="tag">What a pilot includes</span>
      <div class="rows" style="margin-top:0">
        <div><h3>Your environment</h3><p>Runs on your infrastructure or private cloud, with real providers you choose.</p></div>
        <div><h3>Agreed criteria</h3><p>Acceptance criteria we agree and sign up front, so both sides know what success looks like.</p></div>
        <div><h3>A named sponsor</h3><p>One owner on your side who can decide on the next step.</p></div>
        <div><h3>A fixed time-box</h3><p>A set start and end date, with a clear path to production if it works.</p></div>
        <div><h3>Limited places</h3><p>We run a small number of pilots at a time, so each one gets our full attention.</p></div>
      </div>
    </div>
    <form class="form" data-subject="Marshal pilot conversation" novalidate>
      <div class="two-col">
        <div class="field"><label for="pi-name">Name</label><input id="pi-name" name="name" data-label="Name" required autocomplete="name"></div>
        <div class="field"><label for="pi-email">Work email</label><input id="pi-email" name="email" data-label="Email" type="email" required autocomplete="email"></div>
      </div>
      <div class="two-col">
        <div class="field"><label for="pi-company">Company</label><input id="pi-company" name="company" data-label="Company" required autocomplete="organization"></div>
        <div class="field"><label for="pi-role">Your role</label><input id="pi-role" name="role" data-label="Role" autocomplete="organization-title"></div>
      </div>
      <fieldset class="field"><legend>AI providers in use</legend>
        <div class="checks">
          <label><input type="checkbox" id="pi-p-openai" name="providers" value="OpenAI" data-label="Providers"> OpenAI</label>
          <label><input type="checkbox" id="pi-p-anthropic" name="providers" value="Anthropic"> Anthropic</label>
          <label><input type="checkbox" id="pi-p-google" name="providers" value="Google"> Google</label>
          <label><input type="checkbox" id="pi-p-aws" name="providers" value="AWS Bedrock"> AWS Bedrock</label>
          <label><input type="checkbox" id="pi-p-azure" name="providers" value="Azure OpenAI"> Azure OpenAI</label>
          <label><input type="checkbox" id="pi-p-self" name="providers" value="Self-hosted or other"> Self-hosted or other</label>
        </div></fieldset>
      <div class="two-col">
        <div class="field"><label for="pi-users">People using AI</label>
          <select id="pi-users" name="users" data-label="Users">
            <option value="">Choose one</option><option>Under 50</option><option>50 to 250</option><option>250 to 1,000</option><option>More than 1,000</option>
          </select></div>
        <div class="field"><label for="pi-deploy">Where would it run?</label>
          <select id="pi-deploy" name="deploy" data-label="Deployment">
            <option value="">Choose one</option><option>On-premises</option><option>Private cloud (VPC)</option><option>Not sure yet</option>
          </select></div>
      </div>
      <fieldset class="field"><legend>What matters most?</legend>
        <div class="checks">
          <label><input type="checkbox" id="pi-n-who" name="needs" value="Who uses what" data-label="Priorities"> Who uses what</label>
          <label><input type="checkbox" id="pi-n-cost" name="needs" value="Cost by department"> Cost by department</label>
          <label><input type="checkbox" id="pi-n-keys" name="needs" value="Approvals and keys"> Approvals and keys</label>
          <label><input type="checkbox" id="pi-n-audit" name="needs" value="Policy and audit"> Policy and audit</label>
        </div></fieldset>
      <div class="field"><label for="pi-notes">Anything else?</label><textarea id="pi-notes" name="notes" data-label="Notes"></textarea></div>
      <div class="actions"><button class="btn primary" type="submit">Request a pilot conversation</button></div>
      <p class="form-result" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
"""

SERVICES = """
<section class="page-hero">
  <div class="wrap stack-lg">
    <span class="tag">Managed IT &amp; implementation</span>
    <h1 class="sm">Managed IT, for more than 10 years.</h1>
    <p class="lede">Network, security, planning and licensing for organizations of every size, and now deploying AI that IT can govern.</p>
    <div class="actions"><a class="btn primary" href="contact.html">Talk to our team</a></div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="tag">Services</span>
    <div class="pillars">
      <div class="pillar"><h3>Network Management</h3><p>One dashboard for the health of your network.</p></div>
      <div class="pillar"><h3>IT Security</h3><p>Managed security services that lower overall risk and strengthen your security strategy.</p></div>
      <div class="pillar"><h3>IT Planning</h3><p>A proven method for strategic IT planning.</p></div>
      <div class="pillar"><h3>Technology Consulting</h3><p>Use your IT practices to reach your business goals.</p></div>
      <div class="pillar"><h3>License Management</h3><p>A clear, independent view of your licensing compliance.</p></div>
      <div class="pillar"><h3>Digital Strategy</h3><p>Technology choices grounded in a well-managed strategy.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap split">
    <div class="stack">
      <span class="tag">New</span>
      <h2>AI rollout &amp; implementation</h2>
    </div>
    <div class="stack-lg">
      <p class="muted" style="font-size:1.08rem">We deploy Marshal and Legwork in your environment, configure approval chains and reports to match how your organization works, and train your team. The people who install it are the people who support it.</p>
      <div class="actions"><a class="btn" href="marshal.html">About Marshal</a><a class="btn" href="legwork.html">About Legwork</a></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <div class="stack">
      <span class="tag">How we work</span>
      <h2>Your team stays in the process.</h2>
    </div>
    <div class="stack-lg">
      <p class="muted" style="font-size:1.08rem">We start from your business goals and your current IT, recommend what to change, and work alongside your team as priorities shift.</p>
      <div class="actions"><a class="btn primary" href="contact.html">Contact us</a></div>
    </div>
  </div>
</section>
"""

ABOUT = """
<section class="page-hero">
  <div class="wrap stack-lg">
    <span class="tag">About MKA Plus</span>
    <h1 class="sm">From running IT to building AI products.</h1>
    <p class="lede">MKA Plus started as a managed IT company in Saigon and has supported organizations from start-ups to mid-market for more than 10 years.</p>
  </div>
</section>

<section>
  <div class="wrap split">
    <div class="stack">
      <span class="tag">Why we build</span>
      <h2>We saw the same pattern at our clients.</h2>
    </div>
    <div class="prose">
      <p>AI arrives through individuals first: someone signs up, finds it useful, and tells a colleague. IT is asked to govern it later, usually when finance or audit starts asking questions.</p>
      <p>So we build for both ends. <strong>Legwork</strong> helps each person get more from the AI they already use. <strong>Marshal</strong> gives the organization one view of who uses which AI, for what, and at what cost.</p>
      <p>Our implementation team is the same team that has run our clients' systems for years.</p>
    </div>
  </div>
</section>

<section class="surface">
  <div class="wrap">
    <span class="tag">What we do</span>
    <div class="pillars" style="margin-top:24px">
      <div class="pillar"><h3>Legwork</h3><p>A research worker for Claude and ChatGPT that does the digging and reports back with sources.</p><p><a href="legwork.html">Learn more →</a></p></div>
      <div class="pillar"><h3>Marshal</h3><p>A private control plane that routes, approves and accounts for every AI request.</p><p><a href="marshal.html">Learn more →</a></p></div>
      <div class="pillar"><h3>Managed IT</h3><p>Network, security, planning, licensing and AI rollout.</p><p><a href="services.html">Learn more →</a></p></div>
    </div>
  </div>
</section>
"""

CONTACT = form_page_intro(None, None, "Contact us",
                          "Questions about Legwork, Marshal or our IT services. We reply by email.") + """
<section>
  <div class="wrap split">
    <dl class="contact-card">
      <dt>Email</dt><dd>hello@mkaplus.com</dd>
      <dt>Phone</dt><dd>+84 28 3620 5400</dd>
      <dt>Address</dt><dd>36/70/4 D2 Street, Ward 25<br>Binh Thanh District, Ho Chi Minh City, Vietnam</dd>
    </dl>
    <form class="form" data-subject="Website enquiry" novalidate>
      <div class="two-col">
        <div class="field"><label for="ct-name">Name</label><input id="ct-name" name="name" data-label="Name" required autocomplete="name"></div>
        <div class="field"><label for="ct-email">Email</label><input id="ct-email" name="email" data-label="Email" type="email" required autocomplete="email"></div>
      </div>
      <div class="two-col">
        <div class="field"><label for="ct-company">Company <span class="hint">(optional)</span></label><input id="ct-company" name="company" data-label="Company" autocomplete="organization"></div>
        <div class="field"><label for="ct-topic">Topic</label>
          <select id="ct-topic" name="topic" data-label="Topic" required>
            <option value="">Choose one</option><option>Legwork</option><option>Marshal</option><option>Managed IT services</option><option>Something else</option>
          </select></div>
      </div>
      <div class="field"><label for="ct-message">Message</label><textarea id="ct-message" name="message" data-label="Message" required></textarea></div>
      <div class="actions"><button class="btn primary" type="submit">Send message</button></div>
      <p class="form-result" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
"""

PRIVACY = """
<section class="page-hero">
  <div class="wrap stack-lg">
    <h1 class="sm">Privacy</h1>
    <p class="lede">How this website handles your information. Last updated 8 October 2026.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="prose">
      <h2>This website</h2>
      <ul>
        <li>We don't use cookies, analytics or advertising trackers on this site.</li>
        <li>Fonts are loaded from Google Fonts, so Google receives your IP address when a page loads.</li>
        <li>Our forms open your own email app with your details filled in. We receive only what you choose to send.</li>
      </ul>
      <h2>Emails you send us</h2>
      <p>We use what you send only to reply to you and to follow up on your request. We don't sell or share it. To have your messages deleted, email <strong>hello@mkaplus.com</strong>.</p>
      <h2>Legwork and Marshal</h2>
      <p>How Legwork handles your documents and keys is described on <a href="legwork-privacy.html">Your documents and keys</a>. Marshal runs in the customer's own environment under the customer's policies.</p>
    </div>
  </div>
</section>
"""

TERMS = """
<section class="page-hero">
  <div class="wrap stack-lg">
    <h1 class="sm">Terms</h1>
    <p class="lede">Terms for using this website. Last updated 8 October 2026.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="prose">
      <p>The content on this site is provided for general information about MKA Plus, its products and services. It may change without notice.</p>
      <p>Benchmark results describe internal tests under the conditions stated on the <a href="legwork-benchmark.html">benchmark page</a>. Your results may differ.</p>
      <p>Product names and features described as "coming", "pilot" or "early access" are not yet generally available.</p>
      <p>Terms for using Legwork and Marshal will be provided with each product before you start using it.</p>
      <p>Questions: <strong>hello@mkaplus.com</strong>.</p>
    </div>
  </div>
</section>
"""

NOTFOUND = """
<section class="page-hero" style="border-bottom:0">
  <div class="wrap stack-lg">
    <span class="tag">404</span>
    <h1 class="sm">This page isn't here.</h1>
    <p class="lede">It may have moved when we rebuilt the site.</p>
    <div class="actions"><a class="btn primary" href="index.html">Go to the home page</a><a class="btn" href="contact.html">Contact us</a></div>
  </div>
</section>
"""

PAGES = [
    ("index.html", "MKA Plus", "Legwork hands the digging to a low-cost worker so Claude or ChatGPT can keep the thinking. Marshal governs AI use across your organization.", HOME, None, False),
    ("legwork.html", "Legwork | MKA Plus", "A research worker for Claude and ChatGPT. It searches, reads and cross-checks your documents and reports back with sources.", LEGWORK, "legwork.html", False),
    ("legwork-benchmark.html", "Legwork benchmark | MKA Plus", "Internal benchmark: how much work moves off the reasoning model when it delegates, and what happens to answer quality.", BENCH, "legwork.html", False),
    ("legwork-privacy.html", "Your documents and keys | Legwork", "Who reads your documents when you use Legwork, and who pays for model usage.", PRIV_LW, "legwork.html", False),
    ("early-access.html", "Early access | Legwork", "Request early access to Legwork.", EARLY, "legwork.html", True),
    ("marshal.html", "Marshal | MKA Plus", "Route, approve and account for every AI request. A private control plane for enterprise AI.", MARSHAL, "marshal.html", False),
    ("marshal-pilot.html", "Pilot program | Marshal", "Request a time-boxed Marshal pilot in your environment.", PILOT, "marshal.html", True),
    ("services.html", "Managed IT services | MKA Plus", "Network, security, planning, licensing and AI rollout from MKA Plus.", SERVICES, "services.html", False),
    ("about.html", "About | MKA Plus", "MKA Plus: from managed IT to building AI products.", ABOUT, "about.html", False),
    ("contact.html", "Contact | MKA Plus", "Contact MKA Plus about Legwork, Marshal or managed IT services.", CONTACT, "contact.html", True),
    ("privacy.html", "Privacy | MKA Plus", "How the MKA Plus website handles your information.", PRIVACY, None, False),
    ("terms.html", "Terms | MKA Plus", "Terms for using the MKA Plus website.", TERMS, None, False),
    ("404.html", "Page not found | MKA Plus", "Page not found.", NOTFOUND, None, False),
]

for args in PAGES:
    page(*args)

urls = [p[0] for p in PAGES if p[0] != "404.html"]
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    loc = BASE if u == "index.html" else BASE + u
    sm.append(f"  <url><loc>{loc}</loc><lastmod>2026-10-08</lastmod></url>")
sm.append("</urlset>")
(OUT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
print("wrote", len(PAGES), "pages")
