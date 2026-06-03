// ─────────────────────────────────────────────────────────────────────────────
// Y-Menu v0 — Menu Renderer
// Renders beautiful text-UI menus for chat / terminal
// ─────────────────────────────────────────────────────────────────────────────

import { MenuDefinition, MenuItem, RenderedMenu, YMenuState } from './types';
import { StateManager } from './state-manager';
import { AgentSuggestionsManager } from './agent-suggestions';
import { scoreMenuItem, isItemVisible, isItemDisabled } from './scoring';

const NUMBER_EMOJIS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'];
const BOX_WIDTH = 44;

function boxLine(content: string, width: number = BOX_WIDTH): string {
  const pad = Math.max(0, width - content.length - 2);
  return `│ ${content}${' '.repeat(pad)}│`;
}

function boxTop(width: number = BOX_WIDTH): string {
  return `╭${'─'.repeat(width - 2)}╮`;
}

function boxBottom(width: number = BOX_WIDTH): string {
  return `╰${'─'.repeat(width - 2)}╯`;
}

function centred(text: string, width: number = BOX_WIDTH): string {
  const inner = width - 4; // 2 for │ and space each side
  const pad = Math.max(0, inner - text.length);
  const left = Math.floor(pad / 2);
  const right = pad - left;
  return `│ ${' '.repeat(left)}${text}${' '.repeat(right)} │`;
}

export class MenuRenderer {
  constructor(
    private state: StateManager,
    private agentSuggestions: AgentSuggestionsManager,
  ) {}

  render(menu: MenuDefinition, options: { compact?: boolean; maxItems?: number } = {}): RenderedMenu {
    const { compact = false, maxItems = 10 } = options;
    const lines: string[] = [];

    // ── Header Box ────────────────────────────────────────────────────────────
    lines.push(boxTop());
    lines.push(centred(menu.title.toUpperCase()));
    if (menu.subtitle) {
      lines.push(centred(menu.subtitle));
    }
    lines.push(boxBottom());
    lines.push('');

    // ── Context Block ─────────────────────────────────────────────────────────
    if (!compact) {
      const bf = this.state.getBookFactory();
      const session = this.state.getSession();

      if (bf?.active_book_title || session.active_module) {
        lines.push('Context');
        if (session.active_module) {
          lines.push(`• Active module: ${session.active_module}`);
        }
        if (bf?.active_book_title) {
          lines.push(`• Active book: ${bf.active_book_title}`);
        }
        if (bf?.manuscript?.status) {
          const manuscriptLabel = bf.manuscript.status === 'imported' ? 'Manuscript imported' : `Manuscript: ${bf.manuscript.status}`;
          const outputsPending = this.state.getPendingOutputs().length;
          lines.push(`• Status: ${manuscriptLabel} · ${outputsPending} exports pending`);
        }
        lines.push('');
      }
    }

    // ── Collect and score items ───────────────────────────────────────────────
    let items = [...menu.items];

    // Merge agent suggestions
    const agentItems = this.agentSuggestions.toMenuItems(this.state);
    items = [...items, ...agentItems];

    // Filter visible items
    items = items.filter(item => isItemVisible(item, this.state));

    // Score and sort
    const scored = items.map(item => ({
      item,
      score: scoreMenuItem(item, this.state),
      disabled: isItemDisabled(item, this.state),
    }));
    scored.sort((a, b) => b.score - a.score);

    // ── Recommended Next Action ───────────────────────────────────────────────
    const topItem = scored.find(s => !s.disabled && s.score > 0.6);
    let recommendedAction: string | undefined;

    if (topItem) {
      recommendedAction = topItem.item.label;
      lines.push('Recommended next action ⭐');
      lines.push(topItem.item.label + '.');
      lines.push('');
    }

    // ── Numbered Options ──────────────────────────────────────────────────────
    const visibleItems = scored.slice(0, maxItems);
    let counter = 0;

    for (const { item, disabled } of visibleItems) {
      const numEmoji = counter < NUMBER_EMOJIS.length ? NUMBER_EMOJIS[counter] : `${counter + 1}.`;
      const emoji = item.emoji ? `${item.emoji} ` : '';
      const disabledMark = disabled ? ' ⛔' : '';
      const agentMark = item.agent_suggestion ? ' 🤖' : '';
      lines.push(`${numEmoji} ${emoji}${item.label}${disabledMark}${agentMark}`);

      if (!compact && item.description && item.agent_suggestion) {
        lines.push(`   ↳ ${item.description}`);
      }
      counter++;
    }

    if (scored.length > maxItems) {
      lines.push(`… ${scored.length - maxItems} more options available (type "more")`);
    }

    lines.push('');

    // ── Warning Block ─────────────────────────────────────────────────────────
    const missing = this.state.getMissingInputs();
    if (missing.length > 0) {
      lines.push('⚠️  Missing inputs: ' + missing.join(', '));
      lines.push('');
    }

    // ── Command Hints ─────────────────────────────────────────────────────────
    const commands = menu.commands || ['home', 'back', 'status', 'help', 'continue', 'cancel'];
    lines.push(`Commands: ${commands.join(' · ')}`);
    lines.push('Reply with a number or describe your goal.');

    return {
      raw: lines.join('\n'),
      menu_id: menu.id,
      item_count: visibleItems.length,
      recommended_action: recommendedAction,
    };
  }

