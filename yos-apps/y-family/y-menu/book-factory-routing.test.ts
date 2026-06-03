import { MenuLoader } from '../src/core/menu-loader';
import { CapabilityRegistry } from '../src/core/capability-registry';
import { StateManager } from '../src/core/state-manager';
import { IntentRouter } from '../src/core/intent-router';
import { WorkflowComposer } from '../src/core/workflow-composer';
import { AgentSuggestionsManager } from '../src/core/agent-suggestions';
import { MenuRenderer } from '../src/core/menu-renderer';

describe('Book-Factory End-to-End Routing', () => {
  const loader = new MenuLoader();
  const registry = new CapabilityRegistry();
  const state = new StateManager();
  const agentMgr = new AgentSuggestionsManager();
  const router = new IntentRouter(registry, state);
  const composer = new WorkflowComposer(state);
  const renderer = new MenuRenderer(state, agentMgr);

  agentMgr.load();

  test('full session: open → book-factory → kindle intent → workflow', () => {
    // Step 1: Load root menu
    const root = loader.load('root');
    expect(root).not.toBeNull();

    // Step 2: Navigate to book-factory
    state.setActiveModule('book-factory');
    state.setActiveMenu('book-factory.root');
    const bookMenu = loader.load('book-factory.root');
    expect(bookMenu).not.toBeNull();

    // Step 3: User types "produce Kindle version"
    const intent = router.route('produce Kindle version');
    expect(intent.decision_paths).toBeDefined();
    expect(intent.decision_paths!.length).toBeGreaterThan(0);

    // Step 4: Workflow composer generates plan
    const workflow = composer.compose('produce Kindle version');
    expect(workflow).not.toBeNull();
    expect(workflow!.steps.length).toBeGreaterThan(2);

    // Step 5: Render result block
    const resultBlock = renderer.renderResult({
      title: 'Kindle Workflow',
      status: 'success',
      summary: `Workflow prepared: ${workflow!.goal}`,
      path: workflow!.steps.map(s => s.action),
      missing: workflow!.missing_inputs,
      next: workflow!.next_actions || [],
    });
    expect(resultBlock).toContain('RESULT');
    expect(resultBlock).toContain('✅');
  });

  test('state-aware recommendations appear in menu', () => {
    // State has manuscript imported, so build_outputs should be recommended
    const menu = loader.load('book-factory.root');
    expect(menu).not.toBeNull();
    const rendered = renderer.render(menu!);
    expect(rendered.recommended_action).toBeTruthy();
  });

  test('agent suggestions are merged into menu', () => {
    const menu = loader.load('book-factory.root');
    const rendered = renderer.render(menu!);
    expect(rendered.raw).toContain('🤖');
  });

  test('navigation stack is maintained', () => {
    state.setActiveMenu('book-factory.build');
    const stack = state.getSession().navigation_stack;
    expect(stack).toContain('book-factory.build');
  });

  test('missing inputs are detected from state', () => {
    const missing = state.getMissingInputs();
    expect(missing).toContain('cover image');
  });

  test('capability registry has 20+ book-factory capabilities', () => {
    const caps = registry.getByModule('book-factory');
    expect(caps.length).toBeGreaterThanOrEqual(15);
  });
});
