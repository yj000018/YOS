import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Subtitle } from "../components/Subtitle";
import { COLORS, FONTS } from "../utils/theme";

export const DURATION_SEQ13 = 1350; // 45s — inclut pause de 3s au début

// Pause initiale: 90 frames (3s) de silence après la chute
const PAUSE = 90;

const TIMELINE = [
  {
    time: "08:45",
    items: ["réveil", "message reçu", "idée initiale"],
    frame: PAUSE + 60,
  },
  {
    time: "08:49",
    items: ["concept du gag", "fausse enquête cryptographique", "fréquence de quasar", "chute : Bonjour ☀️"],
    frame: PAUSE + 180,
  },
  {
    time: "08:56",
    items: ["scénario", "découpage narratif", "dialogues", "voix off"],
    frame: PAUSE + 320,
  },
  {
    time: "09:03",
    items: ["tableau blanc d'Einstein", "IA futuriste", "cosmologie", "équations manuscrites"],
    frame: PAUSE + 460,
  },
  {
    time: "09:08",
    items: ["sous-titres italiens", "pseudo-code", "graphiques", "glyphes", "animations"],
    frame: PAUSE + 600,
  },
  {
    time: "09:14",
    items: ["brief de réalisation", "pipeline IA", "Remotion", "production"],
    frame: PAUSE + 720,
  },
];

const FINAL_CARDS = [
  { label: "Idée humaine", value: "~ 30 min", frame: PAUSE + 900, color: COLORS.solar },
  { label: "Temps machine", value: "calcul + génération + rendu", frame: PAUSE + 980, color: COLORS.cyan },
  { label: "Résultat", value: "Bonjour ☀️", frame: PAUSE + 1060, color: COLORS.chalk },
];

