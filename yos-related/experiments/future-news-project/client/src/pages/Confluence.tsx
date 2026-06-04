// ═══════════════════════════════════════════════════════════════
// FUTURE NEWS — Confluence Page
// Cross-domain analysis article
// ═══════════════════════════════════════════════════════════════

import { Link, useParams } from 'wouter';
import { useLang } from '@/contexts/LanguageContext';
import { CONFLUENCES, ROUTES } from '@/lib/content';

export default function Confluence() {
  const { id } = useParams<{ id: string }>();
  const { lang } = useLang();
  const confluence = CONFLUENCES.find(c => c.id === id);

  if (!confluence) {
    return (
      <div className="py-16 text-center">
        <p className="headline-md" style={{ color: 'var(--color-muted-text)' }}>Confluence not found.</p>
        <Link href="/"><span style={{ color: 'var(--color-crimson)', cursor: 'pointer', fontFamily: 'Inter', fontSize: '0.75rem', letterSpacing: '0.1em', textTransform: 'uppercase' }}>← Front Page</span></Link>
      </div>
    );
  }

  const title = confluence[`title_${lang}` as keyof typeof confluence] as string;
  const analysis = confluence[`analysis_${lang}` as keyof typeof confluence] as string;
  const paras = analysis.split('\n\n');

  return (
    <div className="animate-fade-in-up">
      <div className="mb-4">
        <Link href="/"><span style={{ fontFamily: 'Inter', fontSize: '0.65rem', letterSpacing: '0.1em', textTransform: 'uppercase', color: 'var(--color-muted-text)', cursor: 'pointer' }}>
          ← {lang === 'en' ? 'Front Page' : lang === 'fr' ? 'Une' : 'Prima Pagina'}
        </span></Link>
      </div>

      <div className="thick-rule mb-6" />

      <div className="grid" style={{ gridTemplateColumns: '2fr 1fr', gap: 0 }}>
        <div style={{ paddingRight: '3rem', borderRight: '1px solid var(--color-rule)' }}>
          {/* Route symbols */}
          <div className="flex items-center gap-2 mb-3">
            {confluence.routes.map(rid => {
              const r = ROUTES.find(x => x.id === rid)!;
              return (
                <span key={rid} className="flex items-center gap-1">
                  <span style={{ color: r.colorHex, fontSize: '0.75rem' }}>{r.symbol}</span>
                  <span className="byline" style={{ color: r.colorHex }}>{r[`name_${lang}` as keyof typeof r] as string}</span>
                </span>
              );
            })}
            <span className="milestone-badge">Confluence</span>
          </div>

          <h1 className="headline-xl mb-4">{title}</h1>

          <div style={{ borderBottom: '1px solid var(--color-rule)', paddingBottom: '0.75rem', marginBottom: '1.5rem' }}>
            <span className="byline">
              {lang === 'en' ? 'Future News Analysis Desk' : lang === 'fr' ? 'Bureau d\'Analyse Future News' : 'Desk Analisi Future News'}
            </span>
            <span style={{ color: 'var(--color-rule)', margin: '0 0.5rem' }}>·</span>
            <span className="dateline">
              {lang === 'en' ? 'April 4, 2027' : lang === 'fr' ? '4 avril 2027' : '4 aprile 2027'}
            </span>
          </div>

          {paras.map((p, i) => (
            <p key={i} className="lead-text" style={{ marginBottom: '1.25rem', fontSize: i === 0 ? '1.0625rem' : '1rem' }}>
              {p}
            </p>
          ))}
        </div>

        {/* Sidebar */}
        <div style={{ paddingLeft: '2rem' }}>
          <div className="section-rule mb-4">
            <span className="byline" style={{ color: 'var(--color-crimson)' }}>
              {lang === 'en' ? 'Routes in this Confluence' : lang === 'fr' ? 'Routes dans cette Confluence' : 'Rotte in questa Confluenza'}
            </span>
          </div>
          {confluence.routes.map(rid => {
            const r = ROUTES.find(x => x.id === rid)!;
            return (
              <Link key={rid} href={`/route/${rid}`}>
                <div
                  className="mb-3 p-3 cursor-pointer"
                  style={{ borderLeft: `3px solid ${r.colorHex}`, backgroundColor: 'var(--color-highlight)' }}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <span style={{ color: r.colorHex, fontSize: '0.75rem' }}>{r.symbol}</span>
                    <span className="byline" style={{ color: r.colorHex }}>{r[`name_${lang}` as keyof typeof r] as string}</span>
                  </div>
                  <p style={{ fontFamily: 'Source Serif 4, Georgia, serif', fontSize: '0.8125rem', lineHeight: 1.5, color: 'var(--color-ink-light)' }}>
                    {r[`desc_${lang}` as keyof typeof r] as string}
                  </p>
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}
