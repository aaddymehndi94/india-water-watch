import { release } from '../../lib/publication';
export const prerender = true;
const fields = ['id','geographyId','metricId','seriesId','value','unit','status','periodStart','periodEnd','periodKind','periodPrecision','cutoffConvention','baselineId','sourceId','evidenceIds','claimId'] as const;
function csv(value: unknown) {
  let text = value === null || value === undefined ? '' : Array.isArray(value) ? JSON.stringify(value) : String(value);
  if (typeof value !== 'number' && /^[=+@\-]/.test(text.trimStart())) text = `'${text}`;
  return `"${text.replaceAll('"','""')}"`;
}
export function GET() {
  const rows = release.observations.filter(o => release.claims.some(c => c.id === o.claimId && ['verified','attributed','corrected'].includes(c.status)) && release.sources.some(s => s.id === o.sourceId) && Number.isFinite(o.value));
  const body = [fields.join(','), ...rows.map(row => fields.map(field => csv(row[field] ?? '')).join(','))].join('\r\n') + '\r\n';
  return new Response(body, {headers:{'content-type':'text/csv; charset=utf-8','content-disposition':'attachment; filename="india-water-watch-observations.csv"'}});
}
