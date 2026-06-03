'use client'

interface SessionControlsProps {
  isMuted: boolean
  showTranscript: boolean
  onStop: () => void
  onToggleMute: () => void
  onToggleTranscript: () => void
  sessionDuration: number // seconds
}

function formatDuration(seconds: number): string {
  const m = Math.floor(seconds / 60).toString().padStart(2, '0')
  const s = (seconds % 60).toString().padStart(2, '0')
  return `${m}:${s}`
}

export default function SessionControls({
  isMuted,
  showTranscript,
  onStop,
  onToggleMute,
  onToggleTranscript,
  sessionDuration,
}: SessionControlsProps) {
  return (
    <div className="flex flex-col items-center gap-4 animate-slide-up">
      {/* Duration */}
      <div className="state-badge text-yos-muted">
        {formatDuration(sessionDuration)}
      </div>

      {/* Controls row */}
      <div className="flex items-center gap-4">
        {/* Mute */}
        <button
          onClick={onToggleMute}
          className={`w-12 h-12 rounded-full flex items-center justify-center transition-all duration-200 ${
            isMuted
              ? 'bg-yos-error/20 border border-yos-error/40 text-yos-error'
              : 'glass-card text-yos-muted hover:text-yos-text hover:border-yos-border'
          }`}
          title={isMuted ? 'Unmute' : 'Mute'}
        >
          {isMuted ? (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="1" y1="1" x2="23" y2="23"/>
              <path d="M9 9v3a3 3 0 0 0 5.12 2.12M15 9.34V4a3 3 0 0 0-5.94-.6"/>
              <path d="M17 16.95A7 7 0 0 1 5 12v-2m14 0v2a7 7 0 0 1-.11 1.23"/>
              <line x1="12" y1="19" x2="12" y2="23"/>
              <line x1="8" y1="23" x2="16" y2="23"/>
            </svg>
          ) : (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
              <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
              <line x1="12" y1="19" x2="12" y2="23"/>
              <line x1="8" y1="23" x2="16" y2="23"/>
            </svg>
          )}
        </button>

        {/* STOP — primary action */}
        <button
          onClick={onStop}
          className="w-16 h-16 rounded-full bg-yos-error/20 border border-yos-error/50 text-yos-error hover:bg-yos-error/30 hover:border-yos-error transition-all duration-200 flex items-center justify-center"
          title="Stop session"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <rect x="6" y="6" width="12" height="12" rx="2"/>
          </svg>
        </button>

        {/* Transcript toggle */}
        <button
          onClick={onToggleTranscript}
          className={`w-12 h-12 rounded-full flex items-center justify-center transition-all duration-200 ${
            showTranscript
              ? 'bg-yos-accent/20 border border-yos-accent/40 text-yos-accent'
              : 'glass-card text-yos-muted hover:text-yos-text'
          }`}
          title={showTranscript ? 'Hide transcript' : 'Show transcript'}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
        </button>
      </div>
    </div>
  )
}
