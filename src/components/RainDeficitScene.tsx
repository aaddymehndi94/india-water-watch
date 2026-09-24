import { useEffect, useState } from 'react';
import type { CSSProperties } from 'react';
import '../styles/rain-deficit-scene.css';

export type RainDeficitSceneProps = {
  /** Reviewed all-India cumulative IMD totals for exactly the same date window. */
  observedMm: number;
  normalMm: number;
  periodLabel: string;
  sourceHref: string;
  sourceLabel: string;
  claimId: string;
};

const formatMm = (value: number) => value.toLocaleString('en-IN', {
  minimumFractionDigits: 1,
  maximumFractionDigits: 1,
});

export default function RainDeficitScene({ observedMm, normalMm, periodLabel, sourceHref, sourceLabel, claimId }: RainDeficitSceneProps) {
  if (!Number.isFinite(observedMm) || !Number.isFinite(normalMm) || observedMm < 0 || normalMm <= 0 || observedMm > normalMm) {
    throw new Error('RainDeficitScene requires reviewed, finite below-normal rainfall totals for one shared period.');
  }
  const [view, setView] = useState<'totals' | 'gap'>('totals');
  const [ready, setReady] = useState(false);
  useEffect(() => setReady(true), []);

  const gapMm = normalMm - observedMm;
  const observedShare = observedMm / normalMm * 100;
  const gapShare = gapMm / normalMm * 100;
  const departurePct = (observedMm / normalMm - 1) * 100;
  const figureStyle = {
    '--rds-observed': `${observedShare}%`,
    '--rds-gap': `${gapShare}%`,
    '--rds-guide': `${100 - .95 * observedShare}%`,
  } as CSSProperties;

  return <section className="rds" aria-labelledby="rds-title" data-view={view} style={figureStyle}>
    <div className="rds-meta"><span>01 / A measured difference</span><span>India · IMD · {periodLabel}</span></div>
    <div className="rds-intro">
      <div><p className="rds-kicker">The national rain ledger</p><h2 id="rds-title">The rainfall gap<br /><em>made visible.</em></h2></div>
      <p>During {periodLabel}, India received <strong>{formatMm(observedMm)} mm</strong> of rain against an IMD same-date normal of <strong>{formatMm(normalMm)} mm</strong>. This is a cumulative national reading, not a report on any one place’s water supply.</p>
    </div>

    <div className="rds-controls" role="group" aria-label="Choose how to read the rainfall comparison">
      <button type="button" aria-pressed={view === 'totals'} disabled={!ready} onClick={() => setView('totals')}><span>01</span> Compare totals</button>
      <button type="button" aria-pressed={view === 'gap'} disabled={!ready} onClick={() => setView('gap')}><span>02</span> Isolate the gap</button>
    </div>
    <p className="rds-mode-caption" aria-live="polite">{view === 'totals' ? 'Both columns share a zero baseline and a single millimetre scale.' : `The hatched band isolates ${formatMm(gapMm)} mm, or ${gapShare.toFixed(1)}% of the same-date normal.`}</p>

    <div className="rds-body">
      <div className="rds-reading">
        <p className="rds-reading-label">Below the normal for these dates</p>
        <p className="rds-headline"><strong>−{Math.abs(departurePct).toFixed(1)}<small>%</small></strong></p>
        <p className="rds-reading-desc"><strong>{formatMm(gapMm)} mm</strong> separates the two cumulative totals. “Normal” is a rainfall reference based on IMD’s 1971–2020 period; it is not a target for taps, reservoirs or crops.</p>
        <a className="rds-source" href={sourceHref}>{sourceLabel} <span aria-hidden="true">↗</span></a>
        <p className="rds-claim">Measured · claim {claimId}</p>
      </div>

      <figure className="rds-figure">
        <div className="rds-plot" role="img" aria-label={`Two rainfall columns share a zero baseline and the same scale. IMD normal: ${formatMm(normalMm)} millimetres. Recorded: ${formatMm(observedMm)} millimetres, or ${Math.abs(departurePct).toFixed(1)} percent below normal. The difference is ${formatMm(gapMm)} millimetres.`}>
          <div className="rds-guide rds-guide-top" aria-hidden="true"><span>{formatMm(normalMm)} mm · normal</span></div>
          <div className="rds-guide rds-guide-observed" aria-hidden="true"><span>{formatMm(observedMm)} mm · recorded</span></div>
          <div className="rds-columns" aria-hidden="true">
            <div className="rds-column rds-normal"><div className="rds-column-fill"><span className="rds-hatch" /></div><span className="rds-column-label">Normal</span></div>
            <div className="rds-column rds-recorded"><div className="rds-column-fill" /><span className="rds-column-label">Recorded</span></div>
          </div>
          <div className="rds-gap-note" aria-hidden="true"><strong>{formatMm(gapMm)}</strong><span>millimetres apart</span></div>
          <div className="rds-zero" aria-hidden="true">0 mm</div>
        </div>
        <figcaption>Both columns start at zero. The hatched top of the normal column marks the gap; it is a comparison, not missing daily observations. The length of each column uses the same millimetre scale.</figcaption>
      </figure>
    </div>
  </section>;
}
