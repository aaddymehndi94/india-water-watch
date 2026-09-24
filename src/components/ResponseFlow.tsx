import { useEffect, useRef, useState } from 'react';
import type { KeyboardEvent } from 'react';
import '../styles/response-flow.css';

export type ResponseSource = { label: string; href: string; claimId?: string };
export type ResponseStage = {
  id: string;
  shortLabel: string;
  title: string;
  status: 'documented' | 'directed' | 'not-verified';
  dateLabel: string;
  headline: string;
  detail: string;
  limit: string;
  sources: ResponseSource[];
};
export type ResponseFlowProps = {
  reviewedAsOf: string;
  headline: string;
  introduction: string;
  scopeLabel: string;
  stages: [ResponseStage, ResponseStage, ResponseStage, ResponseStage, ResponseStage, ResponseStage];
  queryKey?: string;
};

const statusText: Record<ResponseStage['status'], string> = {
  documented: 'Documented action',
  directed: 'Directed by order',
  'not-verified': 'Not verified here',
};

/** All six stage panels are present in prerendered HTML; JS only changes the focus view. */
export default function ResponseFlow({ reviewedAsOf, headline, introduction, scopeLabel, stages, queryKey = 'response-stage' }: ResponseFlowProps) {
  const [selected, setSelected] = useState(stages[0].id);
  const [hydrated, setHydrated] = useState(false);
  const buttons = useRef<(HTMLButtonElement | null)[]>([]);

  useEffect(() => {
    const readUrl = () => {
      const requested = new URLSearchParams(window.location.search).get(queryKey);
      setSelected(stages.some(stage => stage.id === requested) ? requested! : stages[0].id);
    };
    readUrl();
    setHydrated(true);
    window.addEventListener('popstate', readUrl);
    return () => window.removeEventListener('popstate', readUrl);
  }, [queryKey, stages]);

  const choose = (id: string) => {
    setSelected(id);
    const next = new URL(window.location.href);
    if (id === stages[0].id) next.searchParams.delete(queryKey);
    else next.searchParams.set(queryKey, id);
    window.history.pushState(null, '', `${next.pathname}${next.search}${next.hash}`);
  };

  const onStageKey = (event: KeyboardEvent<HTMLButtonElement>, index: number) => {
    const last = stages.length - 1;
    const next = event.key === 'ArrowRight' || event.key === 'ArrowDown' ? Math.min(last, index + 1)
      : event.key === 'ArrowLeft' || event.key === 'ArrowUp' ? Math.max(0, index - 1)
        : event.key === 'Home' ? 0 : event.key === 'End' ? last : -1;
    if (next < 0) return;
    event.preventDefault();
    choose(stages[next].id);
    buttons.current[next]?.focus();
    buttons.current[next]?.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'instant' });
  };

  return <section className="response-flow" data-hydrated={hydrated} aria-labelledby="rf-title">
    <div className="rf-strap"><span>{scopeLabel}</span><span>Reviewed {reviewedAsOf}</span></div>
    <header className="rf-intro">
      <div><p className="rf-kicker">Government response / evidence chain</p><h2 id="rf-title">{headline}</h2></div>
      <p>{introduction}</p>
    </header>
    <p className="rf-instruction">Select a checkpoint to inspect its evidence. Use arrow keys to move through the sequence.</p>
    <div className="rf-layout">
      <div className="rf-track" role="group" aria-label="Six checkpoints from declaration to outcome">
        {stages.map((stage, index) => <button
          key={stage.id}
          ref={element => { buttons.current[index] = element; }}
          id={`rf-button-${stage.id}`}
          type="button"
          disabled={!hydrated}
          aria-controls={`rf-panel-${stage.id}`}
          aria-expanded={hydrated ? selected === stage.id : undefined}
          aria-pressed={hydrated ? selected === stage.id : undefined}
          data-status={stage.status}
          className="rf-step"
          onClick={() => choose(stage.id)}
          onKeyDown={event => onStageKey(event, index)}
        >
          <span className="rf-node" aria-hidden="true"><span>{String(index + 1).padStart(2, '0')}</span></span>
          <span className="rf-step-copy"><strong>{stage.shortLabel}</strong><small>{statusText[stage.status]}</small></span>
          <span className="rf-step-arrow" aria-hidden="true">↗</span>
        </button>)}
      </div>
      <div className="rf-panels">
        {stages.map((stage, index) => <article key={stage.id} id={`rf-panel-${stage.id}`} className="rf-panel" data-active={selected === stage.id} data-status={stage.status} role="region" aria-labelledby={`rf-button-${stage.id}`}>
          <div className="rf-panel-top"><span>Checkpoint {String(index + 1).padStart(2, '0')} / 06</span><span>{stage.dateLabel}</span></div>
          <div className="rf-visual" aria-hidden="true"><span className="rf-visual-number">{String(index + 1).padStart(2, '0')}</span><span className="rf-visual-mark">{stage.status === 'not-verified' ? '?' : '✓'}</span></div>
          <span className="rf-status">{statusText[stage.status]}</span>
          <h3>{stage.title}</h3>
          <p className="rf-panel-headline">{stage.headline}</p>
          <p>{stage.detail}</p>
          <p className="rf-limit">{stage.limit}</p>
          {stage.sources.length > 0 && <div className="rf-sources" aria-label={`Sources for ${stage.shortLabel}`}>
            {stage.sources.map(link => <a key={`${link.href}-${link.claimId ?? ''}`} href={link.href}>{link.label} <span aria-hidden="true">↗</span>{link.claimId && <small>Claim {link.claimId}</small>}</a>)}
          </div>}
        </article>)}
      </div>
    </div>
    <p className="rf-footnote">This is an evidence trail, not a count of people helped. A later checkpoint marked “not verified here” means this release does not establish that step; it does not prove the step never happened.</p>
  </section>;
}
