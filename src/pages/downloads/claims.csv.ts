import { release } from '../../lib/publication';
export const prerender = true;
const fields = ['id','text','status','kind','geographyIds','observationIds','evidenceIds','reviewedAt','limitations'] as const;
function csv(value: unknown) {
  let cell = value === null || value === undefined ? '' : typeof value === 'object' ? JSON.stringify(value) : String(value);
  if (/^[=+@\-]/.test(cell.trimStart())) cell = `'${cell}`;
  return `"${cell.replaceAll('"','""')}"`;
}
export function GET() {
  const rows = release.claims.filter(c => ['verified','attributed','corrected'].includes(c.status));
  const body = [fields.join(','), ...rows.map(row => fields.map(field => csv((row as unknown as Record<string, unknown>)[field] ?? '')).join(','))].join('\r\n') + '\r\n';
  return new Response(body, { headers: { 'content-type': 'text/csv; charset=utf-8', 'content-disposition': 'attachment; filename="india-water-watch-claims.csv"' } });
}
