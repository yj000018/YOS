// ============================================================
// Y-OS Voice & Vision — Core Types
// ============================================================

// Session state machine
export type SessionState =
  | 'idle'
  | 'connecting'
  | 'listening'
  | 'processing'
  | 'speaking'
  | 'error'
  | 'ended'

// Provider modes
export type VoiceMode = 'voice' | 'voice_vision'

// Provider identity
export type ProviderType = 'openai_realtime' | 'gemini_live'

// ============================================================
// Voice Provider Interface (abstraction layer)
// ============================================================
export interface VoiceProvider {
  startSession(context: SessionContext): Promise<void>
  sendAudio(chunk: ArrayBuffer): void
  receiveAudio(): void
  receiveTranscript(): void
  interrupt(): void
  callTool(tool: string, payload: Record<string, unknown>): Promise<unknown>
  closeSession(): Promise<void>
}

// ============================================================
// Session Context (injected before session start)
// ============================================================
export interface SessionContext {
  mode: VoiceMode
  userIntent?: string
  project?: string
  context: string        // condensed memory
  instructions: string   // behavior hints
  timestamp: string
}

// ============================================================
// Transcript & Events
// ============================================================
export interface TranscriptEntry {
  id: string
  role: 'user' | 'assistant'
  text: string
  timestamp: number
  audioStart?: number
  audioEnd?: number
}

export interface SessionEvent {
  type: 'tool_call' | 'interrupt' | 'error' | 'state_change' | 'vision_frame'
  timestamp: number
  data: Record<string, unknown>
}

// ============================================================
// Session Document (post-session synthesis)
// ============================================================
export interface SessionDocument {
  id: string
  mode: VoiceMode
  provider: ProviderType
  startedAt: string
  endedAt: string
  duration: number // seconds
  transcript: TranscriptEntry[]
  events: SessionEvent[]
  synthesis: {
    executiveSummary: string
    keyInsights: string[]
    decisions: string[]
    actions: string[]
    openQuestions: string[]
    memoryDelta: string
    contextToReinject: string
  }
}

// ============================================================
// Context Builder Request/Response
// ============================================================
export interface ContextRequest {
  type: 'context_request'
  mode: VoiceMode
  userIntent?: string
  project?: string
}

export interface ContextResponse {
  context: string
  instructions: string
}

// ============================================================
// OpenAI Realtime
// ============================================================
export interface OpenAIRealtimeConfig {
  model: string
  voice: string
  instructions: string
  tools?: OpenAITool[]
  temperature?: number
  input_audio_format?: 'pcm16' | 'g711_ulaw' | 'g711_alaw'
  output_audio_format?: 'pcm16' | 'g711_ulaw' | 'g711_alaw'
  turn_detection?: {
    type: 'server_vad'
    threshold?: number
    prefix_padding_ms?: number
    silence_duration_ms?: number
  }
}

export interface OpenAITool {
  type: 'function'
  name: string
  description: string
  parameters: Record<string, unknown>
}

// ============================================================
// Gemini Live
// ============================================================
export interface GeminiLiveConfig {
  model: string
  systemInstruction: string
  tools?: GeminiTool[]
  generationConfig?: {
    responseModalities: string[]
    speechConfig?: {
      voiceConfig: {
        prebuiltVoiceConfig: {
          voiceName: string
        }
      }
    }
  }
}

export interface GeminiTool {
  functionDeclarations: {
    name: string
    description: string
    parameters: Record<string, unknown>
  }[]
}

// ============================================================
// Tool Calling (Manus Integration)
// ============================================================
export interface ToolCall {
  id: string
  name: string
  arguments: Record<string, unknown>
}

export interface ToolResult {
  id: string
  result: unknown
  error?: string
}

// ============================================================
// UI State
// ============================================================
export interface UIState {
  sessionState: SessionState
  mode: VoiceMode | null
  provider: ProviderType | null
  isMuted: boolean
  cameraEnabled: boolean
  transcript: TranscriptEntry[]
  currentSpeaker: 'user' | 'assistant' | null
  error: string | null
  sessionId: string | null
  sessionStartTime: number | null
}
