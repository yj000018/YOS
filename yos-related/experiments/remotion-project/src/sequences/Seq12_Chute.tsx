import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Subtitle } from "../components/Subtitle";
import { COLORS, FONTS } from "../utils/theme";

export const DURATION_SEQ12 = 1050; // 35s

export const Seq12_Chute: React.FC = () => {
  const frame = useCurrentFrame();

  // Tout disparaît d'abord (0-60)
  const clearOpacity = interpolate(frame, [0, 60], [1, 0], { extrapolateRight: "clamp" });

  // Fond blanc pur qui apparaît
  const bgWhite = interpolate(frame, [60, 150], [0, 1], { extrapolateRight: "clamp" });

  // "DÉCRYPTAGE FINAL :" apparaît
  const labelOpacity = interpolate(frame, [150, 220], [0, 1], { extrapolateRight: "clamp" });

  // "Bonjour" apparaît
  const bonjourOpacity = interpolate(frame, [260, 360], [0, 1], { extrapolateRight: "clamp" });
  const bonjourScale = interpolate(frame, [260, 360], [0.7, 1], { extrapolateRight: "clamp" });

  // Soleil ☀️ apparaît séparément
  const soleilOpacity = interpolate(frame, [400, 500], [0, 1], { extrapolateRight: "clamp" });
  const soleilScale = interpolate(frame, [400, 500], [0.3, 1], { extrapolateRight: "clamp" });
  const soleilRotate = interpolate(frame, [400, 900], [0, 360], { extrapolateRight: "clamp" });

  // "Avec soleil." apparaît après pause
  const avecSoleilOpacity = interpolate(frame, [600, 680], [0, 1], { extrapolateRight: "clamp" });

  // Sous-titre IT
  const subOpacity = interpolate(frame, [450, 520], [0, 1], { extrapolateRight: "clamp" });

  const isDark = bgWhite < 0.5;
  const textColor = isDark ? COLORS.chalk : COLORS.black;
  const bgColor = isDark
    ? `rgba(0,0,0,${1 - bgWhite * 2})`
    : `rgba(255,255,255,${(bgWhite - 0.5) * 2})`;

  return (
    <AbsoluteFill
      style={{
        background: COLORS.black,
        overflow: "hidden",
      }}
    >
      {/* Transition vers fond blanc */}
      <div
        style={{
          position: "absolute", inset: 0,
          background: `rgba(255,255,255,${bgWhite})`,
        }}
      />

      {/* Silence visuel — tout disparaît */}
      <div style={{ opacity: clearOpacity, position: "absolute", inset: 0 }} />

      {/* Label "DÉCRYPTAGE FINAL" */}
      <div
        style={{
          position: "absolute",
          top: "35%", left: "50%",
          transform: "translate(-50%, -50%)",
          opacity: labelOpacity,
          fontFamily: FONTS.mono,
          fontSize: 22,
          color: bgWhite > 0.5 ? "rgba(0,0,0,0.4)" : COLORS.slate,
          letterSpacing: 6,
        }}
      >
        DÉCRYPTAGE FINAL :
      </div>

      {/* "Bonjour" */}
      <div
        style={{
          position: "absolute",
          top: "50%", left: "50%",
          transform: `translate(-50%, -50%) scale(${bonjourScale})`,
          opacity: bonjourOpacity,
          fontFamily: FONTS.serif,
          fontSize: 160,
          fontWeight: 700,
          color: bgWhite > 0.5 ? "#111111" : COLORS.chalk,
          letterSpacing: -4,
        }}
      >
        Bonjour
      </div>

      {/* ☀️ */}
      <div
        style={{
          position: "absolute",
          top: "50%", left: "50%",
          transform: `translate(340px, -50%) scale(${soleilScale}) rotate(${soleilRotate}deg)`,
          opacity: soleilOpacity,
          fontSize: 120,
          lineHeight: 1,
        }}
      >
        ☀️
      </div>

      {/* "Avec soleil." */}
      <div
        style={{
          position: "absolute",
          top: "65%", left: "50%",
          transform: "translate(-50%, -50%)",
          opacity: avecSoleilOpacity,
          fontFamily: FONTS.mono,
          fontSize: 28,
          color: bgWhite > 0.5 ? "rgba(0,0,0,0.5)" : COLORS.slate,
          letterSpacing: 4,
          fontStyle: "italic",
        }}
      >
        Avec soleil.
      </div>

      {/* Sous-titre IT */}
      {subOpacity > 0 && (
        <div
          style={{
            position: "absolute",
            bottom: 60,
            left: "50%",
            transform: "translateX(-50%)",
            opacity: subOpacity,
            fontFamily: FONTS.serif,
            fontStyle: "italic",
            fontSize: 32,
            color: bgWhite > 0.5 ? "rgba(0,0,0,0.5)" : COLORS.chalk,
            letterSpacing: 1,
            textAlign: "center",
          }}
        >
          Buongiorno ☀️
        </div>
      )}

      {/* [VOICE: IA centrale — quasi sacrée]
          "Décryptage final : Bonjour."
          [pause]
          "Avec soleil." */}
    </AbsoluteFill>
  );
};
