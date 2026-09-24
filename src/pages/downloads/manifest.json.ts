import { release } from '../../lib/publication';
export const prerender = true;
export function GET() {
  return new Response(JSON.stringify({project:'India Water Watch',releaseId:release.releaseId,reviewedAt:release.reviewedAt || null,observationCount:release.observations.length,claimCount:release.claims.length,sourceCount:release.sources.length,methodology:'See methodology/ in this release',meaning:'An observation period is attached to each row; this manifest date is not an observation date.'},null,2),{headers:{'content-type':'application/json; charset=utf-8'}});
}
