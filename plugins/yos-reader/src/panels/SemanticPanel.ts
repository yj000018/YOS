/**
 * SemanticPanel.ts — Y-OS Reader, MVP C
 *
 * MVP C additions over MVP B:
 *   - Preview line rendered under each item title (always visible, no toggle)
 *   - Collapsible groups (▾ expanded / ▸ collapsed)
 *   - Collapsed state: session memory only, resets to expanded on note switch
 *   - Group counts remain visible when collapsed
 *   - Condensed empty state (5-type example)
 *   - Light visual polish via CSS classes
 *
 * Preserved from MVP B:
 *   - 10 semantic types in SEMANTIC_TYPE_ORDER
 *   - Last-valid-leaf tracking (sidebar-focus bug fix from MVP A.1)
 *   - Click-to-source navigation with Reading View notice
 *   - Read-only behavior
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

/** MVP C: condensed empty state — 5 most common types only. */
const EMPTY_STATE_HTML = `
<div class="yos-empty">
  <p class="yos-empty-title">No YMD semantic headings found.</p>
  <p class="yos-empty-hint">Start with:</p>
  <pre class="yos-empty-examples">## ✅ Decision
## ➡️ Action
## ❓ Question
## 🧠 Memory
## 💡 Insight</pre>
</div>
`;

export class SemanticPanel extends ItemView {
  private blocks: SemanticBlock[] = [];
  private plugin: YosReaderPlugin;

  /**
   * Session-only collapsed state.
   * Key: type string (e.g. "decision"). Value: true = collapsed.
   * Reset to empty on every note switch (via refresh()).
   */
  private collapsedGroups: Set<string> = new Set();

  constructor(leaf: WorkspaceLeaf, plugin: YosReaderPlugin) {
    super(leaf);
    this.plugin = plugin;
  }

  getViewType(): string { return YOS_READER_VIEW_TYPE; }
  getDisplayText(): string { return "Y-OS Reader"; }
  getIcon(): string { return "layers"; }

  async onOpen(): Promise<void> { this.renderPanel(); }
  async onClose(): Promise<void> { /* nothing */ }

  /**
   * Called by main.ts whenever content should update.
   * AC-C6: collapsed state resets only on note switch (isNoteSwitch=true).
   * Editor-change and sidebar-focus refreshes preserve collapse state.
   */
  public refresh(markdown: string | null, isNoteSwitch = false): void {
    if (isNoteSwitch) {
      this.collapsedGroups.clear();
    }
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
      if (!group || group.length === 0) continue;

      const typeDef = Object.values(SEMANTIC_TYPES).find(d => d.type === typeKey);
      if (!typeDef) continue;

      this.renderGroup(container, typeKey, typeDef.label, group);
    }
  }

  private renderGroup(
    container: HTMLElement,
    typeKey: string,
    label: string,
    group: SemanticBlock[]
  ): void {
    const isCollapsed = this.collapsedGroups.has(typeKey);
    const groupEl = container.createEl("div", { cls: "yos-group" });

    // Header with collapse toggle
    const headerEl = groupEl.createEl("div", {
      cls: `yos-group-header${isCollapsed ? " yos-group-collapsed" : ""}`,
    });

    // Toggle marker: ▾ expanded, ▸ collapsed
    headerEl.createEl("span", {
      cls: "yos-group-toggle",
      text: isCollapsed ? "▸" : "▾",
    });

    headerEl.createEl("span", {
      cls: "yos-group-label",
      text: `${label} (${group.length})`,
    });

    // Items container — hidden when collapsed
    const itemsEl = groupEl.createEl("div", {
      cls: `yos-group-items${isCollapsed ? " yos-hidden" : ""}`,
    });

    for (const block of group) {
      this.renderItem(itemsEl, block);
    }

    // Click handler on header to toggle collapse
    headerEl.addEventListener("click", () => {
      if (this.collapsedGroups.has(typeKey)) {
        this.collapsedGroups.delete(typeKey);
        headerEl.removeClass("yos-group-collapsed");
        headerEl.querySelector(".yos-group-toggle")!.textContent = "▾";
        itemsEl.removeClass("yos-hidden");
      } else {
        this.collapsedGroups.add(typeKey);
        headerEl.addClass("yos-group-collapsed");
        headerEl.querySelector(".yos-group-toggle")!.textContent = "▸";
        itemsEl.addClass("yos-hidden");
      }
    });
  }

  private renderItem(parent: HTMLElement, block: SemanticBlock): void {
    const item = parent.createEl("div", { cls: "yos-item" });

    // Title row
    const titleRow = item.createEl("div", { cls: "yos-item-title-row" });
    titleRow.createEl("span", { cls: "yos-item-emoji", text: block.emoji });
    titleRow.createEl("span", { cls: "yos-item-title", text: block.title });

    // Preview line — only when preview exists (AC-C1, AC-C4)
    if (block.preview) {
      item.createEl("div", { cls: "yos-item-preview", text: block.preview });
    }

    // Click → navigate to source (AC-C7)
    item.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.navigateTo(block.lineStart);
    });
  }

  // ─── Navigation ───────────────────────────────────────────────────────────

  /**
   * Navigate the Markdown editor to the given line.
   * Preserved from MVP A.1 patch v0.2 — last-valid-leaf strategy.
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
