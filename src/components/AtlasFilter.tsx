import { useEffect, useMemo, useState } from 'react';
import type { Geography, Observation } from '../lib/publication';

type View = 'measurements' | 'coverage';
type Props = { geographies: Geography[]; observations: Observation[]; sourceBase: string; stateBase: string };
const measured = (geography: Geography, observations: Observation[]) => observations.filter(o => o.geographyId === geography.id);
const isState = (geography: Geography) => ['state', 'union_territory', 'ut'].includes(geography.type);
const metricLabel = (metric: string) => metric === 'rainfall_departure_pct' ? 'Rainfall departure' : metric === 'reservoir_live_storage_bcm' ? 'Live reservoir storage' : metric.replaceAll('_', ' ');
const formatValue = (observation: Observation) => observation.value === null ? 'Unavailable' : observation.unit === 'percent' ? `${observation.value > 0 ? '+' : ''}${observation.value.toFixed(1)}%` : `${observation.value.toLocaleString()} ${observation.unit}`;
const formatDate = (iso: string) => new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${iso.slice(0, 10)}T12:00:00Z`));

export default function AtlasFilter({ geographies, observations, sourceBase, stateBase }: Props) {
  const [view, setView] = useState<View>('measurements');
  const [place, setPlace] = useState('');
  const [metric, setMetric] = useState('all');
  const [query, setQuery] = useState('');
  const places = useMemo(() => [...geographies].sort((a, b) => a.name.localeCompare(b.name)), [geographies]);
  const placeNames = useMemo(() => new Map(geographies.map(g => [g.id, g.name])), [geographies]);
  const metrics = useMemo(() => [...new Set(observations.map(o => o.metricId))].sort(), [observations]);
  const localPlaces = useMemo(() => places.filter(isState), [places]);
  useEffect(() => {
    const readUrl = () => {
      const params = new URLSearchParams(location.search);
      const nextPlace = params.get('place') || '';
      const nextMetric = params.get('metric') || 'all';
      setPlace(geographies.some(g => g.id === nextPlace) ? nextPlace : '');
      setMetric(nextMetric === 'all' || metrics.includes(nextMetric) ? nextMetric : 'all');
      setView(params.get('view') === 'coverage' ? 'coverage' : 'measurements');
      setQuery(params.get('q') || '');
    };
    readUrl();
    window.addEventListener('popstate', readUrl);
    return () => window.removeEventListener('popstate', readUrl);
  }, [geographies, metrics]);
  function update(next: { view?: View; place?: string; metric?: string; query?: string }) {
    const values = { view, place, metric, query, ...next };
    setView(values.view); setPlace(values.place); setMetric(values.metric); setQuery(values.query);
    const params = new URLSearchParams();
    if (values.view === 'coverage') params.set('view', 'coverage');
    if (values.place) params.set('place', values.place);
    if (values.metric !== 'all') params.set('metric', values.metric);
    if (values.query.trim()) params.set('q', values.query.trim());
    history.pushState(null, '', `${location.pathname}${params.size ? `?${params}` : ''}`);
  }
  const rows = observations.filter(o => (!place || o.geographyId === place) && (metric === 'all' || o.metricId === metric));
  const matchingPlaces = localPlaces.filter(g => g.name.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase()));
  return <div className="atlas-workbench">
    <div className="atlas-selector" role="group" aria-label="Explore data or geographic coverage">
      <button type="button" aria-pressed={view === 'measurements'} onClick={() => update({ view: 'measurements', place: '', query: '' })}>Measured evidence <span>{observations.length}</span></button>
      <button type="button" aria-pressed={view === 'coverage'} onClick={() => update({ view: 'coverage', place: '', query: '' })}>State & UT coverage <span>{localPlaces.length}</span></button>
    </div>
    {view === 'measurements' ? <>
      <div className="grid-2 atlas-controls">
        <div className="field"><label htmlFor="place-select">Place</label><select id="place-select" value={place} onChange={e => update({ place: e.target.value })}><option value="">All measured places</option>{places.filter(g => measured(g, observations).length > 0).map(g => <option key={g.id} value={g.id}>{g.name}</option>)}</select></div>
        <div className="field"><label htmlFor="metric-select">Indicator</label><select id="metric-select" value={metric} onChange={e => update({ metric: e.target.value })}><option value="all">All available indicators</option>{metrics.map(m => <option key={m} value={m}>{metricLabel(m)}</option>)}</select></div>
      </div>
      <p className="small muted atlas-result" aria-live="polite">{rows.length} reviewed {rows.length === 1 ? 'observation' : 'observations'} match your selection. Dates and evidence travel with each row.</p>
      {rows.length ? <div className="atlas-coverage">{rows.map(o => <article className="atlas-kpi" key={o.id}><div><p className="eyebrow">{placeNames.get(o.geographyId) || o.geographyId}</p><strong>{formatValue(o)}</strong><p>{metricLabel(o.metricId)} · {formatDate(o.periodStart)}–{formatDate(o.periodEnd)}</p></div><div className="atlas-kpi-foot"><span>{o.geographyId === 'india' ? 'India' : o.geographyId.startsWith('imd:') ? 'Broad IMD region' : o.geographyId.startsWith('cwc:') ? 'CWC monitored cohort' : 'Local place'} · reported</span><a href={`${sourceBase}${encodeURIComponent(o.sourceId)}/`}>Evidence ↗</a></div></article>)}</div> : <div className="empty-panel"><h3>No reviewed rows for this selection</h3><p>This is a coverage gap, not a zero value or an indication of safe conditions.</p></div>}
      <div className="table-wrap"><table className="data-table atlas-table"><caption>Approved observations with exact period and source</caption><thead><tr><th scope="col">Place</th><th scope="col">Indicator</th><th scope="col">Reported value</th><th scope="col">Period</th><th scope="col">Source</th></tr></thead><tbody>{rows.map(o => <tr key={o.id}><td>{placeNames.get(o.geographyId) || o.geographyId}</td><td>{metricLabel(o.metricId)}</td><td>{formatValue(o)}</td><td>{formatDate(o.periodStart)} to {formatDate(o.periodEnd)}</td><td><a href={`${sourceBase}${encodeURIComponent(o.sourceId)}/`}>Source record ↗</a></td></tr>)}</tbody></table></div>
      <p className="small muted">IMD’s broad regions and CWC’s monitored reservoir cohorts are distinct geographies and series. They are not administrative states or comparable layers. Regional IMD percentages are provider reports; separate cumulative normal totals are not printed in the source graphic.</p>
    </> : <>
      <div className="field"><label htmlFor="coverage-search">Find a state or union territory</label><input id="coverage-search" type="search" value={query} onChange={e => update({ query: e.target.value })} placeholder="Search 36 places" autoComplete="off" /></div>
      <p className="small muted atlas-result" aria-live="polite">{matchingPlaces.length} of {localPlaces.length} official roster entries shown. These pages are coverage records; the approved snapshot contains no state-level measurements.</p>
      {matchingPlaces.length ? <div className="coverage-grid">{matchingPlaces.map(g => <a className="coverage-card" key={g.id} href={`${stateBase}${encodeURIComponent(g.slug)}/`}><span className="eyebrow">{g.type === 'state' ? 'State' : 'Union territory'}</span><strong>{g.name}</strong><span>{measured(g, observations).length ? `${measured(g, observations).length} observations` : 'Local data pending'} <span aria-hidden="true">↗</span></span></a>)}</div> : <div className="empty-panel"><h3>No roster match</h3><p>Try a different spelling. The directory is the reviewed national roster, not a source of local measurements.</p></div>}
    </>}
  </div>;
}
