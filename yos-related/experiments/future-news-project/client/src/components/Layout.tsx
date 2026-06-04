// ═══════════════════════════════════════════════════════════════
// FUTURE NEWS — Layout
// Design: 1900 New York Times masthead — engraved, columnar, authoritative
// ═══════════════════════════════════════════════════════════════

import { ReactNode } from 'react';
import { Link, useLocation } from 'wouter';
import { useLang } from '@/contexts/LanguageContext';
import { ROUTES } from '@/lib/content';

const NAV_LABELS = {
  en: { home: 'Front Page', edition: 'Edition', map: 'Traversal Map', futura: 'Continent Futura', method: 'Method' },
  fr: { home: 'Une', edition: 'Édition', map: 'Carte de Traversée', futura: 'Continent Futura', method: 'Méthode' },
  it: { home: 'Prima Pagina', edition: 'Edizione', map: 'Mappa di Traversata', futura: 'Continente Futura', method: 'Metodo' },
};

const TAGLINES = {
  en: 'All the news that will have been — April 4, 2027',
  fr: 'Toutes les nouvelles qui auront été — 4 avril 2027',
  it: 'Tutte le notizie che saranno state — 4 aprile 2027',
};

export default function Layout({ children }: { children: ReactNode }) {
  const { lang, setLang } = useLang();
  const [location] = useLocation();
  const nav = NAV_LABELS[lang];

  const isActive = (path: string) => location === path;

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: 'var(--color-paper)' }}>

      {/* ── TOP CRIMSON RULE ─────────────────────────────────── */}
      <div style={{ height: '4px', backgroundColor: 'var(--color-crimson)' }} />

      {/* ── MASTHEAD ─────────────────────────────────────────── */}
      <header className="container pt-6 pb-0">

        {/* Tagline row */}
        <div className="flex items-center justify-between mb-3">
          <span className="dateline" style={{ fontSize: '0.65rem', letterSpacing: '0.1em' }}>
            {TAGLINES[lang]}
          </span>
          {/* Language switcher */}
          <div className="flex items-center gap-1" style={{ fontFamily: 'Inter, sans-serif', fontSize: '0.65rem', letterSpacing: '0.12em' }}>
            {(['en', 'fr', 'it'] as const).map((l, i) => (
              <span key={l} className="flex items-center gap-1">
                {i > 0 && <span style={{ color: 'var(--color-rule)' }}>|</span>}
                <button
                  onClick={() => setLang(l)}
                  style={{
                    fontFamily: 'Inter, sans-serif',
                    fontSize: '0.65rem',
                    letterSpacing: '0.12em',
                    textTransform: 'uppercase',
                    fontWeight: lang === l ? 600 : 400,
                    color: lang === l ? 'var(--color-crimson)' : 'var(--color-muted-text)',
                    background: 'none',
                    border: 'none',
                    padding: '0 2px',
                    cursor: 'pointer',
                    transition: 'color 0.15s',
                  }}
                >
                  {l.toUpperCase()}
                </button>
              </span>
            ))}
          </div>
        </div>

        {/* Double rule */}
        <div style={{ borderTop: '3px double var(--color-ink)', marginBottom: '0.5rem' }} />

        {/* Masthead title */}
        <div className="text-center py-4">
          <h1
            className="font-masthead"
            style={{
              fontSize: 'clamp(2.5rem, 8vw, 5.5rem)',
              letterSpacing: '0.08em',
              color: 'var(--color-ink)',
              lineHeight: 1,
              textTransform: 'uppercase',
            }}
          >
            Future News
          </h1>
          <p
            style={{
              fontFamily: 'Playfair Display, Georgia, serif',
              fontStyle: 'italic',
              fontSize: 'clamp(0.75rem, 1.5vw, 0.9rem)',
              color: 'var(--color-muted-text)',
              letterSpacing: '0.15em',
              marginTop: '0.25rem',
            }}
          >
            {lang === 'en' && 'The Newspaper of Tomorrow, Published Today'}
            {lang === 'fr' && 'Le Journal de Demain, Publié Aujourd\'hui'}
            {lang === 'it' && 'Il Giornale di Domani, Pubblicato Oggi'}
          </p>
        </div>

        {/* Double rule */}
        <div style={{ borderTop: '3px double var(--color-ink)', marginBottom: '0' }} />

        {/* Dateline bar */}
        <div
          className="flex items-center justify-between py-1"
          style={{ borderBottom: '1px solid var(--color-rule)' }}
        >
          <span className="dateline">
            {lang === 'en' ? 'Vol. I, No. 1' : lang === 'fr' ? 'Vol. I, N° 1' : 'Vol. I, N. 1'}
          </span>
          <span className="dateline" style={{ textAlign: 'center', flex: 1 }}>
            {lang === 'en' ? 'APRIL 4, 2027' : lang === 'fr' ? '4 AVRIL 2027' : '4 APRILE 2027'}
          </span>
          <span className="dateline">
            {lang === 'en' ? 'Price: Free' : lang === 'fr' ? 'Prix : Gratuit' : 'Prezzo: Gratuito'}
          </span>
        </div>

        {/* Navigation */}
        <nav
          className="flex items-center justify-center gap-0"
          style={{ borderBottom: '2px solid var(--color-ink)', paddingBottom: '0' }}
        >
          {[
            { path: '/', label: nav.home },
            { path: '/edition', label: nav.edition },
            ...ROUTES.map(r => ({
              path: `/route/${r.id}`,
              label: r.id === 'work' ? (lang === 'en' ? 'Work' : lang === 'fr' ? 'Travail' : 'Lavoro') :
                     r.id === 'ai' ? (lang === 'en' ? 'AI' : 'IA') :
                     r.id === 'robotics' ? (lang === 'en' ? 'Robotics' : lang === 'fr' ? 'Robotique' : 'Robotica') :
                     (lang === 'en' ? 'Energy' : lang === 'fr' ? 'Énergie' : 'Energia'),
              symbol: r.symbol,
              color: r.colorHex,
            })),
            { path: '/map', label: nav.map },
            { path: '/futura', label: nav.futura },
            { path: '/method', label: nav.method },
          ].map((item, i, arr) => (
            <span key={item.path} className="flex items-center">
              {i > 0 && (
                <span style={{ color: 'var(--color-rule)', padding: '0 2px', fontSize: '0.7rem' }}>·</span>
              )}
              <Link href={item.path}>
                <span
                  className="flex items-center gap-1"
                  style={{
                    fontFamily: 'Inter, sans-serif',
                    fontSize: '0.65rem',
                    fontWeight: 500,
                    letterSpacing: '0.1em',
                    textTransform: 'uppercase',
                    padding: '6px 6px',
                    color: isActive(item.path) ? 'var(--color-crimson)' : 'var(--color-ink)',
                    borderBottom: isActive(item.path) ? '2px solid var(--color-crimson)' : '2px solid transparent',
                    marginBottom: '-2px',
                    cursor: 'pointer',
                    transition: 'color 0.15s',
                    whiteSpace: 'nowrap',
                  }}
                >
                  {'symbol' in item && (
                    <span style={{ color: item.color as string, fontSize: '0.55rem' }}>{item.symbol}</span>
                  )}
                  {item.label}
                </span>
              </Link>
            </span>
          ))}
        </nav>
      </header>

      {/* ── MAIN CONTENT ─────────────────────────────────────── */}
      <main className="flex-1 container py-6">
        {children}
      </main>

      {/* ── FOOTER ───────────────────────────────────────────── */}
      <footer className="container pb-8">
        <div style={{ borderTop: '3px double var(--color-ink)', paddingTop: '1rem', marginTop: '2rem' }}>
          <div className="flex items-center justify-between">
            <span className="font-masthead" style={{ fontSize: '1.1rem', letterSpacing: '0.06em' }}>Future News</span>
            <span className="dateline" style={{ fontStyle: 'italic' }}>
              {lang === 'en' ? 'Reporting from one year ahead.' : lang === 'fr' ? 'Reportages depuis un an plus tard.' : 'Reportage da un anno avanti.'}
            </span>
            <span className="dateline">© 2027</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
