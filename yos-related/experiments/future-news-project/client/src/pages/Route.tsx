// ═══════════════════════════════════════════════════════════════
// FUTURE NEWS — Route Page
// All 5 articles for a transformation domain
// ═══════════════════════════════════════════════════════════════

import { Link, useParams } from 'wouter';
import { useLang } from '@/contexts/LanguageContext';
import { getRoute, getHeadlinesByRoute, ROUTES, CONFLUENCES } from '@/lib/content';
import type { RouteId } from '@/lib/content';
import HeadlineCard from '@/components/HeadlineCard';

export default function Route() {
  const { id } = useParams<{ id: string }>();
  const { lang } = useLang();
  const route = getRoute(id as RouteId);

  if (!route) {
    return (
      <div className="py-16 text-center">
        <p className="headline-md" style={{ color: 'var(--color-muted-text)' }}>Route not found.</p>
        <Link href="/"><span style={{ color: 'var(--color-crimson)', cursor: 'pointer', fontFamily: 'Inter', fontSize: '0.75rem', letterSpacing: '0.1em', textTransform: 'uppercase' }}>← Front Page</span></Link>
      </div>
    );
  }

  const headlines = getHeadlinesByRoute(id as RouteId);
  const [primary, ...rest] = headlines;
  const relatedConfluences = CONFLUENCES.filter(c => c.routes.includes(id as RouteId));

  return (
    <div className="animate-fade-in-up">

      {/* Back */}
      <div className="mb-4">
        <Link href="/">
          <span style={{ fontFamily: 'Inter', fontSize: '0.65rem', letterSpacing: '0.1em', textTransform: 'uppercase', color: 'var(--color-muted-text)', cursor: 'pointer' }}>
            ← {lang === 'en' ? 'Front Page' : lang === 'fr' ? 'Une' : 'Prima Pagina'}
          </span>
        </Link>
      </div>

      {/* Route header */}
      <div style={{ borderTop: `4px solid ${route.colorHex}`, paddingTop: '1rem', marginBottom: '1.5rem' }}>
        <div className="flex items-center gap-3 mb-2">
          <span style={{ color: route.colorHex, fontSize: '1.5rem', lineHeight: 1 }}>{route.symbol}</span>
          <div>
            <h1 className="headline-lg" style={{ color: route.colorHex, marginBottom: '0.25rem' }}>
              {route[`name_${lang}` as keyof typeof route] as string}
            </h1>
            <p className="lead-text" style={{ fontSize: '0.9375rem', color: 'var(--color-muted-text)' }}>
              {route[`desc_${lang}` as keyof typeof route] as string}
            </p>
          </div>
        </div>

        {/* Other routes */}
        <div className="flex items-center gap-3 mt-3" style={{ borderTop: '1px solid var(--color-rule)', paddingTop: '0.75rem' }}>
          <span className="byline">{lang === 'en' ? 'Other Routes:' : lang === 'fr' ? 'Autres Routes :' : 'Altre Rotte:'}</span>
          {ROUTES.filter(r => r.id !== id).map(r => (
            <Link key={r.id} href={`/route/${r.id}`}>
              <span
                className="flex items-center gap-1"
                style={{ fontFamily: 'Inter', fontSize: '0.65rem', letterSpacing: '0.08em', textTransform: 'uppercase', color: r.colorHex, cursor: 'pointer' }}
              >
                <span style={{ fontSize: '0.55rem' }}>{r.symbol}</span>
                {r[`name_${lang}` as keyof typeof r] as string}
              </span>
            </Link>
          ))}
        </div>
      </div>

      {/* Primary story */}
      <div className="thick-rule mb-6" />
      <div className="mb-6">
        <HeadlineCard headline={primary} size="xl" showLead={true} />
      </div>

      {/* Remaining stories: 2-column grid */}
      <div className="thick-rule mb-6" />
      <div className="grid" style={{ gridTemplateColumns: '1fr 1fr', gap: 0 }}>
        {rest.map((h, i) => (
          <div
            key={h.id}
            style={{
              paddingRight: i % 2 === 0 ? '2rem' : 0,
              paddingLeft: i % 2 === 1 ? '2rem' : 0,
              paddingBottom: '1.5rem',
              borderRight: i % 2 === 0 ? '1px solid var(--color-rule)' : 'none',
              borderBottom: i < rest.length - 2 ? '1px solid var(--color-rule)' : 'none',
              paddingTop: i >= 2 ? '1.5rem' : 0,
            }}
          >
            <HeadlineCard headline={h} size="md" showLead={true} />
          </div>
        ))}
      </div>

      {/* Confluences */}
      {relatedConfluences.length > 0 && (
        <>
          <div className="thick-rule mb-6 mt-6" />
          <div className="section-rule mb-4">
            <span className="byline" style={{ color: 'var(--color-crimson)' }}>
              {lang === 'en' ? 'Confluences' : lang === 'fr' ? 'Confluences' : 'Confluenze'}
            </span>
          </div>
          {relatedConfluences.map(c => (
            <Link key={c.id} href={`/confluence/${c.id}`}>
              <article className="article-card cursor-pointer mb-4" style={{ borderLeft: `3px solid ${route.colorHex}`, paddingLeft: '0.875rem', paddingTop: '0.5rem', paddingBottom: '0.75rem' }}>
                <div className="flex items-center gap-2 mb-2">
                  {c.routes.map(rid => {
                    const r = ROUTES.find(x => x.id === rid)!;
                    return <span key={rid} style={{ color: r.colorHex, fontSize: '0.6rem' }}>{r.symbol}</span>;
                  })}
                  <span className="milestone-badge">Confluence</span>
                </div>
                <h3 className="headline-md news-link">{c[`title_${lang}` as keyof typeof c] as string}</h3>
              </article>
            </Link>
          ))}
        </>
      )}
    </div>
  );
}
