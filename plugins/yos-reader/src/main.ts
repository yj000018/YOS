/**
 * main.ts — Y-OS Reader, YMD Reader MVP (patch v0.2)
 *
 * Root cause fix: when the user clicks the Y-OS Reader sidebar, Obsidian
 * sets the sidebar leaf as the "active leaf", so getActiveViewOfType(MarkdownView)
 * returns null and the panel incorrectly clears.
 *
 * Fix strategy:
 *   1. Keep a `lastMarkdownLeaf` reference — updated only when a real
 *      MarkdownView becomes active.
 *   2. refreshPanel() uses getActiveViewOfType first; if null, falls back to
 *      lastMarkdownLeaf (still valid when sidebar is focused).
 *   3. Panel is cleared only when the active FILE genuinely changes to a
 *      non-Markdown file or no file is open — not merely because focus moved
 *      to the sidebar.
 */

import {
  Plugin,
  MarkdownView,
  TFile,
  WorkspaceLeaf,
} from "obsidian";
import { SemanticPanel, YOS_READER_VIEW_TYPE } from "./panels/SemanticPanel";

export default class YosReaderPlugin extends Plugin {
  /** Last Markdown leaf that was genuinely active (not the sidebar). */
  private lastMarkdownLeaf: WorkspaceLeaf | null = null;

  async onload(): Promise<void> {
    // Register the sidebar view — pass `this` so the panel can call
    // getLastMarkdownView() for navigation without relying on active leaf.
    this.registerView(
      YOS_READER_VIEW_TYPE,
      (leaf: WorkspaceLeaf) => new SemanticPanel(leaf, this)
    );

    // Ribbon icon
    this.addRibbonIcon("layers", "Y-OS Reader", () => {
      this.activateView();
    });

    // Command palette
    this.addCommand({
      id: "open-yos-reader",
      name: "Open Y-OS Reader",
      callback: () => this.activateView(),
    });

    // ── Event wiring ────────────────────────────────────────────────────────

    // Track active-leaf-change: only update lastMarkdownLeaf when the new
    // active leaf is a real MarkdownView (not our own sidebar).
    this.registerEvent(
      this.app.workspace.on("active-leaf-change", (leaf: WorkspaceLeaf | null) => {
        if (!leaf) return;

        // If the newly active leaf is the Y-OS Reader sidebar, do NOT clear
        // lastMarkdownLeaf — just refresh using the stored reference.
        if (leaf.view?.getViewType() === YOS_READER_VIEW_TYPE) {
          this.refreshPanel(false); // false = don't clear on sidebar focus
          return;
        }

        // Real leaf change: update reference if it's a MarkdownView
        const mdView = leaf.view instanceof MarkdownView ? leaf.view : null;
        if (mdView) {
          this.lastMarkdownLeaf = leaf;
        } else {
          // Non-markdown leaf (e.g. canvas, image) → clear
          this.lastMarkdownLeaf = null;
        }

        this.refreshPanel(true);
      })
    );

    // File opened
    this.registerEvent(
      this.app.workspace.on("file-open", (file: TFile | null) => {
        if (!file) {
          this.lastMarkdownLeaf = null;
          this.refreshPanel(true);
          return;
        }
        // Update lastMarkdownLeaf if the newly opened file is in a MarkdownView
        const mdView = this.app.workspace.getActiveViewOfType(MarkdownView);
        if (mdView) {
          this.lastMarkdownLeaf = mdView.leaf;
        }
        this.refreshPanel(true);
      })
    );

    // Editor content changes (live editing)
    this.registerEvent(
      this.app.workspace.on("editor-change", () => {
        // Always refresh from current content; sidebar focus doesn't trigger this
        this.refreshPanel(false);
      })
    );

    // Initial render
    this.app.workspace.onLayoutReady(() => {
      this.refreshPanel(true);
    });
  }

  async onunload(): Promise<void> {
    this.app.workspace.detachLeavesOfType(YOS_READER_VIEW_TYPE);
  }

  // ── Panel lifecycle ────────────────────────────────────────────────────────

  private async activateView(): Promise<void> {
    const { workspace } = this.app;
    let leaf = workspace.getLeavesOfType(YOS_READER_VIEW_TYPE)[0];

    if (!leaf) {
      const rightLeaf = workspace.getRightLeaf(false);
      if (!rightLeaf) return;
      leaf = rightLeaf;
      await leaf.setViewState({ type: YOS_READER_VIEW_TYPE, active: true });
    }

    workspace.revealLeaf(leaf);
    this.refreshPanel(false);
  }

  /**
   * Push current Markdown content to the panel.
   *
   * @param allowClear - if true, clears the panel when no Markdown is found.
   *   Pass false when the trigger is sidebar focus (we don't want to clear
   *   just because the sidebar grabbed focus).
   */
  public refreshPanel(allowClear: boolean): void {
    const leaves = this.app.workspace.getLeavesOfType(YOS_READER_VIEW_TYPE);
    if (leaves.length === 0) return;

    const panel = leaves[0].view as SemanticPanel;

    // Prefer the currently active MarkdownView
    let mdView = this.app.workspace.getActiveViewOfType(MarkdownView);

    // Fall back to lastMarkdownLeaf if sidebar stole focus
    if (!mdView && this.lastMarkdownLeaf) {
      const v = this.lastMarkdownLeaf.view;
      if (v instanceof MarkdownView) {
        mdView = v;
      }
    }

    if (!mdView || !mdView.file) {
      if (allowClear) {
        panel.refresh(null);
      }
      // If allowClear=false (sidebar focus), keep existing panel content
      return;
    }

    // Update lastMarkdownLeaf to the one we're actually reading from
    this.lastMarkdownLeaf = mdView.leaf;

    const markdown = mdView.editor.getValue();
    panel.refresh(markdown);
  }

  /**
   * Exposed for SemanticPanel to call back into the plugin and get the
   * last known MarkdownView for navigation.
   */
  public getLastMarkdownView(): MarkdownView | null {
    const active = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (active) return active;

    if (this.lastMarkdownLeaf) {
      const v = this.lastMarkdownLeaf.view;
      if (v instanceof MarkdownView) return v;
    }
    return null;
  }
}
