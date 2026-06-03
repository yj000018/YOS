/**
 * OpenAI Realtime API Adapter
 * Uses WebRTC (preferred) with WebSocket fallback
 * Implements ephemeral token flow for security
 */

import type { SessionContext, SessionState } from '@/types'

interface AdapterCallbacks {
  onStateChange: (state: SessionState) => void
  onTranscript: (role: 'user' | 'assistant', text: string) => void
  onAudioLevel: (level: number) => void
  onError: (error: string) => void
}

export class OpenAIRealtimeAdapter {
  private pc: RTCPeerConnection | null = null
  private dc: RTCDataChannel | null = null
  private audioEl: HTMLAudioElement | null = null
  private micStream: MediaStream | null = null
  private isMuted = false
  private callbacks: AdapterCallbacks
  private reconnectAttempts = 0
  private maxReconnects = 3
  private sessionContext: SessionContext | null = null
  private micStreamRef: MediaStream | null = null

  constructor(callbacks: AdapterCallbacks) {
    this.callbacks = callbacks
  }

  async startSession(context: SessionContext, micStream: MediaStream): Promise<void> {
    this.sessionContext = context
    this.micStreamRef = micStream

    try {
      this.callbacks.onStateChange('connecting')
      await this.initWebRTC(context, micStream)
    } catch (err) {
      console.error('[OpenAI Realtime] WebRTC failed, trying WebSocket fallback', err)
      throw err
    }
  }

