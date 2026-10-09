# MKA Plus — Legwork and Marshal website

## Current decision (9 October 2026)

This project uses **Astro with Markdown content stored in Git**. AI agents write,
publish and maintain the articles. Product, article type, topic and tag classification
does not require a separate CMS. There is no CMS admin, content database or publishing API.

Astro builds static HTML into `dist/`; nginx serves that output. Existing page design,
copy, diagrams, benchmark charts, form behavior and `.html` URLs are retained. Marketing pages now include light, one-time motion; article pages stay still.

Reconsider a CMS when concurrent API writers, editorial permissions, a human editing
interface or content shared across multiple channels becomes a real requirement.
Astro can remain the website frontend if a CMS is introduced later.

## Local development

Requires Node **22.12 or newer** (the lockfile pins dependencies).

```sh
npm ci
npm run dev
npm run build
npm test
npm run preview
```

`build` runs Astro's type/content checks before generating HTML. `test` checks the
output, internal links and publication isolation using temporary content fixtures.
Run `build` before `test`. The development server is for local authoring; the public
deployment uses only `dist/`.

## Source layout

```text
src/layouts/SiteLayout.astro       Shared document, metadata, header and footer
src/components/                   Navigation, blog list and combined filters
src/content/site-pages/*.html     Authored HTML fragments for product/static pages
src/data/pages.json               Static page titles, descriptions, active nav, forms
src/content/posts/*.md            Blog content and frontmatter
src/content.config.ts             Required fields and taxonomy validation
src/data/taxonomy.ts               Stable classification IDs and display labels
src/lib/                          Publication rules, sorting and related articles
src/pages/                        Astro routes, including existing .html URLs
public/assets/site.css            Original design plus blog controls
public/assets/forms.js            Original form behavior
docs/CONTENT_GUIDE.md              AI authoring and publishing instructions
AGENTS.md                         Project rules for agents
dist/                             Generated output; never hand-edit or commit
```

The former `build_site.py` and generated HTML in the repository root have been
replaced by these sources. Do not run the former Python generator or edit deployed
HTML. For small product-page edits, change the matching HTML fragment; for shared
changes, edit the layout/components. `src/data/pages.json` controls page metadata.

Original messaging reference: `docs/website/MKAPLUS_SITEMAP_AND_MESSAGING.md` in
`techpace/my-harness`. Claims about Legwork/Marshal must still be checked against
the product's current release state.

## Blog

Read [the content guide](docs/CONTENT_GUIDE.md) before adding a post. Each article has
one product and type, one or more topics, and zero or more tags. The schema rejects
unknown classification IDs, duplicate topics/tags, missing fields and invalid dates.

- `/blog.html`: all published posts, with combined product/type/topic/tag filters.
- `/blog-<slug>.html`: article, taxonomy links and related posts.
- `/blog/product/<id>.html`, `/blog/type/<id>.html`, `/blog/topic/<id>.html`,
  `/blog/tag/<id>.html`: static archive pages, usable without JavaScript.

Combined filters use browser JavaScript and store their values in the URL query.
Without JavaScript, the full index and individual archives remain available.
The current index renders all published posts. Pagination or a search index can be
added when measured page size warrants it; a CMS is not required for either.

Only `status: published` articles whose `publishDate` has arrived are generated.
Dates start at **00:00 UTC**. Future-dated articles require a new build/deploy when
their date arrives. There is no running scheduler in this project. Drafts and future
articles have no public route and do not appear in archives, related posts or sitemaps.
Draft source is still visible to anyone with access to this Git repository; this
repository is public, so it is not a place for confidential drafts.

## Motion (9 October 2026)

Home, Legwork, Marshal, Services and About have a short staggered hero entrance,
one-time section reveals, and subtle hover accents. The Legwork flow arrows/nodes
and Marshal approval steps animate once when visible. No looping animation,
parallax, scroll hijacking or animation dependency is used.

`src/components/Motion.astro` uses IntersectionObserver and the browser's Web
Animations API. Pages opt in through the layout's `motion` prop. HTML/CSS never
hide content pending JavaScript. Missing browser APIs or disabled JavaScript leave
the page readable. Reduced-motion preferences skip/cancel these animations, and
keyboard focus cancels any animation on the focused block. Blog, legal, form and
benchmark detail pages remain still, including article charts.

Verified on Chrome desktop/mobile: one-time playback, final content visibility,
reduced-motion startup and live cancellation, still editorial pages, keyboard focus,
no-JavaScript reading and missing-API fallback. Astro build and four site tests pass.

