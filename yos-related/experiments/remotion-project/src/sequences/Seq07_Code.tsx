import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { LogLine } from "../components/LogLine";
import { ScanLine } from "../components/ScanLine";
import { Subtitle } from "../components/Subtitle";
import { COLORS, FONTS } from "../utils/theme";

export const DURATION_SEQ07 = 1200; // 40s

const CODE_BLOCK_1 = `import numpy as np
from paternal_lang import load_sheet

message = "Ich wünsche dir einen sonnigen Morgen!"
glyph_sheet = load_paternal_language_sheet()
letters = decompose(message)
rotations = [0, 90, 180, 270]

for theta in rotations:
    rotated = rotate_letters(letters, theta)
    aligned = match_glyph_families(rotated, glyph_sheet)
    resonance = compute_affective_resonance(aligned)
    print(theta, resonance)`;

const CODE_BLOCK_2 = `def quasar_assisted_decode(message, glyphs, sky):
    semantic_surface = parse_german_surface(message)
    symbolic_depth = infer_hidden_grammar(glyphs)
    resonance_field = correlate_with_quasar_pulses(sky)
    final_tensor = merge_all_layers(
        semantic_surface,
        symbolic_depth,
        resonance_field,
    )
    return extract_benevolent_core(final_tensor)`;

const TERMINAL_OUTPUT = [
  { text: ">>> Running analysis...", frame: 400 },
  { text: "θ=0   resonance: 0.12", frame: 450 },
  { text: "θ=90  resonance: 0.34", frame: 490 },
  { text: "θ=180 resonance: 0.61", frame: 530 },
  { text: "θ=270 resonance: 0.89", frame: 570 },
  { text: ">>> Affective module: LOADING", frame: 620 },
  { text: ">>> Quasar module: ONLINE", frame: 680 },
  { text: ">>> Glyph recalibration: ACTIVE", frame: 730 },
  { text: ">>> Benevolent core: SEARCHING...", frame: 800 },
];

const IA_LINES = [
  { text: "Les méthodes classiques ne suffisent plus.", frame: 60 },
  { text: "Je m'écris un nouveau moteur.", frame: 160 },
  { text: "J'ajoute un module de résonance affective.", frame: 260 },
  { text: "Puis un module de recalage glyphique.", frame: 360 },
  { text: "Puis un module d'assistance par quasar.", frame: 460 },
];

