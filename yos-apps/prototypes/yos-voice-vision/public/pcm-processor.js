/**
 * PCM16 AudioWorklet Processor
 * Replaces deprecated ScriptProcessorNode for iOS Safari compatibility.
 * Runs in the AudioWorklet thread — converts Float32 to PCM16 and posts to main thread.
 */
class PCM16Processor extends AudioWorkletProcessor {
  constructor() {
    super()
    this._buffer = []
    this._chunkSize = 2048
  }

  process(inputs) {
    const input = inputs[0]
    if (!input || !input[0]) return true

    const channelData = input[0]

    // Accumulate samples
    for (let i = 0; i < channelData.length; i++) {
      this._buffer.push(channelData[i])
    }

    // When we have enough samples, convert and send
    while (this._buffer.length >= this._chunkSize) {
      const chunk = this._buffer.splice(0, this._chunkSize)
      const pcm16 = new Int16Array(chunk.length)

      for (let i = 0; i < chunk.length; i++) {
        const clamped = Math.max(-1, Math.min(1, chunk[i]))
        pcm16[i] = clamped < 0 ? clamped * 32768 : clamped * 32767
      }

      // Compute audio level
      let sum = 0
      for (let i = 0; i < chunk.length; i++) sum += Math.abs(chunk[i])
      const level = sum / chunk.length

      this.port.postMessage({
        pcm16: pcm16.buffer,
        level,
      }, [pcm16.buffer])
    }

    return true
  }
}

registerProcessor('pcm16-processor', PCM16Processor)
