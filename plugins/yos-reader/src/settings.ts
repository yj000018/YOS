import { App, PluginSettingTab, Setting } from "obsidian";
import type YOSReaderPlugin from "./main";

export interface YOSReaderSettings {
  showPreviews: boolean;
  compactPreviews: boolean;
  defaultGroupsCollapsed: boolean;
}

export const DEFAULT_SETTINGS: YOSReaderSettings = {
  showPreviews: true,
  compactPreviews: false,
  defaultGroupsCollapsed: false,
};

export class YOSReaderSettingTab extends PluginSettingTab {
  plugin: YOSReaderPlugin;

  constructor(app: App, plugin: YOSReaderPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    new Setting(containerEl)
      .setName("Show previews")
      .setDesc("Display the first content line under each heading in the sidebar.")
      .addToggle((toggle) =>
        toggle
          .setValue(this.plugin.settings.showPreviews)
          .onChange(async (value) => {
            this.plugin.settings.showPreviews = value;
            await this.plugin.saveData(this.plugin.settings);
            this.plugin.refreshPanel(false);
          })
      );

    new Setting(containerEl)
      .setName("Compact previews")
      .setDesc("Truncate previews at 40 characters instead of 80. Only applies when previews are shown.")
      .addToggle((toggle) =>
        toggle
          .setValue(this.plugin.settings.compactPreviews)
          .onChange(async (value) => {
            this.plugin.settings.compactPreviews = value;
            await this.plugin.saveData(this.plugin.settings);
            this.plugin.refreshPanel(false);
          })
      );

    new Setting(containerEl)
      .setName("Default groups collapsed")
      .setDesc("Collapse all groups when opening a note. You can still expand them manually during the session.")
      .addToggle((toggle) =>
        toggle
          .setValue(this.plugin.settings.defaultGroupsCollapsed)
          .onChange(async (value) => {
            this.plugin.settings.defaultGroupsCollapsed = value;
            await this.plugin.saveData(this.plugin.settings);
            // defaultGroupsCollapsed only takes effect on next note switch — no immediate re-render needed
          })
      );
  }
}