  /**
   * Render a result block
   */
  renderResult(params: {
    title: string;
    status: 'success' | 'warning' | 'error';
    summary: string;
    path?: string[];
    missing?: string[];
    next?: string[];
  }): string {
    const lines: string[] = [];
    const icon = params.status === 'success' ? '✅' : params.status === 'warning' ? '⚠️' : '❌';

    lines.push(boxTop());
    lines.push(centred('RESULT'));
    lines.push(boxBottom());
    lines.push('');
    lines.push(`${icon} ${params.summary}`);

    if (params.path && params.path.length > 0) {
      lines.push('');
      lines.push('Path:');
      for (let i = 0; i < params.path.length; i++) {
        const arrow = i < params.path.length - 1 ? '\n→ ' : '';
        lines.push(params.path[i] + arrow);
      }
    }

    if (params.missing && params.missing.length > 0) {
      lines.push('');
      lines.push('Missing:');
      for (const m of params.missing) {
        lines.push(`⚠️ ${m}`);
      }
    }

    if (params.next && params.next.length > 0) {
      lines.push('');
      lines.push('Next:');
      params.next.forEach((n, i) => {
        const numEmoji = i < NUMBER_EMOJIS.length ? NUMBER_EMOJIS[i] : `${i + 1}.`;
        lines.push(`${numEmoji} ${n}`);
      });
    }

    return lines.join('\n');
  }

  /**
   * Render a status summary
   */
  renderStatus(state: YMenuState): string {
    const lines: string[] = [];
    lines.push(boxTop());
    lines.push(centred('Y-OS STATUS'));
    lines.push(boxBottom());
    lines.push('');

    const session = state.session;
    lines.push(`Active module : ${session.active_module || 'none'}`);
    lines.push(`Active menu   : ${session.active_menu || 'root'}`);
    lines.push(`Last action   : ${session.last_action || 'none'}`);
    lines.push('');

    const bf = state.book_factory;
    if (bf) {
      lines.push('── Book-Factory ──────────────────────────');
      lines.push(`Book          : ${bf.active_book_title || 'none'}`);
      lines.push(`Manuscript    : ${bf.manuscript?.status || 'missing'}`);
      lines.push(`Cover         : ${bf.assets?.cover || 'missing'}`);
      lines.push('');
      lines.push('Outputs:');
      const outputs = bf.outputs || {};
      for (const [k, v] of Object.entries(outputs)) {
        const icon = v && v !== 'missing' ? '✅' : '⬜';
        lines.push(`  ${icon} ${k.replace(/_/g, ' ')}`);
      }
      lines.push('');
      lines.push('Distribution:');
      const dist = bf.distribution || {};
      for (const [k, v] of Object.entries(dist)) {
        const icon = v === 'complete' ? '✅' : v === 'in_progress' ? '🔄' : '⬜';
        lines.push(`  ${icon} ${k}`);
      }
    }

    return lines.join('\n');
  }
}
