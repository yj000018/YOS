// ═══════════════════════════════════════════════════════════════
// FUTURE NEWS — HeadlineCard
// Design: Newspaper article card with domain symbol, milestone badge, horizon
// ═══════════════════════════════════════════════════════════════

import { Link } from 'wouter';
import { useLang } from '@/contexts/LanguageContext';
import { getRoute } from '@/lib/content';
import type { Headline } from '@/lib/content';

interface HeadlineCardProps {
  headline: Headline;
  size?: 'xl' | 'lg' | 'md' | 'sm';
  showLead?: boolean;
  showRoute?: boolean;
  className?: string;
}

const HORIZON_LABELS = {
  en: { Near: 'Near Term', Mid: 'Medium Term', Far: 'Long Term' },
  fr: { Near: 'Court terme', Mid: 'Moyen terme', Far: 'Long terme' },
  it: { Near: 'Breve termine', Mid: 'Medio termine', Far: 'Lungo termine' },
};

export default function HeadlineCard({
  headline,
  size = 'md',
  showLead = true,
  showRoute = false,
  className = '',
}: HeadlineCardProps) {
  const { lang } = useLang();
  const route = getRoute(headline.routeId);
  const horizonLabel = HORIZON_LABELS[lang][headline.horizon];

  const h = headline[`headline_${lang}` as keyof Headline] as string;
  const lead = headline[`lead_${lang}` as keyof Headline] as string;
  const milestone = headline[`milestone_${lang}` as keyof Headline] as string;

  const headlineClass =
    size === 'xl' ? 'headline-xl' :
    size === 'lg' ? 'headline-lg' :
    size === 'md' ? 'headline-md' :
    'headline-sm';

  return (
    <Link href={`/article/${headline.id}`}>
      <article
        className={`article-card cursor-pointer ${className}`}
        style={{
          borderLeft: `3px solid ${route.colorHex}`,
          paddingLeft: '0.875rem',
          paddingTop: '0.5rem',
          paddingBottom: '0.75rem',
        }}
      >
        {/* Domain symbol + milestone badge */}
        <div className="flex items-center gap-2 mb-2 flex-wrap">
          <span
            style={{
              color: route.colorHex,
              fontSize: size === 'xl' ? '0.75rem' : '0.6rem',
              lineHeight: 1,
            }}
          >
            {route.symbol}
          </span>
          {showRoute && (
            <span
              className="byline"
              style={{ color: route.colorHex, fontSize: '0.6rem' }}
            >
              {route[`name_${lang}` as keyof typeof route] as string}
            </span>
          )}
          <span className="milestone-badge">{milestone}</span>
          <span
            className={`horizon-${headline.horizon.toLowerCase()}`}
            style={{
              fontFamily: 'Inter, sans-serif',
              fontSize: '0.6rem',
              fontWeight: 500,
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
            }}
          >
            {horizonLabel}
          </span>
        </div>

        {/* Headline */}
        <h2 className={`${headlineClass} news-link mb-2`} style={{ marginBottom: showLead ? '0.5rem' : 0 }}>
          {h}
        </h2>

        {/* Lead */}
        {showLead && (
          <p
            className="lead-text"
            style={{
              fontSize: size === 'xl' ? '1.0625rem' : size === 'lg' ? '0.9375rem' : '0.875rem',
              display: '-webkit-box',
              WebkitLineClamp: size === 'xl' ? 3 : 2,
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden',
            }}
          >
            {lead}
          </p>
        )}
      </article>
    </Link>
  );
}
