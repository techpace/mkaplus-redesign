# Agent instructions — MKA Plus website

## Current architecture

Read `README.md` and `docs/CONTENT_GUIDE.md` before modifying the website.
The current choice is Astro + Markdown in Git, with static HTML deployment.
AI agents own content creation and management. A separate CMS is deferred.

## Editing rules

- Work from the Legwork/Marshal redesign branch, not the legacy `main` website.
- Edit `src/` for content/templates and `public/` for copied assets.
- Blog articles belong in `src/content/posts/*.md`, with required frontmatter.
- Reuse the IDs in `src/data/taxonomy.ts`; avoid synonyms and duplicate labels.
- Preserve published slugs and existing `.html` URLs. Add redirects when changing them.
- Keep product claims tied to source evidence and owner-approved positioning. For the
  Legwork knowledge positioning, follow the README: describe features directly
  without availability labels, and keep research benchmark claims separate from wiki/RAG.
- Keep the original site design and form behavior unless the task asks to change them.
- Do not edit `dist/`, bring back `build_site.py`, or hand-maintain generated blog indexes.
- Deploy only `dist/`, never the repository root or Markdown sources.
- Do not add a CMS, database, scheduler, form backend or motion system without a request.
- Do not add lesson files or agent memory directories.

## Publication and verification

Use `status: draft` while authoring. Only published posts whose date has arrived are
public. A future publication date needs a later build/deploy; no scheduler exists.
Public Git source is not a confidential draft store.

Before reporting completion, run `npm run build` and `npm test`. For UI changes,
check desktop/mobile and no-JavaScript behavior as appropriate. Document any
remaining deployment or verification limit plainly. Do not push, publish or change
production infrastructure unless authorized in the task.
