#!/usr/bin/env ts-node
// ─────────────────────────────────────────────────────────────────────────────
// Y-Menu v0 — CLI Entry Point
// ─────────────────────────────────────────────────────────────────────────────

import { menuLoader } from './core/menu-loader';
import { MenuRenderer } from './core/menu-renderer';
import { stateManager } from './core/state-manager';
import { capabilityRegistry } from './core/capability-registry';
import { agentSuggestionsManager } from './core/agent-suggestions';
import { IntentRouter } from './core/intent-router';
import { WorkflowComposer } from './core/workflow-composer';
import { checkTools, formatToolStatus } from './core/utils';

// ── Bootstrap ─────────────────────────────────────────────────────────────────

capabilityRegistry.load();
agentSuggestionsManager.load();

const renderer = new MenuRenderer(stateManager, agentSuggestionsManager);
const intentRouter = new IntentRouter(capabilityRegistry, stateManager);
const workflowComposer = new WorkflowComposer(stateManager);

// ── CLI Dispatch ──────────────────────────────────────────────────────────────

const [, , command, ...args] = process.argv;

switch (command) {

  case 'demo': {
    runDemo();
    break;
  }

  case 'menu': {
    const menuId = args[0] || 'root';
    const resolved = menuId === 'book-factory' ? 'book-factory.root' : menuId;
    const menu = menuLoader.load(resolved);
    if (!menu) {
      console.error(`Menu not found: ${resolved}`);
      process.exit(1);
    }
    const rendered = renderer.render(menu);
    console.log(rendered.raw);
    break;
  }

  case 'intent': {
    const phrase = args.join(' ');
    if (!phrase) {
      console.error('Usage: npm run intent -- "your goal here"');
      process.exit(1);
    }
    const result = intentRouter.route(phrase);
    console.log(intentRouter.format(result));

    // Also try workflow composer
    const composition = workflowComposer.compose(phrase);
    if (composition) {
      console.log('');
      console.log(workflowComposer.format(composition));
    }
    break;
  }

  case 'status': {
    const state = stateManager.get();
    console.log(renderer.renderStatus(state));
    break;
  }

  default: {
    console.log('Y-Menu v0 — Cognitive Orchestration Interface for Y-OS');
    console.log('');
    console.log('Commands:');
    console.log('  npm run demo              — Full interactive demo');
    console.log('  npm run menu:book         — Show Book-Factory menu');
    console.log('  npm run intent:kindle     — Route "produce kindle version"');
    console.log('  npm run intent:site       — Route "create mini-site for my book"');
    console.log('  npm run status            — Show Y-OS status');
    console.log('  npm run test              — Run tests');
    break;
  }
}

// ── Demo Function ─────────────────────────────────────────────────────────────

function runDemo(): void {
  const sep = '\n' + '═'.repeat(50) + '\n';

  console.log(sep);
  console.log('Y-MENU v0 — DEMO');
  console.log(sep);

  // 1. Root menu
  console.log('[ 1 / 5 ] Y-Menu Root');
  const rootMenu = menuLoader.load('root');
  if (rootMenu) {
    const rendered = renderer.render(rootMenu, { compact: true });
    console.log(rendered.raw);
  }

  console.log(sep);

  // 2. Book-Factory root menu
  console.log('[ 2 / 5 ] Book-Factory Module');
  const bookMenu = menuLoader.load('book-factory.root');
  if (bookMenu) {
    const rendered = renderer.render(bookMenu);
    console.log(rendered.raw);
  }

  console.log(sep);

  // 3. Intent routing: Kindle
  console.log('[ 3 / 5 ] Intent Router — "produce kindle version"');
  const kindleResult = intentRouter.route('produce kindle version');
  console.log(intentRouter.format(kindleResult));
  const kindleWorkflow = workflowComposer.compose('produce kindle version');
  if (kindleWorkflow) {
    console.log('');
    console.log(workflowComposer.format(kindleWorkflow));
  }

  console.log(sep);

  // 4. Intent routing: mini-site
  console.log('[ 4 / 5 ] Intent Router — "create mini-site for my book"');
  const siteResult = intentRouter.route('create mini-site for my book');
  console.log(intentRouter.format(siteResult));
  const siteWorkflow = workflowComposer.compose('create mini-site for my book');
  if (siteWorkflow) {
    console.log('');
    console.log(workflowComposer.format(siteWorkflow));
  }

  console.log(sep);

  // 5. Status + tool check
  console.log('[ 5 / 5 ] Y-OS Status + Tool Availability');
  const state = stateManager.get();
  console.log(renderer.renderStatus(state));
  console.log('');
  const toolStatus = checkTools(['typst', 'pandoc', 'epubcheck']);
  console.log(formatToolStatus(toolStatus));

  console.log(sep);
  console.log('Demo complete. Run `npm run menu:book` to explore interactively.');
}
