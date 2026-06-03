/**
 * yOS Memory Intake Dispatcher — Step 4
 *
 * Accepts any content type and normalizes it into a yOS Memory Package,
 * then pushes it to the Notion yOS Memory Inbox database.
 *
 * Supported input types:
 *   - text/note
 *   - url/link
 *   - session (voice/text session transcript)
 *   - insight
 *   - decision
 *   - document (base64 or text content)
 *
 * POST /api/intake
 * Body: { type, content, title?, project?, tags?, source_app?, facet?, priority? }
 */

import { NextRequest, NextResponse } from 'next/server'
import { Client } from '@notionhq/client'

const notion = new Client({ auth: process.env.NOTION_API_KEY })
const DB_ID = process.env.NOTION_DATABASE_ID || '938332ffed1d4965849908df442bfa1c'

// ─── Types ────────────────────────────────────────────────────────────────────

type ContentType = 'text' | 'note' | 'url' | 'link' | 'session' | 'insight' | 'decision' | 'document' | 'image' | 'audio' | 'other'

interface IntakeRequest {
  type: ContentType
  content: string
  title?: string
  project?: string
  tags?: string[]
  source_app?: string
  facet?: string
  priority?: 'None' | 'Low' | 'Medium' | 'High' | 'Critical'
  executive_summary?: string
  decisions?: string
  actions?: string
  open_questions?: string
  memory_delta?: string
  context_to_reinject?: string
}

// ─── Normalizer ───────────────────────────────────────────────────────────────

function normalizeTitle(req: IntakeRequest): string {
  if (req.title) return req.title

  // Auto-generate title from content
  const preview = req.content.slice(0, 80).replace(/\n/g, ' ').trim()
  const typeLabel = req.type.toUpperCase()
  return `[${typeLabel}] ${preview}${req.content.length > 80 ? '...' : ''}`
}

function mapTypeToSourceType(type: ContentType): string {
  const map: Record<ContentType, string> = {
    text: 'Text',
    note: 'Note',
    url: 'Link',
    link: 'Link',
    session: 'LLM Session',
    insight: 'Note',
    decision: 'Note',
    document: 'Document',
    image: 'Image',
    audio: 'Audio',
    other: 'Other',
  }
  return map[type] || 'Other'
}

function truncate(text: string, maxLen = 2000): string {
  if (!text) return ''
  if (text.length <= maxLen) return text
  return text.slice(0, maxLen - 3) + '...'
}

// ─── Handler ──────────────────────────────────────────────────────────────────

export async function POST(req: NextRequest) {
  try {
    const body: IntakeRequest = await req.json()

    if (!body.content && !body.title) {
      return NextResponse.json({ error: 'content or title required' }, { status: 400 })
    }

    const title = normalizeTitle(body)
    const sourceType = mapTypeToSourceType(body.type || 'other')

    // Build Notion page properties
    const properties: Record<string, unknown> = {
      title: {
        title: [{ text: { content: title } }],
      },
      Status: {
        select: { name: 'Inbox' },
      },
      'Source Type': {
        select: { name: sourceType },
      },
    }

    // Source App
    if (body.source_app) {
      properties['Source App'] = { select: { name: body.source_app } }
    }

    // Project
    if (body.project) {
      properties['Project'] = {
        multi_select: [{ name: body.project }],
      }
    }

    // Tags
    if (body.tags && body.tags.length > 0) {
      properties['Tags'] = {
        multi_select: body.tags.map(t => ({ name: t })),
      }
    }

    // Facet
    if (body.facet) {
      properties['Facet'] = {
        multi_select: [{ name: body.facet }],
      }
    }

    // Reinject Priority
    if (body.priority) {
      properties['Reinject Priority'] = { select: { name: body.priority } }
    }

    // Rich text fields
    if (body.executive_summary) {
      properties['Executive Summary'] = {
        rich_text: [{ text: { content: truncate(body.executive_summary) } }],
      }
    }

    if (body.decisions) {
      properties['Decisions'] = {
        rich_text: [{ text: { content: truncate(body.decisions) } }],
      }
    }

    if (body.actions) {
      properties['Actions'] = {
        rich_text: [{ text: { content: truncate(body.actions) } }],
      }
    }

    if (body.open_questions) {
      properties['Open Questions'] = {
        rich_text: [{ text: { content: truncate(body.open_questions) } }],
      }
    }

    if (body.memory_delta) {
      properties['Memory Delta'] = {
        rich_text: [{ text: { content: truncate(body.memory_delta) } }],
      }
    }

    if (body.context_to_reinject) {
      properties['Context to Reinject'] = {
        rich_text: [{ text: { content: truncate(body.context_to_reinject) } }],
      }
    }

    // Raw Content
    if (body.content) {
      properties['Raw Content'] = {
        rich_text: [{ text: { content: truncate(body.content, 2000) } }],
      }
    }

    // Create the Notion page
    const page = await notion.pages.create({
      parent: { database_id: DB_ID },
      properties: properties as Parameters<typeof notion.pages.create>[0]['properties'],
    })

    return NextResponse.json({
      success: true,
      page_id: page.id,
      url: (page as { url?: string }).url || `https://notion.so/${page.id.replace(/-/g, '')}`,
      title,
      status: 'Inbox',
    })

  } catch (err) {
    const message = err instanceof Error ? err.message : 'Intake failed'
    console.error('[Intake Dispatcher] Error:', message)
    return NextResponse.json({ error: message }, { status: 500 })
  }
}

// GET — health check
export async function GET() {
  return NextResponse.json({
    service: 'yOS Memory Intake Dispatcher',
    version: '1.0',
    database_id: DB_ID,
    supported_types: ['text', 'note', 'url', 'link', 'session', 'insight', 'decision', 'document', 'image', 'audio', 'other'],
  })
}
