import React from "react";
import { useCurrentFrame } from "remotion";
import { COLORS } from "../utils/theme";

export const ScanLine: React.FC = () => {
  const frame = useCurrentFrame();
  const y = (frame * 4) % 1080;

  return (
    <div
      style={{
        position: "absolute",
        top: y,
        left: 0,
        width: "100%",
        height: 2,
        background: `linear-gradient(90deg, transparent, ${COLORS.cyan}44, ${COLORS.cyan}88, ${COLORS.cyan}44, transparent)`,
        pointerEvents: "none",
      }}
    />
  );
};
