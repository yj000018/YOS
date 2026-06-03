'use client'

import { useEffect, useRef } from 'react'
import type { SessionState, VoiceMode } from '@/types'

interface OrbProps {
  state: SessionState
  mode: VoiceMode | null
  audioLevel?: number // 0-1
}

const STATE_COLORS: Record<SessionState, { primary: string; secondary: string; glow: string }> = {
  idle:       { primary: '#1a1d35', secondary: '#0d0f1e', glow: 'rgba(79, 110, 247, 0.1)' },
  connecting: { primary: '#4f6ef7', secondary: '#3b55e0', glow: 'rgba(79, 110, 247, 0.4)' },
  listening:  { primary: '#22d3ee', secondary: '#0891b2', glow: 'rgba(34, 211, 238, 0.5)' },
  processing: { primary: '#a78bfa', secondary: '#7c3aed', glow: 'rgba(167, 139, 250, 0.4)' },
  speaking:   { primary: '#4f6ef7', secondary: '#818cf8', glow: 'rgba(79, 110, 247, 0.6)' },
  error:      { primary: '#f87171', secondary: '#dc2626', glow: 'rgba(248, 113, 113, 0.4)' },
  ended:      { primary: '#1a1d35', secondary: '#0d0f1e', glow: 'rgba(79, 110, 247, 0.05)' },
}

const MODE_ACCENT: Record<string, string> = {
  voice:        '#4f6ef7',
  voice_vision: '#a78bfa',
}

export default function Orb({ state, mode, audioLevel = 0 }: OrbProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const animFrameRef = useRef<number>(0)
  const timeRef = useRef<number>(0)
  const audioLevelRef = useRef<number>(audioLevel)

  useEffect(() => {
    audioLevelRef.current = audioLevel
  }, [audioLevel])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const size = 240
    canvas.width = size
    canvas.height = size

    const colors = STATE_COLORS[state]
    const accentColor = mode ? MODE_ACCENT[mode] : '#4f6ef7'

    const draw = (timestamp: number) => {
      timeRef.current = timestamp * 0.001
      const t = timeRef.current
      const level = audioLevelRef.current
      ctx.clearRect(0, 0, size, size)

      const cx = size / 2
      const cy = size / 2

      // Outer glow ring
      if (state !== 'idle' && state !== 'ended') {
        const glowRadius = 100 + Math.sin(t * 2) * 5 + level * 15
        const glowGrad = ctx.createRadialGradient(cx, cy, glowRadius * 0.6, cx, cy, glowRadius)
        glowGrad.addColorStop(0, colors.glow)
        glowGrad.addColorStop(1, 'transparent')
        ctx.beginPath()
        ctx.arc(cx, cy, glowRadius, 0, Math.PI * 2)
        ctx.fillStyle = glowGrad
        ctx.fill()
      }

      // Pulsing rings (listening/speaking)
      if (state === 'listening' || state === 'speaking') {
        for (let i = 0; i < 3; i++) {
          const phase = (t * 0.8 + i * 0.4) % 1
          const ringRadius = 70 + phase * 50
          const ringAlpha = (1 - phase) * 0.3
          ctx.beginPath()
          ctx.arc(cx, cy, ringRadius, 0, Math.PI * 2)
          ctx.strokeStyle = colors.primary + Math.round(ringAlpha * 255).toString(16).padStart(2, '0')
          ctx.lineWidth = 1.5
          ctx.stroke()
        }
      }

      // Organic blob shape (main orb)
      const baseRadius = 70
      const points = 64
      ctx.beginPath()
      for (let i = 0; i <= points; i++) {
        const angle = (i / points) * Math.PI * 2
        let r = baseRadius

        if (state === 'speaking') {
          r += Math.sin(angle * 4 + t * 8) * (8 + level * 20)
          r += Math.sin(angle * 7 + t * 5) * (4 + level * 10)
          r += Math.sin(angle * 2 + t * 3) * 6
        } else if (state === 'listening') {
          r += Math.sin(angle * 3 + t * 4) * (5 + level * 15)
          r += Math.sin(angle * 6 + t * 3) * 3
        } else if (state === 'processing') {
          r += Math.sin(angle * 5 + t * 6) * 8
          r += Math.sin(angle * 3 + t * 4) * 4
        } else if (state === 'connecting') {
          r += Math.sin(angle * 2 + t * 3) * 5
        } else {
          r += Math.sin(angle * 2 + t * 1) * 3
        }

        const x = cx + r * Math.cos(angle)
        const y = cy + r * Math.sin(angle)
        if (i === 0) ctx.moveTo(x, y)
        else ctx.lineTo(x, y)
      }
      ctx.closePath()

      // Orb gradient fill
      const orbGrad = ctx.createRadialGradient(cx - 20, cy - 20, 0, cx, cy, baseRadius + 20)
      orbGrad.addColorStop(0, colors.secondary + 'ff')
      orbGrad.addColorStop(0.5, colors.primary + 'cc')
      orbGrad.addColorStop(1, colors.primary + '44')
      ctx.fillStyle = orbGrad
      ctx.fill()

      // Inner highlight
      const highlightGrad = ctx.createRadialGradient(cx - 25, cy - 25, 0, cx - 15, cy - 15, 40)
      highlightGrad.addColorStop(0, 'rgba(255, 255, 255, 0.15)')
      highlightGrad.addColorStop(1, 'transparent')
      ctx.fillStyle = highlightGrad
      ctx.fill()

      // Accent ring
      ctx.beginPath()
      ctx.arc(cx, cy, baseRadius + 2, 0, Math.PI * 2)
      ctx.strokeStyle = accentColor + '40'
      ctx.lineWidth = 1
      ctx.stroke()

      // Processing spinner
      if (state === 'processing') {
        ctx.beginPath()
        ctx.arc(cx, cy, baseRadius + 12, t * 2, t * 2 + Math.PI * 1.5)
        ctx.strokeStyle = accentColor + 'aa'
        ctx.lineWidth = 2
        ctx.lineCap = 'round'
        ctx.stroke()
      }

      // Vision mode indicator (camera icon dot)
      if (mode === 'voice_vision' && state !== 'idle') {
        ctx.beginPath()
        ctx.arc(cx + 50, cy - 50, 5, 0, Math.PI * 2)
        ctx.fillStyle = '#a78bfa'
        ctx.fill()
        ctx.beginPath()
        ctx.arc(cx + 50, cy - 50, 8, 0, Math.PI * 2)
        ctx.strokeStyle = '#a78bfa44'
        ctx.lineWidth = 1
        ctx.stroke()
      }

      animFrameRef.current = requestAnimationFrame(draw)
    }

    animFrameRef.current = requestAnimationFrame(draw)
    return () => cancelAnimationFrame(animFrameRef.current)
  }, [state, mode])

  return (
    <div className="orb-container w-60 h-60 select-none">
      <canvas
        ref={canvasRef}
        className="w-60 h-60"
        style={{ imageRendering: 'pixelated' }}
      />
    </div>
  )
}
