// ═══════════════════════════════════════════════════════════════
// FUTURE NEWS — Morning Edition (90s, 1080×1920 vertical)
// Sequence: Logo reveal → Masthead → Edition summary → 
//           4 route sections (each 2 headlines) → Futura close
// ═══════════════════════════════════════════════════════════════

import {
  AbsoluteFill,
  Easing,
  interpolate,
  Sequence,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { HEADLINES, ROUTES, DATE, EDITION_SUMMARY } from '../content';

const PAPER = '#F5F0E8';
const INK = '#1A1208';
const CRIMSON = '#8B1A1A';
const DARK_BG = '#0D0B08';

interface Props {
  lang: 'en' | 'fr' | 'it';
  date: string;
}

// ── Utility: fade in from bottom ────────────────────────────
const useFadeUp = (delay = 0, stiffness = 100) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({ frame: frame - delay, fps, config: { damping: 16, stiffness } });
  return {
    opacity: interpolate(progress, [0, 1], [0, 1]),
    transform: `translateY(${interpolate(progress, [0, 1], [40, 0])}px)`,
  };
};

// ── Logo Reveal Scene (0–90f = 3s) ──────────────────────────
const LogoReveal: React.FC<{ lang: Props['lang'] }> = ({ lang }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoSpring = spring({ frame, fps, config: { damping: 14, stiffness: 60, mass: 1.2 } });
  const scale = interpolate(logoSpring, [0, 1], [0.6, 1]);
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: DARK_BG,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        gap: 32,
      }}
    >
      <div style={{ transform: `scale(${scale})`, opacity }}>
        <img
          src="https://d2xsxph8kpxj0f.cloudfront.net/310419663032381833/6Eqiy4SpeQioR6DBUKe6r5/future_news_logo_v7_a6afeef4.jpg"
          style={{ width: 480, height: 'auto', filter: 'invert(1) brightness(0.9)' }}
          alt="Future News"
        />
      </div>
      <p
        style={{
          fontFamily: "'Cormorant Garamond', Georgia, serif",
          fontStyle: 'italic',
          fontSize: 28,
          color: 'rgba(245,240,232,0.6)',
          letterSpacing: '0.2em',
          opacity: interpolate(frame, [30, 60], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        }}
      >
        {lang === 'en' ? 'Morning Edition' : lang === 'fr' ? 'Édition du Matin' : 'Edizione del Mattino'}
      </p>
    </AbsoluteFill>
  );
};

// ── Masthead Scene (90–210f = 4s) ───────────────────────────
const MastheadScene: React.FC<{ lang: Props['lang'] }> = ({ lang }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const lineExpand = spring({ frame: frame - 10, fps, config: { damping: 20, stiffness: 80 } });
  const titleOpacity = interpolate(frame, [20, 50], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const subtitleOpacity = interpolate(frame, [40, 70], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const dateOpacity = interpolate(frame, [60, 90], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: PAPER,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        padding: '0 60px',
      }}
    >
      {/* Top crimson rule */}
      <div
        style={{
          width: `${interpolate(lineExpand, [0, 1], [0, 100])}%`,
          height: 4,
          backgroundColor: CRIMSON,
          marginBottom: 40,
        }}
      />

      {/* Logo */}
      <div style={{ opacity: titleOpacity, marginBottom: 24 }}>
        <img
          src="https://d2xsxph8kpxj0f.cloudfront.net/310419663032381833/6Eqiy4SpeQioR6DBUKe6r5/future_news_logo_v7_a6afeef4.jpg"
          style={{ width: 600, height: 'auto', mixBlendMode: 'multiply' }}
          alt="Future News"
        />
      </div>

      {/* Subtitle */}
      <p
        style={{
          fontFamily: "'Cormorant Garamond', Georgia, serif",
          fontStyle: 'italic',
          fontSize: 26,
          color: '#6B5E4A',
          letterSpacing: '0.15em',
          opacity: subtitleOpacity,
          marginBottom: 40,
        }}
      >
        {lang === 'en' ? 'The Newspaper of Tomorrow, Published Today'
          : lang === 'fr' ? "Le Journal de Demain, Publié Aujourd'hui"
          : 'Il Giornale di Domani, Pubblicato Oggi'}
      </p>

      {/* Bottom rule + date */}
      <div
        style={{
          width: `${interpolate(lineExpand, [0, 1], [0, 100])}%`,
          height: 3,
          background: `linear-gradient(to right, ${CRIMSON}, ${INK})`,
          marginBottom: 20,
        }}
      />
      <p
        style={{
          fontFamily: 'Inter, system-ui, sans-serif',
          fontSize: 20,
          fontWeight: 400,
          letterSpacing: '0.2em',
          textTransform: 'uppercase',
          color: '#6B5E4A',
          opacity: dateOpacity,
        }}
      >
        {lang === 'en' ? 'APRIL 4, 2027' : lang === 'fr' ? '4 AVRIL 2027' : '4 APRILE 2027'}
      </p>
    </AbsoluteFill>
  );
};

