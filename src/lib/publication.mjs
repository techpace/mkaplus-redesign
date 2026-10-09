// Publication dates mean midnight UTC. A future date is a scheduled post.
export function isPublished(data, now = new Date()) {
  return data.status === 'published' && new Date(`${data.publishDate}T00:00:00Z`) <= now;
}

export function sortPosts(posts) {
  return [...posts].sort((a, b) =>
    b.data.publishDate.localeCompare(a.data.publishDate) || a.id.localeCompare(b.id));
}

export function matchesTerm(post, kind, id) {
  if (kind === 'topic') return post.data.topics.includes(id);
  if (kind === 'tag') return post.data.tags.includes(id);
  return post.data[kind] === id;
}
