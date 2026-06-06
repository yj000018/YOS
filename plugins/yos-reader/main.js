var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/main.ts
var main_exports = {};
__export(main_exports, {
  default: () => YosReaderPlugin
});
module.exports = __toCommonJS(main_exports);
var import_obsidian2 = require("obsidian");

// src/panels/SemanticPanel.ts
var import_obsidian = require("obsidian");

// src/parser/semanticTypes.ts
var SEMANTIC_TYPES = {
  "\u{1F4E6}": { type: "project", label: "Projects" },
  "\u{1F3D7}\uFE0F": { type: "architecture", label: "Architecture" },
  "\u{1F9E9}": { type: "component", label: "Components" },
  "\u2705": { type: "decision", label: "Decisions" },
  "\u27A1\uFE0F": { type: "action", label: "Actions" },
  "\u26A0\uFE0F": { type: "risk", label: "Risks" },
  "\u2753": { type: "question", label: "Questions" },
  "\u{1F4A1}": { type: "insight", label: "Insights" },
  "\u{1F9E0}": { type: "memory", label: "Memories" },
  "\u{1F501}": { type: "pattern", label: "Patterns" }
};
var SEMANTIC_TYPE_ORDER = Object.values(SEMANTIC_TYPES).map(
  (def) => def.type
);
var EMOJI_VARIANTS = {
  "\u27A1": "\u27A1\uFE0F",
  // ➡  → ➡️
  "\u26A0": "\u26A0\uFE0F"
  // ⚠  → ⚠️
};

