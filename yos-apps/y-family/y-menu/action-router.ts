// ─────────────────────────────────────────────────────────────────────────────
// Y-Menu v0 — Action Router
// Routes user input (number, command, or natural language) to next action
// ─────────────────────────────────────────────────────────────────────────────

import { MenuDefinition } from './types';
import { StateManager } from './state-manager';
import { IntentRouter } from './intent-router';
import { WorkflowComposer } from './workflow-composer';

export type RouteResult =
  | { type: 'submenu'; menuId: string }
  | { type: 'workflow'; workflowPath: string; composition?: string }
  | { type: 'intent'; formatted: string }
  | { type: 'command'; command: string }
  | { type: 'unknown'; message: string };

const FAST_COMMANDS = new Set(['home', 'back', 'status', 'help', 'continue', 'cancel', 'more', 'why', 'diagnose']);

export class ActionRouter {
  constructor(
    private state: StateManager,
    private intentRouter: IntentRouter,
    private workflowComposer: WorkflowComposer,
  ) {}

  route(input: string, currentMenu: MenuDefinition): RouteResult {
    const trimmed = input.trim().toLowerCase();

    // ── Fast commands ─────────────────────────────────────────────────────────
    if (FAST_COMMANDS.has(trimmed)) {
      return { type: 'command', command: trimmed };
    }

    // ── Numeric selection ─────────────────────────────────────────────────────
    const num = parseInt(trimmed, 10);
    if (!isNaN(num) && num >= 1 && num <= currentMenu.items.length) {
      const item = currentMenu.items[num - 1];
      if (item.action_type === 'submenu' && item.target) {
        return { type: 'submenu', menuId: item.target };
      }
      if (item.action_type === 'workflow' && item.target) {
        return { type: 'workflow', workflowPath: item.target };
      }
      // Default: treat as intent with item label
      const result = this.intentRouter.route(item.label);
      return { type: 'intent', formatted: this.intentRouter.format(result) };
    }

    // ── Natural language → workflow composer first ────────────────────────────
    const composition = this.workflowComposer.compose(trimmed);
    if (composition) {
      return {
        type: 'workflow',
        workflowPath: composition.recommended_workflow,
        composition: this.workflowComposer.format(composition),
      };
    }

    // ── Natural language → intent router ─────────────────────────────────────
    const intentResult = this.intentRouter.route(trimmed);
    if (intentResult.best_match && intentResult.best_match.score > 0.3) {
      return { type: 'intent', formatted: this.intentRouter.format(intentResult) };
    }

    return {
      type: 'unknown',
      message: `Could not route: "${input}"\nTry a number, a command (home/back/status), or describe your goal.`,
    };
  }
}
