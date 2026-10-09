import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';
import { taxonomy } from './data/taxonomy';

const ids = (values: Record<string, string>) => Object.keys(values) as [string, ...string[]];
const unique = (values: string[]) => new Set(values).size === values.length;
const posts = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string().trim().min(1),
    summary: z.string().trim().min(1),
    publishDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).refine((value) => {
      const date = new Date(`${value}T00:00:00Z`);
      return !Number.isNaN(date.valueOf()) && date.toISOString().slice(0, 10) === value;
    }, 'Use a valid calendar date, YYYY-MM-DD'),
    product: z.enum(ids(taxonomy.product)),
    type: z.enum(ids(taxonomy.type)),
    topics: z.array(z.enum(ids(taxonomy.topic))).min(1).refine(unique, 'Duplicate topics'),
    tags: z.array(z.enum(ids(taxonomy.tag))).refine(unique, 'Duplicate tags'),
    status: z.enum(['draft', 'published']),
  }),
});
export const collections = { posts };