export const Seq13_Epilogue: React.FC = () => {
  const frame = useCurrentFrame();

  // Silence initial (0-90): fond noir, rien
  const silenceOpacity = interpolate(frame, [0, PAUSE - 10, PAUSE], [0, 0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  // Musique revient doucement (représentée visuellement par une ligne)
  const musicLineW = interpolate(frame, [PAUSE, PAUSE + 120], [0, 1920], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  // Tableau blanc en fond
  const boardOpacity = interpolate(frame, [PAUSE + 20, PAUSE + 80], [0, 0.06], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: COLORS.black,
        overflow: "hidden",
      }}
    >
      {/* Silence initial — fond noir pur */}
      <div style={{ position: "absolute", inset: 0, background: COLORS.black, opacity: 1 - silenceOpacity }} />

      {/* Fond tableau blanc très subtil */}
      <div
        style={{
          position: "absolute", inset: 0,
          background: `radial-gradient(ellipse at 50% 40%, #1a1c22 0%, ${COLORS.black} 70%)`,
          opacity: boardOpacity * 10,
        }}
      />

      {/* Grille de tableau blanc */}
      <svg style={{ position: "absolute", inset: 0, width: 1920, height: 1080, opacity: boardOpacity }}>
        {Array.from({ length: 24 }, (_, i) => (
          <line key={`h${i}`} x1={0} y1={i * 45} x2={1920} y2={i * 45} stroke={COLORS.chalk} strokeWidth={0.3} />
        ))}
        {Array.from({ length: 43 }, (_, i) => (
          <line key={`v${i}`} x1={i * 45} y1={0} x2={i * 45} y2={1080} stroke={COLORS.chalk} strokeWidth={0.3} />
        ))}
      </svg>

      {/* Ligne musicale — reprise douce */}
      <div
        style={{
          position: "absolute", top: 0, left: 0,
          width: musicLineW, height: 2,
          background: `linear-gradient(90deg, transparent, ${COLORS.solar}44, ${COLORS.solar}88)`,
          opacity: silenceOpacity,
        }}
      />

      {/* Label épilogue */}
      <div
        style={{
          position: "absolute",
          top: 50, left: "50%",
          transform: "translateX(-50%)",
          opacity: interpolate(frame, [PAUSE + 30, PAUSE + 70], [0, 0.5], { extrapolateRight: "clamp" }),
          fontFamily: FONTS.mono,
          fontSize: 16,
          color: COLORS.slate,
          letterSpacing: 6,
        }}
      >
        ÉPILOGUE · MAKING OF · 30 MINUTES
      </div>

      {/* Timeline horizontale */}
      <div
        style={{
          position: "absolute",
          top: 120,
          left: 80, right: 80,
          opacity: silenceOpacity,
        }}
      >
        {/* Ligne de temps */}
        <div
          style={{
            position: "absolute",
            top: 28,
            left: 0, right: 0,
            height: 1,
            background: `rgba(232,228,216,0.15)`,
          }}
        />

        {/* Blocs de temps */}
        <div style={{ display: "flex", justifyContent: "space-between", position: "relative" }}>
          {TIMELINE.map((block, i) => {
            const blockOp = interpolate(frame, [block.frame, block.frame + 30], [0, 1], {
              extrapolateLeft: "clamp", extrapolateRight: "clamp",
            });
            return (
              <div
                key={i}
                style={{
                  opacity: blockOp,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  width: 240,
                }}
              >
                {/* Point sur la timeline */}
                <div
                  style={{
                    width: 10, height: 10,
                    borderRadius: "50%",
                    background: COLORS.solar,
                    marginBottom: 12,
                    boxShadow: `0 0 12px ${COLORS.solar}88`,
                  }}
                />

                {/* Heure */}
                <div
                  style={{
                    fontFamily: FONTS.mono,
                    fontSize: 22,
                    color: COLORS.solar,
                    letterSpacing: 2,
                    marginBottom: 10,
                  }}
                >
                  {block.time}
                </div>

                {/* Items */}
                {block.items.map((item, j) => {
                  const itemOp = interpolate(
                    frame,
                    [block.frame + j * 15, block.frame + j * 15 + 20],
                    [0, 0.7],
                    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
                  );
                  return (
                    <div
                      key={j}
                      style={{
                        opacity: itemOp,
                        fontFamily: FONTS.mono,
                        fontSize: 13,
                        color: COLORS.chalk,
                        letterSpacing: 1,
                        textAlign: "center",
                        lineHeight: 1.8,
                      }}
                    >
                      {item}
                    </div>
                  );
                })}
              </div>
            );
          })}
        </div>
      </div>

      {/* Rappels visuels du film */}
      {["Ich wünsche…", "R(θ)=align(…)", "QUASAR PULSE", "M=G×S×Q×H"].map((el, i) => {
        const positions = [
          { x: 100, y: 500 }, { x: 500, y: 600 },
          { x: 1200, y: 520 }, { x: 1600, y: 580 },
        ];
        const p = positions[i];
        const op = interpolate(frame, [PAUSE + 200 + i * 60, PAUSE + 240 + i * 60], [0, 0.2], {
          extrapolateLeft: "clamp", extrapolateRight: "clamp",
        });
        return (
          <div key={i} style={{
            position: "absolute", left: p.x, top: p.y,
            opacity: op,
            fontFamily: FONTS.mono,
            fontSize: 18,
            color: COLORS.cyan,
            letterSpacing: 2,
            transform: `rotate(${[-3, 5, -2, 4][i]}deg)`,
          }}>
            {el}
          </div>
        );
      })}

      {/* Cartes finales */}
      <div
        style={{
          position: "absolute",
          bottom: 160,
          left: "50%",
          transform: "translateX(-50%)",
          display: "flex",
          gap: 60,
        }}
      >
        {FINAL_CARDS.map((card, i) => {
          const op = interpolate(frame, [card.frame, card.frame + 30], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <div
              key={i}
              style={{
                opacity: op,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 8,
                padding: "16px 28px",
                border: `1px solid ${card.color}33`,
                background: `rgba(0,0,0,0.5)`,
              }}
            >
              <div style={{ fontFamily: FONTS.mono, fontSize: 14, color: COLORS.slate, letterSpacing: 3 }}>
                {card.label}
              </div>
              <div style={{ fontFamily: FONTS.serif, fontSize: 24, color: card.color, letterSpacing: 1 }}>
                {card.value}
              </div>
            </div>
          );
        })}
      </div>

      {/* [VOICE: Narrateur — posé, légèrement ému]
          "Tout cela a commencé ce matin, vers 8h45, au réveil.
           Un message arrive. Une idée surgit.
           En une trentaine de minutes, avec les IA,
           se sont construits : le concept, le gag, le scénario…
           Ensuite, les machines calculent. Elles fabriquent.
           Et un simple message du matin devient un petit spectacle cosmique." */}

      <Subtitle
        text={"Tutto questo è cominciato stamattina, verso le 8:45, al risveglio.\nIn una trentina di minuti, con le IA, si sono costruiti:\nil concetto, la gag, la sceneggiatura, i dialoghi, le voci,\ni sottotitoli, le equazioni, le animazioni, la direzione visiva.\nPoi le macchine calcolano. Fabbricano. Renderizzano.\nE un semplice messaggio del mattino diventa un piccolo spettacolo cosmico."}
        startFrame={PAUSE + 60}
        endFrame={1300}
        size={22}
      />
    </AbsoluteFill>
  );
};
