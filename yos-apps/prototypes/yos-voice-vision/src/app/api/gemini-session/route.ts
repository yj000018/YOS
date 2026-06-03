import { NextResponse } from 'next/server'

export async function GET() {
  const apiKey = process.env.GEMINI_API_KEY
  if (!apiKey) {
    return NextResponse.json({ error: 'Gemini API key not configured' }, { status: 500 })
  }

  // Return the API key for client-side WebSocket connection
  // In production, consider using a short-lived token mechanism
  return NextResponse.json({ apiKey })
}
