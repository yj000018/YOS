'use client'

import { useEffect, useRef } from 'react'
import type { TranscriptEntry } from '@/types'

interface TranscriptPanelProps {
  entries: TranscriptEntry[]
  visible: boolean
}

export default function TranscriptPanel({ entries, visible }: TranscriptPanelProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (visible && bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [entries, visible])

  if (!visible) return null

  return (
    <div className="glass-card rounded-2xl p-4 w-full max-w-sm mx-auto max-h-48 overflow-y-auto animate-fade-in">
      <div className="space-y-3">
        {entries.length === 0 ? (
          <p className="text-yos-muted text-xs font-mono text-center py-2">
            Transcript will appear here...
          </p>
        ) : (
          entries.map((entry) => (
            <div
              key={entry.id}
              className={`transcript-entry flex gap-2 ${
                entry.role === 'user' ? 'flex-row-reverse' : 'flex-row'
              }`}
            >
              <div
                className={`flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center text-[9px] font-bold ${
                  entry.role === 'user'
                    ? 'bg-yos-voice/20 text-yos-voice'
                    : 'bg-yos-accent/20 text-yos-accent'
                }`}
              >
                {entry.role === 'user' ? 'Y' : 'AI'}
              </div>
              <div
                className={`flex-1 rounded-xl px-3 py-2 text-xs leading-relaxed ${
                  entry.role === 'user'
                    ? 'bg-yos-voice/10 text-yos-text text-right'
                    : 'bg-yos-accent/10 text-yos-text'
                }`}
              >
                {entry.text}
              </div>
            </div>
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}
