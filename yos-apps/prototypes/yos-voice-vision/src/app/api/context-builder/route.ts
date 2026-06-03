/**
 * yOS Context Builder — Step 5
 *
 * Retrieves relevant memory from Notion yOS Memory Inbox,
 * ranks by reinject priority, and compresses into an injectable context.
 *
 * POST /api/context-builder
 * Body: { type: 'context_request', mode: 'voice' | 'voice_vision', project?: string }
 *
 * Returns: { context: string, instructions: string, sources: number }
 */

import { NextRequest, NextResponse } from 'next/server'
import { Client } from '@notionhq/client'

const notion = new Client({ auth: process.env.NOTION_API_KEY })
const DB_ID = process.env.NOTION_DATABASE_ID || '938332ffed1d4965849908df442bfa1c'

const PRIORITY_WEIGHT: Record<string, number> = {
  Critical: 5, High: 4, Medium: 3, Low: 2, None: 1,
}

const MAX_CONTEXT_CHARS = 3000
const MAX_ITEMS = 8

const YOS_BASE = `Y-OS is the cognitive operating system of Yannick Jolliet.
Core projects: CasaTAO (smart home Sicily), ODYSSEY (3D universe interface), Y-OS architecture.
Yannick is an architect of new society. Direct, dense, precise. No filler.`

const MODE_INSTRUCTIONS: Record<string, string> = {
  voice: 'Voice mode via OpenAI Realtime. Be direct and conversational. No markdown. Short sentences. Use log_insight tool to store insights.',
  voice_vision: 'Voice + Vision mode via Gemini Live. You can see the environment through the camera. Describe what you see concisely. For CasaTAO: identify objects, spaces, lighting. Use control_iot for IoT actions.',
}

interface MemoryItem {
  title: string
  summary: string
  decisions: string
  actions: string
  context_to_reinject: string
  priority: string
  project: string
}

function getTextProp(page: Record<string, unknown>, key: string): string {
  try {
    const props = page.properties as Record<string, Record<string, unknown>>
    const prop = props[key]
    if (!prop) return ''
    if (prop.type === 'title') return ((prop.title as Array<{plain_text: string}>) || []).map(t => t.plain_text).join('')
    if (prop.type === 'rich_text') return ((prop.rich_text as Array<{plain_text: string}>) || []).map(t => t.plain_text).join('')
    if (prop.type === 'select') return (prop.select as {name: string})?.name || ''
    if (prop.type === 'multi_select') return ((prop.multi_select as Array<{name: string}>) || []).map(s => s.name).join(', ')
    if (prop.type === 'created_time') return prop.created_time as string
  } catch { /* ignore */ }
  return ''
}

async function queryMemory(project?: string): Promise<MemoryItem[]> {
  try {
    const andFilters: unknown[] = [
      { property: 'Status', select: { does_not_equal: 'Rejected' } },
      { property: 'Reinject Priority', select: { does_not_equal: 'None' } },
    ]
    if (project) {
      andFilters.push({ property: 'Project', multi_select: { contains: project } })
    }

    const response = await notion.databases.query({
      database_id: DB_ID,
      filter: { and: andFilters } as Parameters<typeof notion.databases.query>[0]['filter'],
      sorts: [{ property: 'Created', direction: 'descending' }],
      page_size: 20,
    })

    const items: MemoryItem[] = response.results.map(page => {
      const p = page as unknown as Record<string, unknown>
      return {
        title: getTextProp(p, 'title'),
        summary: getTextProp(p, 'Executive Summary'),
        decisions: getTextProp(p, 'Decisions'),
        actions: getTextProp(p, 'Actions'),
        context_to_reinject: getTextProp(p, 'Context to Reinject'),
        priority: getTextProp(p, 'Reinject Priority'),
        project: getTextProp(p, 'Project'),
      }
    })

    items.sort((a, b) => (PRIORITY_WEIGHT[b.priority] || 1) - (PRIORITY_WEIGHT[a.priority] || 1))
    return items.slice(0, MAX_ITEMS)
  } catch (err) {
    console.error('[Context Builder] Notion query failed:', err)
    return []
  }
}

function buildContextString(items: MemoryItem[], mode: string, project?: string): string {
  const lines: string[] = [
    YOS_BASE,
    '',
    `Date: ${new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}`,
  ]

  if (project) lines.push(`Active project: ${project}`)
  if (items.length === 0) return lines.join('\n')

  lines.push('', '=== MEMORY CONTEXT ===')
  let charCount = lines.join('\n').length

  for (const item of items) {
    if (charCount >= MAX_CONTEXT_CHARS) break
    const parts: string[] = [`[${item.priority}] ${item.title}`]
    const body = item.context_to_reinject || item.summary
    if (body) parts.push(`→ ${body.slice(0, 200)}`)
    if (item.decisions) parts.push(`Decisions: ${item.decisions.slice(0, 120)}`)
    if (item.actions) parts.push(`Actions: ${item.actions.slice(0, 120)}`)
    const block = parts.join('\n')
    if (charCount + block.length > MAX_CONTEXT_CHARS) break
    lines.push(block, '')
    charCount += block.length
  }

  lines.push('=== END ===')
  return lines.join('\n')
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json()
    const { mode = 'voice', project } = body

    const items = await queryMemory(project)
    const context = buildContextString(items, mode, project)
    const instructions = MODE_INSTRUCTIONS[mode] || MODE_INSTRUCTIONS.voice

    return NextResponse.json({
      context,
      instructions,
      sources: items.length,
      mode,
      project: project || null,
      timestamp: new Date().toISOString(),
    })
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Context builder failed'
    console.error('[Context Builder] Error:', message)
    return NextResponse.json({
      context: YOS_BASE,
      instructions: MODE_INSTRUCTIONS.voice,
      sources: 0,
      error: message,
    })
  }
}

export async function GET() {
  return NextResponse.json({
    service: 'yOS Context Builder',
    version: '2.0',
    database_id: DB_ID,
    max_context_chars: MAX_CONTEXT_CHARS,
  })
}
