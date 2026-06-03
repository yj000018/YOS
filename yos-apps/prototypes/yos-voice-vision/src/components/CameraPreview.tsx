'use client'

import { useEffect, useRef } from 'react'

interface CameraPreviewProps {
  stream: MediaStream | null
  visible: boolean
}

export default function CameraPreview({ stream, visible }: CameraPreviewProps) {
  const videoRef = useRef<HTMLVideoElement>(null)

  useEffect(() => {
    if (videoRef.current && stream) {
      videoRef.current.srcObject = stream
    }
  }, [stream])

  if (!visible || !stream) return null

  return (
    <div className="relative rounded-2xl overflow-hidden w-full max-w-[200px] mx-auto animate-fade-in">
      <video
        ref={videoRef}
        autoPlay
        muted
        playsInline
        className="w-full h-auto rounded-2xl"
        style={{ transform: 'scaleX(-1)' }} // Mirror for selfie view
      />
      <div className="absolute top-2 right-2 flex items-center gap-1.5 bg-black/60 rounded-full px-2 py-1">
        <div className="w-1.5 h-1.5 rounded-full bg-yos-vision animate-pulse" />
        <span className="text-[9px] font-mono text-yos-vision">LIVE</span>
      </div>
      <div className="absolute inset-0 rounded-2xl border border-yos-vision/20 pointer-events-none" />
    </div>
  )
}
