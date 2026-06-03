// ─────────────────────────────────────────────────────────────────────────────
// Y-Menu v0 — Agent Suggestions
// Loads and merges agent-injected suggestions into menus
// ─────────────────────────────────────────────────────────────────────────────

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import { AgentSuggestion, MenuItem } from './types';
import { StateManager } from './state-manager';

const SUGGESTIONS_FILE = path.join(__dirname, '../../examples/example-agent-suggestions.yaml');

interface SuggestionsFile {
  suggestions: AgentSuggestion[];
}

export class AgentSuggestionsManager {
  private suggestions: AgentSuggestion[] = [];

  load(filePath?: string): void {
    const target = filePath || SUGGESTIONS_FILE;
    if (!fs.existsSync(target)) return;

    try {
      const raw = fs.readFileSync(target, 'utf-8');
      const data = yaml.load(raw) as SuggestionsFile;
      this.suggestions = data?.suggestions || [];
    } catch (err) {
      console.error(`[AgentSuggestions] Failed to load: ${err}`);
    }
  }

  /**
   * Get active suggestions (filter out expired ones)
   */
  getActive(state: StateManager): AgentSuggestion[] {
    return this.suggestions.filter(s => {
      if (!s.expires_when || s.expires_when.length === 0) return true;
      // Suggestion is expired if ALL expiry conditions are met
      return !s.expires_when.every(c => state.evaluateCondition(c));
    });
  }

  /**
   * Convert agent suggestions to menu items
   */
  toMenuItems(state: StateManager): MenuItem[] {
    return this.getActive(state).map(s => ({
      id: `agent_${s.id}`,
      label: s.title,
      emoji: '🤖',
      description: `Agent suggestion · ${s.reason}`,
      action_type: s.action_type,
      target: s.target,
      agent_suggestion: true,
      agent_source: s.source_agent,
      agent_confidence: s.confidence,
      agent_reason: s.reason,
    }));
  }

  count(): number {
    return this.suggestions.length;
  }
}

export const agentSuggestionsManager = new AgentSuggestionsManager();
