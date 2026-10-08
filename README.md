# mkaplus.com — static site

Plain HTML + one CSS file. No build step is needed to deploy: the web server serves this folder as is.

```text
index.html                 Home
legwork.html               Legwork
legwork-benchmark.html     Benchmark (methodology + numbers)
legwork-privacy.html       Legwork: your documents and keys
early-access.html          Legwork early access form
marshal.html               Marshal
marshal-pilot.html         Marshal pilot form
services.html              Managed IT services
blog.html                  Blog index (posts are defined in POSTS in build_site.py)
blog-<slug>.html           One page per blog post, served at /blog-<slug>
about.html, contact.html, privacy.html, terms.html, 404.html
assets/site.css            All styles (colors are tokens at the top; light + dark)
assets/forms.js            Form handling
assets/favicon.svg
sitemap.xml, robots.txt
```

Content source: `docs/website/MKAPLUS_SITEMAP_AND_MESSAGING.md` in `techpace/my-harness`.

`10853299-1655312208.5223.html` is kept from the previous site (likely a verification file).

## Editing

- Small text edits: edit the `.html` file directly.
- Header, footer or a block shared by several pages: edit `build_site.py`, then run
  `python3 build_site.py .` from this folder. It rewrites every page and `sitemap.xml`, so do not mix
  hand edits and regeneration without copying the hand edits into the script first.

## Forms

There is no server code. `assets/forms.js` opens the visitor's email app with the form filled in, addressed to
`hello@mkaplus.com`. To receive submissions on the server instead, add a handler (for example a small endpoint
on the Gen8) and set `data-endpoint="/api/forms"` on each `<form>`; the script then POSTs the form data there.

## Deploy on the HP Gen8 (nginx example)

```nginx
server {
    listen 443 ssl http2;
    server_name www.mkaplus.com;
    root /var/www/mkaplus;   # this repo, cloned from git
    index index.html;

    # old site URLs
    location = /our-services.html { return 301 /services.html; }
    location = /our-client.html   { return 301 /; }

    location ~ (\.(py|md)$|^/_redirects$|^/\.git) { return 404; }   # keep build files and git data private
    location /assets/ { expires 7d; add_header Cache-Control "public"; }
    location / { try_files $uri $uri.html =404; }
    error_page 404 /404.html;
}
server { listen 80; server_name mkaplus.com www.mkaplus.com; return 301 https://www.mkaplus.com$request_uri; }
server { listen 443 ssl http2; server_name mkaplus.com; return 301 https://www.mkaplus.com$request_uri; }
```

Deploy = `git pull` in the web root. TLS certificate via certbot or similar.

## Before launch

- [ ] Trademark and domain check for Legwork and Marshal.
- [ ] Legwork reads Word, PDF, spreadsheets and slides (the site claims every document type; the 04A prototype reads `.md`/`.txt` only).
- [ ] Legwork privacy page: publish storage location, retention and isolation details before early access opens (the page promises this).
- [ ] Terms reviewed.
- [ ] If analytics or cookies are added later, update `privacy.html` (it currently says there are none).
- [ ] Add the open-source section when the core repo is public.
