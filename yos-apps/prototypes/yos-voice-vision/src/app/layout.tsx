import type { Metadata, Viewport } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'VIVI — Y-OS Voice & Vision Interface',
  description: 'VIVI — Y-OS Voice & Vision Interface. Real-time voice and vision powered by OpenAI Realtime and Gemini Live.',
  manifest: '/manifest.json',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'black-translucent',
    title: 'VIVI',
    // Startup images for common iPhone sizes
    startupImage: [
      {
        url: '/splash/splash-2796x1290.png',
        media: '(device-width: 430px) and (device-height: 932px) and (-webkit-device-pixel-ratio: 3)',
      },
      {
        url: '/splash/splash-2556x1179.png',
        media: '(device-width: 393px) and (device-height: 852px) and (-webkit-device-pixel-ratio: 3)',
      },
      {
        url: '/splash/splash-2532x1170.png',
        media: '(device-width: 390px) and (device-height: 844px) and (-webkit-device-pixel-ratio: 3)',
      },
      {
        url: '/splash/splash-2340x1080.png',
        media: '(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3)',
      },
    ],
  },
  other: {
    // iOS Safari: allow microphone access in PWA mode
    'apple-mobile-web-app-capable': 'yes',
    // Prevent iOS from detecting phone numbers as links
    'format-detection': 'telephone=no',
  },
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: '#05060f',
  // iOS: prevent bounce/overscroll
  viewportFit: 'cover',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <head>
        {/* iOS PWA: prevent tap highlight */}
        <meta name="mobile-web-app-capable" content="yes" />
        {/* iOS: full-screen status bar */}
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
        {/* Preconnect to API providers for lower latency */}
        <link rel="preconnect" href="https://api.openai.com" />
        <link rel="preconnect" href="https://generativelanguage.googleapis.com" />
      </head>
      <body
        className="bg-yos-bg text-yos-text antialiased noise-overlay"
        style={{
          // iOS Safari: prevent rubber-band scroll, enable safe area insets
          overscrollBehavior: 'none',
          paddingTop: 'env(safe-area-inset-top)',
          paddingBottom: 'env(safe-area-inset-bottom)',
        }}
      >
        {children}
      </body>
    </html>
  )
}
