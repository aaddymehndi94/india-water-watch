import { release } from '../../lib/publication';
import { rainfallDepartureX as x } from '../../lib/charts';
export const prerender = true;
const safe = (v: unknown) => String(v ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[ch] || ch));
export function GET() {
  const dated = release.observations.filter(o => o.metricId === 'rainfall_departure_pct' && o.geographyId !== 'india' && typeof o.value === 'number' && Number.isFinite(o.value));
  const latestEnd = dated.reduce((end, row) => row.periodEnd > end ? row.periodEnd : end, '');
  const rows = dated.filter(row => row.periodEnd === latestEnd).sort((a,b) => a.geographyId.localeCompare(b.geographyId));
  const endDate = rows[0]?.periodEnd.slice(0,10) || 'date unavailable';
  const startDate = rows[0]?.periodStart.slice(0,10) || 'date unavailable';
  const geo = new Map(release.geographies.map(g => [g.id,g.name]));
  const sameWindow = rows.length > 1 && rows.every(o => o.periodStart === rows[0].periodStart && o.periodEnd === rows[0].periodEnd && (o.value ?? 0) >= -50 && (o.value ?? 0) <= 10);
  const height = sameWindow ? 210 + rows.length * 45 : 260;
  const bars = sameWindow ? rows.map((o,i) => { const y=100+i*45; const v=o.value as number; return `<text x="270" y="${y+5}" text-anchor="end" font-size="15" fill="#172d34">${safe(geo.get(o.geographyId) || o.geographyId)}</text><rect x="${Math.min(x(v),x(0))}" y="${y-12}" width="${Math.abs(x(v)-x(0))}" height="25" fill="${o.geographyId === 'india' ? '#1e6571' : '#8daea8'}"/><text x="${x(v)-8}" y="${y+5}" text-anchor="end" font-size="14" font-weight="700" fill="#172d34">${v.toFixed(1)}%</text>`;}).join('') : `<text x="30" y="110" font-size="18">No comparable approved rows for this chart.</text>`;
  const ticks = [-50,-25,0,10].map(t => `<line x1="${x(t)}" x2="${x(t)}" y1="59" y2="69" stroke="#718984"/><text x="${x(t)}" y="51" text-anchor="middle" font-size="13" fill="#425b5d">${t}%</text>`).join('');
  const svg = `<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" width="760" height="${height}" viewBox="0 0 760 ${height}" role="img"><title>IMD reported regional rainfall departure through ${safe(endDate)}</title><desc>Fixed axis −50% to +10%; source records, caveat and release ID are printed below the bars.</desc><rect width="760" height="${height}" fill="#fffdf8"/><text x="30" y="31" font-size="22" font-family="Georgia,serif" fill="#172d34">Reported regional rainfall departure</text><line x1="285" x2="639" y1="64" y2="64" stroke="#718984"/>${ticks}<line x1="${x(0)}" x2="${x(0)}" y1="64" y2="${height-82}" stroke="#41585a" stroke-width="2"/>${bars}<text x="30" y="${height-64}" font-size="12" fill="#56666a">${safe(startDate)} to ${safe(endDate)} · Percent departure · IMD displayed values</text><text x="30" y="${height-46}" font-size="12" fill="#56666a">Four regional cumulative normal totals not printed; provider percentages not independently recomputed.</text><text x="30" y="${height-28}" font-size="12" fill="#56666a">Sources: ${safe([...new Set(rows.map(o => o.sourceId))].join(', '))} · Release: ${safe(release.releaseId)}</text></svg>`;
  return new Response(svg,{headers:{'content-type':'image/svg+xml; charset=utf-8','content-disposition':'attachment; filename="rainfall-departure.svg"'}});
}
