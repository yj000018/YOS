import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Subtitle } from "../components/Subtitle";
import { COLORS, FONTS } from "../utils/theme";

export const DURATION_SEQ06 = 1050; // 35s

const ANGLES = [0, 90, 180, 270];
const ANGLE_LABELS = ["0°", "90°", "180°", "270°"];
const EXTRA_LABELS = ["mirror x", "mirror y", "semantic torque", "radial fold"];

const LETTERS = ["I", "c", "h", "w", "ü", "n", "s", "c", "h", "e"];

const IA_LINES = [
  { text: "Rotation spatiale en cours.", frame: 100 },
  { text: "Certaines formes latines présentent une compatibilité morphologique partielle.", frame: 200 },
  { text: "À 180 degrés, le texte cesse d'être allemand.", frame: 400 },
  { text: "À 270 degrés… il commence à rêver.", frame: 550 },
];

export const Seq06_Rotations: React.FC = () => {
  const frame = useCurrentFrame();

  // Cycle d'angles: chaque angle dure ~200 frames
  const cycleFrame = frame % 800;
  const angleIndex = Math.floor(cycleFrame / 200) % 4;
  const currentAngle = ANGLES[angleIndex];

  const angleProgress = (cycleFrame % 200) / 200;
  const displayAngle = interpolate(angleProgress, [0, 0.3], [0, currentAngle], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 50%, #0c1018 0%, ${COLORS.black} 75%)`,
        overflow: "hidden",
      }}
    >
      {/* Équation de rotation */}
      <div
        style={{
          position: "absolute", top: 60, left: "50%",
          transform: "translateX(-50%)",
          opacity: interpolate(frame, [30, 80], [0, 0.7], { extrapolateRight: "clamp" }),
          fontFamily: FONTS.serif,
          fontSize: 28,
          color: COLORS.chalk,
          letterSpacing: 2,
          textAlign: "center",
        }}
      >
        R(θ) = align(rotate(letter, θ), glyph_family)
        <br />
        <span style={{ color: COLORS.cyan, fontSize: 22 }}>
          θ ∈ {"{"} 0, 90, 180, 270 {"}"}
        </span>
      </div>

      {/* Lettres en rotation 3D */}
      <div
        style={{
          position: "absolute",
          top: "50%", left: "50%",
          transform: "translate(-50%, -50%)",
          display: "flex",
          gap: 24,
        }}
      >
        {LETTERS.map((letter, i) => {
          const delay = i * 15;
          const letterAngle = interpolate(
            frame,
            [delay, delay + 60],
            [0, currentAngle],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          );
          const floatY = Math.sin(frame * 0.04 + i * 0.8) * 12;
          const scale = 1 + Math.sin(frame * 0.03 + i * 0.5) * 0.05;

          return (
            <div
              key={i}
              style={{
                transform: `rotateZ(${letterAngle}deg) translateY(${floatY}px) scale(${scale})`,
                fontFamily: FONTS.serif,
                fontSize: 72,
                fontWeight: 700,
                color: i % 3 === 0 ? COLORS.solar : i % 3 === 1 ? COLORS.cyan : COLORS.chalk,
                textShadow: `0 0 30px currentColor`,
                opacity: interpolate(frame, [0, 40], [0, 1], { extrapolateRight: "clamp" }),
              }}
            >
              {letter}
            </div>
          );
        })}
      </div>

      {/* Indicateur d'angle actuel */}
      <div
        style={{
          position: "absolute",
          top: "50%", right: 120,
          transform: "translateY(-50%)",
          display: "flex",
          flexDirection: "column",
          gap: 16,
          opacity: interpolate(frame, [60, 100], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        {ANGLE_LABELS.map((label, i) => (
          <div
            key={i}
            style={{
              fontFamily: FONTS.mono,
              fontSize: 22,
              color: i === angleIndex ? COLORS.solar : COLORS.slate,
              letterSpacing: 3,
              transition: "color 0.3s",
              borderLeft: `3px solid ${i === angleIndex ? COLORS.solar : COLORS.slate}`,
              paddingLeft: 12,
            }}
          >
            {label}
          </div>
        ))}
        <div style={{ height: 20 }} />
        {EXTRA_LABELS.map((label, i) => (
          <div
            key={`e${i}`}
            style={{
              fontFamily: FONTS.mono,
              fontSize: 16,
              color: "rgba(72,202,228,0.4)",
              letterSpacing: 2,
              paddingLeft: 12,
            }}
          >
            {label}
          </div>
        ))}
      </div>

      {/* Angle actuel affiché */}
      <div
        style={{
          position: "absolute",
          bottom: 200,
          left: "50%",
          transform: "translateX(-50%)",
          fontFamily: FONTS.mono,
          fontSize: 80,
          color: COLORS.solar,
          opacity: 0.15,
          letterSpacing: 8,
        }}
      >
        {Math.round(displayAngle)}°
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
          maxWidth: 1000,
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
              }}
            >
              {line.text}
            </div>
          );
        })}
      </div>

      {/* [VOICE: IA centrale] "Rotation spatiale en cours…" */}

      <Subtitle
        text={"Rotazione spaziale in corso.\nA 180 gradi, il testo cessa di essere tedesco.\nA 270 gradi… comincia a sognare."}
        startFrame={400}
        endFrame={950}
        size={24}
      />
    </AbsoluteFill>
  );
};
