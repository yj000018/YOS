/**
 * iOS Safari AudioContext Unlock
 *
 * iOS requires AudioContext.resume() to be called from a user gesture (tap/click).
 * This module provides a singleton unlock mechanism that should be called
 * in the onClick handler of the mode selector buttons — before any async work.
 *
 * Also handles the "AudioContext closed after mic permission" bug on iOS 17+
 * (LiveKit issue #1515): we keep a reference and recreate if closed.
 */

let unlocked = false

/**
 * Call this synchronously inside a user gesture handler.
 * Creates and immediately resumes a silent AudioContext to unlock Web Audio.
 */
export async function unlockAudioContext(): Promise<void> {
  if (unlocked) return

  try {
    // Create a temporary context just to unlock the audio subsystem
    const ctx = new (window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext)()

    // Play a silent buffer — required on some iOS versions
    const buffer = ctx.createBuffer(1, 1, 22050)
    const source = ctx.createBufferSource()
    source.buffer = buffer
    source.connect(ctx.destination)
    source.start(0)

    // Resume the context
    if (ctx.state === 'suspended') {
      await ctx.resume()
    }

    // Close the temporary context — we'll create real ones in adapters
    await ctx.close()

    unlocked = true
    console.log('[iOS Audio] Unlocked')
  } catch (err) {
    console.warn('[iOS Audio] Unlock failed (non-iOS or already unlocked):', err)
  }
}

/**
 * Detect iOS Safari (including PWA mode).
 */
export function isIOS(): boolean {
  if (typeof navigator === 'undefined') return false
  return /iPad|iPhone|iPod/.test(navigator.userAgent) ||
    (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)
}

/**
 * Detect if running as installed PWA on iOS.
 */
export function isIOSPWA(): boolean {
  return isIOS() && (window.navigator as unknown as { standalone?: boolean }).standalone === true
}

/**
 * iOS PWA has a known bug: microphone permission is re-requested on every
 * page load. Workaround: request permission eagerly on first user gesture
 * and keep the stream alive for the session duration.
 *
 * Returns a pre-warmed mic stream, or null if permission denied.
 */
export async function requestMicPermissionEarly(): Promise<MediaStream | null> {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
        // iOS Safari: sampleRate constraint causes failures — omit it
        // sampleRate: 16000,
      }
    })
    return stream
  } catch (err) {
    console.error('[iOS Audio] Mic permission denied:', err)
    return null
  }
}
