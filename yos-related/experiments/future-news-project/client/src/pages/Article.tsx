// ═══════════════════════════════════════════════════════════════
// FUTURE NEWS — Article Page
// Full article with headline, lead, body, related articles
// ═══════════════════════════════════════════════════════════════

import { Link, useParams } from 'wouter';
import { useLang } from '@/contexts/LanguageContext';
import { getHeadline, getRoute, getHeadlinesByRoute, HEADLINES } from '@/lib/content';
import HeadlineCard from '@/components/HeadlineCard';

const HORIZON_LABELS = {
  en: { Near: 'Near Term', Mid: 'Medium Term', Far: 'Long Term' },
  fr: { Near: 'Court terme', Mid: 'Moyen terme', Far: 'Long terme' },
  it: { Near: 'Breve termine', Mid: 'Medio termine', Far: 'Lungo termine' },
};

// Generate a plausible article body from the lead
function generateBody(lead: string, lang: string): string[] {
  // Split lead into sentences and expand
  const sentences = lead.split('. ').filter(Boolean);
  const para1 = lead;
  const para2 = lang === 'fr'
    ? "Les experts du secteur soulignent que cette évolution s'inscrit dans une tendance plus large de transformation systémique, où les avancées technologiques et les politiques publiques convergent pour créer de nouvelles réalités économiques et sociales. Les premières analyses suggèrent que les effets se propageront bien au-delà du secteur immédiatement concerné."
    : lang === 'it'
    ? "Gli esperti del settore sottolineano che questo sviluppo si inserisce in una tendenza più ampia di trasformazione sistemica, dove i progressi tecnologici e le politiche pubbliche convergono per creare nuove realtà economiche e sociali. Le prime analisi suggeriscono che gli effetti si propagheranno ben oltre il settore immediatamente interessato."
    : "Sector experts note that this development fits within a broader pattern of systemic transformation, where technological advances and public policy converge to create new economic and social realities. Early analyses suggest the effects will propagate well beyond the immediately affected sector.";

  const para3 = lang === 'fr'
    ? "Les parties prenantes interrogées par Future News expriment un optimisme mesuré, tout en soulignant la nécessité d'un cadre réglementaire adapté et d'une attention particulière aux populations les plus vulnérables à la transition. « Ce n'est pas la fin d'une ère, c'est le début d'une autre », résume un analyste sous couvert d'anonymat."
    : lang === 'it'
    ? "Le parti interessate intervistate da Future News esprimono un ottimismo misurato, sottolineando al contempo la necessità di un quadro normativo adeguato e di un'attenzione particolare alle popolazioni più vulnerabili alla transizione. «Non è la fine di un'era, è l'inizio di un'altra», riassume un analista in forma anonima."
    : "Stakeholders interviewed by Future News express measured optimism, while emphasizing the need for an appropriate regulatory framework and particular attention to populations most vulnerable to the transition. \"This is not the end of an era, it is the beginning of another,\" summarizes one analyst speaking on condition of anonymity.";

  return [para1, para2, para3];
}

