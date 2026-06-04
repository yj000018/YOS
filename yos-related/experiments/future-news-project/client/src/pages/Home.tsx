// ═══════════════════════════════════════════════════════════════
// FUTURE NEWS — Front Page (Home)
// Design: 1900 NYT front page — featured story, 3-col grid, sidebar
// ═══════════════════════════════════════════════════════════════

import { Link } from 'wouter';
import { useLang } from '@/contexts/LanguageContext';
import { HEADLINES, ROUTES, CONFLUENCES, EDITION, getHeadlinesByRoute } from '@/lib/content';
import HeadlineCard from '@/components/HeadlineCard';

const SECTION_LABELS = {
  en: { featured: 'Today\'s Lead Story', routes: 'The Four Routes of Transformation', confluences: 'Confluences', readEdition: 'Read Full Edition →', readRoute: 'All stories →', readMore: 'Read more →' },
  fr: { featured: 'Article Phare du Jour', routes: 'Les Quatre Routes de Transformation', confluences: 'Confluences', readEdition: 'Lire l\'Édition Complète →', readRoute: 'Tous les articles →', readMore: 'Lire la suite →' },
  it: { featured: 'Articolo di Punta del Giorno', routes: 'Le Quattro Rotte di Trasformazione', confluences: 'Confluenze', readEdition: 'Leggi l\'Edizione Completa →', readRoute: 'Tutti gli articoli →', readMore: 'Leggi di più →' },
};

