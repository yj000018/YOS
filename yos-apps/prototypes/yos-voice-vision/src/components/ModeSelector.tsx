'use client'

import type { VoiceMode } from '@/types'
import { unlockAudioContext } from '@/lib/ios-audio-unlock'

interface ModeSelectorProps {
  onSelect: (mode: VoiceMode) => void
  disabled?: boolean
}

export default function ModeSelector({ onSelect, disabled }: ModeSelectorProps) {
  const handleSelect = async (mode: VoiceMode) => {
    // iOS Safari: AudioContext MUST be unlocked synchronously inside a user gesture.
    // This call is intentionally before the async startSession chain.
    await unlockAudioContext()
    onSelect(mode)
  }

  return (
    <div className="flex flex-col items-center gap-6 animate-slide-up">
      {/* Header */}
      <div className="text-center space-y-1">
        <p className="state-badge text-yos-muted">SELECT MODE</p>
      </div>

      {/* Mode buttons */}
      <div className="flex flex-col gap-3 w-full max-w-xs">
        {/* Voice mode */}
        <button
          onClick={() => handleSelect('voice')}
          disabled={disabled}
          className="group relative glass-card rounded-2xl p-5 text-left hover:border-yos-voice/40 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-yos-voice/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          <div className="relative flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-yos-voice/10 border border-yos-voice/20 flex items-center justify-center flex-shrink-0 group-hover:bg-yos-voice/20 transition-colors duration-300">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" strokeWidth="2">
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
                <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                <line x1="12" y1="19" x2="12" y2="23"/>
                <line x1="8" y1="23" x2="16" y2="23"/>
              </svg>
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-yos-text font-semibold text-sm">Voice</span>
                <span className="state-badge text-yos-voice/70 bg-yos-voice/10 px-1.5 py-0.5 rounded">OpenAI</span>
              </div>
              <p className="text-yos-muted text-xs leading-relaxed">
                Conversation, reflection, assistance
              </p>
            </div>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" strokeWidth="2" className="flex-shrink-0 group-hover:stroke-yos-voice transition-colors duration-300">
              <path d="M9 18l6-6-6-6"/>
            </svg>
          </div>
        </button>

        {/* Voice + Vision mode */}
        <button
          onClick={() => handleSelect('voice_vision')}
          disabled={disabled}
          className="group relative glass-card rounded-2xl p-5 text-left hover:border-yos-vision/40 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-yos-vision/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          <div className="relative flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-yos-vision/10 border border-yos-vision/20 flex items-center justify-center flex-shrink-0 group-hover:bg-yos-vision/20 transition-colors duration-300">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" strokeWidth="2">
                <path d="M23 7l-7 5 7 5V7z"/>
                <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
              </svg>
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-yos-text font-semibold text-sm">Voice + Vision</span>
                <span className="state-badge text-yos-vision/70 bg-yos-vision/10 px-1.5 py-0.5 rounded">Gemini</span>
              </div>
              <p className="text-yos-muted text-xs leading-relaxed">
                Environment, objects, space, CasaTAO
              </p>
            </div>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" strokeWidth="2" className="flex-shrink-0 group-hover:stroke-yos-vision transition-colors duration-300">
              <path d="M9 18l6-6-6-6"/>
            </svg>
          </div>
        </button>
      </div>

      {/* Footer info */}
      <p className="state-badge text-yos-muted/50 text-center">
        Tap to start · Sessions logged to Notion
      </p>
    </div>
  )
}
