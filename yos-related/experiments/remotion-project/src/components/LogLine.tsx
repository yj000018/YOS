import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { COLORS, FONTS } from "../utils/theme";

interface LogLineProps {
  text: string;
  startFrame: number;
  color?: string;
  size?: number;
}

export const LogLine: React.FC<LogLineProps> = ({
  text,
  startFrame,
  color = COLORS.cyan,
  size = 18,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [startFrame, startFrame + 6], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const charCount = Math.floor(
    interpolate(frame, [startFrame, startFrame + text.length * 1.2], [0, text.length], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );

  return (
    <div
      style={{
        opacity,
        fontFamily: FONTS.mono,
        fontSize: size,
        color,
        letterSpacing: "1px",
        lineHeight: 1.6,
      }}
    >
      {text.slice(0, charCount)}
      {charCount < text.length && (
        <span style={{ opacity: Math.sin(frame * 0.5) > 0 ? 1 : 0 }}>█</span>
      )}
    </div>
  );
};