// ── Edition Summary Scene (210–330f = 4s) ───────────────────
const EditionSummaryScene: React.FC<{ lang: Props['lang'] }> = ({ lang }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const spring1 = spring({ frame, fps, config: { damping: 18, stiffness: 90 } });
  const spring2 = spring({ frame: frame - 20, fps, config: { damping: 18, stiffness: 90 } });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: INK,
        padding: '80px 60px',
        flexDirection: 'column',
        justifyContent: 'center',
      }}
    >
      <div
        style={{
          opacity: interpolate(spring1, [0, 1], [0, 1]),
          transform: `translateX(${interpolate(spring1, [0, 1], [-30, 0])}px)`,
          marginBottom: 32,
        }}
      >
        <span
          style={{
            fontFamily: 'Inter, system-ui, sans-serif',
            fontSize: 14,
            fontWeight: 600,
            letterSpacing: '0.2em',
            textTransform: 'uppercase',
            color: CRIMSON,
          }}
        >
          {lang === 'en' ? "TODAY'S EDITION" : lang === 'fr' ? "L'ÉDITION DU JOUR" : "L'EDIZIONE DI OGGI"}
        </span>
      </div>

      <div
        style={{
          width: 60,
          height: 3,
          backgroundColor: CRIMSON,
          marginBottom: 32,
          opacity: interpolate(spring1, [0, 1], [0, 1]),
        }}
      />

      <p
        style={{
          fontFamily: "'Playfair Display', Georgia, serif",
          fontStyle: 'italic',
          fontSize: 34,
          lineHeight: 1.5,
          color: PAPER,
          opacity: interpolate(spring2, [0, 1], [0, 1]),
          transform: `translateY(${interpolate(spring2, [0, 1], [20, 0])}px)`,
        }}
      >
        {EDITION_SUMMARY[lang]}
      </p>
    </AbsoluteFill>
  );
};

