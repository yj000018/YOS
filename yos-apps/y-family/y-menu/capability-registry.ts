// ─────────────────────────────────────────────────────────────────────────────
// Y-Menu v0 — Capability Registry
// Living memory of what Y-OS can do
// ─────────────────────────────────────────────────────────────────────────────

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import { Capability } from './types';

const CAPABILITIES_DIR = path.join(__dirname, '../../capabilities');

interface CapabilitiesFile {
  capabilities: Capability[];
}

export class CapabilityRegistry {
  private capabilities: Map<string, Capability> = new Map();
  private loaded = false;

  load(): void {
    if (this.loaded) return;

    if (!fs.existsSync(CAPABILITIES_DIR)) {
      this.loaded = true;
      return;
    }

    const files = fs.readdirSync(CAPABILITIES_DIR).filter(f => f.endsWith('.yaml'));

    for (const file of files) {
      try {
        const raw = fs.readFileSync(path.join(CAPABILITIES_DIR, file), 'utf-8');
        const data = yaml.load(raw) as CapabilitiesFile;
        if (data?.capabilities) {
          for (const cap of data.capabilities) {
            this.capabilities.set(cap.id, cap);
          }
        }
      } catch (err) {
        console.error(`[CapabilityRegistry] Failed to load ${file}: ${err}`);
      }
    }

    this.loaded = true;
  }

  getAll(): Capability[] {
    this.load();
    return Array.from(this.capabilities.values());
  }

  getById(id: string): Capability | undefined {
    this.load();
    return this.capabilities.get(id);
  }

  getByModule(module: string): Capability[] {
    this.load();
    return this.getAll().filter(c => c.module === module);
  }

  /**
   * Find capabilities matching a user phrase (fuzzy keyword match)
   */
  findByPhrase(phrase: string): Array<{ capability: Capability; score: number; matched_phrase?: string }> {
    this.load();
    const normalised = phrase.toLowerCase().trim();
    const results: Array<{ capability: Capability; score: number; matched_phrase?: string }> = [];

    for (const cap of this.capabilities.values()) {
      let bestScore = 0;
      let bestPhrase: string | undefined;

      for (const p of cap.user_phrases || []) {
        const score = this.phraseScore(normalised, p.toLowerCase());
        if (score > bestScore) {
          bestScore = score;
          bestPhrase = p;
        }
      }

      // Also score against capability title
      const titleScore = this.phraseScore(normalised, cap.title.toLowerCase()) * 0.8;
      if (titleScore > bestScore) {
        bestScore = titleScore;
        bestPhrase = cap.title;
      }

      if (bestScore > 0.2) {
        results.push({ capability: cap, score: bestScore, matched_phrase: bestPhrase });
      }
    }

    return results.sort((a, b) => b.score - a.score);
  }

  private phraseScore(input: string, phrase: string): number {
    if (input === phrase) return 1.0;
    if (input.includes(phrase) || phrase.includes(input)) return 0.9;

    const inputWords = input.split(/\s+/);
    const phraseWords = phrase.split(/\s+/);
    const matchCount = inputWords.filter(w => phraseWords.some(pw => pw.includes(w) || w.includes(pw))).length;

    if (matchCount === 0) return 0;
    return matchCount / Math.max(inputWords.length, phraseWords.length);
  }

  count(): number {
    this.load();
    return this.capabilities.size;
  }
}

export const capabilityRegistry = new CapabilityRegistry();
