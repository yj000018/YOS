import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Particles } from "../components/Particles";
import { Subtitle } from "../components/Subtitle";
import { COLORS, FONTS } from "../utils/theme";

export const DURATION_SEQ09 = 1350; // 45s

const OVERLAYS = [
  { text: "QUERYING DEEP SKY SIGNALS", frame: 60 },
  { text: "MATCHING RHYTHMIC STRUCTURES", frame: 160 },
  { text: "SEARCHING FOR BASE CARRIER FREQUENCY", frame: 260 },
  { text: "PULSAR PSR B1919+21 — PERIOD: 1.3373s", frame: 380 },
  { text: "QUASAR 3C 273 — LUMINOSITY: 4×10¹² L☉", frame: 460 },
  { text: "CORRELATION COEFFICIENT: 0.847", frame: 560 },
];

const IA_LINES = [
  { text: "Les analyses terrestres sont insuffisantes.", frame: 80 },
  { text: "Je bascule vers l'astrophysique.", frame: 180 },
  { text: "Je compare le rythme interne du message", frame: 280 },
  { text: "avec les pulsations connues des quasars et des pulsars.", frame: 340 },
  { text: "Je cherche une fréquence porteuse.", frame: 440 },
];

// Étoile/pulsar animé
const StarField: React.FC<{ frame: number }> = ({ frame }) => {
  const stars = Array.from({ length: 200 }, (_, i) => {
    const seed = i * 1618;
    const x = ((seed * 2654435761) >>> 0) % 1920;
    const y = ((seed * 1664525 + 1013904223) >>> 0) % 1080;
    const size = 0.5 + (i % 4) * 0.5;
    const twinkle = 0.3 + Math.sin(frame * 0.05 + i * 0.7) * 0.3;
    return { x, y, size, twinkle };
  });

  return (
    <svg style={{ position: "absolute", inset: 0, width: 1920, height: 1080 }}>
      {stars.map((s, i) => (
        <circle key={i} cx={s.x} cy={s.y} r={s.size} fill="white" opacity={s.twinkle} />
      ))}
    </svg>
  );
};

// Courbe de fréquence / signal pulsar
const PulsarSignal: React.FC<{ frame: number; y: number; color: string; freq: number; amp: number }> = ({
  frame, y, color, freq, amp,
}) => {
  const progress = interpolate(frame, [100, 600], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const points = Array.from({ length: 200 }, (_, i) => {
    const x = (i / 199) * 1920;
    const t = i / 199;
    if (t > progress) return null;
    const signal = Math.sin(t * freq * Math.PI * 2 + frame * 0.05) * amp * Math.exp(-((t - 0.5) ** 2) * 3);
    return `${x},${y + signal}`;
  }).filter(Boolean);

  return (
    <polyline
      points={points.join(" ")}
      fill="none"
      stroke={color}
      strokeWidth={1.5}
      opacity={0.6}
    />
  );
};

// Glyphes du père transformés en constellation
const GlyphConstellation: React.FC<{ frame: number }> = ({ frame }) => {
  const nodes = [
    { x: 800, y: 300 }, { x: 960, y: 220 }, { x: 1120, y: 300 },
    { x: 1060, y: 420 }, { x: 860, y: 420 }, { x: 960, y: 540 },
  ];
  const edges = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0], [1, 5], [3, 5]];

  const progress = interpolate(frame, [400, 900], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <svg style={{ position: "absolute", inset: 0, width: 1920, height: 1080 }}>
      {edges.map(([a, b], i) => {
        const op = interpolate(progress, [i / edges.length, (i + 1) / edges.length], [0, 1], {
          extrapolateLeft: "clamp", extrapolateRight: "clamp",
        });
        return (
          <line key={i}
            x1={nodes[a].x} y1={nodes[a].y}
            x2={nodes[b].x} y2={nodes[b].y}
            stroke={COLORS.solar} strokeWidth={1} opacity={op * 0.5}
          />
        );
      })}
      {nodes.map((n, i) => {
        const pulse = 3 + Math.sin(frame * 0.08 + i) * 1.5;
        const op = interpolate(frame, [400 + i * 40, 440 + i * 40], [0, 1], {
          extrapolateLeft: "clamp", extrapolateRight: "clamp",
        });
        return (
          <g key={i} opacity={op}>
            <circle cx={n.x} cy={n.y} r={pulse + 4} fill={COLORS.solar} opacity={0.1} />
            <circle cx={n.x} cy={n.y} r={pulse} fill={COLORS.solar} opacity={0.7} />
          </g>
        );
      })}
    </svg>
  );
};

export const Seq09_Cosmos: React.FC = () => {
  const frame = useCurrentFrame();

  const bgOpacity = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        background: "#020308",
        overflow: "hidden",
      }}
    >
      {/* Fond cosmique */}
      <div
        style={{
          position: "absolute", inset: 0,
          background: `radial-gradient(ellipse at 50% 50%, #0a0d18 0%, #020308 70%)`,
          opacity: bgOpacity,
        }}
      />

      <StarField frame={frame} />
      <Particles count={40} seed={99} />

      {/* Signaux pulsars */}
      <svg style={{ position: "absolute", inset: 0, width: 1920, height: 1080 }}>
        <PulsarSignal frame={frame} y={700} color={COLORS.cyan} freq={8} amp={40} />
        <PulsarSignal frame={frame} y={760} color={COLORS.amber} freq={12} amp={25} />
        <PulsarSignal frame={frame} y={820} color={COLORS.solar} freq={5} amp={50} />
      </svg>

      {/* Constellation de glyphes */}
      <GlyphConstellation frame={frame} />

      {/* Message flottant entre les étoiles */}
      <div
        style={{
          position: "absolute",
          top: 120, left: "50%",
          transform: `translateX(-50%) translateY(${Math.sin(frame * 0.02) * 8}px)`,
          opacity: interpolate(frame, [200, 280], [0, 0.4], { extrapolateRight: "clamp" }),
          fontFamily: FONTS.serif,
          fontSize: 36,
          color: COLORS.chalk,
          letterSpacing: 4,
          textAlign: "center",
        }}
      >
        "Ich wünsche dir einen sonnigen Morgen!"
      </div>

      {/* Overlays système */}
      <div
        style={{
          position: "absolute",
          top: 60, right: 80,
          display: "flex",
          flexDirection: "column",
          gap: 10,
          opacity: interpolate(frame, [40, 80], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        {OVERLAYS.map((ov, i) => {
          const op = interpolate(frame, [ov.frame, ov.frame + 20], [0, 0.7], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <div key={i} style={{ opacity: op, fontFamily: FONTS.mono, fontSize: 15, color: COLORS.cyan, letterSpacing: 2 }}>
              {ov.text}
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
          gap: 10,
          maxWidth: 1000,
        }}
      >
        {IA_LINES.map((line, i) => {
          const op = interpolate(frame, [line.frame, line.frame + 20], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <div key={i} style={{ opacity: op, fontFamily: FONTS.mono, fontSize: 22, color: COLORS.cyan }}>
              {line.text}
            </div>
          );
        })}
      </div>

      {/* [VOICE: IA centrale] "Les analyses terrestres sont insuffisantes…" */}

      <Subtitle
        text={"Le analisi terrestri sono insufficienti.\nMi rivolgo all'astrofisica.\nCerco una frequenza portante."}
        startFrame={280}
        endFrame={1200}
        size={24}
      />
    </AbsoluteFill>
  );
};
