// ─────────────────────────────────────────────────────────────────────────────
// Y-Menu v0 — Utilities
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Check if a CLI tool is available on the system
 */
import { execSync } from 'child_process';

export function checkToolAvailable(tool: string): boolean {
  try {
    execSync(`${tool} --version 2>/dev/null`, { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

export function checkTools(tools: string[]): Record<string, boolean> {
  const result: Record<string, boolean> = {};
  for (const tool of tools) {
    result[tool] = checkToolAvailable(tool);
  }
  return result;
}

export function formatToolStatus(tools: Record<string, boolean>): string {
  const lines = ['Tool availability:'];
  for (const [tool, available] of Object.entries(tools)) {
    lines.push(`  ${available ? '✅' : '❌'} ${tool}${available ? '' : ' (not installed)'}`);
  }
  return lines.join('\n');
}

/**
 * Truncate a string to max length with ellipsis
 */
export function truncate(str: string, max: number): string {
  if (str.length <= max) return str;
  return str.slice(0, max - 3) + '...';
}

/**
 * Pad string to fixed width
 */
export function padEnd(str: string, width: number): string {
  return str.length >= width ? str : str + ' '.repeat(width - str.length);
}

/**
 * Format a date as YYYY-MM-DD
 */
export function formatDate(date: Date = new Date()): string {
  return date.toISOString().split('T')[0];
}