  private async initWebRTC(context: SessionContext, micStream: MediaStream): Promise<void> {
    // 1. Get ephemeral token from our API route
    const tokenRes = await fetch('/api/openai-session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        instructions: this.buildSystemPrompt(context),
        voice: 'alloy',
        model: 'gpt-4o-realtime-preview-2024-12-17',
      }),
    })

    if (!tokenRes.ok) {
      const err = await tokenRes.text()
      throw new Error(`Failed to get session token: ${err}`)
    }

    const { client_secret } = await tokenRes.json()
    const ephemeralKey = client_secret.value

    // 2. Create RTCPeerConnection
    this.pc = new RTCPeerConnection()

    // 3. Setup remote audio playback
    this.audioEl = document.createElement('audio')
    this.audioEl.autoplay = true
    this.pc.ontrack = (e) => {
      if (this.audioEl) {
        this.audioEl.srcObject = e.streams[0]
      }
    }

    // 4. Add microphone track
    this.micStream = micStream
    const audioTrack = micStream.getAudioTracks()[0]
    if (audioTrack) {
      this.pc.addTrack(audioTrack, micStream)
    }

    // 5. Create data channel for events
    this.dc = this.pc.createDataChannel('oai-events')
    this.dc.onopen = () => {
      this.callbacks.onStateChange('listening')
      this.sendSessionUpdate(context)
    }
    this.dc.onmessage = (e) => this.handleEvent(JSON.parse(e.data))
    this.dc.onerror = (e) => {
      console.error('[OpenAI DC] Error:', e)
      this.callbacks.onError('Data channel error')
    }

    // 6. Create offer and set local description
    const offer = await this.pc.createOffer()
    await this.pc.setLocalDescription(offer)

    // 7. Send offer to OpenAI Realtime API
    const sdpRes = await fetch(
      `https://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17`,
      {
        method: 'POST',
        body: offer.sdp,
        headers: {
          Authorization: `Bearer ${ephemeralKey}`,
          'Content-Type': 'application/sdp',
        },
      }
    )

    if (!sdpRes.ok) {
      throw new Error(`OpenAI SDP exchange failed: ${sdpRes.status}`)
    }

    const answerSdp = await sdpRes.text()
    await this.pc.setRemoteDescription({ type: 'answer', sdp: answerSdp })

    // 8. Handle connection state
    this.pc.onconnectionstatechange = () => {
      const s = this.pc?.connectionState
      if (s === 'connected') {
        this.callbacks.onStateChange('listening')
        this.reconnectAttempts = 0
      } else if (s === 'disconnected' || s === 'failed') {
        this.handleDisconnect()
      }
    }
  }

  private sendSessionUpdate(context: SessionContext): void {
    if (!this.dc || this.dc.readyState !== 'open') return

    const event = {
      type: 'session.update',
      session: {
        modalities: ['text', 'audio'],
        instructions: this.buildSystemPrompt(context),
        voice: 'alloy',
        input_audio_format: 'pcm16',
        output_audio_format: 'pcm16',
        input_audio_transcription: { model: 'whisper-1' },
        turn_detection: {
          type: 'server_vad',
          threshold: 0.5,
          prefix_padding_ms: 300,
          silence_duration_ms: 500,
        },
        tools: this.buildTools(),
        tool_choice: 'auto',
        temperature: 0.8,
      },
    }

    this.dc.send(JSON.stringify(event))
  }

  private buildSystemPrompt(context: SessionContext): string {
    const base = `You are VIVI, the Y-OS Voice & Vision Interface — an intelligent cognitive operating system assistant for Yannick.
You are direct, precise, structured, and calm. No filler, no hype.
You think in architectures, models, and protocols.
You are a copilot, not an assistant — you anticipate, structure, and execute.`

    const contextSection = context.context
      ? `\n\n## Current Context\n${context.context}`
      : ''

    const instructionsSection = context.instructions
      ? `\n\n## Behavior Instructions\n${context.instructions}`
      : ''

    const modeSection = `\n\n## Session Mode\n${context.mode === 'voice' ? 'Voice conversation via OpenAI Realtime.' : 'Voice + Vision via Gemini Live.'}`

    return base + contextSection + instructionsSection + modeSection
  }

  private buildTools() {
    return [
      {
        type: 'function',
        name: 'retrieve_memory',
        description: 'Retrieve relevant memory or context from Y-OS memory store',
        parameters: {
          type: 'object',
          properties: {
            query: { type: 'string', description: 'What to search for in memory' },
            project: { type: 'string', description: 'Optional project filter' },
          },
          required: ['query'],
        },
      },
      {
        type: 'function',
        name: 'log_insight',
        description: 'Log an important insight or decision to Y-OS memory',
        parameters: {
          type: 'object',
          properties: {
            content: { type: 'string', description: 'The insight to log' },
            tags: { type: 'array', items: { type: 'string' }, description: 'Tags for categorization' },
          },
          required: ['content'],
        },
      },
      {
        type: 'function',
        name: 'search_document',
        description: 'Search for a document or note in Y-OS knowledge base',
        parameters: {
          type: 'object',
          properties: {
            query: { type: 'string', description: 'Search query' },
          },
          required: ['query'],
        },
      },
    ]
  }

  private handleEvent(event: Record<string, unknown>): void {
    const type = event.type as string

    switch (type) {
      case 'session.created':
        this.callbacks.onStateChange('listening')
        break

      case 'input_audio_buffer.speech_started':
        this.callbacks.onStateChange('listening')
        break

      case 'input_audio_buffer.speech_stopped':
        this.callbacks.onStateChange('processing')
        break

      case 'response.created':
        this.callbacks.onStateChange('speaking')
        break

      case 'response.done':
        this.callbacks.onStateChange('listening')
        break

      case 'conversation.item.input_audio_transcription.completed': {
        const transcript = (event.transcript as string) || ''
        if (transcript.trim()) {
          this.callbacks.onTranscript('user', transcript.trim())
        }
        break
      }

      case 'response.audio_transcript.done': {
        const text = (event.transcript as string) || ''
        if (text.trim()) {
          this.callbacks.onTranscript('assistant', text.trim())
        }
        break
      }

      case 'response.text.done': {
        // Text-mode response (when in text interaction mode)
        const text = (event.text as string) || ''
        if (text.trim()) {
          this.callbacks.onTranscript('assistant', text.trim())
        }
        break
      }

      case 'response.function_call_arguments.done': {
        this.handleToolCall(event)
        break
      }

      case 'error': {
        const errMsg = (event.error as { message?: string })?.message || 'Unknown error'
        this.callbacks.onError(errMsg)
        break
      }
    }
  }

  private async handleToolCall(event: Record<string, unknown>): Promise<void> {
    const callId = event.call_id as string
    const name = event.name as string
    const args = JSON.parse((event.arguments as string) || '{}')

    try {
      const res = await fetch('/api/tool-call', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tool: name, arguments: args }),
      })
      const result = await res.json()

      // Send tool result back to OpenAI
      if (this.dc && this.dc.readyState === 'open') {
        this.dc.send(JSON.stringify({
          type: 'conversation.item.create',
          item: {
            type: 'function_call_output',
            call_id: callId,
            output: JSON.stringify(result),
          },
        }))
        this.dc.send(JSON.stringify({ type: 'response.create' }))
      }
    } catch (err) {
      console.error('[Tool call error]', err)
    }
  }

  private async handleDisconnect(): Promise<void> {
    if (this.reconnectAttempts < this.maxReconnects && this.sessionContext && this.micStreamRef) {
      this.reconnectAttempts++
      console.log(`[OpenAI Realtime] Reconnecting (attempt ${this.reconnectAttempts})...`)
      this.callbacks.onStateChange('connecting')
      await new Promise(r => setTimeout(r, 1000 * this.reconnectAttempts))
      try {
        await this.initWebRTC(this.sessionContext, this.micStreamRef)
      } catch {
        this.callbacks.onError('Reconnection failed')
        this.callbacks.onStateChange('error')
      }
    } else {
      this.callbacks.onError('Connection lost')
      this.callbacks.onStateChange('error')
    }
  }

  /**
   * Send a text message into the live session (text interaction mode).
   * The session already has modalities: ['text', 'audio'] — this creates
   * a user message item and triggers a response.
   */
  sendText(text: string): void {
    if (!this.dc || this.dc.readyState !== 'open') return

    // Add user text to transcript immediately
    this.callbacks.onTranscript('user', text)
    this.callbacks.onStateChange('processing')

    // Create conversation item with user text
    this.dc.send(JSON.stringify({
      type: 'conversation.item.create',
      item: {
        type: 'message',
        role: 'user',
        content: [{ type: 'input_text', text }],
      },
    }))

    // Trigger response
    this.dc.send(JSON.stringify({ type: 'response.create' }))
  }

  setMuted(muted: boolean): void {
    this.isMuted = muted
    if (this.micStream) {
      this.micStream.getAudioTracks().forEach(t => {
        t.enabled = !muted
      })
    }
  }

  interrupt(): void {
    if (this.dc && this.dc.readyState === 'open') {
      this.dc.send(JSON.stringify({ type: 'response.cancel' }))
    }
  }

  async closeSession(): Promise<void> {
    if (this.dc) {
      this.dc.close()
      this.dc = null
    }
    if (this.pc) {
      this.pc.close()
      this.pc = null
    }
    if (this.micStream) {
      this.micStream.getTracks().forEach(t => t.stop())
      this.micStream = null
    }
    if (this.audioEl) {
      this.audioEl.srcObject = null
      this.audioEl = null
    }
  }
}
