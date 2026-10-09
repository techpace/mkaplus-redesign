import { defineConfig } from 'astro/config';
import { readFileSync } from 'node:fs';
import sitemap from '@astrojs/sitemap';
import { satteri } from '@astrojs/markdown-satteri';

export default defineConfig({
  site: 'https://www.mkaplus.com',
  output: 'static',
  markdown: { processor: satteri({ features: { smartPunctuation: false } }) },
  build: { format: 'file' },
  integrations: [sitemap({
    serialize(item) {
      // File output keeps the site's existing .html canonical URLs.
      const url = new URL(item.url);
      if (url.pathname !== '/' && !url.pathname.endsWith('.html')) url.pathname += '.html';
      const file = new URL(`./dist${url.pathname === '/' ? '/index.html' : url.pathname}`, import.meta.url);
      if (readFileSync(file, 'utf8').includes('name="robots" content="noindex"')) return undefined;
      return { ...item, url: url.href };
    },
  })],
});
