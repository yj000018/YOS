import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'yos-bg': '#05060f',
        'yos-surface': '#0d0f1e',
        'yos-border': '#1a1d35',
        'yos-accent': '#4f6ef7',
        'yos-accent-2': '#7c3aed',
        'yos-glow': '#818cf8',
        'yos-text': '#e2e8f0',
        'yos-muted': '#64748b',
        'yos-voice': '#22d3ee',
        'yos-vision': '#a78bfa',
        'yos-active': '#4ade80',
        'yos-error': '#f87171',
      },
      fontFamily: {
        sans: ['var(--font-syne)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-space-mono)', 'monospace'],
      },
      animation: {
        'orb-pulse': 'orbPulse 2s ease-in-out infinite',
        'orb-speak': 'orbSpeak 0.5s ease-in-out infinite alternate',
        'orb-listen': 'orbListen 1s ease-in-out infinite',
        'wave': 'wave 1.5s ease-in-out infinite',
        'glow-ring': 'glowRing 2s ease-in-out infinite',
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
      },
      keyframes: {
        orbPulse: {
          '0%, 100%': { transform: 'scale(1)', opacity: '0.9' },
          '50%': { transform: 'scale(1.05)', opacity: '1' },
        },
        orbSpeak: {
          '0%': { transform: 'scale(1)', boxShadow: '0 0 30px rgba(79, 110, 247, 0.4)' },
          '100%': { transform: 'scale(1.15)', boxShadow: '0 0 60px rgba(79, 110, 247, 0.8)' },
        },
        orbListen: {
          '0%, 100%': { transform: 'scale(1)', boxShadow: '0 0 20px rgba(34, 211, 238, 0.3)' },
          '50%': { transform: 'scale(1.08)', boxShadow: '0 0 50px rgba(34, 211, 238, 0.7)' },
        },
        wave: {
          '0%, 100%': { transform: 'scaleY(0.5)' },
          '50%': { transform: 'scaleY(1.5)' },
        },
        glowRing: {
          '0%, 100%': { opacity: '0.3', transform: 'scale(1)' },
          '50%': { opacity: '0.8', transform: 'scale(1.1)' },
        },
        fadeIn: {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        slideUp: {
          from: { opacity: '0', transform: 'translateY(20px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}

export default config
