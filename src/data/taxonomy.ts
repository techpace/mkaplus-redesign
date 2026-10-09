// Stable IDs are used in frontmatter and URLs. Labels are for readers.
export const taxonomy = {
  product: { legwork: 'Legwork', marshal: 'Marshal', general: 'MKA Plus' },
  type: {
    'build-note': 'Build notes', engineering: 'Engineering', benchmark: 'Benchmarks',
    guide: 'Guides', 'product-update': 'Product updates', 'case-study': 'Case studies',
  },
  topic: {
    'ai-workflows': 'AI workflows', privacy: 'Privacy', security: 'Security',
    performance: 'Performance', governance: 'AI governance', 'managed-it': 'Managed IT',
  },
  tag: {
    research: 'Research', 'model-costs': 'Model costs', evaluation: 'Evaluation',
    'audit-log': 'Audit log', 'document-access': 'Document access',
  },
} as const;
export type TaxonomyKind = keyof typeof taxonomy;
export function label(kind: TaxonomyKind, id: string): string {
  const labels: Record<string, string> = taxonomy[kind];
  return labels[id] ?? id;
}
export function archiveUrl(kind: TaxonomyKind, id: string) {
  return `/blog/${kind}/${id}.html`;
}
