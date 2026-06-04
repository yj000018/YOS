import React from "react";
import { useCurrentFrame } from "remotion";
import { COLORS } from "../utils/theme";

interface ParticlesDef {
  count?: number;
  seed?: number;
}

export const Particles: React.FC<ParticlesDef> = ({ count = 60, seed = 42 }) => {
  const frame = useCurrentFrame();

  const particles = Array.from({ length: count }, (_, i) => {
    const s = (seed * (i + 1) * 2654435761) >>> 0;
    const x = ((s * 1664525 + 1013904223) >>> 0) % 1920;
    const y = ((s * 22695477 + 1) >>> 0) % 1080;
    const size = 1 + (i % 3);
    const speed = 0.2 + (i % 5) * 0.1;
    const phase = (i * 137.5) % 360;
    const opacity = 0.1 + (i % 6) * 0.08;

    const dy = (frame * speed) % 1080;
    const dx = Math.sin((frame * 0.01 + phase) * (Math.PI / 180)) * 30;

    return { x: (x + dx) % 1920, y: (y - dy + 1080) % 1080, size: Math.max(1, i % 3 + 1), opacity };
  });

  return (
    <svg
      style={{ position: "absolute", top: 0, left: 0, width: 1920, height: 1080, pointerEvents: "none" }}
    >
      {particles.map((p, i) => (
        <circle
          key={i}
          cx={p.x}
          cy={p.y}
          r={p.size}
          fill={i % 3 === 0 ? COLORS.cyan : i % 3 === 1 ? COLORS.solar : COLORS.chalk}
          opacity={p.opacity}
        />
      ))}
    </svg>
  );
};