// src/parser/ymdParser.ts
var HEADING_RE = /^(#{1,6})\s+(.+)$/;
var PREVIEW_STRIP_RE = /^(?:#{1,6}|[*\->])\s*/;
function extractPreview(content) {
  if (!content || content.trim().length === 0)
    return void 0;
  const lines = content.split("\n");
  const firstLine = lines.find((l) => l.trim().length > 0);
  if (!firstLine)
    return void 0;
  let stripped = firstLine.trim();
  let prev = "";
  while (stripped !== prev) {
    prev = stripped;
    stripped = stripped.replace(PREVIEW_STRIP_RE, "").trim();
  }
  if (stripped.length === 0)
    return void 0;
  return stripped.length > 80 ? stripped.slice(0, 80) : stripped;
}
function normalizeEmoji(text) {
  let result = text;
  for (const [bare, canonical] of Object.entries(EMOJI_VARIANTS)) {
    result = result.split(bare).join(canonical);
  }
  return result;
}
function extractSemanticEmoji(headingText) {
  const normalized = normalizeEmoji(headingText);
  for (const emoji of Object.keys(SEMANTIC_TYPES)) {
    if (normalized.startsWith(emoji)) {
      const rest = normalized.slice(emoji.length).trimStart();
      return { emoji, rest };
    }
  }
  return null;
}
function parseYmdNote(markdown) {
  if (!markdown || markdown.trim().length === 0)
    return [];
  const lines = markdown.split("\n");
  const blocks = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    const headingMatch = line.match(HEADING_RE);
    if (headingMatch) {
      const level = headingMatch[1].length;
      const headingText = headingMatch[2].trim();
      const extracted = extractSemanticEmoji(headingText);
      if (extracted) {
        const { emoji, rest } = extracted;
        const typeDef = SEMANTIC_TYPES[emoji];
        const lineStart = i;
        const contentLines = [];
        let j = i + 1;
        while (j < lines.length) {
          const nextLine = lines[j];
          const nextHeading = nextLine.match(HEADING_RE);
          if (nextHeading && nextHeading[1].length <= level) {
            break;
          }
          contentLines.push(nextLine);
          j++;
        }
        while (contentLines.length > 0 && contentLines[contentLines.length - 1].trim() === "") {
          contentLines.pop();
        }
        const contentStr = contentLines.join("\n").trim();
        const title = rest.length > 0 ? rest : typeDef.label;
        blocks.push({
          type: typeDef.type,
          emoji,
          label: typeDef.label,
          title,
          content: contentStr,
          preview: extractPreview(contentStr),
          lineStart,
          lineEnd: j - 1
        });
        i = j;
        continue;
      }
    }
    i++;
  }
  return blocks;
}

// src/panels/SemanticPanel.ts
var YOS_READER_VIEW_TYPE = "yos-reader-view";
var EMPTY_STATE_HTML = `
<div class="yos-empty">
  <p class="yos-empty-title">No YMD semantic headings found.</p>
  <p class="yos-empty-hint">Start with:</p>
  <pre class="yos-empty-examples">## \u2705 Decision
## \u27A1\uFE0F Action
## \u2753 Question
## \u{1F9E0} Memory
## \u{1F4A1} Insight</pre>
</div>
`;
var SemanticPanel = class extends import_obsidian.ItemView {
  constructor(leaf, plugin) {
    super(leaf);
    this.blocks = [];
    /**
     * Session-only collapsed state.
     * Key: type string (e.g. "decision"). Value: true = collapsed.
     * Reset to empty on every note switch (via refresh()).
     */
    this.collapsedGroups = /* @__PURE__ */ new Set();
    this.plugin = plugin;
  }
  getViewType() {
    return YOS_READER_VIEW_TYPE;
  }
  getDisplayText() {
    return "Y-OS Reader";
  }
  getIcon() {
    return "layers";
  }
  async onOpen() {
    this.renderPanel();
  }
  async onClose() {
  }
  /**
   * Called by main.ts whenever content should update.
   * AC-C6: collapsed state resets only on note switch (isNoteSwitch=true).
   * Editor-change and sidebar-focus refreshes preserve collapse state.
   */
  refresh(markdown, isNoteSwitch = false) {
    if (isNoteSwitch) {
      this.collapsedGroups.clear();
    }
    this.blocks = markdown ? parseYmdNote(markdown) : [];
    this.renderPanel();
  }
  // ─── Rendering ────────────────────────────────────────────────────────────
  renderPanel() {
    const container = this.containerEl.children[1];
    container.empty();
    container.addClass("yos-reader-panel");
    if (this.blocks.length === 0) {
      container.innerHTML = EMPTY_STATE_HTML;
      return;
    }
    const grouped = this.groupBlocks(this.blocks);
    for (const typeKey of SEMANTIC_TYPE_ORDER) {
      const group = grouped[typeKey];
      if (!group || group.length === 0)
        continue;
      const typeDef = Object.values(SEMANTIC_TYPES).find((d) => d.type === typeKey);
      if (!typeDef)
        continue;
      this.renderGroup(container, typeKey, typeDef.label, group);
    }
  }
  renderGroup(container, typeKey, label, group) {
    const isCollapsed = this.collapsedGroups.has(typeKey);
    const groupEl = container.createEl("div", { cls: "yos-group" });
    const headerEl = groupEl.createEl("div", {
      cls: `yos-group-header${isCollapsed ? " yos-group-collapsed" : ""}`
    });
    headerEl.createEl("span", {
      cls: "yos-group-toggle",
      text: isCollapsed ? "\u25B8" : "\u25BE"
    });
    headerEl.createEl("span", {
      cls: "yos-group-label",
      text: `${label} (${group.length})`
    });
    const itemsEl = groupEl.createEl("div", {
      cls: `yos-group-items${isCollapsed ? " yos-hidden" : ""}`
    });
    for (const block of group) {
      this.renderItem(itemsEl, block);
    }
    headerEl.addEventListener("click", () => {
      if (this.collapsedGroups.has(typeKey)) {
        this.collapsedGroups.delete(typeKey);
        headerEl.removeClass("yos-group-collapsed");
        headerEl.querySelector(".yos-group-toggle").textContent = "\u25BE";
        itemsEl.removeClass("yos-hidden");
      } else {
        this.collapsedGroups.add(typeKey);
        headerEl.addClass("yos-group-collapsed");
        headerEl.querySelector(".yos-group-toggle").textContent = "\u25B8";
        itemsEl.addClass("yos-hidden");
      }
    });
  }
  renderItem(parent, block) {
    const item = parent.createEl("div", { cls: "yos-item" });
    const titleRow = item.createEl("div", { cls: "yos-item-title-row" });
    titleRow.createEl("span", { cls: "yos-item-emoji", text: block.emoji });
    titleRow.createEl("span", { cls: "yos-item-title", text: block.title });
    if (block.preview) {
      item.createEl("div", { cls: "yos-item-preview", text: block.preview });
    }
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
  async navigateTo(lineStart) {
    var _a;
    const mdView = this.plugin.getLastMarkdownView();
    if (!mdView) {
      new import_obsidian.Notice("Y-OS Reader: no Markdown note is open.");
      return;
    }
    this.app.workspace.revealLeaf(mdView.leaf);
    const state = mdView.leaf.getViewState();
    if (((_a = state == null ? void 0 : state.state) == null ? void 0 : _a.mode) === "preview") {
      try {
        await mdView.leaf.setViewState({
          ...state,
          state: { ...state.state, mode: "source" }
        });
      } catch (e) {
        new import_obsidian.Notice(
          "Y-OS Reader: switch to Editing View to navigate to YMD headings."
        );
        return;
      }
    }
    const editor = mdView.editor;
    if (!editor) {
      new import_obsidian.Notice("Y-OS Reader: editor not available. Open the note in Editing View.");
      return;
    }
    editor.setCursor({ line: lineStart, ch: 0 });
    editor.scrollIntoView(
      { from: { line: lineStart, ch: 0 }, to: { line: lineStart, ch: 0 } },
      true
    );
    try {
      mdView.leaf.setEphemeralState({ line: lineStart, startOfLine: true });
    } catch (e) {
    }
  }
  // ─── Helpers ──────────────────────────────────────────────────────────────
  groupBlocks(blocks) {
    const result = {};
    for (const b of blocks) {
      if (!result[b.type])
        result[b.type] = [];
      result[b.type].push(b);
    }
    return result;
  }
};

// src/main.ts
var YosReaderPlugin = class extends import_obsidian2.Plugin {
  constructor() {
    super(...arguments);
    /** Last Markdown leaf that was genuinely active (not the sidebar). */
    this.lastMarkdownLeaf = null;
  }
  async onload() {
    this.registerView(
      YOS_READER_VIEW_TYPE,
      (leaf) => new SemanticPanel(leaf, this)
    );
    this.addRibbonIcon("layers", "Y-OS Reader", () => {
      this.activateView();
    });
    this.addCommand({
      id: "open-yos-reader",
      name: "Open Y-OS Reader",
      callback: () => this.activateView()
    });
    this.registerEvent(
      this.app.workspace.on("active-leaf-change", (leaf) => {
        var _a;
        if (!leaf)
          return;
        if (((_a = leaf.view) == null ? void 0 : _a.getViewType()) === YOS_READER_VIEW_TYPE) {
          this.refreshPanel(false);
          return;
        }
        const mdView = leaf.view instanceof import_obsidian2.MarkdownView ? leaf.view : null;
        if (mdView) {
          this.lastMarkdownLeaf = leaf;
        } else {
          this.lastMarkdownLeaf = null;
        }
        this.refreshPanel(true);
      })
    );
    this.registerEvent(
      this.app.workspace.on("file-open", (file) => {
        if (!file) {
          this.lastMarkdownLeaf = null;
          this.refreshPanel(true);
          return;
        }
        const mdView = this.app.workspace.getActiveViewOfType(import_obsidian2.MarkdownView);
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
  async onunload() {
    this.app.workspace.detachLeavesOfType(YOS_READER_VIEW_TYPE);
  }
  // ── Panel lifecycle ────────────────────────────────────────────────────────
  async activateView() {
    const { workspace } = this.app;
    let leaf = workspace.getLeavesOfType(YOS_READER_VIEW_TYPE)[0];
    if (!leaf) {
      const rightLeaf = workspace.getRightLeaf(false);
      if (!rightLeaf)
        return;
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
  refreshPanel(allowClear) {
    const leaves = this.app.workspace.getLeavesOfType(YOS_READER_VIEW_TYPE);
    if (leaves.length === 0)
      return;
    const panel = leaves[0].view;
    let mdView = this.app.workspace.getActiveViewOfType(import_obsidian2.MarkdownView);
    if (!mdView && this.lastMarkdownLeaf) {
      const v = this.lastMarkdownLeaf.view;
      if (v instanceof import_obsidian2.MarkdownView) {
        mdView = v;
      }
    }
    if (!mdView || !mdView.file) {
      if (allowClear) {
        panel.refresh(null);
      }
      return;
    }
    this.lastMarkdownLeaf = mdView.leaf;
    const markdown = mdView.editor.getValue();
    panel.refresh(markdown, allowClear);
  }
  /**
   * Exposed for SemanticPanel to call back into the plugin and get the
   * last known MarkdownView for navigation.
   */
  getLastMarkdownView() {
    const active = this.app.workspace.getActiveViewOfType(import_obsidian2.MarkdownView);
    if (active)
      return active;
    if (this.lastMarkdownLeaf) {
      const v = this.lastMarkdownLeaf.view;
      if (v instanceof import_obsidian2.MarkdownView)
        return v;
    }
    return null;
  }
};
