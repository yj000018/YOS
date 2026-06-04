import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { COLORS, FONTS } from "../utils/theme";

interface SubtitleProps {
  text: string;
  startFrame: number;
  endFrame: number;
  size?: number;
}

export const Subtitle: React.FC<SubtitleProps> = ({
  text,
  startFrame,
  endFrame,
  size = 28,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(
    frame,
    [startFrame, startFrame + 8, endFrame - 8, endFrame],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  if (opacity === 0) return null;

  return (
    <div
      style={{
        position: "absolute",
        bottom: 52,
        left: "50%",
        transform: "translateX(-50%)",
        opacity,
        textAlign: "center",
        fontFamily: FONTS.serif,
        fontStyle: "italic",
        fontSize: size,
        color: COLORS.chalk,
        textShadow: "0 2px 12px rgba(0,0,0,0.9)",
        background: "rgba(0,0,0,0.35)",
        padding: "6px 24px",
        borderRadius: 4,
        letterSpacing: "0.5px",
        maxWidth: 1400,
        whiteSpace: "pre-wrap",
        lineHeight: 1.5,
      }}
    >
      {text}
    </div>
  );
};
