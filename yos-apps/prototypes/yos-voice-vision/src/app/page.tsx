'use client'

import { useState } from 'react'
import dynamic from 'next/dynamic'
import { useVoiceSession } from '@/hooks/useVoiceSession'
import ModeSelector from '@/components/ModeSelector'
import StateIndicator from '@/components/StateIndicator'
import SessionControls from '@/components/SessionControls'
import TranscriptPanel from '@/components/TranscriptPanel'
import CameraPreview from '@/components/CameraPreview'
import TextInput from '@/components/TextInput'
import type { VoiceMode } from '@/types'

// Dynamic import for canvas-based components (no SSR)
const Orb = dynamic(() => import('@/components/Orb'), { ssr: false })
const Waveform = dynamic(() => import('@/components/Waveform'), { ssr: false })

const PROVIDER_LABELS: Record<string, string> = {
  openai_realtime: 'OpenAI Realtime',
  gemini_live: 'Gemini Live',
}

const PROJECTS = ['yOS', 'CasaTAO', 'ODYSSEY', 'ARC & Deep Health', 'Health', 'Family', 'YANTRA', 'EIA']

export default function Home() {
  const {
    state,
    audioLevel,
    cameraStream,
    sessionDuration,
    interactionMode,
    startSession,
    stopSession,
    toggleMute,
    toggleInteractionMode,
    sendTextMessage,
    resetToIdle,
  } = useVoiceSession()

  const [showTranscript, setShowTranscript] = useState(true)
  const [architectMode, setArchitectMode] = useState(false)
  const [selectedProject, setSelectedProject] = useState<string>('')
  const [showProjectPicker, setShowProjectPicker] = useState(false)

  const isInSession = state.sessionState !== 'idle' && state.sessionState !== 'ended'
  const providerLabel = state.provider ? PROVIDER_LABELS[state.provider] : undefined
  const isOpenAI = state.provider === 'openai_realtime'
  const isTextMode = interactionMode === 'text'

  const handleModeSelect = async (mode: VoiceMode) => {
    setShowTranscript(true)
    setShowProjectPicker(false)
    await startSession(mode, selectedProject || undefined)
  }

  const handleStop = async () => {
    await stopSession()
  }

  const handleReset = () => {
    resetToIdle()
    setShowTranscript(true)
  }

  return (
    <main className="min-h-screen bg-yos-bg flex flex-col items-center justify-center px-4 py-8 relative overflow-hidden">
      {/* Background constellation */}
      <div className="absolute inset-0 constellation-bg pointer-events-none" />

      {/* Ambient glow */}
      <div
        className="absolute inset-0 pointer-events-none transition-opacity duration-1000"
        style={{
          background: state.mode === 'voice_vision'
            ? 'radial-gradient(ellipse at center, rgba(167, 139, 250, 0.04) 0%, transparent 70%)'
            : 'radial-gradient(ellipse at center, rgba(79, 110, 247, 0.04) 0%, transparent 70%)',
          opacity: isInSession ? 1 : 0.3,
        }}
      />

      {/* Main content */}
      <div className="relative z-10 flex flex-col items-center gap-6 w-full max-w-sm">

        {/* Header */}
        <div className="flex items-center justify-between w-full animate-fade-in">
          <div className="flex flex-col items-start gap-0.5">
            <div className="flex items-center gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-yos-accent" />
              <span className="state-badge text-yos-muted">Y-OS</span>
            </div>
            <h1 className="text-yos-text font-bold text-lg tracking-tight">VIVI</h1>
          </div>

          {/* Right controls */}
          <div className="flex items-center gap-2">
            {/* Architect Mode toggle */}
            <button
              onClick={() => setArchitectMode(p => !p)}
              className="text-xs px-2 py-1 rounded-lg transition-all duration-200"
              style={{
                background: architectMode ? 'rgba(245,158,11,0.12)' : 'rgba(255,255,255,0.04)',
                border: `1px solid ${architectMode ? 'rgba(245,158,11,0.35)' : 'rgba(255,255,255,0.08)'}`,
                color: architectMode ? '#f59e0b' : '#8b8fa8',
              }}
              title="Toggle Architect / Simple Mode"
            >
              {architectMode ? '⚙ ARCH' : '○ SIMPLE'}
            </button>

            {/* Voice ↔ Text toggle (OpenAI only, in session) */}
            {isInSession && isOpenAI && (
              <button
                onClick={toggleInteractionMode}
                className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg transition-all duration-200 text-xs"
                style={{
                  background: isTextMode ? 'rgba(79, 110, 247, 0.2)' : 'rgba(255,255,255,0.04)',
                  border: `1px solid ${isTextMode ? 'rgba(79,110,247,0.4)' : 'rgba(255,255,255,0.08)'}`,
                  color: isTextMode ? '#4f6ef7' : '#8b8fa8',
                }}
                title={isTextMode ? 'Switch to voice' : 'Switch to text'}
              >
                {isTextMode ? (
                  <>
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                      <circle cx="6" cy="6" r="4" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M6 4v4M4 6h4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                    </svg>
                    <span>TEXT</span>
                  </>
                ) : (
                  <>
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                      <path d="M6 1a2 2 0 0 1 2 2v3a2 2 0 0 1-4 0V3a2 2 0 0 1 2-2z" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M2 6a4 4 0 0 0 8 0M6 10v1" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                    </svg>
                    <span>VOICE</span>
                  </>
                )}
              </button>
            )}
          </div>
        </div>

        {/* Architect Mode info bar — visible during session */}
        {architectMode && isInSession && (
          <div
            className="glass-card rounded-xl p-3 w-full text-xs space-y-1.5 animate-fade-in"
            style={{ borderColor: 'rgba(245,158,11,0.2)' }}
          >
            <p className="text-amber-400/60 font-semibold tracking-widest mb-1">ARCHITECT MODE</p>
            {[
              ['PROVIDER', providerLabel || '—'],
              ['MODE', state.mode === 'voice_vision' ? 'Voice + Vision' : 'Voice'],
              ['PROJECT', selectedProject || 'none'],
              ['CONTEXT', 'injected ✓'],
              ['MEMORY', 'Notion Inbox'],
              ['TRANSCRIPT', `${state.transcript.length} entries`],
              ['CAMERA', state.mode === 'voice_vision' ? (state.cameraEnabled ? 'active' : 'off') : 'n/a'],
            ].map(([label, value]) => (
              <div key={label} className="flex items-center justify-between">
                <span className="text-amber-400/50">{label}</span>
                <span className="text-yos-text/80">{value}</span>
              </div>
            ))}
          </div>
        )}

        {/* State indicator (when in session) */}
        {isInSession && (
          <div className="animate-fade-in w-full flex items-center justify-center">
            <StateIndicator state={state.sessionState} provider={providerLabel} />
          </div>
        )}

        {/* Camera preview (vision mode) */}
        {state.mode === 'voice_vision' && isInSession && (
          <CameraPreview stream={cameraStream} visible={state.cameraEnabled} />
        )}

        {/* Central ORB — hidden in text mode */}
        {!isTextMode && (
          <div className="flex flex-col items-center gap-4">
            <Orb
              state={state.sessionState}
              mode={state.mode}
              audioLevel={audioLevel}
            />
            {isInSession && (
              <Waveform state={state.sessionState} />
            )}
          </div>
        )}

        {/* Mode selector + project picker (idle state) */}
        {state.sessionState === 'idle' && (
          <div className="flex flex-col gap-3 w-full">
            {/* Project selector */}
            <div className="relative">
              <button
                onClick={() => setShowProjectPicker(p => !p)}
                className="glass-card rounded-xl px-4 py-2.5 w-full text-left flex items-center justify-between transition-all duration-200 hover:border-yos-accent/30"
              >
                <div className="flex items-center gap-2">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#64748b" strokeWidth="2">
                    <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                  </svg>
                  <span className="text-xs" style={{ color: selectedProject ? '#22d3ee' : '#64748b' }}>
                    {selectedProject || 'Select project (optional)'}
                  </span>
                </div>
                <svg
                  width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#64748b" strokeWidth="2"
                  style={{ transform: showProjectPicker ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }}
                >
                  <path d="M6 9l6 6 6-6"/>
                </svg>
              </button>

              {showProjectPicker && (
                <div className="absolute top-full left-0 right-0 mt-1 glass-card rounded-xl overflow-hidden z-20 animate-fade-in">
                  {['', ...PROJECTS].map(p => (
                    <button
                      key={p || '__none__'}
                      onClick={() => { setSelectedProject(p); setShowProjectPicker(false) }}
                      className="w-full text-left px-4 py-2.5 text-xs transition-colors duration-150 hover:bg-white/5"
                      style={{ color: p === selectedProject ? '#22d3ee' : '#8b8fa8' }}
                    >
                      {p || '— No project —'}
                    </button>
                  ))}
                </div>
              )}
            </div>

            <ModeSelector onSelect={handleModeSelect} />
          </div>
        )}

        {/* Session controls (active session) */}
        {isInSession && (
          <SessionControls
            isMuted={state.isMuted}
            showTranscript={showTranscript}
            onStop={handleStop}
            onToggleMute={toggleMute}
            onToggleTranscript={() => setShowTranscript(p => !p)}
            sessionDuration={sessionDuration}
          />
        )}

        {/* Transcript panel — always shown during session, collapsible */}
        {isInSession && (
          <TranscriptPanel
            entries={state.transcript}
            visible={showTranscript}
          />
        )}

        {/* Text input (text mode, OpenAI only) */}
        {isInSession && isOpenAI && isTextMode && (
          <TextInput
            onSend={sendTextMessage}
            disabled={state.sessionState === 'processing' || state.sessionState === 'speaking'}
          />
        )}

        {/* Error state */}
        {state.sessionState === 'error' && (
          <div className="glass-card rounded-2xl p-4 w-full text-center animate-fade-in border-yos-error/20">
            <p className="text-yos-error text-sm mb-3">{state.error || 'An error occurred'}</p>
            <button
              onClick={handleReset}
              className="text-yos-muted hover:text-yos-text text-xs state-badge transition-colors"
            >
              RESET
            </button>
          </div>
        )}

        {/* Session ended state */}
        {state.sessionState === 'ended' && (
          <div className="w-full flex flex-col gap-4 animate-fade-in">
            <div className="glass-card rounded-2xl p-5 w-full text-center">
              <div className="flex items-center justify-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-yos-active" />
                <span className="state-badge text-yos-active">SESSION LOGGED</span>
              </div>
              {architectMode && (
                <div className="text-xs text-yos-muted/60 mb-3 space-y-0.5 text-left px-2">
                  <p>Provider: {providerLabel}</p>
                  <p>Project: {selectedProject || 'none'}</p>
                  <p>Duration: {sessionDuration}s · Entries: {state.transcript.length}</p>
                  <p>Destination: yOS Memory Inbox → Notion</p>
                </div>
              )}
              <p className="text-yos-muted text-xs mb-4">
                Transcript saved to Notion · {sessionDuration}s
              </p>
              <button
                onClick={handleReset}
                className="glass-card rounded-xl px-6 py-2.5 text-yos-text text-sm hover:border-yos-accent/40 transition-all duration-200"
              >
                New Session
              </button>
            </div>
            {/* Full transcript visible after session ends */}
            <TranscriptPanel
              entries={state.transcript}
              visible={true}
            />
          </div>
        )}

        {/* Version */}
        <div className="state-badge text-yos-muted/30">
          VIVI v0.2 · {architectMode ? 'Architect' : 'Simple'}
        </div>
      </div>
    </main>
  )
}
