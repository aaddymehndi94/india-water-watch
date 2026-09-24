import { release } from '../../lib/publication';
export const prerender = true;
const fields = ['id','title','publisher','url','observedThrough','validityEnd','publicationDate','retrievedAt','locator','sha256'] as const;
function csv(value: unknown) {
  let cell = value === null || value === undefined ? '' : typeof value === 'object' ? JSON.stringify(value) : String(value);
  if (/^[=+@\-]/.test(cell.trimStart())) cell = `'${cell}`;
  return `"${cell.replaceAll('"','""')}"`;
}
export function GET() {
  const body = [fields.join(','), ...release.sources.map(row => fields.map(field => csv(row[field] ?? '')).join(','))].join('\r\n') + '\r\n';
  return new Response(body, { headers: { 'content-type': 'text/csv; charset=utf-8', 'content-disposition': 'attachment; filename="india-water-watch-sources.csv"' } });
}
