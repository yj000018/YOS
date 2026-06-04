// ═══════════════════════════════════════════════════════════════
// FUTURE NEWS — Edition Page
// Full edition view with editor's note, all routes, confluences
// ═══════════════════════════════════════════════════════════════

import { Link } from 'wouter';
import { useLang } from '@/contexts/LanguageContext';
import { EDITION, ROUTES, CONFLUENCES, getHeadlinesByRoute } from '@/lib/content';
import HeadlineCard from '@/components/HeadlineCard';

export default function Edition() {
  const { lang } = useLang();
  const enote = EDITION[`editor_note_${lang}` as keyof typeof EDITION] as string;
  const paras = enote.split('\n\n');

  return (
    <div className="animate-fade-in-up">

      {/* Header */}
      <div className="section-rule mb-6">
        <span className="byline" style={{ color: 'var(--color-crimson)' }}>
          {lang === 'en' ? 'April 4, 2027 — Complete Edition' : lang === 'fr' ? '4 Avril 2027 — Édition Complète' : '4 Aprile 2027 — Edizione Completa'}
        </span>
      </div>

      {/* Editor's note + pull quote */}
      <div className="grid mb-8" style={{ gridTemplateColumns: '2fr 1fr', gap: 0 }}>
        <div style={{ paddingRight: '2.5rem', borderRight: '1px solid var(--color-rule)' }}>
          <h2 className="headline-lg mb-4">
            {lang === 'en' ? "Editor's Note" : lang === 'fr' ? 'Note de la Rédaction' : 'Nota della Redazione'}
          </h2>
          {paras.map((p, i) => (
            <p key={i} className="lead-text" style={{ marginBottom: '1rem' }}>{p}</p>
          ))}
        </div>
        <div style={{ paddingLeft: '2.5rem' }}>
          <blockquote className="pull-quote mb-4">
            "{EDITION.quote[lang].text}"
          </blockquote>
          <p className="byline" style={{ color: 'var(--color-muted-text)' }}>
            — {EDITION.quote[lang].attribution}
          </p>
        </div>
      </div>

      <div className="thick-rule mb-8" />

      {/* All 4 routes */}
      {ROUTES.map((route, ri) => {
        const headlines = getHeadlinesByRoute(route.id);
        return (
          <div key={route.id} className="mb-8">
            <div style={{ borderTop: `3px solid ${route.colorHex}`, paddingTop: '0.75rem', marginBottom: '1.25rem' }}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span style={{ color: route.colorHex, fontSize: '1rem' }}>{route.symbol}</span>
                  <h2 className="headline-md" style={{ color: route.colorHex }}>
                    {route[`name_${lang}` as keyof typeof route] as string}
                  </h2>
                </div>
                <Link href={`/route/${route.id}`}>
                  <span style={{ fontFamily: 'Inter', fontSize: '0.6rem', letterSpacing: '0.1em', textTransform: 'uppercase', color: route.colorHex, cursor: 'pointer' }}>
                    {lang === 'en' ? 'All stories →' : lang === 'fr' ? 'Tous les articles →' : 'Tutti gli articoli →'}
                  </span>
                </Link>
              </div>
            </div>

            <div className="grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)', gap: 0 }}>
              {headlines.slice(0, 3).map((h, i) => (
                <div key={h.id} style={{
                  paddingRight: i < 2 ? '1.5rem' : 0,
                  paddingLeft: i > 0 ? '1.5rem' : 0,
                  borderRight: i < 2 ? '1px solid var(--color-rule)' : 'none',
                }}>
                  <HeadlineCard headline={h} size={i === 0 ? 'md' : 'sm'} showLead={i === 0} />
                </div>
              ))}
            </div>

            {ri < ROUTES.length - 1 && <div className="thick-rule mt-6" />}
          </div>
        );
      })}

      {/* Confluences */}
      <div className="thick-rule mb-6" />
      <div className="section-rule mb-4">
        <span className="byline" style={{ color: 'var(--color-crimson)' }}>
          {lang === 'en' ? 'Confluences' : lang === 'fr' ? 'Confluences' : 'Confluenze'}
        </span>
      </div>
      <div className="grid" style={{ gridTemplateColumns: '1fr 1fr', gap: 0 }}>
        {CONFLUENCES.map((c, i) => (
          <div key={c.id} style={{
            paddingRight: i === 0 ? '2rem' : 0,
            paddingLeft: i === 1 ? '2rem' : 0,
            borderRight: i === 0 ? '1px solid var(--color-rule)' : 'none',
          }}>
            <Link href={`/confluence/${c.id}`}>
              <article className="article-card cursor-pointer" style={{ paddingTop: '0.5rem', paddingBottom: '0.75rem' }}>
                <div className="flex items-center gap-1 mb-2">
                  {c.routes.map(rid => {
                    const r = ROUTES.find(x => x.id === rid)!;
                    return <span key={rid} style={{ color: r.colorHex, fontSize: '0.6rem' }}>{r.symbol}</span>;
                  })}
                  <span className="milestone-badge" style={{ marginLeft: '4px' }}>Confluence</span>
                </div>
                <h3 className="headline-md news-link mb-2">{c[`title_${lang}` as keyof typeof c] as string}</h3>
                <p className="lead-text" style={{ fontSize: '0.875rem', display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                  {(c[`analysis_${lang}` as keyof typeof c] as string).split('\n\n')[0]}
                </p>
              </article>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
