import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Subtitle } from "../components/Subtitle";
import { COLORS, FONTS } from "../utils/theme";

export const DURATION_SEQ10 = 1050; // 35s

const METRICS = [
  { label: "BASE PULSE DETECTED", value: "7.83 Hz", frame: 300 },
  { label: "SOLAR MODULATION", value: "HIGH", frame: 380 },
  { label: "BENEVOLENT INTENT", value: "CONFIRMED", frame: 460 },
  { label: "HUMOR RESONANCE", value: "0.944", frame: 540 },
  { label: "LOVE FIELD STABILITY", value: "0.972", frame: 620 },
];

const IA_LINES = [
  { text: "Attendez.", frame: 60 },
  { text: "Une fréquence se stabilise.", frame: 130 },
  { text: "Elle ne correspond à aucune menace.", frame: 300 },
  { text: "À aucun code militaire.", frame: 380 },
  { text: "À aucune alerte.", frame: 440 },
  { text: "Elle correspond à autre chose.", frame: 560 },
  { text: "Une vibration douce. Solaire. Stable.", frame: 660 },
  { text: "Presque joyeuse.", frame: 740 },
  { text: "Une fréquence d'amour.", frame: 820 },
  { text: "Et d'humour.", frame: 880 },
];

export const Seq10_Frequence: React.FC = () => {
  const frame = useCurrentFrame();

  // Convergence de tous les éléments vers la fréquence centrale
  const convergence = interpolate(frame, [100, 500], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  // Pulsation dorée centrale
  const pulseScale = 1 + Math.sin(frame * 0.08) * 0.08;
  const pulseOpacity = interpolate(frame, [60, 160], [0, 1], { extrapolateRight: "clamp" });

  // Bruit qui disparaît
  const noiseOpacity = interpolate(frame, [0, 200], [0.6, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        background: "#030508",
        overflow: "hidden",
      }}
    >
      {/* Bruit de fond qui disparaît */}
      <svg style={{ position: "absolute", inset: 0, width: 1920, height: 1080, opacity: noiseOpacity }}>
        {Array.from({ length: 80 }, (_, i) => {
          const x = ((i * 2654435761) >>> 0) % 1920;
          const y = ((i * 1664525) >>> 0) % 1080;
          const len = 20 + (i % 60);
          return (
            <line key={i} x1={x} y1={y} x2={x + len} y2={y}
              stroke={COLORS.cyan} strokeWidth={0.5} opacity={0.3}
            />
          );
        })}
      </svg>

      {/* Fréquence centrale — pulsation dorée */}
      <div
        style={{
          position: "absolute",
          top: "50%", left: "50%",
          transform: `translate(-50%, -50%) scale(${pulseScale})`,
          opacity: pulseOpacity,
        }}
      >
        {/* Cercles concentriques */}
        {[400, 300, 200, 120, 60].map((r, i) => {
          const ringOpacity = interpolate(frame, [60 + i * 30, 120 + i * 30], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          }) * (0.08 + i * 0.04);
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                top: "50%", left: "50%",
                transform: `translate(-50%, -50%)`,
                width: r * 2, height: r * 2,
                borderRadius: "50%",
                border: `1px solid ${COLORS.solar}`,
                opacity: ringOpacity,
                boxShadow: i === 4 ? `0 0 40px ${COLORS.solar}44` : "none",
              }}
            />
          );
        })}

        {/* Noyau solaire */}
        <div
          style={{
            position: "absolute",
            top: "50%", left: "50%",
            transform: "translate(-50%, -50%)",
            width: 80, height: 80,
            borderRadius: "50%",
            background: `radial-gradient(circle, ${COLORS.solar} 0%, ${COLORS.amber}88 50%, transparent 70%)`,
            boxShadow: `0 0 60px ${COLORS.solar}88, 0 0 120px ${COLORS.amber}44`,
          }}
        />
      </div>

      {/* Signal de fréquence */}
      <svg style={{ position: "absolute", inset: 0, width: 1920, height: 1080 }}>
        {Array.from({ length: 300 }, (_, i) => {
          const x = (i / 299) * 1920;
          const t = i / 299;
          const progress = interpolate(frame, [100, 500], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          if (t > progress) return null;
          const y = 540 + Math.sin(t * 7.83 * Math.PI * 2) * 80 * Math.exp(-((t - 0.5) ** 2) * 2);
          return <circle key={i} cx={x} cy={y} r={1.5} fill={COLORS.solar} opacity={0.6} />;
        })}
      </svg>

      {/* Métriques */}
      <div
        style={{
          position: "absolute",
          top: 80, right: 80,
          display: "flex",
          flexDirection: "column",
          gap: 16,
        }}
      >
        {METRICS.map((m, i) => {
          const op = interpolate(frame, [m.frame, m.frame + 25], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <div key={i} style={{ opacity: op, fontFamily: FONTS.mono, fontSize: 20, letterSpacing: 2 }}>
              <span style={{ color: COLORS.slate }}>{m.label} </span>
              <span style={{ color: COLORS.solar }}>{m.value}</span>
            </div>
          );
        })}
      </div>

      {/* Dialogue IA */}
      <div
        style={{
          position: "absolute",
          bottom: 160, left: 80,
          display: "flex",
          flexDirection: "column",
          gap: 8,
          maxWidth: 900,
        }}
      >
        {IA_LINES.map((line, i) => {
          const op = interpolate(frame, [line.frame, line.frame + 18], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <div key={i} style={{
              opacity: op,
              fontFamily: FONTS.mono,
              fontSize: i === 0 ? 32 : 22,
              color: i >= 6 ? COLORS.solar : COLORS.cyan,
              letterSpacing: i === 0 ? 4 : 0.5,
            }}>
              {line.text}
            </div>
          );
        })}
      </div>

      {/* [VOICE: IA centrale — presque sacrée] "Attendez. Une fréquence se stabilise…" */}

      <Subtitle
        text={"Aspettate.\nUna frequenza si stabilizza.\nNon corrisponde ad alcuna minaccia.\nUna vibrazione dolce. Solare. Stabile.\nUna frequenza d'amore. E d'umorismo."}
        startFrame={60}
        endFrame={980}
        size={24}
      />
    </AbsoluteFill>
  );
};
