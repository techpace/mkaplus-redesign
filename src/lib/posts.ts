import { getCollection, type CollectionEntry } from 'astro:content';
import { isPublished, sortPosts, matchesTerm } from './publication.mjs';
export type Post = CollectionEntry<'posts'>;
export { matchesTerm };
export async function publishedPosts(): Promise<Post[]> {
  const posts = await getCollection('posts');
  for (const post of posts) {
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(post.id)) {
      throw new Error(`Invalid post filename: ${post.id}. Use lowercase kebab-case.`);
    }
  }
  return sortPosts(posts.filter((post) => isPublished(post.data)));
}
export const postUrl = (post: Post) => `/blog-${post.id}.html`;
export function humanDate(date: string) {
  return new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' })
    .format(new Date(`${date}T00:00:00Z`));
}
export function relatedPosts(post: Post, all: Post[]): Post[] {
  const score = (other: Post) =>
    Number(other.data.product === post.data.product) +
    other.data.topics.filter((id) => post.data.topics.includes(id)).length * 2 +
    other.data.tags.filter((id) => post.data.tags.includes(id)).length;
  return all.filter((other) => other.id !== post.id && score(other) > 0)
    .sort((a, b) => score(b) - score(a)).slice(0, 3);
}