To adjust timing, edit the component; hover styles are at the end of
`public/assets/site.css`. Keep movement small and single-run, retain reduced-motion
support, and check mobile, keyboard and no-JavaScript behavior after changing it.

## Forms

Forms retain the current behavior: submission opens the visitor's email app with
details addressed to `hello@mkaplus.com`. A `data-endpoint` can be configured for a
real handler later. This migration does not add a form backend.

## Netlify deployment

The live domain currently points to the Netlify site `glistening-khapse-b69d57`.
`netlify.toml` runs `npm run build && npm test` using Node 22.22.2 and publishes only
`dist/`. Pretty URL post-processing is disabled to preserve `.html` canonicals.
The production branch is controlled in Netlify's site settings; this repository's
configuration does not change that setting.

For an authorized direct production deploy of the tested local output:

```sh
npm run build
npm test
netlify deploy --prod --dir=dist --site=glistening-khapse-b69d57
```

Authenticate through Netlify's CLI/browser login before deploying. Do not commit
credentials. Verify the live homepage, blog filters, articles, assets and old routes
after publication. Production deployment status must be verified from the host,
not inferred from a local build or Git push.

## Alternative deployment on the HP Gen8 (nginx)

Build in a checkout outside the web root, then deploy **only the contents of `dist/`**.
The previous `git pull` directly in the served repository root is no longer sufficient.
Use an atomic release switch to avoid serving half of a copied build:

```sh
# In the project checkout, with production dependencies already installed:
npm ci
npm run build
npm test

# Adapt these paths to the actual server setup before running:
release_dir="/var/www/mkaplus/releases/$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$release_dir"
cp -a dist/. "$release_dir/"
ln -s "$release_dir" /var/www/mkaplus/current.next
mv -Tf /var/www/mkaplus/current.next /var/www/mkaplus/current
```

The `current` path must be a release symlink; do not replace an existing directory
without preparing the deployment layout. Keep the previous release for rollback.
Switch `current` back to that release if needed. These commands are documentation,
not a record of a production deployment.

```nginx
server {
    listen 443 ssl http2;
    server_name www.mkaplus.com;
    root /var/www/mkaplus/current;
    index index.html;

    location = /our-services { return 301 /services.html; }
    location = /our-services.html { return 301 /services.html; }
    location = /our-client { return 301 /; }
    location = /our-client.html { return 301 /; }
    location = /10853299-1655312208.5223.html { return 404; }
    location ~ ^/\. { return 404; }
    location ~ \.(py|md|ts|astro)$ { return 404; }
    location ~ ^/_(headers|redirects)$ { return 404; }
    location /assets/ { expires 7d; add_header Cache-Control "public"; }
    location / { try_files $uri $uri.html =404; }
    error_page 404 /404.html;
}
server { listen 80; server_name mkaplus.com www.mkaplus.com; return 301 https://www.mkaplus.com$request_uri; }
server { listen 443 ssl http2; server_name mkaplus.com; return 301 https://www.mkaplus.com$request_uri; }
```

Configure existing TLS certificates as on the current server. Hosts that understand
Netlify-style `_redirects`/`_headers` can use the copied files in `dist/`. Verify old
extensionless URLs on the actual host; Astro's local preview serves the `.html` routes.
Astro generates `sitemap-index.xml` and `sitemap-0.xml`. `/sitemap.xml` is retained as
a compatibility sitemap index. `robots.txt` points to `sitemap-index.xml`.

## Migration verification (9 October 2026)

- Astro check: no errors, warnings or hints; 37 static HTML pages generated.
- Four automated tests pass: page/assets integrity, internal links, canonical sitemap,
  and publication/schema fixtures (drafts, future posts, invalid topics and dates).
- Chrome: combined filters, URL state, reset, mobile menu and no-JavaScript archive
  navigation verified. Eight key pages checked at 390px width with no page overflow.
- Main page copy and all three article bodies match the original redesign branch;
  original CSS is retained and form JavaScript is unchanged.
- Implementation is local; production deployment remains pending; the motion follow-up is implemented locally.

## Before launch

- [ ] Trademark and domain check for Legwork and Marshal.
- [ ] Check current document-format support against website claims.
- [ ] Publish Legwork storage location, retention and isolation details before early access opens.
- [ ] Terms reviewed.
- [ ] If analytics or cookies are added later, update `privacy.html`.
- [ ] Add the open-source section when the core repo is public.
- [ ] Configure and verify the build/deploy process on the actual host.
