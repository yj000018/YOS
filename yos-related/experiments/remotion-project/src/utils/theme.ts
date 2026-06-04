// ─── PALETTE ────────────────────────────────────────────────────────────────
export const COLORS = {
  black: "#050508",
  deepBlue: "#080d1a",
  graphite: "#1a1d24",
  slate: "#2a2d38",
  chalk: "#e8e4d8",
  ivory: "#f5f0e8",
  white: "#ffffff",
  cyan: "#48cae4",
  amber: "#f4a261",
  solar: "#ffd166",
  orange: "#e76f51",
  red: "#c1121f",
  dimWhite: "rgba(232,228,216,0.15)",
  dimCyan: "rgba(72,202,228,0.25)",
};

// ─── TYPOGRAPHY ─────────────────────────────────────────────────────────────
export const FONTS = {
  mono: "'Courier New', 'Courier', monospace",
  serif: "'Georgia', 'Times New Roman', serif",
  sans: "'Helvetica Neue', 'Arial', sans-serif",
};

// ─── FPS & TIMING ────────────────────────────────────────────────────────────
export const FPS = 30;
export const W = 1920;
export const H = 1080;

// ─── EASING ──────────────────────────────────────────────────────────────────
export const easeOut = (t: number): number => 1 - Math.pow(1 - t, 3);
export const easeIn = (t: number): number => t * t * t;
export const easeInOut = (t: number): number =>
  t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
