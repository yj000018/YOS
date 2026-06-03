// ─────────────────────────────────────────────────────────────────────────────
// Y-Menu v0 — Intent Router
// Translates natural language goals into capability matches + workflow paths
// ─────────────────────────────────────────────────────────────────────────────

import { IntentRouterResult, IntentMatch } from './types';
import { CapabilityRegistry } from './capability-registry';
import { StateManager } from './state-manager';

// Fast-path decision rules for common intents
const DECISION_RULES: Record<string, (state: StateManager) => string[]> = {
  kindle: (state) => {
    const bf = state.getBookFactory();
    const bookType = bf?.book_type || 'unknown';
    if (['illustrated', 'children_book', 'comic', 'artbook', 'visual_essay'].includes(bookType)) {
      return [
        'Book type: ' + bookType + ' → Fixed-layout EPUB workflow',
        'Use HTML/CSS/SVG engine → EPUB FXL → Kindle validation',
        'Workflow: book-factory/build-epub-fxl.md',
      ];
    }
    if (bookType === 'print_replica') {
      return [
        'Book type: print replica → PDF/KDP print workflow',
        'Workflow: book-factory/prepare-kdp.md',
      ];
    }
    return [
      'Book type: text-only → Reflowable EPUB via Pandoc',
      'Workflow: book-factory/build-epub-pandoc.md → KDP checklist',
    ];
  },

  site: (_state) => {
    return [
      'Use Lovable if: one book · simple landing page · speed matters',
      'Use Astro if: multi-book catalogue · industrial platform · long-term site',
      'Use Astro + Visual Engine if: interactive / multimedia web edition',
    ];
  },

  pdf: (_state) => {
    return [
      'Premium print PDF → Use Typst (not Pandoc, not Scrivener)',
      'Workflow: book-factory/build-pdf-typst.md',
      'Digital PDF → Typst with screen-optimised layout',
    ];
  },

  epub: (_state) => {
    return [
      'Standard reflowable EPUB → Use Pandoc',
      'Workflow: book-factory/build-epub-pandoc.md',
      'For illustrated/children/BD → Use fixed-layout EPUB workflow instead',
    ];
  },

  distribute: (_state) => {
    return [
      '1️⃣ Amazon KDP → workflow: prepare-kdp.md',
      '2️⃣ IngramSpark → workflow: prepare-ingram.md',
      '3️⃣ Draft2Digital → workflow: prepare-draft2digital.md',
      '4️⃣ Gumroad/direct → generate download package',
    ];
  },

  release: (_state) => {
    return [
      '1️⃣ Bump version → generate changelog',
      '2️⃣ Archive release folder',
      '3️⃣ Generate release report',
      '4️⃣ Sync summary to Notion',
    ];
  },
};

// Keyword → decision rule mapping
const KEYWORD_MAP: Record<string, string> = {
  kindle: 'kindle',
  amazon: 'kindle',
  kdp: 'kindle',
  ebook: 'kindle',
  'e-book': 'kindle',
  site: 'site',
  website: 'site',
  'mini-site': 'site',
  minisite: 'site',
  lovable: 'site',
  astro: 'site',
  web: 'site',
  pdf: 'pdf',
  print: 'pdf',
  typst: 'pdf',
  epub: 'epub',
  pandoc: 'epub',
  reflowable: 'epub',
  distribut: 'distribute',
  ingram: 'distribute',
  draft2digital: 'distribute',
  gumroad: 'distribute',
  publish: 'distribute',
  release: 'release',
  edition: 'release',
  version: 'release',
  changelog: 'release',
};

export class IntentRouter {
  constructor(
    private registry: CapabilityRegistry,
    private state: StateManager,
  ) {}

  route(input: string): IntentRouterResult {
    const normalised = input.toLowerCase().trim();

    // 1. Match capabilities from registry
    const matches: IntentMatch[] = this.registry
      .findByPhrase(normalised)
      .map(m => ({
        capability: m.capability,
        score: m.score,
        matched_phrase: m.matched_phrase,
      }));

    // 2. Detect decision rule key
    const ruleKey = this.detectRuleKey(normalised);
    const decisionPaths = ruleKey ? DECISION_RULES[ruleKey]?.(this.state) : undefined;

    // 3. Determine if clarification needed
    const bf = this.state.getBookFactory();
    let needsClarification = false;
    let clarificationQuestion: string | undefined;

    if (ruleKey === 'kindle' && (!bf?.book_type || bf.book_type === 'unknown')) {
      needsClarification = true;
      clarificationQuestion = 'What type of book is this?\n1️⃣ Text-only\n2️⃣ Illustrated / artbook\n3️⃣ Children\'s book / comic / BD\n4️⃣ Print replica';
    }

    return {
      intent: normalised,
      matches: matches.slice(0, 5),
      best_match: matches[0],
      needs_clarification: needsClarification,
      clarification_question: clarificationQuestion,
      decision_paths: decisionPaths,
    };
  }

  private detectRuleKey(input: string): string | undefined {
    for (const [keyword, ruleKey] of Object.entries(KEYWORD_MAP)) {
      if (input.includes(keyword)) return ruleKey;
    }
    return undefined;
  }

  /**
   * Format intent result as readable text
   */
  format(result: IntentRouterResult): string {
    const lines: string[] = [];
    const BOX = '╭────────────────────────────────────────────╮';
    const BOX_BOT = '╰────────────────────────────────────────────╯';

    lines.push(BOX);
    lines.push('│           INTENT ROUTER                    │');
    lines.push(BOX_BOT);
    lines.push('');
    lines.push(`Goal detected: "${result.intent}"`);
    lines.push('');

    if (result.best_match) {
      lines.push(`Best match: ${result.best_match.capability.title}`);
      lines.push(`Confidence: ${Math.round(result.best_match.score * 100)}%`);
      lines.push('');
    }

    if (result.decision_paths && result.decision_paths.length > 0) {
      lines.push('Decision paths:');
      result.decision_paths.forEach((p, i) => {
        lines.push(`  ${i + 1}. ${p}`);
      });
      lines.push('');
    }

    if (result.needs_clarification && result.clarification_question) {
      lines.push('⚠️  One question needed:');
      lines.push(result.clarification_question);
      lines.push('');
    }

    if (result.best_match?.capability.next_actions?.length) {
      lines.push('Recommended next actions:');
      result.best_match.capability.next_actions.forEach((a, i) => {
        const emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣'];
        lines.push(`${emojis[i] || (i + 1) + '.'} ${a}`);
      });
    }

    return lines.join('\n');
  }
}
