// ═══════════════════════════════════════════════════════════════
// FUTURE NEWS — Traversal Map
// Visual map of all 4 routes + confluences + futura
// ═══════════════════════════════════════════════════════════════

import { Link } from 'wouter';
import { useLang } from '@/contexts/LanguageContext';
import { ROUTES, CONFLUENCES, HEADLINES } from '@/lib/content';

export default function MapPage() {
  const { lang } = useLang();

  return (
    <div className="animate-fade-in-up">
      <div className="mb-4">
        <Link href="/"><span style={{ fontFamily: 'Inter', fontSize: '0.65rem', letterSpacing: '0.1em', textTransform: 'uppercase', color: 'var(--color-muted-text)', cursor: 'pointer' }}>
          ← {lang === 'en' ? 'Front Page' : lang === 'fr' ? 'Une' : 'Prima Pagina'}
        </span></Link>
      </div>

      <div className="thick-rule mb-6" />

      <div className="text-center mb-8">
        <p className="byline mb-2" style={{ color: 'var(--color-crimson)', letterSpacing: '0.2em' }}>
          {lang === 'en' ? 'NAVIGATION' : lang === 'fr' ? 'NAVIGATION' : 'NAVIGAZIONE'}
        </p>
        <h1 className="headline-xl">
          {lang === 'en' ? 'Traversal Map' : lang === 'fr' ? 'Carte de Traversée' : 'Mappa di Traversata'}
        </h1>
        <p style={{ fontFamily: 'Playfair Display, Georgia, serif', fontStyle: 'italic', fontSize: '0.9375rem', color: 'var(--color-muted-text)', marginTop: '0.5rem' }}>
          {lang === 'en' ? 'Navigate the four routes of transformation and their confluences.' : lang === 'fr' ? 'Naviguez les quatre routes de transformation et leurs confluences.' : 'Naviga le quattro rotte di trasformazione e le loro confluenze.'}
        </p>
      </div>

      {/* Routes grid */}
      <div className="grid mb-8" style={{ gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.5rem' }}>
        {ROUTES.map(route => {
          const headlines = HEADLINES.filter(h => h.routeId === route.id);
          return (
            <Link key={route.id} href={`/route/${route.id}`}>
              <div
                className="cursor-pointer"
                style={{
                  border: `2px solid ${route.colorHex}`,
                  padding: '1.25rem',
                  transition: 'background-color 0.15s',
                }}
              >
                <div className="flex items-center gap-2 mb-3">
                  <span style={{ color: route.colorHex, fontSize: '1.25rem', lineHeight: 1 }}>{route.symbol}</span>
                  <span className="headline-sm" style={{ color: route.colorHex }}>
                    {route[`name_${lang}` as keyof typeof route] as string}
                  </span>
                </div>
                <p style={{ fontFamily: 'Source Serif 4, Georgia, serif', fontSize: '0.8125rem', lineHeight: 1.5, color: 'var(--color-ink-light)', marginBottom: '1rem' }}>
                  {route[`desc_${lang}` as keyof typeof route] as string}
                </p>
                <div style={{ borderTop: `1px solid ${route.colorHex}`, paddingTop: '0.75rem' }}>
                  <span className="byline" style={{ color: route.colorHex }}>
                    {headlines.length} {lang === 'en' ? 'stories' : lang === 'fr' ? 'articles' : 'articoli'} →
                  </span>
                </div>
              </div>
            </Link>
          );
        })}
      </div>

      {/* Confluences */}
      <div className="thick-rule mb-6" />
      <div className="section-rule mb-4">
        <span className="byline" style={{ color: 'var(--color-crimson)' }}>
          {lang === 'en' ? 'Confluences — Where Routes Intersect' : lang === 'fr' ? 'Confluences — Là où les Routes se Croisent' : 'Confluenze — Dove le Rotte si Incrociano'}
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
              <div className="cursor-pointer p-4" style={{ backgroundColor: 'var(--color-highlight)', borderTop: '2px solid var(--color-rule)' }}>
                <div className="flex items-center gap-2 mb-2">
                  {c.routes.map(rid => {
                    const r = ROUTES.find(x => x.id === rid)!;
                    return <span key={rid} style={{ color: r.colorHex, fontSize: '0.75rem' }}>{r.symbol}</span>;
                  })}
                </div>
                <h3 className="headline-sm news-link">
                  {c[`title_${lang}` as keyof typeof c] as string}
                </h3>
              </div>
            </Link>
          </div>
        ))}
      </div>

      {/* Futura */}
      <div className="thick-rule mb-6 mt-6" />
      <Link href="/futura">
        <div
          className="cursor-pointer text-center p-8"
          style={{
            background: 'linear-gradient(135deg, var(--color-highlight) 0%, var(--color-paper) 100%)',
            border: '2px solid var(--color-ink)',
          }}
        >
          <p className="byline mb-2" style={{ color: 'var(--color-crimson)', letterSpacing: '0.2em' }}>
            {lang === 'en' ? 'DESTINATION' : lang === 'fr' ? 'DESTINATION' : 'DESTINAZIONE'}
          </p>
          <h2 className="font-masthead" style={{ fontSize: '2rem', letterSpacing: '0.1em', textTransform: 'uppercase' }}>
            {lang === 'en' ? 'Continent Futura' : lang === 'fr' ? 'Continent Futura' : 'Continente Futura'}
          </h2>
          <p style={{ fontFamily: 'Playfair Display, Georgia, serif', fontStyle: 'italic', fontSize: '0.9375rem', color: 'var(--color-muted-text)', marginTop: '0.5rem' }}>
            {lang === 'en' ? 'Where all routes converge →' : lang === 'fr' ? 'Là où toutes les routes convergent →' : 'Dove tutte le rotte convergono →'}
          </p>
        </div>
      </Link>
    </div>
  );
}
