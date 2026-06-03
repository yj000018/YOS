import { NextRequest, NextResponse } from 'next/server'
import { Client } from '@notionhq/client'

const notion = new Client({ auth: process.env.NOTION_API_KEY })

// Tool registry — maps tool names to handlers
const TOOLS: Record<string, (args: Record<string, unknown>) => Promise<unknown>> = {

  retrieve_memory: async (args) => {
    const query = args.query as string
    // Search Notion for relevant memory
    try {
      const dbId = process.env.NOTION_DATABASE_ID
      if (!dbId) return { result: 'Memory store not configured', items: [] }

      const res = await notion.databases.query({
        database_id: dbId,
        filter: {
          property: 'Name',
          title: { contains: query },
        },
        page_size: 3,
      })

      const items = res.results.map((page: Record<string, unknown>) => {
        const props = (page as { properties: Record<string, unknown> }).properties
        const nameArr = (props.Name as { title: Array<{ plain_text: string }> })?.title
        return nameArr?.[0]?.plain_text || 'Untitled'
      })

      return { query, items, count: items.length }
    } catch {
      return { query, items: [], note: 'Memory search unavailable' }
    }
  },

  log_insight: async (args) => {
    const content = args.content as string
    const tags = (args.tags as string[]) || []

    try {
      const dbId = process.env.NOTION_DATABASE_ID
      if (!dbId) {
        // Log to console as fallback
        console.log('[Y-OS Insight]', content, tags)
        return { logged: true, method: 'console' }
      }

      await notion.pages.create({
        parent: { database_id: dbId },
        properties: {
          Name: {
            title: [{ text: { content: content.slice(0, 100) } }],
          },
          Tags: {
            multi_select: tags.map(t => ({ name: t })),
          },
          Type: {
            select: { name: 'Voice Insight' },
          },
          Date: {
            date: { start: new Date().toISOString() },
          },
        },
        children: [
          {
            object: 'block',
            type: 'paragraph',
            paragraph: {
              rich_text: [{ type: 'text', text: { content } }],
            },
          },
        ],
      })

      return { logged: true, method: 'notion', content: content.slice(0, 50) + '...' }
    } catch (err) {
      console.error('[log_insight] Error:', err)
      return { logged: false, error: 'Failed to log insight' }
    }
  },

  search_document: async (args) => {
    const query = args.query as string
    try {
      const res = await notion.search({
        query,
        filter: { property: 'object', value: 'page' },
        page_size: 3,
      })

      const results = res.results.map((page: Record<string, unknown>) => {
        const props = (page as { properties: Record<string, unknown>; url: string }).properties
        const nameArr = (props.Name as { title: Array<{ plain_text: string }> })?.title ||
                        (props.title as { title: Array<{ plain_text: string }> })?.title
        return {
          title: nameArr?.[0]?.plain_text || 'Untitled',
          url: (page as { url: string }).url,
        }
      })

      return { query, results }
    } catch {
      return { query, results: [], note: 'Search unavailable' }
    }
  },

  control_iot: async (args) => {
    const { device, action, value } = args as { device: string; action: string; value?: string }
    // CasaTAO IoT integration placeholder
    // In production: connect to Home Assistant, MQTT, etc.
    console.log(`[CasaTAO IoT] ${device} → ${action}${value ? ` (${value})` : ''}`)
    return {
      device,
      action,
      value,
      status: 'queued',
      note: 'IoT bridge not yet connected — command logged',
    }
  },
}

export async function POST(req: NextRequest) {
  try {
    const { tool, arguments: args } = await req.json()

    if (!tool || typeof tool !== 'string') {
      return NextResponse.json({ error: 'Invalid tool name' }, { status: 400 })
    }

    const handler = TOOLS[tool]
    if (!handler) {
      return NextResponse.json({ error: `Unknown tool: ${tool}` }, { status: 404 })
    }

    const result = await handler(args || {})
    return NextResponse.json(result)
  } catch (err) {
    console.error('[Tool Call] Error:', err)
    return NextResponse.json(
      { error: err instanceof Error ? err.message : 'Tool execution failed' },
      { status: 500 }
    )
  }
}