export default function Article() {
  const { id } = useParams<{ id: string }>();
  const { lang } = useLang();
  const headline = getHeadline(id);

  if (!headline) {
    return (
      <div className="py-16 text-center">
        <p className="headline-md" style={{ color: 'var(--color-muted-text)' }}>Article not found.</p>
        <Link href="/">
          <span style={{ color: 'var(--color-crimson)', fontFamily: 'Inter', fontSize: '0.75rem', letterSpacing: '0.1em', textTransform: 'uppercase', cursor: 'pointer' }}>
            ← Return to Front Page
          </span>
        </Link>
      </div>
    );
  }

  const route = getRoute(headline.routeId);
  const h = headline[`headline_${lang}` as keyof typeof headline] as string;
  const lead = headline[`lead_${lang}` as keyof typeof headline] as string;
  const milestone = headline[`milestone_${lang}` as keyof typeof headline] as string;
  const body = generateBody(lead, lang);
  const horizonLabel = HORIZON_LABELS[lang][headline.horizon];

  // Related: other headlines from same route
  const related = getHeadlinesByRoute(headline.routeId)
    .filter(h2 => h2.id !== headline.id)
    .slice(0, 3);

  return (
    <div className="animate-fade-in-up">

      {/* Back link */}
      <div className="mb-4 flex items-center gap-3">
        <Link href={`/route/${headline.routeId}`}>
          <span
            style={{
              fontFamily: 'Inter, sans-serif',
              fontSize: '0.65rem',
              letterSpacing: '0.1em',
              textTransform: 'uppercase',
              color: route.colorHex,
              cursor: 'pointer',
            }}
          >
            ← {route[`name_${lang}` as keyof typeof route] as string}
          </span>
        </Link>
        <span style={{ color: 'var(--color-rule)' }}>·</span>
        <Link href="/">
          <span
            style={{
              fontFamily: 'Inter, sans-serif',
              fontSize: '0.65rem',
              letterSpacing: '0.1em',
              textTransform: 'uppercase',
              color: 'var(--color-muted-text)',
              cursor: 'pointer',
            }}
          >
            {lang === 'en' ? 'Front Page' : lang === 'fr' ? 'Une' : 'Prima Pagina'}
          </span>
        </Link>
      </div>

      <div className="thick-rule mb-6" />

      {/* Article layout: 2/3 main + 1/3 sidebar */}
      <div className="grid" style={{ gridTemplateColumns: '2fr 1fr', gap: 0 }}>

        {/* Main article */}
        <div style={{ paddingRight: '3rem', borderRight: '1px solid var(--color-rule)' }}>

          {/* Domain + badges */}
          <div className="flex items-center gap-2 mb-3 flex-wrap">
            <span style={{ color: route.colorHex, fontSize: '0.75rem' }}>{route.symbol}</span>
            <span className="byline" style={{ color: route.colorHex }}>
              {route[`name_${lang}` as keyof typeof route] as string}
            </span>
            <span className="milestone-badge">{milestone}</span>
            <span
              className={`horizon-${headline.horizon.toLowerCase()}`}
              style={{ fontFamily: 'Inter', fontSize: '0.6rem', fontWeight: 500, letterSpacing: '0.08em', textTransform: 'uppercase' }}
            >
              {horizonLabel}
            </span>
          </div>

          {/* Headline */}
          <h1 className="headline-xl mb-4">{h}</h1>

          {/* Byline */}
          <div className="flex items-center gap-3 mb-4" style={{ borderBottom: '1px solid var(--color-rule)', paddingBottom: '0.75rem' }}>
            <span className="byline">
              {lang === 'en' ? 'Future News Correspondent' : lang === 'fr' ? 'Correspondant Future News' : 'Corrispondente Future News'}
            </span>
            <span style={{ color: 'var(--color-rule)' }}>·</span>
            <span className="dateline">
              {lang === 'en' ? 'April 4, 2027' : lang === 'fr' ? '4 avril 2027' : '4 aprile 2027'}
            </span>
          </div>

          {/* Article body */}
          <div style={{ maxWidth: '65ch' }}>
            {body.map((para, i) => (
              <p
                key={i}
                className="lead-text"
                style={{
                  marginBottom: '1.25rem',
                  fontSize: i === 0 ? '1.125rem' : '1rem',
                  fontWeight: i === 0 ? 400 : 400,
                }}
              >
                {para}
              </p>
            ))}
          </div>

          {/* Interaction teaser */}
          <div
            className="mt-8 p-4"
            style={{
              backgroundColor: 'var(--color-highlight)',
              borderLeft: `3px solid ${route.colorHex}`,
            }}
          >
            <p
              style={{
                fontFamily: 'Inter, sans-serif',
                fontSize: '0.75rem',
                letterSpacing: '0.05em',
                color: 'var(--color-muted-text)',
                fontStyle: 'italic',
              }}
            >
              {lang === 'en'
                ? '↗ Interactive features — deep dives, infographics, and AI-guided exploration — coming in the next release.'
                : lang === 'fr'
                ? '↗ Fonctionnalités interactives — analyses approfondies, infographies et exploration guidée par IA — dans la prochaine version.'
                : '↗ Funzionalità interattive — approfondimenti, infografiche ed esplorazione guidata dall\'IA — nella prossima versione.'}
            </p>
          </div>
        </div>

        {/* Sidebar: related articles */}
        <div style={{ paddingLeft: '2rem' }}>
          <div className="section-rule mb-4">
            <span className="byline" style={{ color: 'var(--color-crimson)' }}>
              {lang === 'en' ? 'More from this Route' : lang === 'fr' ? 'Plus sur cette Route' : 'Altro da questa Rotta'}
            </span>
          </div>

          {related.map((rel, i) => (
            <div key={rel.id}>
              {i > 0 && <div className="thin-rule my-3" />}
              <HeadlineCard headline={rel} size="sm" showLead={false} />
            </div>
          ))}

          <div className="thin-rule my-4" />

          {/* Route description */}
          <div
            style={{
              padding: '0.75rem',
              backgroundColor: 'var(--color-highlight)',
              borderTop: `2px solid ${route.colorHex}`,
            }}
          >
            <div className="flex items-center gap-2 mb-2">
              <span style={{ color: route.colorHex, fontSize: '0.75rem' }}>{route.symbol}</span>
              <span className="byline" style={{ color: route.colorHex }}>
                {lang === 'en' ? 'About this Route' : lang === 'fr' ? 'À propos de cette Route' : 'Su questa Rotta'}
              </span>
            </div>
            <p style={{ fontFamily: 'Source Serif 4, Georgia, serif', fontSize: '0.8125rem', lineHeight: 1.6, color: 'var(--color-ink-light)' }}>
              {route[`desc_${lang}` as keyof typeof route] as string}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
