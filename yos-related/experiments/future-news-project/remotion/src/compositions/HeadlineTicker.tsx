// ═══════════════════════════════════════════════════════════════
// FUTURE NEWS — Headline Ticker (30s, 1920×1080)
// CNEWS-style: dark background, logo reveal, headline carousel
// ═══════════════════════════════════════════════════════════════

import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { HEADLINES, ROUTES, DATE } from '../content';

const PAPER = '#F5F0E8';
const INK = '#1A1208';
const CRIMSON = '#8B1A1A';
const DARK_BG = '#0D0B08';

interface Props {
  lang: 'en' | 'fr' | 'it';
  date: string;
}

// ── Individual headline slide ────────────────────────────────
const HeadlineSlide: React.FC<{
  headline: typeof HEADLINES[0];
  lang: 'en' | 'fr' | 'it';
  frame: number;
  startFrame: number;
  durationFrames: number;
}> = ({ headline, lang, frame, startFrame, durationFrames }) => {
  const { fps } = useVideoConfig();
  const localFrame = frame - startFrame;

  const route = ROUTES.find(r => r.id === headline.routeId)!;

  // Slide in from bottom
  const slideIn = spring({
    frame: localFrame,
    fps,
    config: { damping: 18, stiffness: 120, mass: 0.8 },
  });

  // Fade out near end
  const fadeOut = interpolate(
    localFrame,
    [durationFrames - 15, durationFrames],
    [1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const translateY = interpolate(slideIn, [0, 1], [60, 0]);
  const opacity = Math.min(slideIn, fadeOut);

  return (
    <AbsoluteFill
      style={{
        opacity,
        transform: `translateY(${translateY}px)`,
        justifyContent: 'flex-end',
        padding: '0 80px 80px',
      }}
    >
      {/* Route badge */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 12,
          marginBottom: 16,
        }}
      >
        <div
          style={{
            width: 4,
            height: 32,
            backgroundColor: route.color,
          }}
        />
        <span
          style={{
            fontFamily: 'Inter, system-ui, sans-serif',
            fontSize: 16,
            fontWeight: 600,
            letterSpacing: '0.15em',
            textTransform: 'uppercase',
            color: route.color,
          }}
        >
          {route.symbol} {route.name[lang]}
        </span>
        <span
          style={{
            fontFamily: 'Inter, system-ui, sans-serif',
            fontSize: 13,
            fontWeight: 500,
            letterSpacing: '0.12em',
            textTransform: 'uppercase',
            color: CRIMSON,
            border: `1px solid ${CRIMSON}`,
            padding: '2px 8px',
          }}
        >
          {headline.milestone[lang]}
        </span>
      </div>

      {/* Headline */}
      <h1
        style={{
          fontFamily: "'Playfair Display', Georgia, serif",
          fontSize: 56,
          fontWeight: 700,
          lineHeight: 1.15,
          color: PAPER,
          margin: 0,
          maxWidth: 1400,
          textShadow: '0 2px 20px rgba(0,0,0,0.5)',
        }}
      >
        {headline.title[lang]}
      </h1>
    </AbsoluteFill>
  );
};

// ── Main composition ─────────────────────────────────────────
export const HeadlineTicker: React.FC<Props> = ({ lang }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const INTRO_FRAMES = 60; // 2s logo reveal
  const OUTRO_FRAMES = 45; // 1.5s fade out
  const CONTENT_FRAMES = durationInFrames - INTRO_FRAMES - OUTRO_FRAMES;
  const perHeadline = Math.floor(CONTENT_FRAMES / HEADLINES.length);

  // Logo reveal
  const logoScale = spring({ frame, fps, config: { damping: 14, stiffness: 80 } });
  const logoOpacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });

  // Background pulse — subtle vignette
  const vignetteOpacity = interpolate(frame, [0, 60], [0.8, 0.4], { extrapolateRight: 'clamp' });

  // Overall fade out
  const globalFade = interpolate(
    frame,
    [durationInFrames - OUTRO_FRAMES, durationInFrames],
    [1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  // Which headline is active
  const contentFrame = Math.max(0, frame - INTRO_FRAMES);
  const activeIndex = Math.min(Math.floor(contentFrame / perHeadline), HEADLINES.length - 1);

  return (
    <AbsoluteFill style={{ backgroundColor: DARK_BG, opacity: globalFade }}>
      {/* Vignette overlay */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,${vignetteOpacity}) 100%)`,
          pointerEvents: 'none',
        }}
      />

      {/* Top bar */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: 6,
          backgroundColor: CRIMSON,
        }}
      />

      {/* Date + edition line */}
      <div
        style={{
          position: 'absolute',
          top: 24,
          left: 80,
          right: 80,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <span
          style={{
            fontFamily: 'Inter, system-ui, sans-serif',
            fontSize: 14,
            fontWeight: 400,
            letterSpacing: '0.15em',
            textTransform: 'uppercase',
            color: 'rgba(245,240,232,0.5)',
          }}
        >
          {lang === 'en' ? 'ALL THE NEWS THAT WILL HAVE BEEN' : lang === 'fr' ? 'TOUTES LES NOUVELLES QUI AURONT ÉTÉ' : 'TUTTE LE NOTIZIE CHE SARANNO STATE'}
        </span>
        <span
          style={{
            fontFamily: 'Inter, system-ui, sans-serif',
            fontSize: 14,
            fontWeight: 400,
            letterSpacing: '0.15em',
            textTransform: 'uppercase',
            color: 'rgba(245,240,232,0.5)',
          }}
        >
          {lang === 'en' ? 'APRIL 4, 2027' : lang === 'fr' ? '4 AVRIL 2027' : '4 APRILE 2027'}
        </span>
      </div>

      {/* Logo — center, fades out after intro */}
      {frame < INTRO_FRAMES + 30 && (
        <AbsoluteFill
          style={{
            justifyContent: 'center',
            alignItems: 'center',
            opacity: interpolate(frame, [INTRO_FRAMES, INTRO_FRAMES + 30], [1, 0], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }),
          }}
        >
          <div
            style={{
              transform: `scale(${interpolate(logoScale, [0, 1], [0.7, 1])})`,
              opacity: logoOpacity,
              textAlign: 'center',
            }}
          >
            <img
              src="https://d2xsxph8kpxj0f.cloudfront.net/310419663032381833/6Eqiy4SpeQioR6DBUKe6r5/future_news_logo_v7_a6afeef4.jpg"
              style={{ height: 280, width: 'auto', filter: 'invert(1) brightness(0.9)' }}
              alt="Future News"
            />
            <p
              style={{
                fontFamily: "'Cormorant Garamond', Georgia, serif",
                fontStyle: 'italic',
                fontSize: 22,
                color: 'rgba(245,240,232,0.7)',
                letterSpacing: '0.2em',
                marginTop: 16,
              }}
            >
              {lang === 'en' ? 'Morning Edition' : lang === 'fr' ? 'Édition du Matin' : 'Edizione del Mattino'}
            </p>
          </div>
        </AbsoluteFill>
      )}

      {/* Headline slides */}
      {frame >= INTRO_FRAMES && HEADLINES.map((h, i) => {
        const startFrame = INTRO_FRAMES + i * perHeadline;
        if (i !== activeIndex) return null;
        return (
          <HeadlineSlide
            key={h.routeId + i}
            headline={h}
            lang={lang}
            frame={frame}
            startFrame={startFrame}
            durationFrames={perHeadline}
          />
        );
      })}

      {/* Bottom rule */}
      <div
        style={{
          position: 'absolute',
          bottom: 48,
          left: 80,
          right: 80,
          height: 1,
          backgroundColor: 'rgba(245,240,232,0.15)',
        }}
      />

      {/* Progress dots */}
      {frame >= INTRO_FRAMES && (
        <div
          style={{
            position: 'absolute',
            bottom: 24,
            left: '50%',
            transform: 'translateX(-50%)',
            display: 'flex',
            gap: 8,
          }}
        >
          {HEADLINES.map((_, i) => (
            <div
              key={i}
              style={{
                width: i === activeIndex ? 24 : 6,
                height: 6,
                backgroundColor: i === activeIndex ? CRIMSON : 'rgba(245,240,232,0.3)',
                transition: 'width 0.3s',
              }}
            />
          ))}
        </div>
      )}
    </AbsoluteFill>
  );
};
