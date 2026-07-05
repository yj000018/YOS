/**
 * semanticTypes.ts — MVP B
 *
 * Extensible map of emoji → semantic type definition.
 * To add a new type: add one entry here. No parser changes needed.
 *
 * MVP B supports exactly 10 types in this sidebar order.
 */

export interface SemanticTypeDefinition {
  type: string;
  label: string;
}

/**
 * SEMANTIC_TYPES — canonical map, insertion order = sidebar display order.
 * Key: the canonical emoji (with variation selectors where applicable).
 */
export const SEMANTIC_TYPES: Record<string, SemanticTypeDefinition> = {
  "📦":  { type: "project",      label: "Projects"      },
  "🏗️": { type: "architecture", label: "Architecture"  },
  "🧩":  { type: "component",    label: "Components"    },
  "✅":  { type: "decision",     label: "Decisions"     },
  "➡️": { type: "action",       label: "Actions"       },
  "⚠️": { type: "risk",         label: "Risks"         },
  "❓":  { type: "question",     label: "Questions"     },
  "💡":  { type: "insight",      label: "Insights"      },
  "🧠":  { type: "memory",       label: "Memories"      },
  "🔁":  { type: "pattern",      label: "Patterns"      },
};

/**
 * Canonical display order for sidebar groups.
 * Derived from SEMANTIC_TYPES insertion order (ES2015+).
 */
export const SEMANTIC_TYPE_ORDER: string[] = Object.values(SEMANTIC_TYPES).map(
  (def) => def.type
);

/**
 * EMOJI_VARIANTS — normalize bare codepoints to their canonical form
 * before matching against SEMANTIC_TYPES.
 *
 * Covers the two most common false-negative cases in real notes:
 *   ➡  (U+27A1, no variation selector) → ➡️ (U+27A1 U+FE0F)
 *   ⚠  (U+26A0, no variation selector) → ⚠️ (U+26A0 U+FE0F)
 */
export const EMOJI_VARIANTS: Record<string, string> = {
  "\u27A1":           "\u27A1\uFE0F",   // ➡  → ➡️
  "\u26A0":           "\u26A0\uFE0F",   // ⚠  → ⚠️
};
