// ═══════════════════════════════════════════════════════════════
// FUTURE NEWS — Continent Futura
// Poetic destination page with coordinates
// ═══════════════════════════════════════════════════════════════

import { Link } from 'wouter';
import { useLang } from '@/contexts/LanguageContext';
import { FUTURA, ROUTES } from '@/lib/content';

export default function Futura() {
  const { lang } = useLang();
  const desc = FUTURA[`description_${lang}` as keyof typeof FUTURA] as string;
  const paras = desc.split('\n\n');

  return (
    <div className="animate-fade-in-up">
      <div className="mb-4">
        <Link href="/"><span style={{ fontFamily: 'Inter', fontSize: '0.65rem', letterSpacing: '0.1em', textTransform: 'uppercase', color: 'var(--color-muted-text)', cursor: 'pointer' }}>
          ← {lang === 'en' ? 'Front Page' : lang === 'fr' ? 'Une' : 'Prima Pagina'}
        </span></Link>
      </div>

      <div className="thick-rule mb-6" />

      {/* Header */}
      <div className="text-center mb-8">
        <p className="byline mb-2" style={{ color: 'var(--color-crimson)', letterSpacing: '0.2em' }}>
          {lang === 'en' ? 'DESTINATION' : lang === 'fr' ? 'DESTINATION' : 'DESTINAZIONE'}
        </p>
        <h1 className="font-masthead" style={{ fontSize: 'clamp(2rem, 6vw, 4rem)', letterSpacing: '0.12em', textTransform: 'uppercase' }}>
          {lang === 'en' ? 'Continent Futura' : lang === 'fr' ? 'Continent Futura' : 'Continente Futura'}
        </h1>
        <p style={{ fontFamily: 'Playfair Display, Georgia, serif', fontStyle: 'italic', fontSize: '1rem', color: 'var(--color-muted-text)', marginTop: '0.5rem' }}>
          {lang === 'en' ? 'A state of being, not a place on a map.' : lang === 'fr' ? 'Un état d\'être, pas un lieu sur une carte.' : 'Uno stato d\'essere, non un luogo su una mappa.'}
        </p>
      </div>

      <div className="grid" style={{ gridTemplateColumns: '2fr 1fr', gap: 0 }}>
        {/* Description */}
        <div style={{ paddingRight: '3rem', borderRight: '1px solid var(--color-rule)' }}>
          {paras.map((p, i) => (
            <p key={i} className="lead-text" style={{ marginBottom: '1.25rem', fontSize: i === 0 ? '1.0625rem' : '1rem' }}>
              {p}
            </p>
          ))}
        </div>

        {/* Coordinates */}
        <div style={{ paddingLeft: '2rem' }}>
          <div className="section-rule mb-4">
            <span className="byline" style={{ color: 'var(--color-crimson)' }}>
              {lang === 'en' ? 'Coordinates' : lang === 'fr' ? 'Coordonnées' : 'Coordinate'}
            </span>
          </div>

          {FUTURA.coordinates.map((coord, i) => {
            const route = ROUTES.find(r => r.id === coord.routeId)!;
            const name = coord[`name_${lang}` as keyof typeof coord] as string;
            return (
              <div key={i}>
                {i > 0 && <div className="thin-rule my-3" />}
                <div style={{ borderLeft: `3px solid ${route.colorHex}`, paddingLeft: '0.75rem' }}>
                  <div className="flex items-center gap-2 mb-1">
                    <span style={{ color: route.colorHex, fontSize: '0.6rem' }}>{route.symbol}</span>
                    <span className="byline" style={{ color: route.colorHex }}>{name}</span>
                  </div>
                  <p style={{ fontFamily: 'Source Serif 4, Georgia, serif', fontSize: '0.8125rem', lineHeight: 1.5, color: 'var(--color-ink-light)' }}>
                    {coord.description_en}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
