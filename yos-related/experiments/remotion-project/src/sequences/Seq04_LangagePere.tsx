import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { Subtitle } from "../components/Subtitle";
import { COLORS, FONTS } from "../utils/theme";

export const DURATION_SEQ04 = 1200; // 40s

const GLYPH_FAMILIES = [
  { id: "A", label: "GLYPH FAMILY A — ARC + CORE DOT", x: 120, y: 160 },
  { id: "B", label: "GLYPH FAMILY B — OPEN SEMICIRCLE", x: 120, y: 220 },
  { id: "C", label: "GLYPH FAMILY C — AXIAL STEM", x: 120, y: 280 },
  { id: "D", label: "GLYPH FAMILY D — BIFID CONNECTOR", x: 120, y: 340 },
  { id: "E", label: "GLYPH FAMILY E — SHIELDED CAPSULE", x: 120, y: 400 },
  { id: "F", label: "GLYPH FAMILY F — TERMINAL MARKER", x: 120, y: 460 },
];

const IA_LINES = [
  { text: "Artefact secondaire reçu.", frame: 200 },
  { text: "Je détecte un système graphique personnel, cohérent, non trivial.", frame: 270 },
  { text: "Ceci n'est pas un gribouillage.", frame: 380 },
  { text: "Ceci ressemble à une écriture.", frame: 450 },
];

const ANNOTATIONS = [
  { label: "Glyphe orbital", x: 680, y: 200, angle: -12 },
  { label: "Noyau ponctuel", x: 820, y: 350, angle: 8 },
  { label: "Connecteur axial", x: 600, y: 500, angle: -5 },
  { label: "Capsule sémantique", x: 900, y: 600, angle: 10 },
  { label: "Marqueur terminal", x: 720, y: 720, angle: -8 },
  { label: "Symétrie locale détectée", x: 850, y: 180, angle: 5 },
];

export const Seq04_LangagePere: React.FC = () => {
  const frame = useCurrentFrame();

  // Entrée de l'image
  const imgOpacity = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: "clamp" });
  const imgScale = interpolate(frame, [0, 60], [0.9, 1], { extrapolateRight: "clamp" });

  // Zoom progressif sur la feuille
  const zoom = interpolate(frame, [100, 800], [1, 1.25], { extrapolateRight: "clamp" });
  const panX = interpolate(frame, [100, 800], [0, -40], { extrapolateRight: "clamp" });
  const panY = interpolate(frame, [100, 800], [0, 20], { extrapolateRight: "clamp" });

  // Halo de scan sur l'image
  const scanY = interpolate(frame, [80, 400], [0, 680], { extrapolateRight: "clamp" });
  const scanOpacity = interpolate(frame, [80, 120, 380, 420], [0, 0.8, 0.8, 0], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 40% 50%, #0d1220 0%, ${COLORS.black} 70%)`,
        overflow: "hidden",
      }}
    >
      {/* Label muséal */}
      <div
        style={{
          position: "absolute", top: 60, left: "50%",
          transform: "translateX(-50%)",
          opacity: interpolate(frame, [30, 70], [0, 0.6], { extrapolateRight: "clamp" }),
          fontFamily: FONTS.mono,
          fontSize: 15,
          color: COLORS.cyan,
          letterSpacing: 5,
        }}
      >
        ARTEFACT GRAPHIQUE · ANALYSE EN COURS · CLASSIFICATION ACTIVE
      </div>

      {/* Image de la feuille — centrage légèrement à gauche */}
      <div
        style={{
          position: "absolute",
          top: "50%", left: "42%",
          transform: `translate(-50%, -50%) scale(${imgScale * zoom}) translate(${panX}px, ${panY}px)`,
          opacity: imgOpacity,
          boxShadow: `0 0 60px rgba(72,202,228,0.15), 0 0 120px rgba(0,0,0,0.8)`,
          border: `1px solid rgba(232,228,216,0.12)`,
        }}
      >
        <Img
          src={staticFile("assets/father-language.png")}
          style={{ width: 480, height: "auto", display: "block" }}
        />

        {/* Ligne de scan sur l'image */}
        <div
          style={{
            position: "absolute",
            top: scanY,
            left: 0, right: 0,
            height: 3,
            background: `linear-gradient(90deg, transparent, ${COLORS.cyan}cc, transparent)`,
            opacity: scanOpacity,
            boxShadow: `0 0 12px ${COLORS.cyan}`,
          }}
        />

        {/* Cercles de détourage sur les glyphes */}
        {[
          { cx: 120, cy: 80, r: 28 },
          { cx: 240, cy: 80, r: 28 },
          { cx: 360, cy: 80, r: 28 },
          { cx: 120, cy: 200, r: 28 },
          { cx: 240, cy: 200, r: 28 },
          { cx: 360, cy: 200, r: 28 },
        ].map((circle, i) => {
          const op = interpolate(frame, [300 + i * 30, 340 + i * 30], [0, 0.7], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <svg
              key={i}
              style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", overflow: "visible" }}
            >
              <circle
                cx={circle.cx}
                cy={circle.cy}
                r={circle.r}
                fill="none"
                stroke={COLORS.cyan}
                strokeWidth={1.5}
                opacity={op}
                strokeDasharray="4 3"
              />
            </svg>
          );
        })}
      </div>

      {/* Panneau de classification — droite */}
      <div
        style={{
          position: "absolute",
          top: "50%", right: 80,
          transform: "translateY(-50%)",
          display: "flex",
          flexDirection: "column",
          gap: 14,
          opacity: interpolate(frame, [250, 320], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        {GLYPH_FAMILIES.map((gf, i) => {
          const op = interpolate(frame, [280 + i * 25, 320 + i * 25], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <div
              key={i}
              style={{
                opacity: op,
                fontFamily: FONTS.mono,
                fontSize: 16,
                color: i % 2 === 0 ? COLORS.cyan : COLORS.amber,
                letterSpacing: 1,
                borderLeft: `2px solid ${i % 2 === 0 ? COLORS.cyan : COLORS.amber}55`,
                paddingLeft: 12,
              }}
            >
              {gf.label}
            </div>
          );
        })}
      </div>

      {/* Dialogue IA */}
      <div
        style={{
          position: "absolute",
          bottom: 160,
          left: 80,
          display: "flex",
          flexDirection: "column",
          gap: 10,
          maxWidth: 900,
        }}
      >
        {IA_LINES.map((line, i) => {
          const op = interpolate(frame, [line.frame, line.frame + 20], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <div
              key={i}
              style={{
                opacity: op,
                fontFamily: FONTS.mono,
                fontSize: 22,
                color: COLORS.cyan,
                letterSpacing: 0.5,
              }}
            >
              {line.text}
            </div>
          );
        })}
      </div>

      {/* [VOICE: IA centrale] "Artefact secondaire reçu…" */}

      <Subtitle
        text={"Artefatto secondario ricevuto.\nRilevo un sistema grafico personale, coerente, non banale.\nQuesto non è uno scarabocchio.\nQuesto assomiglia a una scrittura."}
        startFrame={200}
        endFrame={1000}
        size={24}
      />
    </AbsoluteFill>
  );
};
