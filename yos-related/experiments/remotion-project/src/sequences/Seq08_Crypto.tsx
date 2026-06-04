import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Subtitle } from "../components/Subtitle";
import { COLORS, FONTS } from "../utils/theme";

export const DURATION_SEQ08 = 1200; // 40s

const SCORES = [
  { label: "Threat Index", value: "0.0003", color: COLORS.cyan },
  { label: "Poetic Density", value: "0.981", color: COLORS.solar },
  { label: "Affective Load", value: "0.972", color: COLORS.amber },
  { label: "Paternal Signature", value: "0.998", color: COLORS.chalk },
];

const CATEGORIES = [
  { label: "CRYPTOGRAPHIE MILITAIRE", frame: 60 },
  { label: "LANGAGES INVENTÉS", frame: 130 },
  { label: "ABSTRACTION GRAPHIQUE", frame: 200 },
  { label: "HISTOIRE DE L'ART", frame: 270 },
  { label: "NOTATIONS PRIVÉES", frame: 340 },
];

const IA_LINES = [
  { text: "J'ouvre maintenant les couches de comparaison historique.", frame: 60 },
  { text: "Aucun recouvrement strict.", frame: 500 },
  { text: "Mais une certitude émerge :", frame: 600 },
  { text: "ce système n'est pas défensif.", frame: 680 },
  { text: "Il est expressif.", frame: 760 },
];

// Roue cryptographique SVG
const CipherWheel: React.FC<{ frame: number; cx: number; cy: number; r: number; speed: number }> = ({
  frame, cx, cy, r, speed,
}) => {
  const rot = frame * speed;
  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  return (
    <g transform={`translate(${cx}, ${cy})`}>
      <circle r={r} fill="none" stroke={COLORS.cyan} strokeWidth={1} opacity={0.3} />
      <circle r={r * 0.65} fill="none" stroke={COLORS.amber} strokeWidth={1} opacity={0.25} />
      {letters.split("").map((l, i) => {
        const angle = (i / 26) * Math.PI * 2 + (rot * Math.PI) / 180;
        const x = Math.cos(angle) * r * 0.88;
        const y = Math.sin(angle) * r * 0.88;
        return (
          <text key={i} x={x} y={y} fill={COLORS.chalk} fontSize={14} textAnchor="middle" dominantBaseline="middle" opacity={0.4} fontFamily={FONTS.mono}>
            {l}
          </text>
        );
      })}
      {letters.split("").map((l, i) => {
        const angle = (i / 26) * Math.PI * 2 - (rot * Math.PI) / 180;
        const x = Math.cos(angle) * r * 0.58;
        const y = Math.sin(angle) * r * 0.58;
        return (
          <text key={`i${i}`} x={x} y={y} fill={COLORS.amber} fontSize={11} textAnchor="middle" dominantBaseline="middle" opacity={0.35} fontFamily={FONTS.mono}>
            {l}
          </text>
        );
      })}
    </g>
  );
};

// Graphique radar SVG
const RadarChart: React.FC<{ frame: number; cx: number; cy: number; r: number }> = ({ frame, cx, cy, r }) => {
  const axes = 6;
  const values = [0.92, 0.78, 0.65, 0.88, 0.71, 0.95];
  const progress = interpolate(frame, [300, 700], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const points = values.map((v, i) => {
    const angle = (i / axes) * Math.PI * 2 - Math.PI / 2;
    const rv = v * r * progress;
    return [cx + Math.cos(angle) * rv, cy + Math.sin(angle) * rv];
  });

  const polyPoints = points.map((p) => p.join(",")).join(" ");

  return (
    <g>
      {Array.from({ length: axes }, (_, i) => {
        const angle = (i / axes) * Math.PI * 2 - Math.PI / 2;
        return (
          <line key={i} x1={cx} y1={cy} x2={cx + Math.cos(angle) * r} y2={cy + Math.sin(angle) * r}
            stroke={COLORS.slate} strokeWidth={1} opacity={0.4} />
        );
      })}
      {[0.33, 0.66, 1].map((scale, i) => {
        const pts = Array.from({ length: axes }, (_, j) => {
          const angle = (j / axes) * Math.PI * 2 - Math.PI / 2;
          return `${cx + Math.cos(angle) * r * scale},${cy + Math.sin(angle) * r * scale}`;
        }).join(" ");
        return <polygon key={i} points={pts} fill="none" stroke={COLORS.slate} strokeWidth={0.5} opacity={0.3} />;
      })}
      <polygon points={polyPoints} fill={`${COLORS.cyan}22`} stroke={COLORS.cyan} strokeWidth={1.5} opacity={0.8} />
    </g>
  );
};

export const Seq08_Crypto: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(135deg, #080c14 0%, #0a0f1a 50%, #060810 100%)`,
        overflow: "hidden",
      }}
    >
      {/* Roues cryptographiques */}
      <svg style={{ position: "absolute", inset: 0, width: 1920, height: 1080 }}>
        <CipherWheel frame={frame} cx={300} cy={300} r={220} speed={0.3} />
        <CipherWheel frame={frame} cx={1650} cy={280} r={180} speed={-0.2} />
        <CipherWheel frame={frame} cx={1700} cy={750} r={140} speed={0.4} />
        <RadarChart frame={frame} cx={960} cy={300} r={180} />
      </svg>

      {/* Catégories analysées */}
      <div
        style={{
          position: "absolute",
          top: "50%", left: 80,
          transform: "translateY(-50%)",
          display: "flex",
          flexDirection: "column",
          gap: 18,
        }}
      >
        {CATEGORIES.map((cat, i) => {
          const op = interpolate(frame, [cat.frame, cat.frame + 25], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          const barW = interpolate(frame, [cat.frame + 30, cat.frame + 120], [0, 200 + i * 40], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <div key={i} style={{ opacity: op }}>
              <div style={{ fontFamily: FONTS.mono, fontSize: 18, color: COLORS.chalk, letterSpacing: 2, marginBottom: 6 }}>
                {cat.label}
              </div>
              <div style={{ width: 400, height: 2, background: COLORS.slate }}>
                <div style={{ width: barW, height: "100%", background: COLORS.cyan }} />
              </div>
            </div>
          );
        })}
      </div>

      {/* Scores */}
      <div
        style={{
          position: "absolute",
          bottom: 200, right: 80,
          display: "flex",
          flexDirection: "column",
          gap: 12,
          opacity: interpolate(frame, [600, 660], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        {SCORES.map((score, i) => {
          const op = interpolate(frame, [620 + i * 30, 660 + i * 30], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <div key={i} style={{ opacity: op, fontFamily: FONTS.mono, fontSize: 22, color: score.color, letterSpacing: 2 }}>
              {score.label.padEnd(22, ".")} {score.value}
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

      {/* [VOICE: IA centrale] "J'ouvre maintenant les couches de comparaison historique…" */}

      <Subtitle
        text={"Nessuna sovrapposizione rigorosa.\nMa emerge una certezza:\nquesto sistema non è difensivo.\nÈ espressivo."}
        startFrame={600}
        endFrame={1100}
        size={24}
      />
    </AbsoluteFill>
  );
};