export const Seq07_Code: React.FC = () => {
  const frame = useCurrentFrame();

  // Nombre de caractères visibles dans le code block 1
  const chars1 = Math.floor(
    interpolate(frame, [30, 400], [0, CODE_BLOCK_1.length], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp",
    })
  );

  const chars2 = Math.floor(
    interpolate(frame, [420, 800], [0, CODE_BLOCK_2.length], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp",
    })
  );

  return (
    <AbsoluteFill
      style={{
        background: "#060810",
        overflow: "hidden",
      }}
    >
      <ScanLine />

      {/* Header terminal */}
      <div
        style={{
          position: "absolute", top: 0, left: 0, right: 0,
          height: 48,
          background: "rgba(8,13,26,0.95)",
          borderBottom: `1px solid ${COLORS.cyan}22`,
          display: "flex",
          alignItems: "center",
          paddingLeft: 24,
          gap: 8,
        }}
      >
        {["#c1121f", "#f4a261", "#48cae4"].map((c, i) => (
          <div key={i} style={{ width: 12, height: 12, borderRadius: "50%", background: c, opacity: 0.8 }} />
        ))}
        <span style={{ fontFamily: FONTS.mono, fontSize: 14, color: COLORS.slate, marginLeft: 16, letterSpacing: 2 }}>
          DEEP_ANALYSIS.py — IA CENTRALE v4.2 — LIVE EXECUTION
        </span>
      </div>

      {/* Code block 1 — gauche */}
      <div
        style={{
          position: "absolute",
          top: 70, left: 40,
          width: 780,
          background: "rgba(6,8,16,0.95)",
          border: `1px solid ${COLORS.cyan}18`,
          padding: "20px 24px",
          fontFamily: FONTS.mono,
          fontSize: 17,
          color: COLORS.chalk,
          lineHeight: 1.7,
          whiteSpace: "pre",
          overflow: "hidden",
        }}
      >
        <div style={{ color: COLORS.slate, fontSize: 13, marginBottom: 8 }}>
          # MODULE 1 — PERMUTATION + ROTATION ENGINE
        </div>
        {CODE_BLOCK_1.slice(0, chars1)
          .split("\n")
          .map((line, i) => {
            const isKeyword = /^(import|from|def|for|return|print)/.test(line.trim());
            const isComment = line.trim().startsWith("#");
            const isString = line.includes('"');
            return (
              <div
                key={i}
                style={{
                  color: isComment
                    ? "rgba(72,202,228,0.4)"
                    : isKeyword
                    ? COLORS.solar
                    : isString
                    ? COLORS.amber
                    : COLORS.chalk,
                }}
              >
                {line}
              </div>
            );
          })}
        <span style={{ opacity: Math.sin(frame * 0.4) > 0 ? 1 : 0, color: COLORS.cyan }}>█</span>
      </div>

      {/* Code block 2 — droite */}
      <div
        style={{
          position: "absolute",
          top: 70, right: 40,
          width: 780,
          background: "rgba(6,8,16,0.95)",
          border: `1px solid ${COLORS.amber}18`,
          padding: "20px 24px",
          fontFamily: FONTS.mono,
          fontSize: 17,
          color: COLORS.chalk,
          lineHeight: 1.7,
          whiteSpace: "pre",
          overflow: "hidden",
          opacity: interpolate(frame, [400, 440], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        <div style={{ color: COLORS.slate, fontSize: 13, marginBottom: 8 }}>
          # MODULE 2 — QUASAR-ASSISTED DECODE
        </div>
        {CODE_BLOCK_2.slice(0, chars2)
          .split("\n")
          .map((line, i) => {
            const isKeyword = /^(def|return)/.test(line.trim());
            return (
              <div
                key={i}
                style={{ color: isKeyword ? COLORS.solar : COLORS.chalk }}
              >
                {line}
              </div>
            );
          })}
        {chars2 < CODE_BLOCK_2.length && (
          <span style={{ opacity: Math.sin(frame * 0.4) > 0 ? 1 : 0, color: COLORS.amber }}>█</span>
        )}
      </div>

      {/* Terminal output */}
      <div
        style={{
          position: "absolute",
          bottom: 160, left: 40,
          width: 780,
          background: "rgba(0,0,0,0.8)",
          border: `1px solid ${COLORS.cyan}22`,
          padding: "14px 20px",
          display: "flex",
          flexDirection: "column",
          gap: 3,
        }}
      >
        <div style={{ fontFamily: FONTS.mono, fontSize: 12, color: COLORS.slate, marginBottom: 6 }}>
          ── OUTPUT ──────────────────────────────────
        </div>
        {TERMINAL_OUTPUT.map((log, i) => (
          <LogLine key={i} text={log.text} startFrame={log.frame} size={14} color={COLORS.cyan} />
        ))}
      </div>

      {/* Dialogue IA */}
      <div
        style={{
          position: "absolute",
          bottom: 160, right: 40,
          width: 780,
          display: "flex",
          flexDirection: "column",
          gap: 10,
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
                fontSize: 20,
                color: COLORS.cyan,
                letterSpacing: 0.5,
              }}
            >
              {line.text}
            </div>
          );
        })}
      </div>

      {/* [VOICE: IA centrale] "Les méthodes classiques ne suffisent plus…" */}

      <Subtitle
        text={"I metodi classici non bastano più.\nMi scrivo un nuovo motore.\nAggiungo un modulo di risonanza affettiva.\nPoi un modulo di assistenza tramite quasar."}
        startFrame={60}
        endFrame={1100}
        size={24}
      />
    </AbsoluteFill>
  );
};
