import { NextRequest, NextResponse } from 'next/server'
import { Client } from '@notionhq/client'
import type { BlockObjectRequest } from '@notionhq/client/build/src/api-endpoints'

const notion = new Client({ auth: process.env.NOTION_API_KEY })

interface TranscriptEntry {
  id: string
  role: 'user' | 'assistant'
  text: string
  timestamp: number
}

interface SessionLogRequest {
  sessionId: string
  mode: string
  provider: string
  transcript: TranscriptEntry[]
  startedAt: string
  endedAt: string
  duration: number
}

interface SessionSynthesis {
  executiveSummary: string
  keyInsights: string[]
  decisions: string[]
  actions: string[]
  openQuestions: string[]
  memoryDelta: string
}

async function synthesizeSession(data: SessionLogRequest): Promise<SessionSynthesis> {
  const apiKey = process.env.OPENAI_API_KEY
  if (!apiKey || data.transcript.length === 0) {
    return {
      executiveSummary: `${data.mode} session — ${data.duration}s — ${data.transcript.length} exchanges`,
      keyInsights: [],
      decisions: [],
      actions: [],
      openQuestions: [],
      memoryDelta: '',
    }
  }

  const transcriptText = data.transcript
    .map(e => `${e.role === 'user' ? 'Yannick' : 'Y-OS'}: ${e.text}`)
    .join('\n')

  const prompt = `Analyze this Y-OS voice session and extract structured insights.

Session: ${data.mode} mode | ${data.duration}s | ${new Date(data.startedAt).toLocaleString()}

Transcript:
${transcriptText}

Respond in JSON with this exact structure:
{
  "executiveSummary": "1-2 sentences",
  "keyInsights": ["insight 1", "insight 2"],
  "decisions": ["decision 1"],
  "actions": ["action 1"],
  "openQuestions": ["question 1"],
  "memoryDelta": "What should be remembered from this session"
}`

  try {
    const res = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-4o-mini',
        messages: [
          {
            role: 'system',
            content: 'You are a session analyst for Y-OS. Extract structured insights from voice sessions. Respond only with valid JSON.',
          },
          { role: 'user', content: prompt },
        ],
        temperature: 0.3,
        response_format: { type: 'json_object' },
      }),
    })

    if (!res.ok) throw new Error('OpenAI synthesis failed')

    const completion = await res.json()
    const content = completion.choices[0]?.message?.content || '{}'
    return JSON.parse(content) as SessionSynthesis
  } catch (err) {
    console.error('[Session synthesis] Error:', err)
    return {
      executiveSummary: `${data.mode} session — ${data.duration}s`,
      keyInsights: [],
      decisions: [],
      actions: [],
      openQuestions: [],
      memoryDelta: '',
    }
  }
}

function makeHeading2(text: string): BlockObjectRequest {
  return {
    object: 'block',
    type: 'heading_2',
    heading_2: { rich_text: [{ type: 'text', text: { content: text } }] },
  }
}

function makeParagraph(text: string): BlockObjectRequest {
  return {
    object: 'block',
    type: 'paragraph',
    paragraph: { rich_text: [{ type: 'text', text: { content: text } }] },
  }
}

function makeBullet(text: string): BlockObjectRequest {
  return {
    object: 'block',
    type: 'bulleted_list_item',
    bulleted_list_item: { rich_text: [{ type: 'text', text: { content: text } }] },
  }
}

function makeTodo(text: string): BlockObjectRequest {
  return {
    object: 'block',
    type: 'to_do',
    to_do: {
      rich_text: [{ type: 'text', text: { content: text } }],
      checked: false,
    },
  }
}

function makeCallout(text: string, emoji: string): BlockObjectRequest {
  return {
    object: 'block',
    type: 'callout',
    callout: {
      rich_text: [{ type: 'text', text: { content: text } }],
      icon: { type: 'emoji', emoji: emoji as '🧠' },
    },
  }
}

async function logToNotion(data: SessionLogRequest, synthesis: SessionSynthesis): Promise<void> {
  const dbId = process.env.NOTION_DATABASE_ID
  if (!dbId) {
    console.log('[Session Log] No Notion DB configured')
    console.log('[Session]', synthesis.executiveSummary)
    return
  }

  const transcriptText = data.transcript
    .map(e => `${e.role === 'user' ? 'Yannick' : 'Y-OS'}: ${e.text}`)
    .join('\n\n')

  const formatDuration = (s: number) => {
    const m = Math.floor(s / 60)
    const sec = s % 60
    return m > 0 ? `${m}m ${sec}s` : `${sec}s`
  }

  // Build blocks array
  const blocks: BlockObjectRequest[] = [
    makeHeading2('Executive Summary'),
    makeParagraph(synthesis.executiveSummary),
  ]

  if (synthesis.keyInsights.length > 0) {
    blocks.push(makeHeading2('Key Insights'))
    synthesis.keyInsights.forEach(i => blocks.push(makeBullet(i)))
  }

  if (synthesis.decisions.length > 0) {
    blocks.push(makeHeading2('Decisions'))
    synthesis.decisions.forEach(d => blocks.push(makeBullet(d)))
  }

  if (synthesis.actions.length > 0) {
    blocks.push(makeHeading2('Actions'))
    synthesis.actions.forEach(a => blocks.push(makeTodo(a)))
  }

  if (synthesis.openQuestions.length > 0) {
    blocks.push(makeHeading2('Open Questions'))
    synthesis.openQuestions.forEach(q => blocks.push(makeBullet(q)))
  }

  if (synthesis.memoryDelta) {
    blocks.push(makeHeading2('Memory Delta'))
    blocks.push(makeCallout(synthesis.memoryDelta, '🧠'))
  }

  blocks.push(makeHeading2('Transcript'))
  blocks.push(makeParagraph(transcriptText.slice(0, 2000)))

  try {
    await notion.pages.create({
      parent: { database_id: dbId },
      properties: {
        Name: {
          title: [{
            text: {
              content: `Voice Session — ${new Date(data.startedAt).toLocaleDateString('en-US', {
                month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
              })}`,
            },
          }],
        },
        Type: {
          select: { name: data.mode === 'voice' ? 'Voice Session' : 'Voice+Vision Session' },
        },
        Date: {
          date: { start: data.startedAt },
        },
        Tags: {
          multi_select: [
            { name: 'voice' },
            { name: data.mode },
            { name: 'yOS' },
          ],
        },
      },
      children: blocks,
    })
  } catch (err) {
    console.error('[Session Log] Notion error:', err)
    console.log('[Session Fallback]', synthesis.executiveSummary)
  }
}

export async function POST(req: NextRequest) {
  try {
    const data: SessionLogRequest = await req.json()

    const synthesis = await synthesizeSession(data)

    // Fire-and-forget Notion logging
    logToNotion(data, synthesis).catch(console.error)

    return NextResponse.json({
      logged: true,
      sessionId: data.sessionId,
      synthesis: {
        executiveSummary: synthesis.executiveSummary,
        actionsCount: synthesis.actions.length,
        insightsCount: synthesis.keyInsights.length,
      },
    })
  } catch (err) {
    console.error('[Session Log] Error:', err)
    return NextResponse.json(
      { logged: false, error: err instanceof Error ? err.message : 'Unknown error' },
      { status: 500 }
    )
  }
}
