import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { LogLine } from "../components/LogLine";
import { Subtitle } from "../components/Subtitle";
import { COLORS, FONTS } from "../utils/theme";

export const DURATION_SEQ05 = 1200; // 40s

const SOURCE = "Ich wünsche dir einen sonnigen Morgen";
const LETTERS = SOURCE.replace(/\s/g, "").split("");

// Pseudo-random seeded positions
function seededRand(seed: number): number {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

const LOGS = [
  { text: "RUNNING LETTER PERMUTATION ENGINE v7.3", frame: 20 },
  { text: "TOTAL POSSIBILITY SPACE: 10^47 COMBINATIONS", frame: 80 },
  { text: "WORD ORDER INSTABILITY DETECTED", frame: 140 },
  { text: "SEMANTIC DENSITY RISING ████████░░ 82%", frame: 200 },
  { text: "INTRA-WORD PERMUTATION: ACTIVE", frame: 280 },
  { text: "INTER-WORD PERMUTATION: ACTIVE", frame: 340 },
  { text: "SYLLABIC INVERSION: ACTIVE", frame: 400 },
  { text: "MAGNETIC FIELD ALIGNMENT: SEARCHING...", frame: 500 },
  { text: "RECOMPOSITION IMPOSSIBLE DETECTED", frame: 600 },
  { text: "NOYAU DU MESSAGE: NON RÉSOLU", frame: 700 },
];

const PERMUTED_WORDS = [
  "hcI", "ünschew", "rid", "nenie", "nigenons", "nMroge",
  "Ich", "wünsche", "dir", "einen", "sonnigen", "Morgen",
  "cIh", "schünwe", "ird", "neeni", "igensno", "nMorge",
];

export const Seq05_Permutations: React.FC = () => {
  const frame = useCurrentFrame();

  // Phase 1: explosion (0-200)
  // Phase 2: lévitation chaotique (200-800)
  // Phase 3: tentative de recomposition (800-1100)

  const phase = frame < 200 ? 1 : frame < 800 ? 2 : 3;

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 50%, #0a0e1a 0%, ${COLORS.black} 80%)`,
        overflow: "hidden",
      }}
    >
      {/* Lettres en lévitation */}
      {LETTERS.map((letter, i) => {
        const seed = i * 137.5;
        const baseX = 200 + (i % 12) * 130;
        const baseY = 300 + Math.floor(i / 12) * 120;

        // Position chaotique
        const chaosX = seededRand(seed) * 1600 + 160;
        const chaosY = seededRand(seed + 1) * 700 + 150;

        // Explosion depuis le centre
        const explodeX = interpolate(frame, [0, 120], [960, chaosX], {
          extrapolateLeft: "clamp", extrapolateRight: "clamp",
        });
        const explodeY = interpolate(frame, [0, 120], [540, chaosY], {
          extrapolateLeft: "clamp", extrapolateRight: "clamp",
        });

        // Flottement
        const floatX = explodeX + Math.sin(frame * 0.02 + seed) * 20;
        const floatY = explodeY + Math.cos(frame * 0.015 + seed * 0.7) * 15;

        // Recomposition
        const recompX = interpolate(frame, [800, 1000], [floatX, baseX], {
          extrapolateLeft: "clamp", extrapolateRight: "clamp",
        });
        const recompY = interpolate(frame, [800, 1000], [floatY, baseY], {
          extrapolateLeft: "clamp", extrapolateRight: "clamp",
        });

        const finalX = phase === 3 ? recompX : floatX;
        const finalY = phase === 3 ? recompY : floatY;

        const rotation = Math.sin(frame * 0.03 + seed) * 25;
        const opacity = interpolate(frame, [0, 30], [0, 0.85], { extrapolateRight: "clamp" });

        const isVowel = "aeiouäöüAEIOUÄÖÜ".includes(letter);

        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: finalX,
              top: finalY,
              transform: `rotate(${rotation}deg)`,
              opacity,
              fontFamily: FONTS.serif,
              fontSize: 42 + (i % 3) * 12,
              fontWeight: 700,
              color: isVowel ? COLORS.solar : COLORS.chalk,
              textShadow: isVowel
                ? `0 0 20px ${COLORS.solar}55`
                : `0 0 10px rgba(232,228,216,0.2)`,
            }}
          >
            {letter}
          </div>
        );
      })}

      {/* Mots permutés qui apparaissent */}
      {PERMUTED_WORDS.map((word, i) => {
        const startF = 300 + i * 40;
        const op = interpolate(frame, [startF, startF + 20, startF + 80, startF + 100], [0, 0.4, 0.4, 0], {
          extrapolateLeft: "clamp", extrapolateRight: "clamp",
        });
        const x = 100 + (i % 6) * 280;
        const y = 80 + Math.floor(i / 6) * 80;
        return (
          <div
            key={`w${i}`}
            style={{
              position: "absolute", left: x, top: y,
              opacity: op,
              fontFamily: FONTS.mono,
              fontSize: 20,
              color: COLORS.cyan,
              letterSpacing: 2,
            }}
          >
            {word}
          </div>
        );
      })}

      {/* Terminal logs */}
      <div
        style={{
          position: "absolute",
          bottom: 160,
          right: 80,
          width: 600,
          background: "rgba(0,0,0,0.7)",
          border: `1px solid ${COLORS.cyan}22`,
          padding: "16px 20px",
          display: "flex",
          flexDirection: "column",
          gap: 4,
        }}
      >
        {LOGS.map((log, i) => (
          <LogLine key={i} text={log.text} startFrame={log.frame} size={13} />
        ))}
      </div>

      {/* Voix IA */}
      <div
        style={{
          position: "absolute",
          top: 60, left: 80,
          opacity: interpolate(frame, [500, 540], [0, 1], { extrapolateRight: "clamp" }),
          fontFamily: FONTS.mono,
          fontSize: 22,
          color: COLORS.cyan,
          maxWidth: 900,
          lineHeight: 1.6,
        }}
      >
        {`J'active le moteur de permutation brute.\nToutes les lettres sont testées.\nAucune combinaison n'ouvre encore le noyau du message.`}
      </div>

      {/* [VOICE: IA centrale] "J'active le moteur de permutation brute…" */}

      <Subtitle
        text={"Attivo il motore di permutazione bruta.\nTutte le lettere vengono testate.\nNessuna combinazione apre ancora il nucleo del messaggio."}
        startFrame={500}
        endFrame={1100}
        size={24}
      />
    </AbsoluteFill>
  );
};
