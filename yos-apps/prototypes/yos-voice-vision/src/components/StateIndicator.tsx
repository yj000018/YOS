'use client'

import type { SessionState } from '@/types'

interface StateIndicatorProps {
  state: SessionState
  provider?: string
}

const STATE_CONFIG: Record<SessionState, { label: string; color: string; dot: string }> = {
  idle:       { label: 'IDLE',       color: 'text-yos-muted',   dot: 'bg-yos-muted' },
  connecting: { label: 'CONNECTING', color: 'text-yos-accent',  dot: 'bg-yos-accent animate-pulse' },
  listening:  { label: 'LISTENING',  color: 'text-yos-voice',   dot: 'bg-yos-voice animate-ping-slow' },
  processing: { label: 'PROCESSING', color: 'text-yos-vision',  dot: 'bg-yos-vision animate-spin-slow' },
  speaking:   { label: 'SPEAKING',   color: 'text-yos-accent',  dot: 'bg-yos-accent animate-pulse' },
  error:      { label: 'ERROR',      color: 'text-yos-error',   dot: 'bg-yos-error' },
  ended:      { label: 'ENDED',      color: 'text-yos-muted',   dot: 'bg-yos-muted' },
}

export default function StateIndicator({ state, provider }: StateIndicatorProps) {
  const cfg = STATE_CONFIG[state]

  return (
    <div className="flex items-center gap-3">
      <div className="relative flex items-center justify-center w-3 h-3">
        <div className={`w-2 h-2 rounded-full ${cfg.dot}`} />
      </div>
      <div className="flex flex-col">
        <span className={`state-badge ${cfg.color}`}>{cfg.label}</span>
        {provider && (
          <span className="state-badge text-yos-muted mt-0.5">{provider}</span>
        )}
      </div>
    </div>
  )
}