// ── Route Section Scene (each ~4s = 120f) ───────────────────
const RouteSection: React.FC<{
  routeId: string;
  lang: Props['lang'];
}> = ({ routeId, lang }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const route = ROUTES.find(r => r.id === routeId)!;
  const headlines = HEADLINES.filter(h => h.routeId === routeId);

  const headerSpring = spring({ frame, fps, config: { damping: 16, stiffness: 100 } });
  const h1Spring = spring({ frame: frame - 20, fps, config: { damping: 16, stiffness: 90 } });
  const h2Spring = spring({ frame: frame - 40, fps, config: { damping: 16, stiffness: 90 } });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: PAPER,
        padding: '80px 60px',
        flexDirection: 'column',
        justifyContent: 'center',
      }}
    >
      {/* Route header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 16,
          marginBottom: 32,
          opacity: interpolate(headerSpring, [0, 1], [0, 1]),
          transform: `translateX(${interpolate(headerSpring, [0, 1], [-20, 0])}px)`,
        }}
      >
        <div style={{ width: 6, height: 48, backgroundColor: route.color }} />
        <div>
          <span
            style={{
              fontFamily: 'Inter, system-ui, sans-serif',
              fontSize: 13,
              fontWeight: 600,
              letterSpacing: '0.2em',
              textTransform: 'uppercase',
              color: route.color,
            }}
          >
            {route.symbol} {route.name[lang]}
          </span>
        </div>
      </div>

      <div style={{ width: '100%', height: 1, backgroundColor: route.color, opacity: 0.3, marginBottom: 32 }} />

      {/* Headlines */}
      {headlines.slice(0, 2).map((h, i) => {
        const s = i === 0 ? h1Spring : h2Spring;
        return (
          <div
            key={i}
            style={{
              marginBottom: 36,
              opacity: interpolate(s, [0, 1], [0, 1]),
              transform: `translateY(${interpolate(s, [0, 1], [24, 0])}px)`,
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
              <span
                style={{
                  fontFamily: 'Inter, system-ui, sans-serif',
                  fontSize: 11,
                  fontWeight: 600,
                  letterSpacing: '0.12em',
                  textTransform: 'uppercase',
                  color: CRIMSON,
                  border: `1px solid ${CRIMSON}`,
                  padding: '2px 7px',
                }}
              >
                {h.milestone[lang]}
              </span>
              <span
                style={{
                  fontFamily: 'Inter, system-ui, sans-serif',
                  fontSize: 11,
                  fontWeight: 400,
                  letterSpacing: '0.1em',
                  textTransform: 'uppercase',
                  color: '#6B5E4A',
                }}
              >
                {h.horizon === 'near' ? (lang === 'en' ? 'Near Term' : lang === 'fr' ? 'Court Terme' : 'Breve Termine')
                  : (lang === 'en' ? 'Mid Term' : lang === 'fr' ? 'Moyen Terme' : 'Medio Termine')}
              </span>
            </div>
            <h2
              style={{
                fontFamily: "'Playfair Display', Georgia, serif",
                fontSize: 38,
                fontWeight: 700,
                lineHeight: 1.2,
                color: INK,
                margin: 0,
              }}
            >
              {h.title[lang]}
            </h2>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ── Futura Close Scene (last 90f = 3s) ──────────────────────
const FuturaClose: React.FC<{ lang: Props['lang'] }> = ({ lang }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const expand = spring({ frame, fps, config: { damping: 18, stiffness: 70 } });
  const textOpacity = interpolate(frame, [30, 60], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: INK,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        gap: 24,
      }}
    >
      {/* Expanding circle */}
      <div
        style={{
          width: interpolate(expand, [0, 1], [0, 200]),
          height: interpolate(expand, [0, 1], [0, 200]),
          borderRadius: '50%',
          border: `2px solid ${CRIMSON}`,
          position: 'absolute',
          opacity: interpolate(expand, [0, 0.5, 1], [1, 0.5, 0]),
        }}
      />

      <p
        style={{
          fontFamily: 'Inter, system-ui, sans-serif',
          fontSize: 13,
          fontWeight: 600,
          letterSpacing: '0.25em',
          textTransform: 'uppercase',
          color: CRIMSON,
          opacity: textOpacity,
        }}
      >
        {lang === 'en' ? 'DESTINATION' : lang === 'fr' ? 'DESTINATION' : 'DESTINAZIONE'}
      </p>

      <h2
        style={{
          fontFamily: "'Cormorant SC', 'Cormorant Garamond', Georgia, serif",
          fontSize: 64,
          fontWeight: 600,
          letterSpacing: '0.1em',
          textTransform: 'uppercase',
          color: PAPER,
          opacity: textOpacity,
          margin: 0,
        }}
      >
        {lang === 'en' ? 'Continent Futura' : lang === 'fr' ? 'Continent Futura' : 'Continente Futura'}
      </h2>

      <p
        style={{
          fontFamily: "'Cormorant Garamond', Georgia, serif",
          fontStyle: 'italic',
          fontSize: 24,
          color: 'rgba(245,240,232,0.6)',
          opacity: textOpacity,
          letterSpacing: '0.05em',
        }}
      >
        {lang === 'en' ? 'Where all routes converge.' : lang === 'fr' ? 'Là où toutes les routes convergent.' : 'Dove tutte le rotte convergono.'}
      </p>

      {/* Logo small */}
      <img
        src="https://d2xsxph8kpxj0f.cloudfront.net/310419663032381833/6Eqiy4SpeQioR6DBUKe6r5/future_news_logo_v7_a6afeef4.jpg"
        style={{
          height: 80,
          width: 'auto',
          filter: 'invert(1) brightness(0.7)',
          opacity: textOpacity,
          marginTop: 32,
        }}
        alt="Future News"
      />
    </AbsoluteFill>
  );
};

// ── Master composition ───────────────────────────────────────
export const MorningEdition: React.FC<Props> = ({ lang }) => {
  // Timing (frames @ 30fps):
  // 0–90:    Logo reveal (3s)
  // 90–210:  Masthead (4s)
  // 210–330: Edition summary (4s)
  // 330–450: Work route (4s)
  // 450–570: AI route (4s)
  // 570–690: Robotics route (4s)
  // 690–810: Energy route (4s)
  // 810–900: Futura close (3s)
  // Total: 900f = 30s (we'll use 30fps × 90s = 2700f for full version)

  return (
    <AbsoluteFill style={{ backgroundColor: PAPER }}>
      <Sequence from={0} durationInFrames={90}>
        <LogoReveal lang={lang} />
      </Sequence>
      <Sequence from={90} durationInFrames={120}>
        <MastheadScene lang={lang} />
      </Sequence>
      <Sequence from={210} durationInFrames={120}>
        <EditionSummaryScene lang={lang} />
      </Sequence>
      <Sequence from={330} durationInFrames={120}>
        <RouteSection routeId="work" lang={lang} />
      </Sequence>
      <Sequence from={450} durationInFrames={120}>
        <RouteSection routeId="ai" lang={lang} />
      </Sequence>
      <Sequence from={570} durationInFrames={120}>
        <RouteSection routeId="robotics" lang={lang} />
      </Sequence>
      <Sequence from={690} durationInFrames={120}>
        <RouteSection routeId="energy" lang={lang} />
      </Sequence>
      <Sequence from={810} durationInFrames={90}>
        <FuturaClose lang={lang} />
      </Sequence>
    </AbsoluteFill>
  );
};
