// @ts-ignore Node built-ins are available during Astro's build; root toolchain owns @types/node.
import { existsSync, readFileSync } from 'node:fs';
// @ts-ignore Node built-ins are available during Astro's build; root toolchain owns @types/node.
import { resolve } from 'node:path';
import registry from '../../references/source_registry.json';
import approvedGeographies from '../../data/approved/geographies.json';

export type Geography = { id: string; name: string; type: string; slug: string; code?: string; version?: string };
export type Observation = { id: string; geographyId: string; metricId: string; value: number | null; unit: string; periodStart: string; periodEnd: string; sourceId: string; claimId: string; seriesId?: string; periodKind?: string; periodPrecision?: string; cutoffConvention?: string; baselineId?: string | null; status?: string; evidenceIds?: string[] };
export type Source = { id: string; title: string; publisher: string; url?: string | null; entry_url?: string | null; observedThrough?: string | null; validityEnd?: string | null; publicationDate?: string | null; retrievedAt?: string | null; locator?: string; sha256?: string | null; access_status?: string; access_notes?: string; checked_on?: string | null; production_approved?: boolean; topics?: string[] };
export type Claim = { id: string; text: string; evidenceIds: string[]; status: string; reviewedAt?: string; limitations?: string[] };
type Publication = { releaseId: string; reviewedAt: string; observations: Observation[]; geographies: Geography[]; sources: Source[]; claims: Claim[] };

const path = resolve('data/approved/publication.json');
const empty: Publication = { releaseId: 'No approved release', reviewedAt: '', observations: [], geographies: [], sources: [], claims: [] };
let publication: Publication = empty;
if (existsSync(path)) {
  const parsed: unknown = JSON.parse(readFileSync(path, 'utf8'));
  if (parsed && typeof parsed === 'object' && 'releaseId' in parsed && 'reviewedAt' in parsed && 'observations' in parsed && 'geographies' in parsed && 'sources' in parsed && 'claims' in parsed) {
    const p = parsed as Publication;
    if ([p.observations, p.geographies, p.sources, p.claims].every(Array.isArray) && typeof p.releaseId === 'string' && typeof p.reviewedAt === 'string') publication = p;
  }
}
for (const geo of publication.geographies) {
  if (['state', 'union_territory', 'ut'].includes(geo.type) && geo.id.startsWith('india:')) geo.slug = geo.id.slice('india:'.length);
}
export const release = publication;
if (publication.geographies.length === 0) {
  publication.geographies = approvedGeographies.filter(g => ['state', 'union_territory', 'ut'].includes(g.kind)).map(g => ({
    id: g.id, name: g.name, type: g.kind, slug: g.id.split(':').at(-1) || g.id,
    version: g.boundary_version,
  }));
}
export const discoverySources: Source[] = registry;
export const publishedSources = publication.sources;
export const sourceById = (id: string) => publication.sources.find((source) => source.id === id);
export const observationsFor = (geographyId: string) => publication.observations.filter((row) => row.geographyId === geographyId && Number.isFinite(row.value) && sourceById(row.sourceId) && publication.claims.some((claim) => claim.id === row.claimId && ['verified','attributed','corrected'].includes(claim.status)));
export const url = (path: string) => `${import.meta.env.BASE_URL.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;
