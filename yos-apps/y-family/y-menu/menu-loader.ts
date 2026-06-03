// ─────────────────────────────────────────────────────────────────────────────
// Y-Menu v0 — Menu Loader
// Loads YAML menu definitions from disk
// ─────────────────────────────────────────────────────────────────────────────

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import { MenuDefinition } from './types';

const MENUS_DIR = path.join(__dirname, '../../menus');

export class MenuLoader {
  private cache: Map<string, MenuDefinition> = new Map();

  /**
   * Load a menu by its dot-notation ID (e.g. "book-factory.root")
   */
  load(menuId: string): MenuDefinition | null {
    if (this.cache.has(menuId)) {
      return this.cache.get(menuId)!;
    }

    const filePath = this.resolveMenuPath(menuId);
    if (!filePath || !fs.existsSync(filePath)) {
      return null;
    }

    try {
      const raw = fs.readFileSync(filePath, 'utf-8');
      const menu = yaml.load(raw) as MenuDefinition;
      this.cache.set(menuId, menu);
      return menu;
    } catch (err) {
      console.error(`[MenuLoader] Failed to load menu "${menuId}": ${err}`);
      return null;
    }
  }

  /**
   * Load all menus from a module directory
   */
  loadModule(moduleName: string): MenuDefinition[] {
    const moduleDir = path.join(MENUS_DIR, 'modules', moduleName);
    if (!fs.existsSync(moduleDir)) return [];

    const files = fs.readdirSync(moduleDir).filter(f => f.endsWith('.menu.yaml'));
    return files
      .map(f => {
        const raw = fs.readFileSync(path.join(moduleDir, f), 'utf-8');
        try {
          return yaml.load(raw) as MenuDefinition;
        } catch {
          return null;
        }
      })
      .filter((m): m is MenuDefinition => m !== null);
  }

  /**
   * Load root Y-Menu
   */
  loadRoot(): MenuDefinition | null {
    return this.load('root');
  }

  /**
   * List all available menu IDs
   */
  listAll(): string[] {
    const ids: string[] = [];
    this.scanDir(MENUS_DIR, ids, '');
    return ids;
  }

  private scanDir(dir: string, ids: string[], prefix: string): void {
    if (!fs.existsSync(dir)) return;
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isDirectory()) {
        this.scanDir(path.join(dir, entry.name), ids, prefix ? `${prefix}.${entry.name}` : entry.name);
      } else if (entry.name.endsWith('.menu.yaml')) {
        const base = entry.name.replace('.menu.yaml', '');
        const id = prefix ? `${prefix}.${base}` : base;
        ids.push(id);
      }
    }
  }

  private resolveMenuPath(menuId: string): string | null {
    // "root" → menus/root.menu.yaml
    // "book-factory.root" → menus/modules/book-factory/root.menu.yaml
    // "book-factory.build" → menus/modules/book-factory/build.menu.yaml

    const parts = menuId.split('.');

    if (parts.length === 1) {
      return path.join(MENUS_DIR, `${parts[0]}.menu.yaml`);
    }

    if (parts.length === 2) {
      const [module, menuName] = parts;
      return path.join(MENUS_DIR, 'modules', module, `${menuName}.menu.yaml`);
    }

    return null;
  }

  clearCache(): void {
    this.cache.clear();
  }
}

export const menuLoader = new MenuLoader();
