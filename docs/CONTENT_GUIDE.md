# AI content workflow

## Decision and source of truth

As of 9 October 2026, content lives in Git as Markdown and Astro generates the website.
There is no separate CMS. Do not create a database, admin UI or publishing service
without a new requirement. The current taxonomy is `src/data/taxonomy.ts`, and
`src/content.config.ts` enforces it.

## Add an article

1. Create `src/content/posts/<slug>.md`. Use a stable lowercase kebab-case filename;
   the public URL will be `/blog-<slug>.html`. Do not add a separate `slug` field.
2. Copy `docs/templates/post.md` as the starting point. Keep `status: draft` while writing.
3. Select existing classification IDs. Check the actual product release and benchmark
   evidence before making claims. Preserve distinctions between built/tested, pilot,
   and publicly available behavior.
4. Use ordinary Markdown for prose. Existing figures use raw HTML to preserve their
   layout and accessibility. Raw HTML is trusted executable website source: do not
   paste scripts or unreviewed embeds into posts.
5. Put images in `public/assets/posts/<slug>/`. Reference them as
   `/assets/posts/<slug>/image.webp`, with useful alt text. Use root-relative internal
   links so they also work from nested taxonomy archives.
6. Build and verify. When ready to publish, change the status to `published`, set the
   intended date, run `npm run build` and `npm test`, and inspect the preview.
7. Commit source and lockfile changes together where relevant. Deploy only after
   authorization, following the README's build/deploy instructions.

## Frontmatter fields

| Field | Meaning | Rule |
| --- | --- | --- |
| `title` | Visible article title | Nonempty string |
| `summary` | List excerpt and SEO description | Nonempty string |
| `publishDate` | Publication date | Quoted `YYYY-MM-DD`, valid calendar date |
| `product` | Primary product | One ID from `taxonomy.product` |
| `type` | Article format | One ID from `taxonomy.type` |
| `topics` | Main subject areas | At least one ID from `taxonomy.topic`, no duplicates |
| `tags` | Specific details | IDs from `taxonomy.tag`, may be empty, no duplicates |
| `status` | Publication state | `draft` or `published` |

Keep the date quoted: `publishDate: "2026-10-09"`. Publication starts at midnight
UTC on that date. Future dates are filtered until a build runs on or after the date.
Setting the date does not schedule a build. No scheduler has been installed.

The filename owns the URL. Renaming a published file needs a redirect on both nginx
and `_redirects`; otherwise external links will break. Articles are ordered by date
descending, then slug for a stable tie-break. Related posts use shared topics, tags
and product and include only published content.

## Classification

- Product answers “which product is this mainly about?”: `legwork`, `marshal`, `general`.
- Type answers “what kind of article?”: build note, engineering, benchmark, guide,
  product update, case study.
- Topic answers “what subject does this cover?”: e.g. privacy or performance.
- Tag adds a specific detail: e.g. audit-log or model-costs.

Use the IDs in `src/data/taxonomy.ts`, not display labels in frontmatter. Before adding
an ID, check for an existing synonym. Add a new ID and human-readable label in that
file only when the distinction is useful. IDs become URLs, so keep them stable.
Do not generate near-duplicate tags for every article. If an ID must change, migrate
every article that uses it and redirect the old archive URL.

## Drafts and previews

Draft and future content is excluded from the dev/production article routes, index,
archive listings, related articles and sitemap. To inspect its rendered appearance,
use a temporary local checkout, set it to `published` with a date that has arrived,
run the preview, then discard that temporary change. Do not accidentally publish
that preview change. A private draft preview service is not included.

This is a public GitHub repository. Draft exclusion prevents website publication,
not access to committed source. Keep confidential writing outside the public repo.

## Verification

```sh
npm run build
npm test
npm run preview
```

Check the article URL, metadata, prose, figures, links, mobile layout and taxonomy
archives. Try combined filters on `/blog.html`; selections are retained in the URL.
Archive pages and the full article index remain usable without JavaScript.

The automated suite checks all local HTML links/assets, publication isolation,
schema rejection of unknown taxonomy IDs, old article URLs and sitemap exclusion.
Tests create isolated temporary fixtures and leave the real content unchanged.
