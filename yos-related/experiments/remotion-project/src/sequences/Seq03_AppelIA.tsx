import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { LogLine } from "../components/LogLine";
import { ScanLine } from "../components/ScanLine";
import { Subtitle } from "../components/Subtitle";
import { COLORS, FONTS } from "../utils/theme";

export const DURATION_SEQ03 = 900; // 30s

const DIALOG_NARR = [
  { text: "NARRATEUR :", frame: 20, color: COLORS.chalk, size: 22 },
  { text: "« Ô intelligence artificielle, j'ai besoin de toi.", frame: 50, color: COLORS.ivory, size: 28 },
  { text: "Je viens de recevoir un message.", frame: 110, color: COLORS.ivory, size: 28 },
  { text: "Je soupçonne une structure cryptée,", frame: 170, color: COLORS.ivory, size: 28 },
  { text: "un encodage familial profond,", frame: 220, color: COLORS.ivory, size: 28 },
  { text: "ou pire… une couche symbolique cachée. »", frame: 270, color: COLORS.ivory, size: 28 },
];

const DIALOG_IA = [
  { text: "IA CENTRALE :", frame: 380, color: COLORS.cyan, size: 22 },
  { text: "Analyse engagée.", frame: 410, color: COLORS.cyan, size: 26 },
  { text: "Hypothèse 1 : salutation germanique ordinaire.", frame: 460, color: COLORS.cyan, size: 24 },
  { text: "Hypothèse 2 : leurre.", frame: 520, color: COLORS.amber, size: 24 },
  { text: "Hypothèse 3 : message hybride couplé", frame: 570, color: COLORS.solar, size: 24 },
  { text: "à un système graphique expérimental.", frame: 610, color: COLORS.solar, size: 24 },
];

const LOGS = [
  { text: "> INITIALIZING DEEP ANALYSIS MODULE v4.2.1", frame: 30 },
  { text: "> LOADING LINGUISTIC CORPUS [DE/FR/IT/SYMBOLIC]", frame: 80 },
  { text: "> CROSS-REFERENCING PATERNAL SIGNAL PATTERNS", frame: 140 },
  { text: "> HYPOTHESIS ENGINE ONLINE", frame: 200 },
  { text: "> STRUCTURE PROFONDE NON RÉSOLUE", frame: 640 },
  { text: "> ESCALATING TO TIER-2 ANALYSIS", frame: 700 },
];

export const Seq03_AppelIA: React.FC = () => {
  const frame = useCurrentFrame();

  const bgOpacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        background: COLORS.black,
        overflow: "hidden",
      }}
    >
      {/* Fond laboratoire */}
      <div
        style={{
          position: "absolute", inset: 0,
          background: `linear-gradient(180deg, ${COLORS.black} 0%, #0a0f1e 60%, ${COLORS.black} 100%)`,
          opacity: bgOpacity,
        }}
      />

      {/* Scan line IA */}
      <ScanLine />

      {/* Fenêtres flottantes de terminal */}
      <div
        style={{
          position: "absolute", top: 60, right: 80,
          width: 480,
          background: "rgba(8,13,26,0.9)",
          border: `1px solid ${COLORS.cyan}33`,
          padding: "16px 20px",
          fontFamily: FONTS.mono,
          fontSize: 14,
          color: COLORS.cyan,
          opacity: interpolate(frame, [20, 60], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        <div style={{ color: COLORS.slate, marginBottom: 8, fontSize: 12 }}>
          ── TERMINAL ANALYTIQUE ──────────────────
        </div>
        {LOGS.map((log, i) => (
          <LogLine key={i} text={log.text} startFrame={log.frame} size={13} color={COLORS.cyan} />
        ))}
      </div>

      {/* Annotations manuscrites au feutre blanc */}
      {["?", "⟶", "∅", "≠"].map((sym, i) => {
        const positions = [
          { x: 80, y: 200, rot: -5 },
          { x: 200, y: 450, rot: 0 },
          { x: 1700, y: 300, rot: 8 },
          { x: 1750, y: 600, rot: -3 },
        ];
        const p = positions[i];
        const op = interpolate(frame, [100 + i * 60, 140 + i * 60], [0, 0.25], { extrapolateRight: "clamp" });
        return (
          <div
            key={i}
            style={{
              position: "absolute", left: p.x, top: p.y,
              transform: `rotate(${p.rot}deg)`,
              fontFamily: FONTS.serif,
              fontSize: 64,
              color: COLORS.chalk,
              opacity: op,
            }}
          >
            {sym}
          </div>
        );
      })}

      {/* Dialogue principal */}
      <div
        style={{
          position: "absolute",
          top: "50%", left: 120,
          transform: "translateY(-50%)",
          display: "flex",
          flexDirection: "column",
          gap: 12,
          maxWidth: 1100,
        }}
      >
        {[...DIALOG_NARR, ...DIALOG_IA].map((line, i) => {
          const op = interpolate(frame, [line.frame, line.frame + 15], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <div
              key={i}
              style={{
                opacity: op,
                fontFamily: line.color === COLORS.chalk || line.color === COLORS.ivory ? FONTS.serif : FONTS.mono,
                fontSize: line.size,
                color: line.color,
                letterSpacing: 0.5,
                lineHeight: 1.4,
              }}
            >
              {line.text}
            </div>
          );
        })}
      </div>

      {/* Curseur clignotant */}
      <div
        style={{
          position: "absolute", bottom: 120, left: 120,
          fontFamily: FONTS.mono,
          fontSize: 28,
          color: COLORS.cyan,
          opacity: Math.sin(frame * 0.3) > 0 ? 1 : 0,
        }}
      >
        █
      </div>

      {/* [VOICE: Narrateur] "Ô intelligence artificielle…" */}
      {/* [VOICE: IA centrale — calme, analytique] "Analyse engagée…" */}

      <Subtitle
        text={"Analisi avviata.\nIpotesi 1: saluto germanico ordinario.\nIpotesi 3: messaggio ibrido con sistema grafico sperimentale."}
        startFrame={410}
        endFrame={820}
        size={24}
      />
    </AbsoluteFill>
  );
};
