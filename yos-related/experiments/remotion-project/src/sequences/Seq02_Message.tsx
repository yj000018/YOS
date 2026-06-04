import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Subtitle } from "../components/Subtitle";
import { COLORS, FONTS } from "../utils/theme";

export const DURATION_SEQ02 = 750; // 25s

const MESSAGE = "Ich wünsche dir einen sonnigen Morgen!";
const WORDS = MESSAGE.split(" ");
const HIGHLIGHT = ["wünsche", "sonnigen", "Morgen!"];

export const Seq02_Message: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 40], [0, 1], { extrapolateRight: "clamp" });
  const titleScale = interpolate(frame, [0, 40], [0.85, 1], { extrapolateRight: "clamp" });
  const breathe = 1 + Math.sin(frame * 0.04) * 0.012;

  // Micro fissures lumineuses sur les mots surlignés
  const crackOpacity = interpolate(frame, [200, 260, 400, 460], [0, 0.6, 0.6, 0], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  // Zoom progressif sur le message
  const zoom = interpolate(frame, [0, 600], [1, 1.06], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 40%, ${COLORS.deepBlue} 0%, ${COLORS.black} 75%)`,
        overflow: "hidden",
      }}
    >
      {/* Grille de fond légère */}
      <svg style={{ position: "absolute", inset: 0, width: 1920, height: 1080, opacity: 0.04 }}>
        {Array.from({ length: 30 }, (_, i) => (
          <line key={`h${i}`} x1={0} y1={i * 36} x2={1920} y2={i * 36} stroke={COLORS.chalk} strokeWidth={0.5} />
        ))}
        {Array.from({ length: 54 }, (_, i) => (
          <line key={`v${i}`} x1={i * 36} y1={0} x2={i * 36} y2={1080} stroke={COLORS.chalk} strokeWidth={0.5} />
        ))}
      </svg>

      {/* Label analytique */}
      <div
        style={{
          position: "absolute", top: 80, left: "50%",
          transform: "translateX(-50%)",
          opacity: interpolate(frame, [60, 100], [0, 0.5], { extrapolateRight: "clamp" }),
          fontFamily: FONTS.mono,
          fontSize: 16,
          color: COLORS.cyan,
          letterSpacing: 4,
        }}
      >
        ANALYSE LEXICO-SYMBOLIQUE EN COURS ·· SURFACE GERMANIQUE DÉTECTÉE
      </div>

      {/* Message principal */}
      <div
        style={{
          position: "absolute",
          top: "50%", left: "50%",
          transform: `translate(-50%, -50%) scale(${titleScale * breathe * zoom})`,
          opacity: titleOpacity,
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: 18,
          maxWidth: 1500,
        }}
      >
        {WORDS.map((word, i) => {
          const isHL = HIGHLIGHT.some((h) => word.includes(h.replace("!", "")));
          const wordDelay = i * 8;
          const wordOpacity = interpolate(frame, [wordDelay, wordDelay + 20], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          const wordY = interpolate(frame, [wordDelay, wordDelay + 20], [20, 0], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });

          return (
            <span
              key={i}
              style={{
                opacity: wordOpacity,
                transform: `translateY(${wordY}px)`,
                display: "inline-block",
                fontFamily: FONTS.serif,
                fontSize: 76,
                fontWeight: 700,
                color: isHL ? COLORS.solar : COLORS.chalk,
                letterSpacing: isHL ? 3 : 1,
                textShadow: isHL
                  ? `0 0 40px ${COLORS.solar}66, 0 0 80px ${COLORS.amber}33`
                  : `0 0 20px rgba(232,228,216,0.15)`,
                position: "relative",
              }}
            >
              {word}
              {/* Fissure lumineuse sur les mots clés */}
              {isHL && (
                <span
                  style={{
                    position: "absolute",
                    bottom: -4, left: 0, right: 0,
                    height: 2,
                    background: `linear-gradient(90deg, transparent, ${COLORS.solar}, transparent)`,
                    opacity: crackOpacity,
                  }}
                />
              )}
            </span>
          );
        })}
      </div>

      {/* Annotations analytiques */}
      {[
        { word: "wünsche", label: "VERBE MODAL — DÉSIR", x: 580, y: 380 },
        { word: "sonnigen", label: "ADJ. SOLAIRE — LUMINOSITÉ", x: 1100, y: 620 },
        { word: "Morgen", label: "SUBSTANTIF — MATIN / DEMAIN", x: 1400, y: 380 },
      ].map((ann, i) => {
        const op = interpolate(frame, [300 + i * 40, 340 + i * 40], [0, 0.7], {
          extrapolateLeft: "clamp", extrapolateRight: "clamp",
        });
        return (
          <div
            key={i}
            style={{
              position: "absolute", left: ann.x, top: ann.y,
              opacity: op,
              fontFamily: FONTS.mono,
              fontSize: 14,
              color: COLORS.cyan,
              letterSpacing: 2,
              borderLeft: `2px solid ${COLORS.cyan}66`,
              paddingLeft: 10,
            }}
          >
            {ann.label}
          </div>
        );
      })}

      {/* Voix off placeholder */}
      {/* [VOICE: Narrateur — grave]
          "Le texte semblait limpide.
           Trop limpide.
           Une telle simplicité… était suspecte." */}

      <Subtitle
        text={"Il testo sembrava limpido.\nTroppo limpido.\nUna simile semplicità… era sospetta."}
        startFrame={350}
        endFrame={680}
        size={26}
      />
    </AbsoluteFill>
  );
};
