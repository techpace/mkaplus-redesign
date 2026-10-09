import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync, readdirSync, mkdtempSync, cpSync, symlinkSync, writeFileSync, rmSync } from 'node:fs';
import { join, resolve, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');
const read = (path) => readFileSync(path, 'utf8');
const walk = (path) => readdirSync(path, { withFileTypes: true }).flatMap((item) =>
  item.isDirectory() ? walk(join(path, item.name)) : [join(path, item.name)]);

test('existing pages, charts, forms and metadata are present in the built site', () => {
  assert.ok(existsSync(dist), 'Run npm run build before npm test');
  const pages = JSON.parse(read(join(root, 'src/data/pages.json')));
  for (const page of pages) {
    const html = read(join(dist, `${page.slug}.html`));
    assert.match(html, /<main>/);
    assert.match(html, /rel="canonical"/);
    if (page.forms) assert.match(html, /src="\/assets\/forms.js"/);
  }
  for (const slug of ['why-we-built-legwork', 'what-legwork-wont-read', 'legwork-benchmark-costs']) {
    const html = read(join(dist, `blog-${slug}.html`));
    assert.match(html, /property="og:type" content="article"/);
    assert.match(html, /class="post-fig"/);
    assert.match(html, /Related notes/);
  }
  const blog = read(join(dist, 'blog.html'));
  assert.match(blog, /data-blog-filters/);
  assert.match(blog, /data-post/);
  assert.match(blog, /Browse by product/);
});

test('all generated internal links and assets resolve, including nested archives', () => {
  for (const file of walk(dist).filter((path) => path.endsWith('.html'))) {
    const html = read(file);
    for (const match of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
      const value = match[1];
      if (/^(?:[a-z]+:|#|\/\/)/i.test(value)) continue;
      const url = new URL(value.replaceAll('&amp;', '&'), `https://www.mkaplus.com/${file.slice(dist.length + 1)}`);
      const path = join(dist, decodeURIComponent(url.pathname));
      assert.ok(existsSync(path) || existsSync(join(path, 'index.html')), `${file}: broken ${value}`);
    }
  }
});

test('sitemap URLs match canonical URLs and omit empty noindex archives', () => {
  const sitemap = read(join(dist, 'sitemap-0.xml'));
  assert.doesNotMatch(sitemap, /404|blog\/product\/marshal/);
  for (const match of sitemap.matchAll(/<loc>(.*?)<\/loc>/g)) {
    const url = new URL(match[1]);
    const html = read(join(dist, url.pathname === '/' ? 'index.html' : url.pathname));
    assert.ok(html.includes(`rel="canonical" href="${url.href}"`), `Canonical differs: ${url.href}`);
  }
});

test('draft/future articles never enter output and unknown taxonomy fails the build', { timeout: 120000 }, () => {
  const fixture = mkdtempSync(join(tmpdir(), 'mkaplus-content-test-'));
  const runBuild = () => execFileSync(process.execPath, [join(root, 'node_modules/astro/bin/astro.mjs'), 'build'], {
    cwd: fixture, encoding: 'utf8', stdio: 'pipe', timeout: 60000,
  });
  const post = (title, status, date, topic = 'privacy') => `---
title: "${title}"
summary: "Private publication fixture"
publishDate: "${date}"
product: legwork
type: engineering
topics: [${topic}]
tags: [audit-log]
status: ${status}
---

PRIVATE-FIXTURE-BODY-${title}
`;
  try {
    for (const file of ['src', 'public', 'astro.config.mjs', 'tsconfig.json', 'package.json'])
      cpSync(join(root, file), join(fixture, file), { recursive: true });
    symlinkSync(join(root, 'node_modules'), join(fixture, 'node_modules'), 'dir');
    const content = join(fixture, 'src/content/posts');
    writeFileSync(join(content, 'private-draft.md'), post('PRIVATE-DRAFT-TITLE', 'draft', '2020-01-01'));
    writeFileSync(join(content, 'private-future.md'), post('PRIVATE-FUTURE-TITLE', 'published', '2999-01-01'));
    runBuild();
    const output = join(fixture, 'dist');
    for (const slug of ['private-draft', 'private-future']) assert.ok(!existsSync(join(output, `blog-${slug}.html`)));
    for (const file of walk(output).filter((path) => /\.(html|xml|js|json)$/.test(path))) {
      assert.doesNotMatch(read(file), /PRIVATE-(?:DRAFT|FUTURE|FIXTURE)/, `${file}: private content leaked`);
    }
    writeFileSync(join(content, 'invalid-topic.md'), post('INVALID', 'published', '2020-01-01', 'typo-topic'));
    assert.throws(runBuild, (error) => /topics|typo-topic/.test(`${error.stdout} ${error.stderr}`), 'Unknown taxonomy must fail');
    rmSync(join(content, 'invalid-topic.md'));
    writeFileSync(join(content, 'invalid-date.md'), post('INVALID-DATE', 'published', '2026-02-30'));
    assert.throws(runBuild, (error) => /publishDate|calendar date/.test(`${error.stdout} ${error.stderr}`), 'Invalid dates must fail');
  } finally {
    rmSync(fixture, { recursive: true, force: true });
  }
});
