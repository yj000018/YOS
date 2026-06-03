'use client'

import { useState, useCallback, useRef, useEffect } from 'react'
import type { UIState, VoiceMode, SessionState, TranscriptEntry, ProviderType } from '@/types'
import { OpenAIRealtimeAdapter } from '@/lib/openai-realtime'
import { GeminiLiveAdapter } from '@/lib/gemini-live'

function generateId(): string {
  return Math.random().toString(36).slice(2) + Date.now().toString(36)
}

export type InteractionMode = 'voice' | 'text'

export function useVoiceSession() {
  const [state, setState] = useState<UIState>({
    sessionState: 'idle',
    mode: null,
    provider: null,
    isMuted: false,
    cameraEnabled: false,
    transcript: [],
    currentSpeaker: null,
    error: null,
    sessionId: null,
    sessionStartTime: null,
  })

  const [audioLevel, setAudioLevel] = useState(0)
  const [cameraStream, setCameraStream] = useState<MediaStream | null>(null)
  const [sessionDuration, setSessionDuration] = useState(0)
  // Voice ↔ Text toggle (OpenAI mode only)
  const [interactionMode, setInteractionMode] = useState<InteractionMode>('voice')

  const adapterRef = useRef<OpenAIRealtimeAdapter | GeminiLiveAdapter | null>(null)
  const durationTimerRef = useRef<ReturnType<typeof setInterval> | null>(null)
  const audioContextRef = useRef<AudioContext | null>(null)
  const analyserRef = useRef<AnalyserNode | null>(null)
  const audioLevelTimerRef = useRef<ReturnType<typeof setInterval> | null>(null)

  // Duration counter
  useEffect(() => {
    if (state.sessionState !== 'idle' && state.sessionState !== 'ended' && state.sessionStartTime) {
      durationTimerRef.current = setInterval(() => {
        setSessionDuration(Math.floor((Date.now() - (state.sessionStartTime || 0)) / 1000))
      }, 1000)
    } else {
      if (durationTimerRef.current) clearInterval(durationTimerRef.current)
    }
    return () => {
      if (durationTimerRef.current) clearInterval(durationTimerRef.current)
    }
  }, [state.sessionState, state.sessionStartTime])

  const updateState = useCallback((updates: Partial<UIState>) => {
    setState(prev => ({ ...prev, ...updates }))
  }, [])

  const addTranscriptEntry = useCallback((role: 'user' | 'assistant', text: string) => {
    const entry: TranscriptEntry = {
      id: generateId(),
      role,
      text,
      timestamp: Date.now(),
    }
    setState(prev => ({
      ...prev,
      transcript: [...prev.transcript, entry],
    }))
  }, [])

  const setSessionState = useCallback((sessionState: SessionState) => {
    setState(prev => ({ ...prev, sessionState }))
  }, [])

  // Setup audio level monitoring
  const setupAudioMonitor = useCallback((stream: MediaStream) => {
    try {
      audioContextRef.current = new AudioContext()
      analyserRef.current = audioContextRef.current.createAnalyser()
      analyserRef.current.fftSize = 256
      const source = audioContextRef.current.createMediaStreamSource(stream)
      source.connect(analyserRef.current)

      const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount)
      audioLevelTimerRef.current = setInterval(() => {
        if (!analyserRef.current) return
        analyserRef.current.getByteFrequencyData(dataArray)
        const avg = dataArray.reduce((a, b) => a + b, 0) / dataArray.length
        setAudioLevel(avg / 255)
      }, 50)
    } catch {
      // Audio monitoring not critical
    }
  }, [])

  const startSession = useCallback(async (mode: VoiceMode, project?: string) => {
    try {
      setInteractionMode('voice')
      updateState({
        sessionState: 'connecting',
        mode,
        provider: mode === 'voice' ? 'openai_realtime' : 'gemini_live',
        error: null,
        transcript: [],
        sessionId: generateId(),
        sessionStartTime: Date.now(),
      })
      setSessionDuration(0)

      // Get context from context builder
      let context = ''
      let instructions = ''
      try {
        const ctxRes = await fetch('/api/context-builder', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ type: 'context_request', mode, project: project || undefined }),
        })
        if (ctxRes.ok) {
          const ctxData = await ctxRes.json()
          context = ctxData.context || ''
          instructions = ctxData.instructions || ''
        }
      } catch {
        // Context builder failure is non-blocking
      }

      const sessionContext = {
        mode,
        context,
        instructions,
        timestamp: new Date().toISOString(),
      }

      // Get camera stream for vision mode
      let videoStream: MediaStream | null = null
      if (mode === 'voice_vision') {
        try {
          videoStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false })
          setCameraStream(videoStream)
          updateState({ cameraEnabled: true })
        } catch {
          // Fallback to audio-only if camera unavailable
          console.warn('Camera unavailable, falling back to audio-only')
        }
      }

      // Get microphone stream
      const micStream = await navigator.mediaDevices.getUserMedia({ audio: true })
      setupAudioMonitor(micStream)

      // Create adapter based on mode
      if (mode === 'voice') {
        const adapter = new OpenAIRealtimeAdapter({
          onStateChange: setSessionState,
          onTranscript: addTranscriptEntry,
          onAudioLevel: setAudioLevel,
          onError: (err) => updateState({ sessionState: 'error', error: err }),
        })
        adapterRef.current = adapter
        await adapter.startSession(sessionContext, micStream)
      } else {
        const adapter = new GeminiLiveAdapter({
          onStateChange: setSessionState,
          onTranscript: addTranscriptEntry,
          onAudioLevel: setAudioLevel,
          onError: (err) => updateState({ sessionState: 'error', error: err }),
        })
        adapterRef.current = adapter
        await adapter.startSession(sessionContext, micStream, videoStream || undefined)
      }

    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to start session'
      updateState({ sessionState: 'error', error: message })
    }
  }, [updateState, setSessionState, addTranscriptEntry, setupAudioMonitor])

  const stopSession = useCallback(async () => {
    try {
      if (adapterRef.current) {
        await adapterRef.current.closeSession()
        adapterRef.current = null
      }

      // Stop camera
      if (cameraStream) {
        cameraStream.getTracks().forEach(t => t.stop())
        setCameraStream(null)
      }

      // Stop audio monitoring
      if (audioLevelTimerRef.current) clearInterval(audioLevelTimerRef.current)
      if (audioContextRef.current) {
        audioContextRef.current.close()
        audioContextRef.current = null
      }
      setAudioLevel(0)

      // Log session to Notion
      const currentState = state
      if (currentState.sessionId && currentState.transcript.length > 0) {
        try {
          await fetch('/api/session-log', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              sessionId: currentState.sessionId,
              mode: currentState.mode,
              provider: currentState.provider,
              transcript: currentState.transcript,
              startedAt: new Date(currentState.sessionStartTime || 0).toISOString(),
              endedAt: new Date().toISOString(),
              duration: sessionDuration,
            }),
          })
        } catch {
          // Logging failure is non-blocking
        }
      }

      updateState({ sessionState: 'ended' })
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error stopping session'
      updateState({ sessionState: 'error', error: message })
    }
  }, [state, cameraStream, sessionDuration, updateState])

  const toggleMute = useCallback(() => {
    if (adapterRef.current) {
      const newMuted = !state.isMuted
      adapterRef.current.setMuted(newMuted)
      updateState({ isMuted: newMuted })
    }
  }, [state.isMuted, updateState])

  /**
   * Toggle between voice and text interaction modes (OpenAI only).
   * Mutes/unmutes the mic accordingly. Transcript is preserved.
   */
  const toggleInteractionMode = useCallback(() => {
    if (state.provider !== 'openai_realtime') return
    const adapter = adapterRef.current as OpenAIRealtimeAdapter | null
    if (!adapter) return

    const newMode: InteractionMode = interactionMode === 'voice' ? 'text' : 'voice'
    setInteractionMode(newMode)

    // Mute mic when switching to text mode
    adapter.setMuted(newMode === 'text')
    updateState({ isMuted: newMode === 'text' })
  }, [interactionMode, state.provider, updateState])

  /**
   * Send a text message (text interaction mode, OpenAI only).
   */
  const sendTextMessage = useCallback((text: string) => {
    if (state.provider !== 'openai_realtime') return
    const adapter = adapterRef.current as OpenAIRealtimeAdapter | null
    if (!adapter) return
    adapter.sendText(text)
  }, [state.provider])

  const resetToIdle = useCallback(() => {
    setInteractionMode('voice')
    updateState({
      sessionState: 'idle',
      mode: null,
      provider: null,
      isMuted: false,
      cameraEnabled: false,
      transcript: [],
      currentSpeaker: null,
      error: null,
      sessionId: null,
      sessionStartTime: null,
    })
    setSessionDuration(0)
    setAudioLevel(0)
  }, [updateState])

  return {
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
  }
}
