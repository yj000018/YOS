import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Subtitle } from "../components/Subtitle";
import { COLORS, FONTS } from "../utils/theme";

export const DURATION_SEQ11 = 900; // 30s

const LAYERS = [
  { label: "Message allemand", color: COLORS.chalk, frame: 20 },
  { label: "Glyphes du père", color: COLORS.amber, frame: 60 },
  { label: "Équations", color: COLORS.cyan, frame: 100 },
  { label: "Code", color: COLORS.solar, frame: 140 },
  { label: "Graphes", color: COLORS.cyan, frame: 180 },
  { label: "Ciel profond", color: COLORS.chalk, frame: 220 },
  { label: "Annotations manuscrites", color: COLORS.amber, frame: 260 },
];

const FORMULA_PARTS = [
  { text: "Meaning = ", frame: 400, color: COLORS.chalk },
  { text: "(surface_german)", frame: 440, color: COLORS.solar },
  { text: " × ", frame: 480, color: COLORS.chalk },
  { text: "(glyphic_intent)", frame: 500, color: COLORS.amber },
  { text: " × ", frame: 540, color: COLORS.chalk },
  { text: "(quasar_pulse)", frame: 560, color: COLORS.cyan },
  { text: " × ", frame: 600, color: COLORS.chalk },
  { text: "(paternal_humor)", frame: 620, color: COLORS.solar },
];

const IA_LINES = [
  { text: "Après permutation alphabétique,", frame: 100 },
  { text: "rotation spatiale,", frame: 160 },
  { text: "comparaison glyphique,", frame: 210 },
  { text: "cryptanalyse historique,", frame: 260 },
  { text: "corrélation astrophysique", frame: 310 },
  { text: "et recalage émotionnel,", frame: 360 },
  { text: "le sens profond du message peut enfin être confirmé.", frame: 430 },
];

export const Seq11_Synthese: React.FC = () => {
  const frame = useCurrentFrame();

  // Réduction finale vers la formule
  const reductionProgress = interpolate(frame, [350, 700], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 50%, #0d1020 0%, ${COLORS.black} 70%)`,
        overflow: "hidden",
      }}
    >
      {/* Couches qui reviennent */}
      <div
        style={{
          position: "absolute",
          top: 60, right: 80,
          display: "flex",
          flexDirection: "column",
          gap: 12,
        }}
      >
        {LAYERS.map((layer, i) => {
          const op = interpolate(frame, [layer.frame, layer.frame + 20], [0, 0.6], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          }) * (1 - reductionProgress * 0.7);
          return (
            <div key={i} style={{ opacity: op, fontFamily: FONTS.mono, fontSize: 18, color: layer.color, letterSpacing: 2 }}>
              ▸ {layer.label}
            </div>
          );
        })}
      </div>

      {/* Équations flottantes */}
      {["E = mc²", "∇Ψ = 0", "∫f(x)dx", "M = G×S×Q×H"].map((eq, i) => {
        const positions = [
          { x: 100, y: 150 }, { x: 1600, y: 200 },
          { x: 200, y: 700 }, { x: 1500, y: 650 },
        ];
        const p = positions[i];
        const op = interpolate(frame, [i * 30, i * 30 + 40], [0, 0.2], { extrapolateRight: "clamp" })
          * (1 - reductionProgress * 0.8);
        return (
          <div key={i} style={{
            position: "absolute", left: p.x, top: p.y,
            opacity: op,
            fontFamily: FONTS.serif,
            fontSize: 36,
            color: COLORS.chalk,
            transform: `rotate(${[-5, 8, -3, 6][i]}deg)`,
          }}>
            {eq}
          </div>
        );
      })}

      {/* Dialogue IA */}
      <div
        style={{
          position: "absolute",
          top: "50%", left: 80,
          transform: "translateY(-50%)",
          display: "flex",
          flexDirection: "column",
          gap: 10,
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
              fontSize: i === 6 ? 26 : 22,
              color: i === 6 ? COLORS.solar : COLORS.cyan,
              letterSpacing: 0.5,
            }}>
              {line.text}
            </div>
          );
        })}
      </div>

      {/* Formule finale */}
      <div
        style={{
          position: "absolute",
          bottom: 180,
          left: "50%",
          transform: "translateX(-50%)",
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          opacity: interpolate(frame, [400, 460], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        {FORMULA_PARTS.map((part, i) => {
          const op = interpolate(frame, [part.frame, part.frame + 20], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <span key={i} style={{
              opacity: op,
              fontFamily: FONTS.mono,
              fontSize: 28,
              color: part.color,
              letterSpacing: 1,
            }}>
              {part.text}
            </span>
          );
        })}
      </div>

      {/* Légende formule */}
      <div
        style={{
          position: "absolute",
          bottom: 100,
          left: "50%",
          transform: "translateX(-50%)",
          display: "flex",
          gap: 40,
          opacity: interpolate(frame, [650, 700], [0, 0.6], { extrapolateRight: "clamp" }),
          fontFamily: FONTS.mono,
          fontSize: 16,
          color: COLORS.slate,
          letterSpacing: 1,
        }}
      >
        <span>G = german surface</span>
        <span>S = symbolic substrate</span>
        <span>Q = quasar pulse</span>
        <span>H = humor resonance</span>
      </div>

      {/* [VOICE: IA centrale] "Après permutation alphabétique…" */}

      <Subtitle
        text={"Dopo permutazione alfabetica, rotazione spaziale,\ncrittoanalisi storica, correlazione astrofisica\ne ricalibrazione emotiva,\nil senso profondo del messaggio può finalmente essere confermato."}
        startFrame={100}
        endFrame={830}
        size={23}
      />
    </AbsoluteFill>
  );
};
