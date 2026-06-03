// ─────────────────────────────────────────────────────────────────────────────
// Y-Menu v0 — State Manager
// Manages Y-OS session and project state
// ─────────────────────────────────────────────────────────────────────────────

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import { YMenuState, BookFactoryState } from './types';

const DEFAULT_STATE_PATH = path.join(__dirname, '../../examples/example-book-factory-state.yaml');

const DEFAULT_STATE: YMenuState = {
  session: {
    active_module: undefined,
    active_menu: 'root',
    navigation_stack: ['root'],
    last_action: undefined,
    last_result: undefined,
    recent_actions: [],
  },
  user: {
    preferred_interaction_style: 'y-com',
    preferred_output_style: 'concise_structured',
    default_language: 'fr',
  },
  book_factory: {
    active_book_id: undefined,
    active_book_title: undefined,
    manuscript: { status: 'missing' },
    assets: { cover: 'missing', images: 'missing' },
    outputs: {
      print_pdf: 'missing',
      digital_pdf: 'missing',
      epub_reflowable: 'missing',
      epub_fixed_layout: 'missing',
      kindle_package: 'missing',
      lovable_site_prompt: 'missing',
      astro_site_spec: 'missing',
    },
    distribution: {
      kdp: 'not_started',
      ingram: 'not_started',
      draft2digital: 'not_started',
    },
    recommendations: [],
  },
};

export class StateManager {
  private state: YMenuState;

  constructor(statePath?: string) {
    this.state = this.loadState(statePath);
  }

  private loadState(statePath?: string): YMenuState {
    const target = statePath || DEFAULT_STATE_PATH;
    if (fs.existsSync(target)) {
      try {
        const raw = fs.readFileSync(target, 'utf-8');
        return yaml.load(raw) as YMenuState;
      } catch {
        // fall through to default
      }
    }
    return JSON.parse(JSON.stringify(DEFAULT_STATE));
  }

  get(): YMenuState {
    return this.state;
  }

  getSession() {
    return this.state.session;
  }

  getBookFactory(): BookFactoryState | undefined {
    return this.state.book_factory;
  }

  setActiveModule(module: string): void {
    this.state.session.active_module = module;
  }

  setActiveMenu(menuId: string): void {
    this.state.session.active_menu = menuId;
    if (!this.state.session.navigation_stack) {
      this.state.session.navigation_stack = [];
    }
    this.state.session.navigation_stack.push(menuId);
  }

  navigateBack(): string | undefined {
    const stack = this.state.session.navigation_stack || [];
    if (stack.length > 1) {
      stack.pop();
      const prev = stack[stack.length - 1];
      this.state.session.active_menu = prev;
      return prev;
    }
    return stack[0];
  }

  recordAction(action: string, result?: string): void {
    this.state.session.last_action = action;
    this.state.session.last_result = result;
    if (!this.state.session.recent_actions) {
      this.state.session.recent_actions = [];
    }
    this.state.session.recent_actions.unshift(action);
    if (this.state.session.recent_actions.length > 10) {
      this.state.session.recent_actions = this.state.session.recent_actions.slice(0, 10);
    }
  }

  /**
   * Evaluate a simple condition string against current state
   * e.g. "manuscript.status == imported"
   */
  evaluateCondition(condition: string): boolean {
    const bf = this.state.book_factory;
    if (!bf) return false;

    // manuscript.status == X
    const manuscriptMatch = condition.match(/manuscript\.status\s*==\s*(\w+)/);
    if (manuscriptMatch) {
      return bf.manuscript?.status === manuscriptMatch[1];
    }

    // outputs.X == Y
    const outputMatch = condition.match(/outputs\.(\w+)\s*==\s*(\w+)/);
    if (outputMatch) {
      const [, key, val] = outputMatch;
      return bf.outputs?.[key] === val;
    }

    // distribution.X == Y
    const distMatch = condition.match(/distribution\.(\w+)\s*==\s*(\w+)/);
    if (distMatch) {
      const [, key, val] = distMatch;
      const dist = bf.distribution as Record<string, string | undefined>;
      return dist?.[key] === val;
    }

    // assets.X == Y
    const assetMatch = condition.match(/assets\.(\w+)\s*==\s*(\w+)/);
    if (assetMatch) {
      const [, key, val] = assetMatch;
      const assets = bf.assets as Record<string, string | undefined>;
      return assets?.[key] === val;
    }

    return false;
  }

  /**
   * Get recommended next actions from state
   */
  getRecommendations(): string[] {
    return this.state.book_factory?.recommendations || [];
  }

  /**
   * Get missing inputs for active book
   */
  getMissingInputs(): string[] {
    const bf = this.state.book_factory;
    if (!bf) return [];

    const missing: string[] = [];
    if (bf.manuscript?.status === 'missing') missing.push('manuscript');
    if (bf.assets?.cover === 'missing') missing.push('cover image');
    if (bf.assets?.images === 'missing') missing.push('interior images');
    return missing;
  }

  /**
   * Get completed outputs
   */
  getCompletedOutputs(): string[] {
    const outputs = this.state.book_factory?.outputs || {};
    return Object.entries(outputs)
      .filter(([, v]) => v && v !== 'missing' && v !== 'not_started')
      .map(([k]) => k);
  }

  /**
   * Get pending outputs
   */
  getPendingOutputs(): string[] {
    const outputs = this.state.book_factory?.outputs || {};
    return Object.entries(outputs)
      .filter(([, v]) => !v || v === 'missing')
      .map(([k]) => k);
  }
}

export const stateManager = new StateManager();