export default function Home() {
  const { lang } = useLang();
  const labels = SECTION_LABELS[lang];

  // Featured: first work headline
  const featured = HEADLINES[0];

  // 3 column stories: first headline from ai, robotics, energy
  const col1 = getHeadlinesByRoute('ai')[0];
  const col2 = getHeadlinesByRoute('robotics')[0];
  const col3 = getHeadlinesByRoute('energy')[0];

  // Secondary stories per route
  const workSecondary = getHeadlinesByRoute('work').slice(1, 3);
  const aiSecondary = getHeadlinesByRoute('ai').slice(1, 2);
  const roboticsSecondary = getHeadlinesByRoute('robotics').slice(1, 2);
  const energySecondary = getHeadlinesByRoute('energy').slice(1, 2);

  return (
    <div className="animate-fade-in-up">

      {/* ── FEATURED STORY (full width) ──────────────────────── */}
      <section className="mb-6">
        <div className="section-rule">
          <span className="byline" style={{ color: 'var(--color-crimson)' }}>
            {labels.featured}
          </span>
        </div>
        <div className="mt-4">
          <HeadlineCard headline={featured} size="xl" showLead={true} showRoute={true} />
        </div>
      </section>

      {/* ── THICK RULE ───────────────────────────────────────── */}
      <div className="thick-rule mb-6" />

      {/* ── 3-COLUMN GRID ────────────────────────────────────── */}
      <div
        className="grid mb-6"
        style={{
          gridTemplateColumns: '1fr 1fr 1fr',
          gap: 0,
        }}
      >
        {[col1, col2, col3].map((h, i) => (
          <div
            key={h.id}
            style={{
              paddingRight: i < 2 ? '1.5rem' : 0,
              paddingLeft: i > 0 ? '1.5rem' : 0,
              borderRight: i < 2 ? '1px solid var(--color-rule)' : 'none',
            }}
          >
            <HeadlineCard headline={h} size="lg" showLead={true} showRoute={true} />
          </div>
        ))}
      </div>

      {/* ── THICK RULE ───────────────────────────────────────── */}
      <div className="thick-rule mb-6" />

      {/* ── THE FOUR ROUTES ──────────────────────────────────── */}
      <section className="mb-8">
        <div className="section-rule mb-4">
          <span className="byline" style={{ color: 'var(--color-crimson)' }}>
            {labels.routes}
          </span>
        </div>

        <div
          className="grid"
          style={{ gridTemplateColumns: 'repeat(4, 1fr)', gap: 0 }}
        >
          {ROUTES.map((route, i) => {
            const routeHeadlines = getHeadlinesByRoute(route.id);
            const primary = routeHeadlines[0];
            const secondary = routeHeadlines[1];

            return (
              <div
                key={route.id}
                style={{
                  paddingRight: i < 3 ? '1.25rem' : 0,
                  paddingLeft: i > 0 ? '1.25rem' : 0,
                  borderRight: i < 3 ? '1px solid var(--color-rule)' : 'none',
                }}
              >
                {/* Route header */}
                <div className="flex items-center gap-2 mb-3" style={{ borderBottom: `2px solid ${route.colorHex}`, paddingBottom: '0.4rem' }}>
                  <span style={{ color: route.colorHex, fontSize: '0.8rem', fontWeight: 700 }}>
                    {route.symbol}
                  </span>
                  <Link href={`/route/${route.id}`}>
                    <span
                      className="byline"
                      style={{ color: route.colorHex, cursor: 'pointer', fontSize: '0.6rem' }}
                    >
                      {route[`name_${lang}` as keyof typeof route] as string}
                    </span>
                  </Link>
                </div>

                {/* Primary headline */}
                <HeadlineCard headline={primary} size="sm" showLead={true} className="mb-3" />

                {/* Thin rule */}
                <div className="thin-rule my-3" />

                {/* Secondary headline */}
                <HeadlineCard headline={secondary} size="sm" showLead={false} />

                {/* Read more link */}
                <Link href={`/route/${route.id}`}>
                  <span
                    style={{
                      display: 'block',
                      marginTop: '0.75rem',
                      fontFamily: 'Inter, sans-serif',
                      fontSize: '0.6rem',
                      letterSpacing: '0.1em',
                      textTransform: 'uppercase',
                      color: route.colorHex,
                      cursor: 'pointer',
                    }}
                  >
                    {labels.readRoute}
                  </span>
                </Link>
              </div>
            );
          })}
        </div>
      </section>

      {/* ── THICK RULE ───────────────────────────────────────── */}
      <div className="thick-rule mb-6" />

      {/* ── CONFLUENCES + EDITOR'S NOTE ──────────────────────── */}
      <div className="grid" style={{ gridTemplateColumns: '2fr 1fr', gap: 0 }}>

        {/* Confluences */}
        <div style={{ paddingRight: '2rem', borderRight: '1px solid var(--color-rule)' }}>
          <div className="section-rule mb-4">
            <span className="byline" style={{ color: 'var(--color-crimson)' }}>
              {labels.confluences}
            </span>
          </div>

          {CONFLUENCES.map((c, i) => (
            <div key={c.id}>
              {i > 0 && <div className="thin-rule my-4" />}
              <Link href={`/confluence/${c.id}`}>
                <article className="article-card cursor-pointer" style={{ paddingTop: '0.25rem', paddingBottom: '0.5rem' }}>
                  {/* Route symbols */}
                  <div className="flex items-center gap-1 mb-2">
                    {c.routes.map(rid => {
                      const r = ROUTES.find(x => x.id === rid)!;
                      return (
                        <span key={rid} style={{ color: r.colorHex, fontSize: '0.6rem' }}>
                          {r.symbol}
                        </span>
                      );
                    })}
                    <span className="milestone-badge" style={{ marginLeft: '4px' }}>
                      {lang === 'en' ? 'Confluence' : lang === 'fr' ? 'Confluence' : 'Confluenza'}
                    </span>
                  </div>
                  <h3 className="headline-md news-link mb-2">
                    {c[`title_${lang}` as keyof typeof c] as string}
                  </h3>
                  <p
                    className="lead-text"
                    style={{
                      fontSize: '0.875rem',
                      display: '-webkit-box',
                      WebkitLineClamp: 3,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden',
                    }}
                  >
                    {(c[`analysis_${lang}` as keyof typeof c] as string).split('\n\n')[0]}
                  </p>
                </article>
              </Link>
            </div>
          ))}
        </div>

        {/* Editor's note sidebar */}
        <div style={{ paddingLeft: '2rem' }}>
          <div className="section-rule mb-4">
            <span className="byline" style={{ color: 'var(--color-crimson)' }}>
              {lang === 'en' ? "Editor's Note" : lang === 'fr' ? 'Note de la Rédaction' : 'Nota della Redazione'}
            </span>
          </div>

          {/* Pull quote */}
          <blockquote className="pull-quote mb-4">
            "{EDITION.quote[lang].text}"
          </blockquote>
          <p
            className="byline"
            style={{ marginBottom: '1rem', color: 'var(--color-muted-text)' }}
          >
            — {EDITION.quote[lang].attribution}
          </p>

          <div className="thin-rule my-4" />

          <p
            className="lead-text"
            style={{
              fontSize: '0.875rem',
              display: '-webkit-box',
              WebkitLineClamp: 6,
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden',
            }}
          >
            {EDITION.editor_note_en.split('\n\n')[0]}
          </p>

          <Link href="/edition">
            <span
              style={{
                display: 'block',
                marginTop: '1rem',
                fontFamily: 'Inter, sans-serif',
                fontSize: '0.6rem',
                letterSpacing: '0.1em',
                textTransform: 'uppercase',
                color: 'var(--color-crimson)',
                cursor: 'pointer',
              }}
            >
              {labels.readEdition}
            </span>
          </Link>
        </div>
      </div>

    </div>
  );
}
