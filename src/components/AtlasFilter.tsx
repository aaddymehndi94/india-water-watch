import { useEffect, useMemo, useState } from 'react';
import type { Claim, Geography, Observation } from '../lib/publication';

type View = 'rainfall' | 'storage' | 'coverage';
type CoverageLayout = 'schematic' | 'az';
type Props = { geographies: Geography[]; observations: Observation[]; claims: Claim[]; sourceBase: string; stateBase: string };
const isState = (g: Geography) => ['state', 'union_territory', 'ut'].includes(g.type);
const date = (iso: string) => new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${iso.slice(0, 10)}T12:00:00Z`));
const evidenceKind = (o: Observation) => o.geographyId === 'india' ? 'India' : o.geographyId.startsWith('imd:') ? 'IMD homogeneous region' : o.geographyId.startsWith('cwc:') ? 'CWC monitored cohort' : 'Local place';
const capacityFrom = (claim?: Claim) => { const match = claim?.text.match(/combined ([\d.]+) BCM live capacity/); return match ? Number(match[1]) : null; };
// Equal-size navigation tiles. Coordinates are deliberately schematic and do
// not represent boundaries, area, observed conditions, or an official code.
const schematic: Record<string, { column: number; row: number; label: string }> = {
  'andhra-pradesh': { column: 5, row: 7, label: 'AP' },
  'arunachal-pradesh': { column: 9, row: 2, label: 'AR' },
  'assam': { column: 8, row: 3, label: 'AS' },
  'bihar': { column: 5, row: 4, label: 'BR' },
  'chhattisgarh': { column: 4, row: 5, label: 'CG' },
  'goa': { column: 2, row: 7, label: 'GA' },
  'gujarat': { column: 1, row: 5, label: 'GJ' },
  'haryana': { column: 3, row: 3, label: 'HR' },
  'himachal-pradesh': { column: 3, row: 2, label: 'HP' },
  'jharkhand': { column: 5, row: 5, label: 'JH' },
  'karnataka': { column: 3, row: 7, label: 'KA' },
  'kerala': { column: 3, row: 8, label: 'KL' },
  'madhya-pradesh': { column: 3, row: 5, label: 'MP' },
  'maharashtra': { column: 3, row: 6, label: 'MH' },
  'manipur': { column: 10, row: 4, label: 'MN' },
  'meghalaya': { column: 7, row: 4, label: 'ML' },
  'mizoram': { column: 9, row: 5, label: 'MZ' },
  'nagaland': { column: 9, row: 3, label: 'NL' },
  'odisha': { column: 5, row: 6, label: 'OD' },
  'punjab': { column: 2, row: 2, label: 'PB' },
  'rajasthan': { column: 2, row: 4, label: 'RJ' },
  'sikkim': { column: 7, row: 3, label: 'SK' },
  'tamil-nadu': { column: 4, row: 8, label: 'TN' },
  'telangana': { column: 4, row: 6, label: 'TS' },
  'tripura': { column: 8, row: 5, label: 'TR' },
  'uttar-pradesh': { column: 4, row: 4, label: 'UP' },
  'uttarakhand': { column: 4, row: 2, label: 'UK' },
  'west-bengal': { column: 6, row: 5, label: 'WB' },
  'andaman-and-nicobar-islands': { column: 9, row: 8, label: 'AN' },
  'chandigarh': { column: 2, row: 3, label: 'CH' },
  'dadra-and-nagar-haveli-and-daman-and-diu': { column: 1, row: 6, label: 'DD' },
  'delhi': { column: 4, row: 3, label: 'DL' },
  'jammu-and-kashmir': { column: 3, row: 1, label: 'JK' },
  'ladakh': { column: 4, row: 1, label: 'LA' },
  'lakshadweep': { column: 1, row: 8, label: 'LD' },
  'puducherry': { column: 5, row: 8, label: 'PY' },
};

function RainFocus({ row, name, sourceBase }: { row: Observation; name: string; sourceBase: string }) {
  const value = row.value ?? 0;
  return <article className="evidence-focus" aria-live="polite"><div><p className="eyebrow">Selected rainfall record · {name}</p><strong key={row.id} className="evidence-focus-value motion-number">{value > 0 ? '+' : ''}{value.toFixed(1)}%</strong><p>IMD-reported departure, {date(row.periodStart)} to {date(row.periodEnd)}. The source graphic is provider-rounded.</p></div><div><p className="small">{evidenceKind(row)}. This is rainfall, not a measure of storage, groundwater, crop loss or household supply.</p><a href={`${sourceBase}${encodeURIComponent(row.sourceId)}/`}>Inspect graphic and exact locator ↗</a></div></article>;
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
  const [coverageLayout, setCoverageLayout] = useState<CoverageLayout>('schematic');
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
      setCoverageLayout(params.get('layout') === 'az' ? 'az' : 'schematic');
      setHydrated(true);
    };
    read(); window.addEventListener('popstate', read); return () => window.removeEventListener('popstate', read);
  }, [places, rain, storage]);
  function update(next: { view?: View; selected?: string; query?: string; layout?: CoverageLayout }) {
    const v = next.view ?? view;
    const s = next.selected ?? selected;
    const q = next.query ?? query;
    const layout = next.layout ?? coverageLayout;
    setView(v); setSelected(s); setQuery(q); setCoverageLayout(layout);
    const params = new URLSearchParams();
    if (v !== 'rainfall') params.set('view', v);
    if (s && !(v === 'rainfall' && s === 'india')) params.set('place', s);
    if (q.trim() && v === 'coverage') params.set('q', q.trim());
    if (v === 'coverage' && layout === 'az') params.set('layout', 'az');
    history.pushState(null, '', `${location.pathname}${params.size ? `?${params}` : ''}`);
  }
  function changeView(next: View) {
    update({ view: next, selected: next === 'coverage' ? '' : next === 'storage' ? storage[0]?.geographyId || '' : rain.find(o => o.geographyId === 'india')?.geographyId || rain[0]?.geographyId || '', query: '' });
  }
  const selectedRain = rain.find(o => o.geographyId === selected) || rain.find(o => o.geographyId === 'india') || rain[0];
  const matchingPlaces = places.filter(g => g.name.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase()));
  const schematicPlaces = places.filter(g => schematic[g.slug]).sort((a, b) => schematic[a.slug].row - schematic[b.slug].row || schematic[a.slug].column - schematic[b.slug].column);
  const unmappedPlaces = places.filter(g => !schematic[g.slug]);
  const selectedPlace = places.find(g => g.id === selected);
  const karnatakaAction = claims.find(c => c.id === 'C-KA-DROUGHT-ORDER-20260922');
  const placeDetail = <div className="place-detail" aria-live="polite">{selectedPlace ? <><p className="eyebrow">{selectedPlace.type === 'state' ? 'State' : 'Union territory'} · official name record</p><h4>{selectedPlace.name}</h4><p>{observations.some(o => o.geographyId === selectedPlace.id) ? 'Reviewed local numeric observations exist for this place.' : 'No approved state or UT numeric water observation in this release. National or broad regional values are not assigned here.'}</p>{selectedPlace.id === 'india:karnataka' && karnatakaAction && <div className="note"><strong>Separate government action record · 22 September 2026</strong><p>The Karnataka gazette declared 53 listed taluks in 17 districts drought-affected for the 2026 kharif season. This declaration does not measure current household service or prove relief delivery.</p><a href={`${sourceBase}${encodeURIComponent(karnatakaAction.evidenceIds[0])}/`}>Inspect the order ↗</a></div>}<a href={`${stateBase}${encodeURIComponent(selectedPlace.slug)}/`}>Open {selectedPlace.name} evidence page ↗</a></> : <><p className="eyebrow">Select a place</p><h4>What is known locally?</h4><p>Choose a tile or a name from the A–Z list to open its coverage summary. The diagram does not show water severity.</p></>}</div>;
  return <div id="atlas-workbench" className="atlas-workbench evidence-stage" data-hydrated={hydrated}>
    <div className="atlas-selector evidence-stage-nav" role="group" aria-label="Choose a layer of evidence">
      <button type="button" disabled={!hydrated} aria-pressed={view === 'rainfall'} onClick={() => changeView('rainfall')}>01 <span>Rainfall</span> <b>{rain.length}</b></button>
      <button type="button" disabled={!hydrated} aria-pressed={view === 'storage'} onClick={() => changeView('storage')}>02 <span>Storage</span> <b>{storage.length}</b></button>
      <button type="button" disabled={!hydrated} aria-pressed={view === 'coverage'} onClick={() => changeView('coverage')}>03 <span>Places</span> <b>{places.length}</b></button>
    </div>
    {view === 'rainfall' && <section aria-labelledby="atlas-rain-title"><div className="section-head"><div><p className="eyebrow">IMD · {rainPeriod}</p><h3 id="atlas-rain-title">How far from the normal?</h3></div><p>Tap a bar to inspect a reported value and its source. These are rainfall departures; separate regional cumulative normal totals are not printed in the provider graphic.</p></div>
      {rain.length ? <><div className="evidence-plot" role="group" aria-label="Select a reported rainfall departure">{rain.map(o => { const magnitude = Math.min(100, Math.abs(o.value ?? 0) / 50 * 100); return <button className="evidence-bar" type="button" disabled={!hydrated} key={o.id} aria-pressed={selectedRain?.id === o.id} onClick={() => update({ selected: o.geographyId })}><span className="evidence-bar-label">{names.get(o.geographyId) || o.geographyId}<small>{evidenceKind(o)}</small></span><span className="evidence-bar-track" aria-hidden="true"><span className="evidence-bar-fill" style={{ width: `${magnitude}%` }} /></span><strong>{o.value?.toFixed(1)}%</strong></button>; })}</div>{selectedRain && <RainFocus row={selectedRain} name={names.get(selectedRain.geographyId) || selectedRain.geographyId} sourceBase={sourceBase} />}<p className="small muted">Bar lengths use a fixed 0 to −50% magnitude axis. They are not local conditions or a ranking of harm. <a href={`${sourceBase}${encodeURIComponent(rain[0].sourceId)}/`}>See source records ↗</a></p><details><summary>Read all rainfall values as a table</summary><div className="table-wrap"><table className="data-table atlas-table"><caption>IMD rainfall departure reports, with period and evidence</caption><thead><tr><th scope="col">Place</th><th scope="col">Departure</th><th scope="col">Period</th><th scope="col">Source</th></tr></thead><tbody>{rain.map(o => <tr key={o.id}><td>{names.get(o.geographyId) || o.geographyId}</td><td>{o.value?.toFixed(1)}%</td><td>{date(o.periodStart)} to {date(o.periodEnd)}</td><td><a href={`${sourceBase}${encodeURIComponent(o.sourceId)}/`}>Evidence ↗</a></td></tr>)}</tbody></table></div></details></> : <div className="empty-panel"><p>No approved rainfall observations in this release.</p></div>}
    </section>}
    {view === 'storage' && <section aria-labelledby="atlas-storage-title"><div className="section-head"><div><p className="eyebrow">CWC · {storagePeriod}</p><h3 id="atlas-storage-title">What monitored reservoirs held</h3></div><p>Each fill is a fraction of its own monitored cohort’s live capacity. The two gauges do not share a denominator and are not a basin map.</p></div><div className="storage-pair">{storage.map(o => { const claim = claims.find(c => c.id === o.claimId); const capacity = capacityFrom(claim); const percent = capacity && o.value !== null ? 100 * o.value / capacity : null; return <article className="storage-meter" key={o.id}><p className="eyebrow">{names.get(o.geographyId) || o.geographyId}</p><div className="storage-meter-figure" role="img" aria-label={percent === null ? `${o.value} BCM reported live storage; cohort capacity unavailable` : `${o.value} of ${capacity} BCM live capacity, ${percent.toFixed(2)} percent`}>{percent !== null ? <div className="storage-meter-track"><div className="storage-meter-fill" style={{ height: `${Math.max(0, Math.min(100, percent))}%` }} /></div> : <p>Capacity unavailable; no fill shown.</p>}<div className="storage-meter-value"><strong>{o.value?.toFixed(3)}</strong><span>BCM live storage</span>{percent !== null && <b>{percent.toFixed(2)}% of own capacity</b>}</div></div><p className="small">Status date {date(o.periodEnd)} · {evidenceKind(o)}. {capacity === null ? 'Capacity not available in the approved claim.' : `Combined live capacity ${capacity.toFixed(3)} BCM.`}</p><a href={`${sourceBase}${encodeURIComponent(o.sourceId)}/`}>CWC bulletin and limits ↗</a></article>; })}</div><p className="small muted">CWC’s southern cohort consists of 50 monitored reservoirs and is not IMD’s South Peninsular rainfall region. The national CWC cohort contains the southern one, so these are not independent sums. Neither gauge measures household supply.</p><details><summary>Read monitored storage values as a table</summary><div className="table-wrap"><table className="data-table atlas-table"><caption>CWC monitored reservoir live storage, {storagePeriod}</caption><thead><tr><th scope="col">Cohort</th><th scope="col">Live storage</th><th scope="col">Capacity</th><th scope="col">Status date</th><th scope="col">Source</th></tr></thead><tbody>{storage.map(o => { const capacity = capacityFrom(claims.find(c => c.id === o.claimId)); return <tr key={o.id}><td>{names.get(o.geographyId) || o.geographyId}</td><td>{o.value?.toFixed(3)} BCM</td><td>{capacity === null ? 'Not available' : `${capacity.toFixed(3)} BCM`}</td><td>{date(o.periodEnd)}</td><td><a href={`${sourceBase}${encodeURIComponent(o.sourceId)}/`}>Evidence ↗</a></td></tr>; })}</tbody></table></div></details></section>}
    {view === 'coverage' && <section aria-labelledby="atlas-places-title"><div className="section-head"><div><p className="eyebrow">Official roster · {stateCount} states & {places.length - stateCount} UTs</p><h3 id="atlas-places-title">Find a place. See the gap.</h3></div><p>Choose an equal-size tile or the A–Z list. Neither view displays a measured state condition; a blank local reading remains unknown.</p></div>
      <div className="locator-intro"><div><p className="eyebrow">A schematic locator, not a map</p><p>These {schematicPlaces.length} tiles suggest broad placement for navigation only. They do not trace borders, show area, assign regional rainfall to states, or classify water stress.</p></div><div className="locator-key"><span><i aria-hidden="true" /> State</span><span><i className="ut" aria-hidden="true" /> Union territory</span><span>Selected tile has a gold outline</span></div></div>
      <div className="locator-controls"><div className="locator-modes" role="group" aria-label="Choose place locator view"><button type="button" disabled={!hydrated} aria-pressed={coverageLayout === 'schematic'} onClick={() => update({ layout: 'schematic', query: '' })}>Schematic tiles</button><button type="button" disabled={!hydrated} aria-pressed={coverageLayout === 'az'} onClick={() => update({ layout: 'az' })}>A–Z list</button></div><div className="field"><label htmlFor="coverage-search">Search a state or union territory</label><input id="coverage-search" type="search" value={query} onChange={e => update({ query: e.target.value, selected: '', layout: e.target.value ? 'az' : coverageLayout })} placeholder="Type a place name" autoComplete="off" /></div></div>
      <p className="small muted atlas-result" aria-live="polite">{matchingPlaces.length} of {places.length} official roster names shown · {places.filter(g => observations.some(o => o.geographyId === g.id)).length} with approved local numeric measurements. Tile initials are editorial shorthand, not official codes.</p>
      {coverageLayout === 'schematic' ? <div className="cartogram-layout"><div><p id="schematic-note" className="cartogram-instruction">Scroll sideways on a narrow screen. Tab to a tile and press Enter or Space to select it; the A–Z list is an alternative.</p><div className="cartogram-scroll" role="region" tabIndex={0} aria-label="Schematic state and union territory tile locator" aria-describedby="schematic-note"><div className="cartogram-board" role="group" aria-label="Equal-size place tiles, approximately positioned">{schematicPlaces.map(g => { const tile = schematic[g.slug]; const hasLocal = observations.some(o => o.geographyId === g.id); const hasOrder = g.id === 'india:karnataka' && Boolean(karnatakaAction); return <button key={g.id} type="button" disabled={!hydrated} className={`cartogram-tile${g.type === 'state' ? '' : ' is-ut'}`} style={{ gridColumn: tile.column, gridRow: tile.row }} aria-label={`Select ${g.name}; ${hasLocal ? 'reviewed local numeric measurement available' : hasOrder ? 'separate government order available, local numeric measurements unavailable' : 'local numeric measurements unavailable'}`} aria-pressed={selectedPlace?.id === g.id} title={g.name} onClick={() => update({ selected: g.id })}><b aria-hidden="true">{tile.label}</b><small aria-hidden="true">{g.type === 'state' ? 'S' : 'UT'}</small></button>; })}</div></div><p className="cartogram-foot">Equal tiles and approximate placement. Islands and small territories are enlarged as tiles; distances and borders are intentionally absent. Every tile has the same fill because no state or UT numeric water observation is approved in this release.</p>{unmappedPlaces.length > 0 && <p className="small">{unmappedPlaces.length} newer roster entries have no schematic position yet. Use the <button type="button" className="text-button" onClick={() => update({ layout: 'az' })}>A–Z list</button> to find them.</p>}</div>{placeDetail}</div> : <><div className="place-mosaic" role="group" aria-label="Alphabetical state and union territory locator">{matchingPlaces.map(g => <button key={g.id} className="place-tile" type="button" disabled={!hydrated} aria-pressed={selectedPlace?.id === g.id} onClick={() => update({ selected: g.id })}><span>{g.name}</span><small>{observations.some(o => o.geographyId === g.id) ? 'Measured' : g.id === 'india:karnataka' && karnatakaAction ? 'Official action' : 'Local data gap'}</small></button>)}</div>{!matchingPlaces.length && <div className="empty-panel"><p>No roster match. Try another spelling.</p></div>}{placeDetail}</>}
      <p className="small muted">The {places.length}-name roster is attributed to the <a href={`${sourceBase}E-INDIA-ROSTER-20260923/`}>National Portal of India evidence record ↗</a>. Codes and reusable boundary geometry are not verified. <a href={`${stateBase}`}>Browse full place records ↗</a></p></section>}
  </div>;
}
