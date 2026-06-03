/**
 * Gemini Live API Adapter — iOS-compatible
 *
 * Changes vs previous version:
 * 1. ScriptProcessorNode replaced by AudioWorklet (pcm-processor.js)
 *    with ScriptProcessor as fallback for browsers that don't support AudioWorklet
 * 2. AudioContext created without sampleRate constraint (iOS Safari rejects it)
 *    — resampling handled in the worklet
 * 3. audioContext.resume() called after creation (iOS autoplay policy)
 * 4. Correct outbound format: realtimeInput.audio with base64 PCM16
 * 5. Output audio uses Web Audio API decodeAudioData with error recovery
 * 6. Video frame capture waits for readyState >= 2
 */

import type { SessionContext, SessionState } from '@/types'

interface AdapterCallbacks {
  onStateChange: (state: SessionState) => void
  onTranscript: (role: 'user' | 'assistant', text: string) => void
  onAudioLevel: (level: number) => void
  onError: (error: string) => void
}

export class GeminiLiveAdapter {
  private ws: WebSocket | null = null
  private audioContext: AudioContext | null = null
  private workletNode: AudioWorkletNode | null = null
  private scriptProcessor: ScriptProcessorNode | null = null
  private micSource: MediaStreamAudioSourceNode | null = null
  private micStream: MediaStream | null = null
  private videoStream: MediaStream | null = null
  private videoCanvas: HTMLCanvasElement | null = null
  private videoCtx: CanvasRenderingContext2D | null = null
  private videoEl: HTMLVideoElement | null = null
  private videoFrameTimer: ReturnType<typeof setInterval> | null = null
  private outputAudioContext: AudioContext | null = null
  private audioQueue: ArrayBuffer[] = []
  private isPlaying = false
  private isMuted = false
  private callbacks: AdapterCallbacks
  private sessionContext: SessionContext | null = null
  private reconnectAttempts = 0
  private maxReconnects = 3
  private setupComplete = false

  constructor(callbacks: AdapterCallbacks) {
    this.callbacks = callbacks
  }

  async startSession(
    context: SessionContext,
    micStream: MediaStream,
    videoStream?: MediaStream
  ): Promise<void> {
    this.sessionContext = context
    this.micStream = micStream
    this.videoStream = videoStream || null

    this.callbacks.onStateChange('connecting')
    await this.connectWebSocket(context)
  }

  private async connectWebSocket(context: SessionContext): Promise<void> {
    const apiKey = await this.getApiKey()

    const wsUrl = `wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key=${apiKey}`

    this.ws = new WebSocket(wsUrl)
    this.ws.binaryType = 'arraybuffer'

    this.ws.onopen = () => {
      this.sendSetupMessage(context)
    }

    this.ws.onmessage = (e) => this.handleMessage(e)

    this.ws.onerror = (e) => {
      console.error('[Gemini Live] WebSocket error:', e)
      this.callbacks.onError('WebSocket connection error')
    }

    this.ws.onclose = (e) => {
      console.log('[Gemini Live] WebSocket closed:', e.code, e.reason)
      if (e.code !== 1000 && this.reconnectAttempts < this.maxReconnects) {
        this.handleDisconnect()
      }
    }
  }

  private async getApiKey(): Promise<string> {
    const res = await fetch('/api/gemini-session', { method: 'GET' })
    if (!res.ok) throw new Error('Failed to get Gemini API key')
    const { apiKey } = await res.json()
    return apiKey
  }

  private sendSetupMessage(context: SessionContext): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return

    const setup = {
      setup: {
        model: 'models/gemini-2.5-flash-native-audio-latest',
        generationConfig: {
          responseModalities: ['AUDIO'],
          speechConfig: {
            voiceConfig: {
              prebuiltVoiceConfig: {
                voiceName: 'Aoede',
              },
            },
          },
        },
        systemInstruction: {
          parts: [{ text: this.buildSystemPrompt(context) }],
        },
        tools: this.buildTools(),
      },
    }

