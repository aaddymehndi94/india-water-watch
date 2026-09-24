import { useEffect, useMemo, useRef, useState } from 'react';
import type { Claim, Geography, Observation } from '../lib/publication';

type View = 'rainfall' | 'storage' | 'coverage';
type Props = { geographies: Geography[]; observations: Observation[]; claims: Claim[]; sourceBase: string; stateBase: string };
const isState = (g: Geography) => ['state', 'union_territory', 'ut'].includes(g.type);
const date = (iso: string) => new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${iso.slice(0, 10)}T12:00:00Z`));
const evidenceKind = (o: Observation) => o.geographyId === 'india' ? 'India' : o.geographyId.startsWith('imd:') ? 'IMD homogeneous region' : o.geographyId.startsWith('cwc:') ? 'CWC monitored cohort' : 'Local place';
const capacityFrom = (claim?: Claim) => { const match = claim?.text.match(/combined ([\d.]+) BCM live capacity/); return match ? Number(match[1]) : null; };

function useAnimatedValue(value: number) {
  const [shown, setShown] = useState(value);
  const previous = useRef(value);
  const first = useRef(true);
  useEffect(() => {
    if (first.current) { first.current = false; previous.current = value; setShown(value); return; }
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { previous.current = value; setShown(value); return; }
    const start = previous.current;
    const started = performance.now();
    let frame = 0;
    function tick(now: number) {
      const progress = Math.min(1, (now - started) / 520);
      const eased = 1 - Math.pow(1 - progress, 3);
      setShown(start + (value - start) * eased);
      if (progress < 1) frame = requestAnimationFrame(tick);
      else previous.current = value;
    }
    frame = requestAnimationFrame(tick);
    return () => { cancelAnimationFrame(frame); previous.current = value; };
  }, [value]);
  return shown;
}

function RainFocus({ row, name, sourceBase }: { row: Observation; name: string; sourceBase: string }) {
  const shown = useAnimatedValue(row.value ?? 0);
  return <article className="evidence-focus" aria-live="polite"><div><p className="eyebrow">Selected rainfall record · {name}</p><strong className="evidence-focus-value motion-number">{shown > 0 ? '+' : ''}{shown.toFixed(1)}%</strong><p>IMD-reported departure, {date(row.periodStart)} to {date(row.periodEnd)}. The source graphic is provider-rounded.</p></div><div><p className="small">{evidenceKind(row)}. This is rainfall, not a measure of storage, groundwater, crop loss or household supply.</p><a href={`${sourceBase}${encodeURIComponent(row.sourceId)}/`}>Inspect graphic and exact locator ↗</a></div></article>;
}

export default function AtlasFilter({ geographies, observations, claims, sourceBase, stateBase }: Props) {
  const rain = useMemo(() => observations.filter(o => o.metricId === 'rainfall_departure_pct' && typeof o.value === 'number'), [observations]);
  const storage = useMemo(() => observations.filter(o => o.metricId === 'reservoir_live_storage_bcm' && typeof o.value === 'number'), [observations]);
  const places = useMemo(() => geographies.filter(isState).sort((a, b) => a.name.localeCompare(b.name)), [geographies]);
  const stateCount = places.filter(g => g.type === 'state').length;
  const rainPeriod = rain.length && rain.every(o => o.periodStart === rain[0].periodStart && o.periodEnd === rain[0].periodEnd) ? `${date(rain[0].periodStart)} to ${date(rain[0].periodEnd)}` : 'See row dates';
  const storagePeriod = storage.length && storage.every(o => o.periodEnd === storage[0].periodEnd) ? date(storage[0].periodEnd) : 'See row dates';
  const names = useMemo(() => new Map(geographies.map(g => [g.id, g.name])), [geographies]);
  const [view, setView] = useState<View>('rainfall');
  const [selected, setSelected] = useState('india');
  const [query, setQuery] = useState('');
  const [hydrated, setHydrated] = useState(false);
  useEffect(() => {
    const read = () => {
      const params = new URLSearchParams(location.search);
      const nextView = params.get('view');
      const nextMetric = params.get('metric');
      const stage: View = nextView === 'coverage' || nextView === 'storage' || nextView === 'rainfall' ? nextView : nextMetric === 'reservoir_live_storage_bcm' ? 'storage' : 'rainfall';
      const place = params.get('place') || '';
      setView(stage);
      setSelected(stage === 'coverage' ? places.some(g => g.id === place) ? place : '' : stage === 'storage' ? storage.some(o => o.geographyId === place) ? place : storage[0]?.geographyId || '' : rain.some(o => o.geographyId === place) ? place : rain.find(o => o.geographyId === 'india')?.geographyId || rain[0]?.geographyId || '');
      setQuery(params.get('q') || '');
      setHydrated(true);
    };
    read(); window.addEventListener('popstate', read); return () => window.removeEventListener('popstate', read);
  }, [places, rain, storage]);
  function update(next: { view?: View; selected?: string; query?: string }) {
    const v = next.view ?? view;
    const s = next.selected ?? selected;
    const q = next.query ?? query;
    setView(v); setSelected(s); setQuery(q);
    const params = new URLSearchParams();
    if (v !== 'rainfall') params.set('view', v);
    if (s && !(v === 'rainfall' && s === 'india')) params.set('place', s);
    if (q.trim() && v === 'coverage') params.set('q', q.trim());
    history.pushState(null, '', `${location.pathname}${params.size ? `?${params}` : ''}`);
  }
  function changeView(next: View) {
    update({ view: next, selected: next === 'coverage' ? '' : next === 'storage' ? storage[0]?.geographyId || '' : rain.find(o => o.geographyId === 'india')?.geographyId || rain[0]?.geographyId || '', query: '' });
  }
  const selectedRain = rain.find(o => o.geographyId === selected) || rain.find(o => o.geographyId === 'india') || rain[0];
  const matchingPlaces = places.filter(g => g.name.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase()));
  const selectedPlace = places.find(g => g.id === selected);
  const karnatakaAction = claims.find(c => c.id === 'C-KA-DROUGHT-ORDER-20260922');
  return <div className="atlas-workbench evidence-stage" data-hydrated={hydrated}>
    <div className="atlas-selector evidence-stage-nav" role="group" aria-label="Choose a layer of evidence">
      <button type="button" disabled={!hydrated} aria-pressed={view === 'rainfall'} onClick={() => changeView('rainfall')}>01 <span>Rainfall</span> <b>{rain.length}</b></button>
      <button type="button" disabled={!hydrated} aria-pressed={view === 'storage'} onClick={() => changeView('storage')}>02 <span>Storage</span> <b>{storage.length}</b></button>
      <button type="button" disabled={!hydrated} aria-pressed={view === 'coverage'} onClick={() => changeView('coverage')}>03 <span>Places</span> <b>{places.length}</b></button>
    </div>
    {view === 'rainfall' && <section aria-labelledby="atlas-rain-title"><div className="section-head"><div><p className="eyebrow">IMD · {rainPeriod}</p><h3 id="atlas-rain-title">How far from the normal?</h3></div><p>Tap a bar to inspect a reported value and its source. These are rainfall departures; separate regional cumulative normal totals are not printed in the provider graphic.</p></div>
      {rain.length ? <><div className="evidence-plot" role="group" aria-label="Select a reported rainfall departure">{rain.map(o => { const magnitude = Math.min(100, Math.abs(o.value ?? 0) / 50 * 100); return <button className="evidence-bar" type="button" disabled={!hydrated} key={o.id} aria-pressed={selectedRain?.id === o.id} onClick={() => update({ selected: o.geographyId })}><span className="evidence-bar-label">{names.get(o.geographyId) || o.geographyId}<small>{evidenceKind(o)}</small></span><span className="evidence-bar-track" aria-hidden="true"><span className="evidence-bar-fill" style={{ width: `${magnitude}%` }} /></span><strong>{o.value?.toFixed(1)}%</strong></button>; })}</div>{selectedRain && <RainFocus row={selectedRain} name={names.get(selectedRain.geographyId) || selectedRain.geographyId} sourceBase={sourceBase} />}<p className="small muted">Bar lengths use a fixed 0 to −50% magnitude axis. They are not local conditions or a ranking of harm. <a href={`${sourceBase}${encodeURIComponent(rain[0].sourceId)}/`}>See source records ↗</a></p><details><summary>Read all rainfall values as a table</summary><div className="table-wrap"><table className="data-table atlas-table"><caption>IMD rainfall departure reports, with period and evidence</caption><thead><tr><th scope="col">Place</th><th scope="col">Departure</th><th scope="col">Period</th><th scope="col">Source</th></tr></thead><tbody>{rain.map(o => <tr key={o.id}><td>{names.get(o.geographyId) || o.geographyId}</td><td>{o.value?.toFixed(1)}%</td><td>{date(o.periodStart)} to {date(o.periodEnd)}</td><td><a href={`${sourceBase}${encodeURIComponent(o.sourceId)}/`}>Evidence ↗</a></td></tr>)}</tbody></table></div></details></> : <div className="empty-panel"><p>No approved rainfall observations in this release.</p></div>}
    </section>}
    {view === 'storage' && <section aria-labelledby="atlas-storage-title"><div className="section-head"><div><p className="eyebrow">CWC · {storagePeriod}</p><h3 id="atlas-storage-title">What monitored reservoirs held</h3></div><p>Each fill is a fraction of its own monitored cohort’s live capacity. The two gauges do not share a denominator and are not a basin map.</p></div><div className="storage-pair">{storage.map(o => { const claim = claims.find(c => c.id === o.claimId); const capacity = capacityFrom(claim); const percent = capacity && o.value !== null ? 100 * o.value / capacity : null; return <article className="storage-meter" key={o.id}><p className="eyebrow">{names.get(o.geographyId) || o.geographyId}</p><div className="storage-meter-figure" role="img" aria-label={percent === null ? `${o.value} BCM reported live storage; cohort capacity unavailable` : `${o.value} of ${capacity} BCM live capacity, ${percent.toFixed(2)} percent`}>{percent !== null ? <div className="storage-meter-track"><div className="storage-meter-fill" style={{ height: `${Math.max(0, Math.min(100, percent))}%` }} /></div> : <p>Capacity unavailable; no fill shown.</p>}<div className="storage-meter-value"><strong>{o.value?.toFixed(3)}</strong><span>BCM live storage</span>{percent !== null && <b>{percent.toFixed(2)}% of own capacity</b>}</div></div><p className="small">Status date {date(o.periodEnd)} · {evidenceKind(o)}. {capacity === null ? 'Capacity not available in the approved claim.' : `Combined live capacity ${capacity.toFixed(3)} BCM.`}</p><a href={`${sourceBase}${encodeURIComponent(o.sourceId)}/`}>CWC bulletin and limits ↗</a></article>; })}</div><p className="small muted">CWC’s southern cohort consists of 50 monitored reservoirs and is not IMD’s South Peninsular rainfall region. The national CWC cohort contains the southern one, so these are not independent sums. Neither gauge measures household supply.</p><details><summary>Read monitored storage values as a table</summary><div className="table-wrap"><table className="data-table atlas-table"><caption>CWC monitored reservoir live storage, {storagePeriod}</caption><thead><tr><th scope="col">Cohort</th><th scope="col">Live storage</th><th scope="col">Capacity</th><th scope="col">Status date</th><th scope="col">Source</th></tr></thead><tbody>{storage.map(o => { const capacity = capacityFrom(claims.find(c => c.id === o.claimId)); return <tr key={o.id}><td>{names.get(o.geographyId) || o.geographyId}</td><td>{o.value?.toFixed(3)} BCM</td><td>{capacity === null ? 'Not available' : `${capacity.toFixed(3)} BCM`}</td><td>{date(o.periodEnd)}</td><td><a href={`${sourceBase}${encodeURIComponent(o.sourceId)}/`}>Evidence ↗</a></td></tr>; })}</tbody></table></div></details></section>}
    {view === 'coverage' && <section aria-labelledby="atlas-places-title"><div className="section-head"><div><p className="eyebrow">Official roster · {stateCount} states & {places.length - stateCount} UTs</p><h3 id="atlas-places-title">Find a place. See the gap.</h3></div><p>This alphabetical tile index is a locator, not a geographic map. A grey tile means local numeric data are not approved here, not that water conditions are normal.</p></div><div className="field"><label htmlFor="coverage-search">Search a state or union territory</label><input id="coverage-search" type="search" value={query} onChange={e => update({ query: e.target.value, selected: '' })} placeholder="Type a place name" autoComplete="off" /></div><p className="small muted atlas-result" aria-live="polite">{matchingPlaces.length} of {places.length} official roster names shown · {places.filter(g => observations.some(o => o.geographyId === g.id)).length} with approved local numeric measurements.</p><div className="place-mosaic" role="group" aria-label="Alphabetical state and union territory locator">{matchingPlaces.map(g => <button key={g.id} className="place-tile" type="button" aria-pressed={selectedPlace?.id === g.id} onClick={() => update({ selected: g.id })}><span>{g.name}</span><small>{observations.some(o => o.geographyId === g.id) ? 'Measured' : g.id === 'india:karnataka' && karnatakaAction ? 'Official action' : 'Data gap'}</small></button>)}</div>{!matchingPlaces.length && <div className="empty-panel"><p>No roster match. Try another spelling.</p></div>}<div className="place-detail" aria-live="polite">{selectedPlace ? <><p className="eyebrow">{selectedPlace.type === 'state' ? 'State' : 'Union territory'} · official name record</p><h4>{selectedPlace.name}</h4><p>{observations.some(o => o.geographyId === selectedPlace.id) ? 'Reviewed local numeric observations exist for this place.' : 'No approved state or UT numeric water observation in this release. National or broad regional values are not assigned here.'}</p>{selectedPlace.id === 'india:karnataka' && karnatakaAction && <div className="note"><strong>Separate government action record · 22 September 2026</strong><p>The Karnataka gazette declared 53 listed taluks in 17 districts drought-affected for the 2026 kharif season. This declaration does not measure current household service or prove relief delivery.</p><a href={`${sourceBase}${encodeURIComponent(karnatakaAction.evidenceIds[0])}/`}>Inspect the order ↗</a></div>}<a href={`${stateBase}${encodeURIComponent(selectedPlace.slug)}/`}>Open {selectedPlace.name} evidence page ↗</a></> : <><p className="eyebrow">Select a place</p><h4>What is known locally?</h4><p>Choose a tile to open its coverage summary. The tile layout is alphabetical, with no implied geography or water severity.</p></>}</div><p className="small muted">The {places.length}-name roster is attributed to the <a href={`${sourceBase}E-INDIA-ROSTER-20260923/`}>National Portal of India evidence record ↗</a>. Codes and reusable boundary geometry are not verified.</p></section>}
  </div>;
}
