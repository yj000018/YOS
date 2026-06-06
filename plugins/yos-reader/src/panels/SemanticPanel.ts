/**
 * SemanticPanel.ts — Y-OS Reader, MVP B
 *
 * MVP B changes over MVP A.1 (patch v0.2):
 *   - Group counts shown in header: "Decisions (2)"
 *   - Empty groups hidden (only groups with ≥1 item rendered)
 *   - Updated empty state listing all 10 supported types
 *   - SEMANTIC_TYPE_ORDER drives sidebar order (10 types)
 *   - No scope changes: read-only, current-note only, no vault indexing
 */

import {
  ItemView,
  MarkdownView,
  Notice,
  WorkspaceLeaf,
} from "obsidian";
import { SemanticBlock, parseYmdNote } from "../parser/ymdParser";
import { SEMANTIC_TYPES, SEMANTIC_TYPE_ORDER } from "../parser/semanticTypes";
import type YosReaderPlugin from "../main";

export const YOS_READER_VIEW_TYPE = "yos-reader-view";

/** MVP B: updated empty state listing all 10 types. */
const EMPTY_STATE_HTML = `
<div class="yos-empty">
  <p>No YMD semantic headings found in this note.</p>
  <p>Try:</p>
  <pre>## 📦 Project
## 🏗️ Architecture
## 🧩 Component
## ✅ Decision
## ➡️ Action
## ⚠️ Risk
## ❓ Question
## 💡 Insight
## 🧠 Memory
## 🔁 Pattern</pre>
</div>
`;

export class SemanticPanel extends ItemView {
  private blocks: SemanticBlock[] = [];
  private plugin: YosReaderPlugin;

  constructor(leaf: WorkspaceLeaf, plugin: YosReaderPlugin) {
    super(leaf);
    this.plugin = plugin;
  }

  getViewType(): string { return YOS_READER_VIEW_TYPE; }
  getDisplayText(): string { return "Y-OS Reader"; }
  getIcon(): string { return "layers"; }

  async onOpen(): Promise<void> { this.renderPanel(); }
  async onClose(): Promise<void> { /* nothing */ }

  /** Called by main.ts whenever content should update. */
  public refresh(markdown: string | null): void {
    this.blocks = markdown ? parseYmdNote(markdown) : [];
    this.renderPanel();
  }

  // ─── Rendering ────────────────────────────────────────────────────────────

  private renderPanel(): void {
    const container = this.containerEl.children[1] as HTMLElement;
    container.empty();
    container.addClass("yos-reader-panel");

    if (this.blocks.length === 0) {
      container.innerHTML = EMPTY_STATE_HTML;
      return;
    }

    const grouped = this.groupBlocks(this.blocks);

    for (const typeKey of SEMANTIC_TYPE_ORDER) {
      const group = grouped[typeKey];

      // AC-B6: hide empty groups
      if (!group || group.length === 0) continue;

      const typeDef = Object.values(SEMANTIC_TYPES).find(d => d.type === typeKey);
      if (!typeDef) continue;

      const groupEl = container.createEl("div", { cls: "yos-group" });

      // AC-B5: show count in group header
      groupEl.createEl("div", {
        cls: "yos-group-header",
        text: `${typeDef.label} (${group.length})`,
      });

      for (const block of group) {
        this.renderItem(groupEl, block);
      }
    }
  }

  private renderItem(parent: HTMLElement, block: SemanticBlock): void {
    const item = parent.createEl("div", { cls: "yos-item" });
    item.createEl("span", { cls: "yos-item-emoji", text: block.emoji });
    item.createEl("span", { cls: "yos-item-title", text: block.title });

    item.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.navigateTo(block.lineStart);
    });
  }

  // ─── Navigation ───────────────────────────────────────────────────────────

  /**
   * Navigate the Markdown editor to the given line.
   *
   * Strategy (preserved from MVP A.1 patch v0.2):
   *   1. Get last known MarkdownView via plugin back-reference.
   *   2. Reveal (focus) its leaf.
   *   3. If Reading View, attempt switch to Live Preview; show Notice on fail.
   *   4. Set cursor and scroll.
   */
  private async navigateTo(lineStart: number): Promise<void> {
    const mdView = this.plugin.getLastMarkdownView();

    if (!mdView) {
      new Notice("Y-OS Reader: no Markdown note is open.");
      return;
    }

    this.app.workspace.revealLeaf(mdView.leaf);

    const state = mdView.leaf.getViewState();
    if (state?.state?.mode === "preview") {
      try {
        await mdView.leaf.setViewState({
          ...state,
          state: { ...state.state, mode: "source" },
        });
      } catch {
        new Notice(
          "Y-OS Reader: switch to Editing View to navigate to YMD headings."
        );
        return;
      }
    }

    const editor = mdView.editor;
    if (!editor) {
      new Notice("Y-OS Reader: editor not available. Open the note in Editing View.");
      return;
    }

    editor.setCursor({ line: lineStart, ch: 0 });
    editor.scrollIntoView(
      { from: { line: lineStart, ch: 0 }, to: { line: lineStart, ch: 0 } },
      true
    );

    try {
      mdView.leaf.setEphemeralState({ line: lineStart, startOfLine: true });
    } catch {
      // Non-critical
    }
  }

  // ─── Helpers ──────────────────────────────────────────────────────────────

  private groupBlocks(blocks: SemanticBlock[]): Record<string, SemanticBlock[]> {
    const result: Record<string, SemanticBlock[]> = {};
    for (const b of blocks) {
      if (!result[b.type]) result[b.type] = [];
      result[b.type].push(b);
    }
    return result;
  }
}
