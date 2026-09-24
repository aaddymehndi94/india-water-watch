import { useEffect, useState } from 'react';
import type { CSSProperties } from 'react';
import '../styles/water-story-stage.css';

/** Pass only reviewed publication data from the Astro page. Each window stands alone. */
export type RainWindow = {
  id: 'june' | 'season-to-date';
  tabLabel: string;
  periodLabel: string;
  actualMm: number;
  normalMm: number;
  sourceHref: string;
  sourceLabel: string;
  claimId: string;
  finding?: string;
  limit: string;
};

export type PricePair = {
  place: string;
  commodity: string;
  unit: string;
  earlierDate: string;
  earlierValue: number;
  laterDate: string;
  laterValue: number;
  earlierSourceHref: string;
  laterSourceHref: string;
  claimId: string;
};

export type WaterStoryStageProps = {
  june: RainWindow;
  seasonToDate: RainWindow;
  price?: PricePair;
  queryKey?: string;
};

const oneDecimal = (value: number) => value.toLocaleString('en-IN', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
const whole = (value: number) => value.toLocaleString('en-IN', { maximumFractionDigits: 0 });

export default function WaterStoryStage({ june, seasonToDate, price, queryKey = 'rain-window' }: WaterStoryStageProps) {
  // Server output always contains the completed season-to-date reading and a full two-row table.
  const [selected, setSelected] = useState<RainWindow['id']>('season-to-date');
  const [hydrated, setHydrated] = useState(false);
  const windows = [june, seasonToDate];

  useEffect(() => {
    const readLocation = () => {
      const requested = new URLSearchParams(window.location.search).get(queryKey);
      setSelected(requested === 'june' ? 'june' : 'season-to-date');
    };
    readLocation();
    setHydrated(true);
    window.addEventListener('popstate', readLocation);
    return () => window.removeEventListener('popstate', readLocation);
  }, [queryKey]);

  const choose = (id: RainWindow['id']) => {
    setSelected(id);
    const next = new URL(window.location.href);
    if (id === 'june') next.searchParams.set(queryKey, id);
    else next.searchParams.delete(queryKey);
    window.history.pushState(null, '', `${next.pathname}${next.search}${next.hash}`);
  };

  const current = selected === 'june' ? june : seasonToDate;
  const departure = (current.actualMm / current.normalMm - 1) * 100;
  const belowNormal = current.normalMm - current.actualMm;
  const fraction = Math.max(0, Math.min(1, current.actualMm / current.normalMm));
  const normalLabel = `Normal for ${current.periodLabel}: ${oneDecimal(current.normalMm)} millimetres`;
  const observedLabel = `Recorded for ${current.periodLabel}: ${oneDecimal(current.actualMm)} millimetres`;

  return <section className="water-story-stage" aria-labelledby="wss-title" data-hydrated={hydrated}>
    <div className="wss-topline"><span>01 / The measurement</span><span>India · IMD · two distinct time windows</span></div>
    <header className="wss-head">
      <div><p className="wss-kicker">Read the rain, by date</p><h2 id="wss-title">The missing rain<br /><em>has a number.</em></h2></div>
      <p>Pick a window to see what India received against its normal for <strong>those same dates</strong>. The month and cumulative season are separate readings, each with its own baseline.</p>
    </header>

    <div className="wss-window-switch" role="group" aria-label="Choose a rainfall time window">
      {windows.map((item, index) => <button key={item.id} type="button" disabled={!hydrated} aria-pressed={selected === item.id} onClick={() => choose(item.id)}>
        <span className="wss-switch-index">0{index + 1}</span><span>{item.tabLabel}<small>{item.periodLabel}</small></span><strong className="wss-switch-value">{oneDecimal((item.actualMm / item.normalMm - 1) * 100)}%</strong><span className="wss-switch-arrow" aria-hidden="true">↗</span>
      </button>)}
    </div>

    <div className="wss-main" key={current.id}>
      <div className="wss-stat"><p className="wss-stat-label">Rainfall departure · {current.periodLabel}</p><div className="wss-stat-number" role="img" aria-label={`${oneDecimal(Math.abs(departure))} percent below normal`}><span aria-hidden="true">−{oneDecimal(Math.abs(departure))}<small>%</small></span></div><p className="wss-stat-sub">below the normal for this window</p>
        {current.finding && <p className="wss-finding"><span>IMD historical finding</span><strong>{current.finding}</strong></p>}
      </div>

      <figure className="wss-chart">
        <div className="wss-chart-heading"><p>What the gauge actually says</p><span>Rainfall · millimetres</span></div>
        <div className="wss-bar-group" role="img" aria-label={`${observedLabel}. ${normalLabel}. ${oneDecimal(belowNormal)} millimetres below normal. Bars share a zero baseline within this selected date window.`}>
          <div className="wss-bar-row"><div className="wss-bar-label"><span>Recorded</span><strong>{oneDecimal(current.actualMm)}<small> mm</small></strong></div><div className="wss-bar-track"><span className="wss-bar-measured" style={{ '--wss-fill': `${fraction * 100}%` } as CSSProperties} /></div></div>
          <div className="wss-bar-row"><div className="wss-bar-label"><span>Normal</span><strong>{oneDecimal(current.normalMm)}<small> mm</small></strong></div><div className="wss-bar-track"><span className="wss-bar-normal" /></div></div>
        </div>
        <figcaption><strong>{oneDecimal(belowNormal)} mm</strong> separates the two totals for this window. The normal is a long-period rainfall reference, not a water-supply target. Each selection rescales to its own normal; do not compare bar lengths across windows.</figcaption>
      </figure>
    </div>

    <div className="wss-evidence"><div><span className="wss-pill">Measured · official data</span><span className="wss-pill wss-pill-date">{current.periodLabel}</span><span className="wss-pill">mm · all India</span></div><p>{current.limit}</p><a href={current.sourceHref}>{current.sourceLabel} <span aria-hidden="true">↗</span></a><small>Claim {current.claimId}</small></div>

    {price && <aside className="wss-market" aria-labelledby="wss-market-title"><div className="wss-market-head"><span>02 / A separate market signal</span><span className="wss-pill">Government price record</span></div><div className="wss-market-body"><div><h3 id="wss-market-title">A price moved.<br /><em>The cause is unproven.</em></h3><p>Retail {price.commodity.toLowerCase()} at one monitored {price.place} centre, on the same calendar date one year apart.</p></div><div className="wss-price-comparison"><div><span>{price.earlierDate}</span><strong>₹{whole(price.earlierValue)}</strong></div><span className="wss-price-arrow" aria-hidden="true">→</span><div><span>{price.laterDate}</span><strong>₹{whole(price.laterValue)}</strong></div><small>{price.unit} · one monitored centre</small></div></div><p className="wss-market-limit">This two-point record does not show prices between these dates or attribute the change to rainfall, water shortage, crops, trade or any other cause. It is not a Bengaluru city average.</p><div className="wss-price-sources"><a href={price.earlierSourceHref}>Earlier official record ↗</a><a href={price.laterSourceHref}>Later official record ↗</a></div><small>Claim {price.claimId}</small></aside>}

    <details className="wss-data-table"><summary>Read the exact rainfall values as a table</summary><div className="wss-table-scroll"><table><caption>Two distinct, nested all-India rainfall windows, each compared with its own same-date normal</caption><thead><tr><th scope="col">Window</th><th scope="col">Recorded</th><th scope="col">Normal</th><th scope="col">Departure</th><th scope="col">Source</th></tr></thead><tbody>{windows.map(item => <tr key={item.id}><th scope="row">{item.periodLabel}</th><td>{oneDecimal(item.actualMm)} mm</td><td>{oneDecimal(item.normalMm)} mm</td><td>{oneDecimal((item.actualMm / item.normalMm - 1) * 100)}%</td><td><a href={item.sourceHref}>{item.sourceLabel}</a></td></tr>)}</tbody></table></div></details>
  </section>;
}
