import { useEffect, useId, useRef, useState } from 'react';
import type { KeyboardEvent } from 'react';
import '../styles/voices-scene.css';

export type VoiceSource = {
  label: string;
  href: string;
  claimId?: string;
};

/** Copy is supplied by the reviewed parent page; this island adds presentation only. */
export type VoicePerspective = {
  id: string;
  kind: 'farm' | 'flood' | 'response';
  tabLabel: string;
  date: string;
  dateTime: string;
  place: string;
  speaker: string;
  descriptor: string;
  outlet: string;
  status: string;
  displayWord: string;
  headline: string;
  account: string;
  context: string;
  limit: string;
  source: VoiceSource;
};

export type VoicesSceneProps = {
  eyebrow: string;
  title: string;
  introduction: string;
  sampleNote: string;
  voices: [VoicePerspective, VoicePerspective, VoicePerspective];
  queryKey?: string;
};

/** All three accounts are readable in prerendered HTML before hydration or without JS. */
export default function VoicesScene({ eyebrow, title, introduction, sampleNote, voices, queryKey = 'voice' }: VoicesSceneProps) {
  const [active, setActive] = useState(voices[0].id);
  const [hydrated, setHydrated] = useState(false);
  const buttons = useRef<(HTMLButtonElement | null)[]>([]);
  const instance = useId().replace(/:/g, '');

  useEffect(() => {
    const fromUrl = () => {
      const requested = new URLSearchParams(window.location.search).get(queryKey);
      setActive(voices.some(voice => voice.id === requested) ? requested! : voices[0].id);
    };
    fromUrl();
    setHydrated(true);
    window.addEventListener('popstate', fromUrl);
    return () => window.removeEventListener('popstate', fromUrl);
  }, [queryKey, voices]);

  const choose = (id: string) => {
    setActive(id);
    const next = new URL(window.location.href);
    if (id === voices[0].id) next.searchParams.delete(queryKey);
    else next.searchParams.set(queryKey, id);
    window.history.pushState(null, '', `${next.pathname}${next.search}${next.hash}`);
  };

  const onKey = (event: KeyboardEvent<HTMLButtonElement>, index: number) => {
    const next = event.key === 'ArrowRight' || event.key === 'ArrowDown' ? (index + 1) % voices.length
      : event.key === 'ArrowLeft' || event.key === 'ArrowUp' ? (index - 1 + voices.length) % voices.length
        : event.key === 'Home' ? 0 : event.key === 'End' ? voices.length - 1 : -1;
    if (next === -1) return;
    event.preventDefault();
    choose(voices[next].id);
    buttons.current[next]?.focus();
  };

  return <section className="voices-scene" data-hydrated={hydrated} aria-labelledby={`${instance}-title`}>
    <div className="vs-topline"><span>{eyebrow}</span><span aria-hidden="true">India Water Watch / reporting</span></div>
    <header className="vs-header">
      <div><h2 id={`${instance}-title`}>{title}</h2></div>
      <p>{introduction}</p>
    </header>
    <p className="vs-instruction">Select a perspective. Arrow keys move between accounts.</p>
    <div className="vs-nav" role="group" aria-label="Three dated reporting perspectives">
      {voices.map((voice, index) => <button
        key={voice.id}
        ref={element => { buttons.current[index] = element; }}
        id={`${instance}-button-${voice.id}`}
        type="button"
        className="vs-tab"
        data-kind={voice.kind}
        disabled={!hydrated}
        aria-controls={`${instance}-panel-${voice.id}`}
        aria-pressed={hydrated ? active === voice.id : undefined}
        aria-expanded={hydrated ? active === voice.id : undefined}
        onClick={() => choose(voice.id)}
        onKeyDown={event => onKey(event, index)}
      >
        <span className="vs-tab-number">{String(index + 1).padStart(2, '0')}</span>
        <span className="vs-tab-copy"><strong>{voice.tabLabel}</strong><small>{voice.place} / {voice.date}</small></span>
        <span className="vs-tab-arrow" aria-hidden="true">↗</span>
      </button>)}
    </div>
    <div className="vs-panels">
      {voices.map((voice, index) => <article
        key={voice.id}
        id={`${instance}-panel-${voice.id}`}
        className="vs-panel"
        data-kind={voice.kind}
        data-active={active === voice.id}
        role="region"
        aria-labelledby={`${instance}-heading-${voice.id}`}
      >
        <div className="vs-frame">
          <div className="vs-visual" aria-hidden="true">
            <span className="vs-visual-index">{String(index + 1).padStart(2, '0')} <small>/ 03</small></span>
            <span className="vs-visual-word">{voice.displayWord}</span>
            <span className="vs-visual-grid" />
          </div>
          <div className="vs-story">
            <div className="vs-meta"><span>{voice.place}</span><time dateTime={voice.dateTime}>{voice.date}</time></div>
            <span className="vs-status">{voice.status}</span>
            <h3 id={`${instance}-heading-${voice.id}`}>{voice.headline}</h3>
            <p className="vs-account">{voice.account}</p>
            <div className="vs-byline"><strong>{voice.speaker}</strong><span>{voice.descriptor}</span></div>
            <p className="vs-context">{voice.context}</p>
            <p className="vs-limit">{voice.limit}</p>
            <a className="vs-source" href={voice.source.href}>
              <span><small>Reported by {voice.outlet}</small><strong>{voice.source.label}</strong>{voice.source.claimId && <small>Claim {voice.source.claimId}</small>}</span>
              <span aria-hidden="true">↗</span>
            </a>
          </div>
        </div>
      </article>)}
    </div>
    <p className="vs-sample-note">{sampleNote}</p>
  </section>;
}
