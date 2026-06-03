'use client'

import { useEffect, useRef } from 'react'
import type { SessionState } from '@/types'

interface WaveformProps {
  state: SessionState
  audioData?: Float32Array
  barCount?: number
}

const STATE_COLOR: Record<SessionState, string> = {
  idle:       '#1a1d35',
  connecting: '#4f6ef7',
  listening:  '#22d3ee',
  processing: '#a78bfa',
  speaking:   '#4f6ef7',
  error:      '#f87171',
  ended:      '#1a1d35',
}

export default function Waveform({ state, audioData, barCount = 32 }: WaveformProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const animRef = useRef<number>(0)
  const timeRef = useRef<number>(0)
  const audioDataRef = useRef<Float32Array | undefined>(audioData)

  useEffect(() => {
    audioDataRef.current = audioData
  }, [audioData])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const W = 280
    const H = 60
    canvas.width = W
    canvas.height = H

    const color = STATE_COLOR[state]
    const isActive = state === 'listening' || state === 'speaking'

    const draw = (timestamp: number) => {
      timeRef.current = timestamp * 0.001
      const t = timeRef.current
      ctx.clearRect(0, 0, W, H)

      const barW = 3
      const gap = (W - barCount * barW) / (barCount + 1)
      const maxH = H * 0.8
      const minH = H * 0.08

      for (let i = 0; i < barCount; i++) {
        const x = gap + i * (barW + gap)

        let h: number
        if (!isActive) {
          h = minH + Math.sin(t * 0.5 + i * 0.3) * (minH * 0.5)
        } else if (audioDataRef.current && audioDataRef.current.length > 0) {
          const idx = Math.floor((i / barCount) * audioDataRef.current.length)
          const raw = Math.abs(audioDataRef.current[idx] || 0)
          h = minH + raw * maxH
        } else {
          // Animated fallback
          const freq1 = Math.sin(t * 3 + i * 0.4) * 0.5 + 0.5
          const freq2 = Math.sin(t * 5 + i * 0.7) * 0.3 + 0.3
          const freq3 = Math.sin(t * 2 + i * 0.2) * 0.2 + 0.2
          h = minH + (freq1 * 0.5 + freq2 * 0.3 + freq3 * 0.2) * maxH
        }

        h = Math.max(minH, Math.min(maxH, h))

        const y = (H - h) / 2

        // Bar gradient
        const grad = ctx.createLinearGradient(x, y, x, y + h)
        grad.addColorStop(0, color + '44')
        grad.addColorStop(0.5, color + 'cc')
        grad.addColorStop(1, color + '44')

        ctx.beginPath()
        ctx.roundRect(x, y, barW, h, 1.5)
        ctx.fillStyle = grad
        ctx.fill()
      }

      animRef.current = requestAnimationFrame(draw)
    }

    animRef.current = requestAnimationFrame(draw)
    return () => cancelAnimationFrame(animRef.current)
  }, [state, barCount])

  return (
    <canvas
      ref={canvasRef}
      className="w-[280px] h-[60px]"
      style={{ imageRendering: 'auto' }}
    />
  )
}
