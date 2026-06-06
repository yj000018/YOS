/**
 * SemanticPanel.ts — Y-OS Reader v0.5.0 (MVP D — Settings Tab)
 *
 * MVP D additions over MVP C:
 *   - Accepts YOSReaderSettings on every refresh()
 *   - showPreviews: hides/shows preview lines
 *   - compactPreviews: 40-char truncation when true (80 when false)
 *   - defaultGroupsCollapsed: initial group state on note switch
 *
 * Preserved from MVP C:
 *   - Collapsible groups (▾/▸), session-only state
 *   - Preview lines (now settings-driven)
 *   - Group counts
 *   - Hidden empty groups
 *   - Click-to-source navigation (last-valid-leaf strategy)
 *   - Reading View notice
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
import type YOSReaderPlugin from "../main";
import { YOSReaderSettings, DEFAULT_SETTINGS } from "../settings";

export const YOS_READER_VIEW_TYPE = "yos-reader-view";

/** Condensed empty state — 5 most common types. */
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
  private plugin: YOSReaderPlugin;
  private settings: YOSReaderSettings = { ...DEFAULT_SETTINGS };

  /**
   * Session-only collapsed state.
   * Key: type string. Value: true = collapsed.
   * Reset on note switch (isNoteSwitch=true) using defaultGroupsCollapsed setting.
   */
  private collapsedGroups: Set<string> = new Set();

  constructor(leaf: WorkspaceLeaf, plugin: YOSReaderPlugin) {
    super(leaf);
    this.plugin = plugin;
  }

  getViewType(): string { return YOS_READER_VIEW_TYPE; }
  getDisplayText(): string { return "Y-OS Reader"; }
  getIcon(): string { return "layers"; }

  async onOpen(): Promise<void> { this.renderPanel(); }
  async onClose(): Promise<void> { /* nothing */ }

  /**
   * Called by main.ts whenever content or settings should update.
   *
   * @param markdown  - current note content, or null to clear
   * @param isNoteSwitch - true = real note change → reset collapse state
   * @param settings  - current plugin settings
   */
  public refresh(
    markdown: string | null,
    isNoteSwitch = false,
    settings?: YOSReaderSettings
  ): void {
    if (settings) {
      this.settings = settings;
    }

    if (isNoteSwitch) {
      // Reset collapse state using defaultGroupsCollapsed setting
      this.collapsedGroups.clear();
      if (this.settings.defaultGroupsCollapsed) {
        // Pre-populate all type keys as collapsed
        for (const typeKey of SEMANTIC_TYPE_ORDER) {
          this.collapsedGroups.add(typeKey);
        }
      }
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

    // Preview line — controlled by showPreviews setting (AC-D2)
    if (this.settings.showPreviews && block.preview) {
      // Apply compactPreviews: truncate at 40 instead of 80 (AC-D3)
      let previewText = block.preview;
      if (this.settings.compactPreviews && previewText.length > 40) {
        previewText = previewText.slice(0, 40) + "…";
      }
      item.createEl("div", { cls: "yos-item-preview", text: previewText });
    }

    // Click → navigate to source
    item.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.navigateTo(block.lineStart);
    });
  }

  // ─── Navigation ───────────────────────────────────────────────────────────

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
