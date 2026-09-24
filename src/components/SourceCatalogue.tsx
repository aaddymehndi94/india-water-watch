import { useEffect, useState } from 'react';
import type { Source } from '../lib/publication';

type Props = { approved: Source[]; leads: Source[]; base: string };
type Filter = 'all' | 'approved' | 'discovery';
export default function SourceCatalogue({ approved, leads, base }: Props) {
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState<Filter>('all');
  useEffect(() => {
    const read = () => { const params = new URLSearchParams(location.search); setQuery(params.get('q') || ''); const f = params.get('status'); setFilter(f === 'approved' || f === 'discovery' ? f : 'all'); };
    read(); window.addEventListener('popstate', read); return () => window.removeEventListener('popstate', read);
  }, []);
  function update(q: string, f: Filter) {
    setQuery(q); setFilter(f);
    const params = new URLSearchParams();
    if (q.trim()) params.set('q', q.trim());
    if (f !== 'all') params.set('status', f);
    history.pushState(null, '', `${location.pathname}${params.size ? `?${params}` : ''}`);
  }
  const entries = [...approved.map(source => ({ source, approved: true })), ...leads.map(source => ({ source, approved: false }))].filter(({ source, approved }) => {
    if (filter === 'approved' && !approved) return false;
    if (filter === 'discovery' && approved) return false;
    const haystack = [source.title, source.publisher, source.locator, ...(source.topics || [])].join(' ').toLocaleLowerCase();
    return haystack.includes(query.trim().toLocaleLowerCase());
  });
  return <div className="atlas-workbench"><div className="grid-2 atlas-controls"><div className="field"><label htmlFor="source-query">Find a source</label><input id="source-query" type="search" value={query} onChange={e => update(e.target.value, filter)} placeholder="Rainfall, storage, households…" /></div><div className="field"><label htmlFor="source-filter">Record status</label><select id="source-filter" value={filter} onChange={e => update(query, e.target.value as Filter)}><option value="all">All records</option><option value="approved">Approved evidence</option><option value="discovery">Discovery leads</option></select></div></div><p className="small muted atlas-result" aria-live="polite">{entries.length} of {approved.length + leads.length} records match. A discovery lead does not support a published finding.</p>{entries.length ? <ul className="source-list">{entries.map(({ source, approved }) => <li key={`${approved ? 'approved' : 'lead'}-${source.id}`}><span className="tag">{approved ? 'Approved evidence' : 'Discovery lead'}</span><a href={`${base}${encodeURIComponent(source.id)}/`}>{source.title} ↗</a><small>{source.publisher} · {approved ? `retrieved ${source.retrievedAt?.slice(0, 10) || 'date unknown'}` : `last checked ${source.checked_on || 'date unknown'}`}</small></li>)}</ul> : <div className="empty-panel"><h3>No matching source</h3><p>Try a broader term or show all records.</p></div>}</div>;
}
