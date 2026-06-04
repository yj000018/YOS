import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Particles } from "../components/Particles";
import { Subtitle } from "../components/Subtitle";
import { COLORS, FONTS } from "../utils/theme";

// Duration: 750 frames = 25s @30fps
export const DURATION_SEQ01 = 750;

const lines = [
  { text: "TRANSMISSION REÇUE.", frame: 30 },
  { text: "ORIGINE : PATERNELLE.", frame: 75 },
  { text: "NATURE APPARENTE : BIENVEILLANTE.", frame: 120 },
  { text: "NIVEAU RÉEL DE COMPLEXITÉ : INCONNU.", frame: 175 },
];

export const Seq01_Prologue: React.FC = () => {
  const frame = useCurrentFrame();

  const bgOpacity = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: "clamp" });
  const sheetOpacity = interpolate(frame, [40, 120], [0, 0.08], { extrapolateRight: "clamp" });
  const pulseScale = 1 + Math.sin(frame * 0.05) * 0.04;

  return (
    <AbsoluteFill style={{ background: COLORS.black, overflow: "hidden" }}>
      {/* Background gradient */}
      <div
        style={{
          position: "absolute", inset: 0,
          background: `radial-gradient(ellipse at 50% 50%, ${COLORS.deepBlue} 0%, ${COLORS.black} 70%)`,
          opacity: bgOpacity,
        }}
      />

      {/* Particles */}
      <Particles count={80} seed={7} />

      {/* Pulsation centrale */}
      <div
        style={{
          position: "absolute",
          top: "50%", left: "50%",
          transform: `translate(-50%, -50%) scale(${pulseScale})`,
          width: 300, height: 300,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${COLORS.cyan}18 0%, transparent 70%)`,
          opacity: interpolate(frame, [0, 60], [0, 1], { extrapolateRight: "clamp" }),
        }}
      />

      {/* Feuille blanche semi-transparente */}
      <div
        style={{
          position: "absolute",
          top: "50%", left: "50%",
          transform: "translate(-50%, -50%) rotate(-2deg)",
          width: 520, height: 680,
          background: `rgba(245,240,232,${sheetOpacity})`,
          border: `1px solid rgba(232,228,216,0.06)`,
          boxShadow: "0 0 80px rgba(72,202,228,0.04)",
        }}
      />

      {/* Équations manuscrites flottantes */}
      {["E = mc²", "∇·B = 0", "Ψ(x,t)", "∫∞₀", "λ = h/p"].map((eq, i) => {
        const x = [120, 1600, 300, 1500, 900][i];
        const y = [200, 150, 700, 750, 120][i];
        const rot = [-8, 12, -5, 7, -3][i];
        const delay = [20, 40, 60, 80, 100][i];
        const op = interpolate(frame, [delay, delay + 30], [0, 0.18], { extrapolateRight: "clamp" });
        return (
          <div
            key={i}
            style={{
              position: "absolute", left: x, top: y,
              transform: `rotate(${rot}deg)`,
              fontFamily: FONTS.serif,
              fontSize: 32,
              color: COLORS.chalk,
              opacity: op,
              letterSpacing: 2,
            }}
          >
            {eq}
          </div>
        );
      })}

      {/* Textes de transmission */}
      <div
        style={{
          position: "absolute",
          top: "50%", left: "50%",
          transform: "translate(-50%, -50%)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 20,
        }}
      >
        {lines.map((line, i) => {
          const op = interpolate(frame, [line.frame, line.frame + 20], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <div
              key={i}
              style={{
                opacity: op,
                fontFamily: FONTS.mono,
                fontSize: i === 0 ? 38 : 26,
                letterSpacing: i === 0 ? 6 : 3,
                textAlign: "center",
                color: i === 0 ? COLORS.chalk : "rgba(232,228,216,0.55)",
              }}
            >
              {line.text}
            </div>
          );
        })}
      </div>

      {/* Sous-titres IT */}
      <Subtitle
        text={"Questa mattina è arrivato un messaggio.\nIn apparenza, una semplice frase tedesca.\nIn realtà… forse molto di più."}
        startFrame={300}
        endFrame={680}
        size={26}
      />

      {/* Voix off placeholder */}
      {/* [VOICE: Narrateur — grave, posé]
          "Ce matin, un message est arrivé.
           En apparence, une simple phrase allemande.
           En réalité… peut-être bien davantage." */}
    </AbsoluteFill>
  );
};
