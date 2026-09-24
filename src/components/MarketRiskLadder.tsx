import { useEffect, useRef, useState } from 'react';
import type { KeyboardEvent } from 'react';
import '../styles/market-risk-ladder.css';

/** The parent page passes reviewed public claim text and source routes only. */
export type MarketEvidenceLink = { label: string; href: string; claimId?: string };
export type PhysicalWaterSignal = {
  headline: string;
  place: string;
  observationPeriod: string;
  description: string;
  limitation: string;
  sources: MarketEvidenceLink[];
};
export type CompanyWaterDisclosure = {
  company: string;
  reportingPeriod: string;
  headline: string;
  description: string;
  limitation: string;
  sources: MarketEvidenceLink[];
};
export type HistoricalCeaRecord = {
  fiscalYear: string;
  outages: number;
  potentialGenerationLossMu: number;
  denominatorNote: string;
  comparisonNote?: string;
  source: MarketEvidenceLink;
};
export type MarketRiskLadderProps = {
  reviewedAsOf: string;
  physical?: PhysicalWaterSignal;
  exposure?: CompanyWaterDisclosure;
  historicalCea?: HistoricalCeaRecord;
  queryKey?: string;
};

type GateId = 'water' | 'exposure' | 'operations' | 'earnings' | 'price';
const gates: { id: GateId; number: string; short: string; title: string; question: string }[] = [
  { id: 'water', number: '01', short: 'Physical water', title: 'What happened to the water?', question: 'A dated observation for the relevant catchment, source or service area.' },
  { id: 'exposure', number: '02', short: 'Company exposure', title: 'Where does the company depend on it?', question: 'A specific asset, supply route or company disclosure.' },
  { id: 'operations', number: '03', short: '2026 operations', title: 'Did the asset actually stop or slow?', question: 'A dated company or operator notice linking water to output.' },
  { id: 'earnings', number: '04', short: 'Earnings effect', title: 'Did it reach the accounts?', question: 'A quantified, attributable effect in a company filing.' },
  { id: 'price', number: '05', short: 'Share-price move', title: 'Did the market react to this cause?', question: 'A price series plus a defensible attribution analysis.' },
];
const hasGate = (id: GateId, physical?: PhysicalWaterSignal, exposure?: CompanyWaterDisclosure) => id === 'water' ? Boolean(physical) : id === 'exposure' ? Boolean(exposure) : false;

