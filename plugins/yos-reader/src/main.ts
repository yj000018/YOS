/**
 * main.ts — Y-OS Reader v0.5.0 (MVP D — Settings Tab)
 *
 * Changes from v0.4.0:
 *   - Loads YOSReaderSettings via loadData (merged with DEFAULT_SETTINGS)
 *   - Registers YOSReaderSettingTab
 *   - Passes settings to SemanticPanel on every refresh
 *
 * Preserved from v0.4.0:
 *   - lastMarkdownLeaf tracking (sidebar-focus bug fix)
 *   - refreshPanel(allowClear) logic
 *   - getLastMarkdownView() for navigation
 */

import {
  Plugin,
  MarkdownView,
  TFile,
  WorkspaceLeaf,
} from "obsidian";
import { SemanticPanel, YOS_READER_VIEW_TYPE } from "./panels/SemanticPanel";
import {
  YOSReaderSettings,
  DEFAULT_SETTINGS,
  YOSReaderSettingTab,
} from "./settings";

export default class YOSReaderPlugin extends Plugin {
  /** Persisted settings (loaded from Obsidian data store). */
  public settings: YOSReaderSettings = { ...DEFAULT_SETTINGS };

  /** Last Markdown leaf that was genuinely active (not the sidebar). */
  private lastMarkdownLeaf: WorkspaceLeaf | null = null;

  async onload(): Promise<void> {
    // Load persisted settings, merging with defaults to handle new fields
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());

    // Register the sidebar view
    this.registerView(
      YOS_READER_VIEW_TYPE,
      (leaf: WorkspaceLeaf) => new SemanticPanel(leaf, this)
    );

    // Register Settings Tab
    this.addSettingTab(new YOSReaderSettingTab(this.app, this));

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

    this.registerEvent(
      this.app.workspace.on("active-leaf-change", (leaf: WorkspaceLeaf | null) => {
        if (!leaf) return;

        if (leaf.view?.getViewType() === YOS_READER_VIEW_TYPE) {
          this.refreshPanel(false);
          return;
        }

        const mdView = leaf.view instanceof MarkdownView ? leaf.view : null;
        if (mdView) {
          this.lastMarkdownLeaf = leaf;
        } else {
          this.lastMarkdownLeaf = null;
        }

        this.refreshPanel(true);
      })
    );

    this.registerEvent(
      this.app.workspace.on("file-open", (file: TFile | null) => {
        if (!file) {
          this.lastMarkdownLeaf = null;
          this.refreshPanel(true);
          return;
        }
        const mdView = this.app.workspace.getActiveViewOfType(MarkdownView);
        if (mdView) {
          this.lastMarkdownLeaf = mdView.leaf;
        }
        this.refreshPanel(true);
      })
    );

    this.registerEvent(
      this.app.workspace.on("editor-change", () => {
        this.refreshPanel(false);
      })
    );

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
   * Push current Markdown content + settings to the panel.
   *
   * @param allowClear - if true, clears the panel when no Markdown is found.
   *   Pass false when the trigger is sidebar focus or editor-change.
   */
  public refreshPanel(allowClear: boolean): void {
    const leaves = this.app.workspace.getLeavesOfType(YOS_READER_VIEW_TYPE);
    if (leaves.length === 0) return;

    const panel = leaves[0].view as SemanticPanel;

    let mdView = this.app.workspace.getActiveViewOfType(MarkdownView);

    if (!mdView && this.lastMarkdownLeaf) {
      const v = this.lastMarkdownLeaf.view;
      if (v instanceof MarkdownView) {
        mdView = v;
      }
    }

    if (!mdView || !mdView.file) {
      if (allowClear) {
        panel.refresh(null, true, this.settings);
      }
      return;
    }

    this.lastMarkdownLeaf = mdView.leaf;

    const markdown = mdView.editor.getValue();
    panel.refresh(markdown, allowClear, this.settings);
  }

  /**
   * Exposed for SemanticPanel navigation and for settings tab re-render.
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
