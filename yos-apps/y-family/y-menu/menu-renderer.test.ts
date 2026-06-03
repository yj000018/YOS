import { MenuLoader } from '../src/core/menu-loader';
import { MenuRenderer } from '../src/core/menu-renderer';
import { StateManager } from '../src/core/state-manager';
import { AgentSuggestionsManager } from '../src/core/agent-suggestions';

const loader = new MenuLoader();
const state = new StateManager();
const agentMgr = new AgentSuggestionsManager();
agentMgr.load();
const renderer = new MenuRenderer(state, agentMgr);

describe('MenuRenderer', () => {
  test('renders root menu', () => {
    const menu = loader.load('root');
    expect(menu).not.toBeNull();
    const rendered = renderer.render(menu!);
    expect(rendered.raw).toContain('Y-MENU');
    expect(rendered.item_count).toBeGreaterThan(0);
  });

  test('renders book-factory root menu', () => {
    const menu = loader.load('book-factory.root');
    expect(menu).not.toBeNull();
    const rendered = renderer.render(menu!);
    expect(rendered.raw).toContain('Y-PUBLISHING FACTORY');
    expect(rendered.item_count).toBeGreaterThan(5);
  });

  test('rendered menu contains numbered emoji options', () => {
    const menu = loader.load('book-factory.root');
    const rendered = renderer.render(menu!);
    expect(rendered.raw).toContain('1️⃣');
    expect(rendered.raw).toContain('2️⃣');
  });

  test('rendered menu contains command hints', () => {
    const menu = loader.load('book-factory.root');
    const rendered = renderer.render(menu!);
    expect(rendered.raw).toContain('Commands:');
    expect(rendered.raw).toContain('home');
  });

  test('rendered menu shows recommended action when applicable', () => {
    const menu = loader.load('book-factory.root');
    const rendered = renderer.render(menu!);
    // State has manuscript imported, so some recommendation should appear
    expect(rendered.raw).toContain('⭐');
  });

  test('renders status block', () => {
    const state2 = new StateManager();
    const status = renderer.renderStatus(state2.get());
    expect(status).toContain('Y-OS STATUS');
    expect(status).toContain('Book-Factory');
  });

  test('renders result block', () => {
    const result = renderer.renderResult({
      title: 'Test',
      status: 'success',
      summary: 'Workflow prepared: Kindle-ready package',
      path: ['Markdown manuscript', 'Pandoc EPUB', 'KDP checklist'],
      missing: ['Cover image'],
      next: ['Generate cover brief', 'Build EPUB draft'],
    });
    expect(result).toContain('RESULT');
    expect(result).toContain('✅');
    expect(result).toContain('Cover image');
  });

  test('merges agent suggestions into menu', () => {
    const menu = loader.load('book-factory.root');
    const rendered = renderer.render(menu!);
    // Agent suggestions should be merged (🤖 marker)
    expect(rendered.raw).toContain('🤖');
  });
});