export default function MarketRiskLadder({ reviewedAsOf, physical, exposure, historicalCea, queryKey = 'market-gate' }: MarketRiskLadderProps) {
  const [active, setActive] = useState<GateId>('water');
  const [hydrated, setHydrated] = useState(false);
  const buttons = useRef<(HTMLButtonElement | null)[]>([]);

  useEffect(() => {
    const readLocation = () => {
      const requested = new URLSearchParams(window.location.search).get(queryKey);
      setActive(gates.some(g => g.id === requested) ? requested as GateId : 'water');
    };
    readLocation(); setHydrated(true);
    window.addEventListener('popstate', readLocation);
    return () => window.removeEventListener('popstate', readLocation);
  }, [queryKey]);

  const choose = (id: GateId) => {
    setActive(id);
    const next = new URL(window.location.href);
    if (id === 'water') next.searchParams.delete(queryKey);
    else next.searchParams.set(queryKey, id);
    window.history.pushState(null, '', `${next.pathname}${next.search}${next.hash}`);
  };

  const keyMove = (event: KeyboardEvent<HTMLButtonElement>, index: number) => {
    const next = event.key === 'ArrowRight' || event.key === 'ArrowDown' ? Math.min(4, index + 1) : event.key === 'ArrowLeft' || event.key === 'ArrowUp' ? Math.max(0, index - 1) : event.key === 'Home' ? 0 : event.key === 'End' ? 4 : -1;
    if (next < 0) return;
    event.preventDefault();
    choose(gates[next].id);
    buttons.current[next]?.focus();
    buttons.current[next]?.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'instant' });
  };

  return <section className="market-risk-ladder" aria-labelledby="mrl-title" data-hydrated={hydrated}>
    <div className="mrl-overline"><span>Water × business / an evidence test</span><span>Reviewed {reviewedAsOf}</span></div>
    <header className="mrl-header"><div><p className="mrl-kicker">Five gates to a market claim</p><h2 id="mrl-title">Can water move<br /><em>a share price?</em></h2></div><p>A company can disclose a water risk before a measurable 2026 disruption occurs. Open each gate to see the dated evidence available here and the records still needed.</p></header>

    <div className="mrl-track-wrap"><p className="mrl-swipe-note">Select a gate. On a narrow screen, scroll the sequence sideways. Arrow keys move between gates.</p><div className="mrl-track" role="group" aria-label="Five evidence gates from physical water to attributed share-price movement">
      {gates.map((gate, index) => <button key={gate.id} ref={el => { buttons.current[index] = el; }} id={`mrl-button-${gate.id}`} type="button" disabled={!hydrated} aria-controls={`mrl-panel-${gate.id}`} aria-expanded={hydrated ? active === gate.id : undefined} aria-pressed={hydrated ? active === gate.id : undefined} onClick={() => choose(gate.id)} onKeyDown={event => keyMove(event, index)} className="mrl-gate-button" data-available={hasGate(gate.id, physical, exposure)}>
        <span className="mrl-gate-top"><b>{gate.number}</b><i aria-hidden="true">{hasGate(gate.id, physical, exposure) ? '●' : '○'}</i></span><span className="mrl-gate-name">{gate.short}</span><small>{hasGate(gate.id, physical, exposure) ? gate.id === 'water' ? 'Dated context' : 'Risk disclosed' : 'Not verified here'}</small>
      </button>)}
    </div></div>

    <div className="mrl-panels">
      {gates.map(gate => <article key={gate.id} id={`mrl-panel-${gate.id}`} className="mrl-panel" data-active={active === gate.id} role="region" aria-labelledby={`mrl-button-${gate.id}`}>
        <div className="mrl-panel-lead"><span className="mrl-panel-number" aria-hidden="true">{gate.number}<small>/05</small></span><span className={`mrl-status${hasGate(gate.id, physical, exposure) ? ' is-sourced' : ''}`}>{hasGate(gate.id, physical, exposure) ? gate.id === 'water' ? 'Dated physical context' : 'Company risk disclosure' : `Not verified here · ${reviewedAsOf}`}</span><h3>{gate.title}</h3></div>
        <div className="mrl-panel-detail"><p className="mrl-gate-question">{gate.question}</p>
          {gate.id === 'water' && (physical ? <><p className="mrl-fact-date">{physical.place} · {physical.observationPeriod}</p><p className="mrl-fact-headline">{physical.headline}</p><p>{physical.description}</p><p className="mrl-limitation">{physical.limitation}</p><SourceLinks links={physical.sources} /></> : <><p>No matched physical observation has been supplied for this company or asset in this reviewed release.</p><p className="mrl-limitation">A national rain or reservoir figure cannot be assigned to a plant without its location and supply catchment.</p></>)}
          {gate.id === 'exposure' && (exposure ? <><p className="mrl-fact-date">{exposure.company} · {exposure.reportingPeriod}</p><p className="mrl-fact-headline">{exposure.headline}</p><p>{exposure.description}</p><p className="mrl-limitation">{exposure.limitation}</p><SourceLinks links={exposure.sources} /></> : <><p>No reviewed company or asset disclosure is supplied for this gate.</p><p className="mrl-limitation">A broad sector dependency does not establish that a named listed firm was exposed in 2026.</p></>)}
          {gate.id === 'operations' && <><p className="mrl-fact-headline">No verified 2026 water-related operational event is shown here.</p><p>To move past this gate, check a dated company filing or operator notice naming the asset, the interruption, the water mechanism and the duration.</p><p className="mrl-limitation">A disclosed risk describes what could disrupt production; it does not document an event.</p></>}
          {gate.id === 'earnings' && <><p className="mrl-fact-headline">No attributable 2026 earnings effect is verified here.</p><p>A financial claim needs an earnings or exchange filing that quantifies the effect and separates water from demand, fuel, inputs, trade, currency and other drivers.</p><p className="mrl-limitation">A historical generation opportunity loss measured in energy units is not a rupee loss.</p></>}
          {gate.id === 'price' && <><p className="mrl-fact-headline">No water-attributed 2026 share-price move is verified here.</p><p>A dated traded-price series and event analysis would be needed before connecting a price move to the named water event rather than concurrent news and market forces.</p><p className="mrl-limitation">This sequence is a reporting test, not a stock forecast, probability or investment signal.</p></>}
        </div>
      </article>)}
    </div>

    {historicalCea && <aside className="mrl-archive" aria-labelledby="mrl-archive-title"><div className="mrl-archive-rule"><span>Archive / separate clock</span><span>{historicalCea.fiscalYear} · CEA</span></div><div className="mrl-archive-grid"><div><h3 id="mrl-archive-title">Water has interrupted generation before.</h3><p>This historical CEA category gives a documented operational example. It does not fill any 2026 company, earnings or stock-price gate above.</p></div><div className="mrl-archive-figures"><div><strong>{historicalCea.outages.toLocaleString('en-IN')}</strong><span>raw-water-problem outages</span></div><div><strong>{historicalCea.potentialGenerationLossMu.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</strong><span>MU potential generation loss</span></div></div></div><p className="mrl-archive-note">{historicalCea.denominatorNote} {historicalCea.comparisonNote || ''} This category does not attribute every outage to drought or measure consumer cuts, financial loss or a share-price effect.</p><a href={historicalCea.source.href}>{historicalCea.source.label} ↗</a>{historicalCea.source.claimId && <small>Claim {historicalCea.source.claimId}</small>}</aside>}
    <p className="mrl-footer-note">A dated water signal and a company risk disclosure remain separate records until the relevant asset and supply source are matched. The sequence stops wherever evidence stops. An empty gate means <strong>not verified in this release</strong>, not proof that no effect occurred.</p>
  </section>;
}

function SourceLinks({ links }: { links: MarketEvidenceLink[] }) {
  return <div className="mrl-sources" aria-label="Evidence sources">{links.map(link => <a key={`${link.href}-${link.claimId || ''}`} href={link.href}>{link.label} <span aria-hidden="true">↗</span>{link.claimId && <small>Claim {link.claimId}</small>}</a>)}</div>;
}
