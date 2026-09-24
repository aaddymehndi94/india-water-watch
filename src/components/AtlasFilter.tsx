import { useEffect, useMemo, useState } from 'react';
import type { Geography, Observation } from '../lib/publication';

export default function AtlasFilter({ geographies, observations, sourceBase }: { geographies: Geography[]; observations: Observation[]; sourceBase: string }) {
  const [place, setPlace] = useState('');
  const [metric, setMetric] = useState('all');
  useEffect(() => {
    const readUrl = () => {
    const params = new URLSearchParams(location.search);
    const p = params.get('place') || '';
    const m = params.get('metric') || 'all';
    setPlace(geographies.some(g => g.id === p) ? p : '');
    setMetric(m === 'all' || observations.some(o => o.metricId === m) ? m : 'all');
    };
    readUrl();
    window.addEventListener('popstate', readUrl);
    return () => window.removeEventListener('popstate', readUrl);
  }, [geographies, observations]);
  function update(nextPlace: string, nextMetric: string) {
    setPlace(nextPlace); setMetric(nextMetric);
    const params = new URLSearchParams();
    if (nextPlace) params.set('place', nextPlace);
    if (nextMetric !== 'all') params.set('metric', nextMetric);
    history.pushState(null, '', `${location.pathname}${params.size ? '?' + params : ''}`);
  }
  const metrics = [...new Set(observations.map(o => o.metricId))].sort();
  const rows = useMemo(() => observations.filter(o => (!place || o.geographyId === place) && (metric === 'all' || o.metricId === metric)), [observations, place, metric]);
  return <>
    <div className="grid-2"><div className="field"><label htmlFor="place-select">Place</label><select id="place-select" value={place} onChange={e => update(e.target.value, metric)}><option value="">All available places</option>{geographies.map(g => <option key={g.id} value={g.id}>{g.name}</option>)}</select></div><div className="field"><label htmlFor="metric-select">Indicator</label><select id="metric-select" value={metric} onChange={e => update(place, e.target.value)}><option value="all">All available indicators</option>{metrics.map(m => <option key={m} value={m}>{m.replaceAll('_', ' ')}</option>)}</select></div></div>
    <p className="small muted" aria-live="polite">{rows.length} approved observations match these filters. The URL includes your selection.</p>
    <div className="table-wrap"><table className="data-table atlas-table"><caption className="sr-only">Approved observations by place and indicator</caption><thead><tr><th scope="col">Place</th><th scope="col">Indicator</th><th scope="col">Value</th><th scope="col">Period</th><th scope="col">Evidence</th></tr></thead><tbody>{rows.map(o => <tr key={o.id}><td>{geographies.find(g => g.id === o.geographyId)?.name || o.geographyId}</td><td>{o.metricId.replaceAll('_', ' ')}</td><td>{o.value === null ? 'Unavailable' : `${o.value.toLocaleString()} ${o.unit}`}</td><td>{o.periodStart.slice(0,10)} to {o.periodEnd.slice(0,10)}</td><td><a href={`${sourceBase}${encodeURIComponent(o.sourceId)}/`}>Source</a></td></tr>)}</tbody></table></div>
    {rows.length === 0 && <div className="empty-panel"><h3>No reviewed rows for this selection</h3><p>This is a coverage gap, not a zero value or an indication of safe conditions.</p></div>}
  </>;
}
