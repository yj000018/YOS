// ─────────────────────────────────────────────────────────────────────────────
// Y-Menu v0 — Scoring Engine
// Scores menu items by relevance given current state
// ─────────────────────────────────────────────────────────────────────────────

import { MenuItem } from './types';
import { StateManager } from './state-manager';

export function scoreMenuItem(item: MenuItem, state: StateManager): number {
  let score = 0.5; // base

  // Boost if recommended_when conditions are met
  if (item.recommended_when && item.recommended_when.length > 0) {
    const met = item.recommended_when.filter(c => state.evaluateCondition(c)).length;
    score += (met / item.recommended_when.length) * 0.4;
  }

  // Penalise if disabled_when conditions are met
  if (item.disabled_when && item.disabled_when.length > 0) {
    const met = item.disabled_when.filter(c => state.evaluateCondition(c)).length;
    if (met > 0) score -= 0.6;
  }

  // Boost agent suggestions
  if (item.agent_suggestion) {
    score += (item.agent_confidence || 0.5) * 0.2;
  }

  // Boost items whose required inputs are available
  if (item.requires && item.requires.length > 0) {
    const missing = state.getMissingInputs();
    const allPresent = item.requires.every(r => !missing.includes(r));
    if (allPresent) score += 0.1;
    else score -= 0.15;
  }

  return Math.max(0, Math.min(1, score));
}

export function isItemVisible(item: MenuItem, state: StateManager): boolean {
  if (!item.visible_when || item.visible_when.length === 0) return true;
  return item.visible_when.some(c => state.evaluateCondition(c));
}

export function isItemDisabled(item: MenuItem, state: StateManager): boolean {
  if (!item.disabled_when || item.disabled_when.length === 0) return false;
  return item.disabled_when.some(c => state.evaluateCondition(c));
}