    this.ws.send(JSON.stringify(setup))
  }

  private buildSystemPrompt(context: SessionContext): string {
    const base = `You are VIVI, the Y-OS Voice & Vision Interface — an intelligent cognitive operating system assistant for Yannick.
You are direct, precise, structured, and calm. No filler, no hype.
You are a copilot with vision — you can see the environment through the camera when in vision mode.
When describing what you see, be concise and actionable.
For CasaTAO (the user's home), you can identify objects, spaces, and suggest actions.`

    const contextSection = context.context
      ? `\n\nCurrent Context:\n${context.context}`
      : ''

    const instructionsSection = context.instructions
      ? `\n\nBehavior Instructions:\n${context.instructions}`
      : ''

    return base + contextSection + instructionsSection
  }

  private buildTools() {
    return [
      {
        functionDeclarations: [
          {
            name: 'retrieve_memory',
            description: 'Retrieve relevant memory from Y-OS memory store',
            parameters: {
              type: 'OBJECT',
              properties: {
                query: { type: 'STRING', description: 'What to search for' },
              },
              required: ['query'],
            },
          },
          {
            name: 'log_insight',
            description: 'Log an insight to Y-OS memory',
            parameters: {
              type: 'OBJECT',
              properties: {
                content: { type: 'STRING', description: 'The insight to log' },
              },
              required: ['content'],
            },
          },
          {
            name: 'control_iot',
            description: 'Control a CasaTAO IoT device or scene',
            parameters: {
              type: 'OBJECT',
              properties: {
                device: { type: 'STRING', description: 'Device or scene name' },
                action: { type: 'STRING', description: 'Action to perform' },
                value: { type: 'STRING', description: 'Optional value' },
              },
              required: ['device', 'action'],
            },
          },
        ],
      },
    ]
  }

  private handleMessage(e: MessageEvent): void {
    try {
      let data: Record<string, unknown>

      if (typeof e.data === 'string') {
        data = JSON.parse(e.data)
      } else {
        this.playAudioChunk(e.data as ArrayBuffer)
        return
      }

      if (data.setupComplete) {
        console.log('[Gemini Live] Setup complete, starting mic capture')
        this.setupComplete = true
        this.callbacks.onStateChange('listening')
        this.startMicCapture()
        if (this.videoStream) {
          this.startVideoCapture()
        }
        return
      }

      if (data.serverContent) {
        const sc = data.serverContent as Record<string, unknown>

        if (sc.turnComplete) {
          this.callbacks.onStateChange('listening')
        }

        if (sc.modelTurn) {
          const parts = (sc.modelTurn as Record<string, unknown>).parts as Array<Record<string, unknown>>
          if (parts) {
            for (const part of parts) {
              if (part.text) {
                this.callbacks.onTranscript('assistant', part.text as string)
              }
              if (part.inlineData) {
                const audio = part.inlineData as Record<string, unknown>
                if (typeof audio.mimeType === 'string' && audio.mimeType.startsWith('audio/')) {
                  const raw = atob(audio.data as string)
                  const buf = new ArrayBuffer(raw.length)
                  const view = new Uint8Array(buf)
                  for (let i = 0; i < raw.length; i++) view[i] = raw.charCodeAt(i)
                  this.playAudioChunk(buf)
                  this.callbacks.onStateChange('speaking')
                }
              }
            }
          }
        }

        if (sc.inputTranscription) {
          const t = sc.inputTranscription as Record<string, unknown>
          if (t.text) {
            this.callbacks.onTranscript('user', t.text as string)
          }
        }
      }

      if (data.toolCall) {
        this.handleToolCall(data.toolCall as Record<string, unknown>)
      }

    } catch (err) {
      console.error('[Gemini Live] Message parse error:', err)
    }
  }

  private async startMicCapture(): Promise<void> {
    if (!this.micStream) {
      console.error('[Gemini Live] No mic stream available')
      return
    }

    try {
      // iOS Safari: do NOT pass sampleRate — let the browser decide
      // We'll handle resampling in the worklet/processor
      const AudioContextClass = window.AudioContext ||
        (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext
      this.audioContext = new AudioContextClass()

      // iOS requires resume() from user gesture context — should already be unlocked
      if (this.audioContext.state === 'suspended') {
        await this.audioContext.resume()
      }

      this.micSource = this.audioContext.createMediaStreamSource(this.micStream)

      // Try AudioWorklet first (modern browsers + iOS 14.5+)
      const useWorklet = typeof AudioWorkletNode !== 'undefined'

      if (useWorklet) {
        try {
          await this.audioContext.audioWorklet.addModule('/pcm-processor.js')
          this.workletNode = new AudioWorkletNode(this.audioContext, 'pcm16-processor')

          this.workletNode.port.onmessage = (e) => {
            if (this.isMuted || !this.ws || this.ws.readyState !== WebSocket.OPEN) return

            const { pcm16, level } = e.data as { pcm16: ArrayBuffer; level: number }
            this.callbacks.onAudioLevel(Math.min(level * 4, 1))

            const message = {
              realtimeInput: {
                audio: {
                  data: this.arrayBufferToBase64(pcm16),
                  mimeType: 'audio/pcm;rate=16000',
                },
              },
            }

            try {
              this.ws!.send(JSON.stringify(message))
            } catch (sendErr) {
              console.error('[Gemini Live] Audio send error:', sendErr)
            }
          }

          this.micSource.connect(this.workletNode)
          // Connect to silent gain to keep graph alive without echo
          const silentGain = this.audioContext.createGain()
          silentGain.gain.value = 0
          this.workletNode.connect(silentGain)
          silentGain.connect(this.audioContext.destination)

          console.log('[Gemini Live] AudioWorklet mic capture started')
          return
        } catch (workletErr) {
          console.warn('[Gemini Live] AudioWorklet failed, falling back to ScriptProcessor:', workletErr)
        }
      }

      // Fallback: ScriptProcessorNode (deprecated but still works on older iOS)
      const CHUNK_SIZE = 2048
      this.scriptProcessor = this.audioContext.createScriptProcessor(CHUNK_SIZE, 1, 1)

      this.scriptProcessor.onaudioprocess = (e) => {
        if (this.isMuted || !this.ws || this.ws.readyState !== WebSocket.OPEN) return

        const inputData = e.inputBuffer.getChannelData(0)

        let sum = 0
        for (let i = 0; i < inputData.length; i++) sum += Math.abs(inputData[i])
        this.callbacks.onAudioLevel(Math.min((sum / inputData.length) * 4, 1))

        const pcm16 = this.float32ToPCM16(inputData)

        const message = {
          realtimeInput: {
            audio: {
              data: this.arrayBufferToBase64(pcm16.buffer as ArrayBuffer),
              mimeType: 'audio/pcm;rate=16000',
            },
          },
        }

        try {
          this.ws!.send(JSON.stringify(message))
        } catch (sendErr) {
          console.error('[Gemini Live] Audio send error:', sendErr)
        }
      }

      this.micSource.connect(this.scriptProcessor)
      const silentGain = this.audioContext.createGain()
      silentGain.gain.value = 0
      this.scriptProcessor.connect(silentGain)
      silentGain.connect(this.audioContext.destination)

      console.log('[Gemini Live] ScriptProcessor mic capture started (fallback)')

    } catch (err) {
      console.error('[Gemini Live] Mic capture error:', err)
      this.callbacks.onError('Microphone capture failed')
    }
  }

  private startVideoCapture(): void {
    if (!this.videoStream) return

    this.videoCanvas = document.createElement('canvas')
    this.videoCanvas.width = 640
    this.videoCanvas.height = 480
    this.videoCtx = this.videoCanvas.getContext('2d')

    this.videoEl = document.createElement('video')
    this.videoEl.srcObject = this.videoStream
    this.videoEl.autoplay = true
    this.videoEl.muted = true
    this.videoEl.playsInline = true  // Required for iOS

    this.videoEl.onloadeddata = () => {
      this.videoFrameTimer = setInterval(() => {
        this.sendVideoFrame()
      }, 1000)
    }

    this.videoEl.play().catch(err => {
      console.warn('[Gemini Live] Video play error:', err)
    })
  }

  private sendVideoFrame(): void {
    if (
      !this.videoCanvas ||
      !this.videoCtx ||
      !this.videoEl ||
      !this.ws ||
      this.ws.readyState !== WebSocket.OPEN ||
      this.videoEl.readyState < 2
    ) return

    try {
      this.videoCtx.drawImage(this.videoEl, 0, 0, 640, 480)
      const dataUrl = this.videoCanvas.toDataURL('image/jpeg', 0.7)
      const base64 = dataUrl.split(',')[1]

      const message = {
        realtimeInput: {
          video: {
            data: base64,
            mimeType: 'image/jpeg',
          },
        },
      }
      this.ws.send(JSON.stringify(message))
    } catch (err) {
      console.error('[Gemini Live] Video frame error:', err)
    }
  }

  private async playAudioChunk(buffer: ArrayBuffer): Promise<void> {
    this.audioQueue.push(buffer)
    if (!this.isPlaying) {
      await this.drainAudioQueue()
    }
  }

  private async drainAudioQueue(): Promise<void> {
    if (this.audioQueue.length === 0) {
      this.isPlaying = false
      return
    }

    this.isPlaying = true

    try {
      if (!this.outputAudioContext) {
        const AudioContextClass = window.AudioContext ||
          (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext
        this.outputAudioContext = new AudioContextClass()
      }

      // iOS: resume if suspended
      if (this.outputAudioContext.state === 'suspended') {
        await this.outputAudioContext.resume()
      }

      const buffer = this.audioQueue.shift()!
      const audioBuffer = await this.outputAudioContext.decodeAudioData(buffer.slice(0))
      const source = this.outputAudioContext.createBufferSource()
      source.buffer = audioBuffer
      source.connect(this.outputAudioContext.destination)
      source.onended = () => this.drainAudioQueue()
      source.start()
    } catch {
      // Try next chunk on decode error
      this.drainAudioQueue()
    }
  }

  private async handleToolCall(toolCall: Record<string, unknown>): Promise<void> {
    const calls = toolCall.functionCalls as Array<Record<string, unknown>>
    if (!calls) return

    for (const call of calls) {
      const name = call.name as string
      const args = call.args as Record<string, unknown>
      const callId = call.id as string

      try {
        const res = await fetch('/api/tool-call', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ tool: name, arguments: args }),
        })
        const result = await res.json()

        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(JSON.stringify({
            toolResponse: {
              functionResponses: [{
                id: callId,
                name,
                response: { output: result },
              }],
            },
          }))
        }
      } catch (err) {
        console.error('[Gemini Live] Tool call error:', err)
      }
    }
  }

  private async handleDisconnect(): Promise<void> {
    if (this.reconnectAttempts < this.maxReconnects && this.sessionContext) {
      this.reconnectAttempts++
      console.log(`[Gemini Live] Reconnecting (attempt ${this.reconnectAttempts})...`)
      this.callbacks.onStateChange('connecting')
      await new Promise(r => setTimeout(r, 1000 * this.reconnectAttempts))
      try {
        await this.connectWebSocket(this.sessionContext)
      } catch {
        this.callbacks.onError('Reconnection failed')
        this.callbacks.onStateChange('error')
      }
    } else {
      this.callbacks.onError('Connection lost')
      this.callbacks.onStateChange('error')
    }
  }

  private float32ToPCM16(float32Array: Float32Array): Int16Array {
    const pcm16 = new Int16Array(float32Array.length)
    for (let i = 0; i < float32Array.length; i++) {
      const clamped = Math.max(-1, Math.min(1, float32Array[i]))
      pcm16[i] = clamped < 0 ? clamped * 32768 : clamped * 32767
    }
    return pcm16
  }

  private arrayBufferToBase64(buffer: ArrayBuffer): string {
    const bytes = new Uint8Array(buffer)
    let binary = ''
    for (let i = 0; i < bytes.byteLength; i++) {
      binary += String.fromCharCode(bytes[i])
    }
    return btoa(binary)
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
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ clientContent: { turnComplete: true } }))
    }
  }

  async closeSession(): Promise<void> {
    if (this.videoFrameTimer) {
      clearInterval(this.videoFrameTimer)
      this.videoFrameTimer = null
    }

    if (this.workletNode) {
      this.workletNode.disconnect()
      this.workletNode = null
    }
    if (this.scriptProcessor) {
      this.scriptProcessor.disconnect()
      this.scriptProcessor = null
    }
    if (this.micSource) {
      this.micSource.disconnect()
      this.micSource = null
    }
    if (this.audioContext) {
      await this.audioContext.close()
      this.audioContext = null
    }
    if (this.outputAudioContext) {
      await this.outputAudioContext.close()
      this.outputAudioContext = null
    }

    if (this.micStream) {
      this.micStream.getTracks().forEach(t => t.stop())
      this.micStream = null
    }
    if (this.videoStream) {
      this.videoStream.getTracks().forEach(t => t.stop())
      this.videoStream = null
    }

    if (this.ws) {
      this.ws.close(1000, 'Session ended')
      this.ws = null
    }

    this.audioQueue = []
    this.isPlaying = false
    this.setupComplete = false
  }
}
