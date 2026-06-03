import { WorkflowComposer } from '../src/core/workflow-composer';
import { StateManager } from '../src/core/state-manager';

const state = new StateManager();
const composer = new WorkflowComposer(state);

describe('WorkflowComposer', () => {
  test('composes kindle workflow', () => {
    const result = composer.compose('produce kindle version');
    expect(result).not.toBeNull();
    expect(result!.goal).toContain('Kindle');
    expect(result!.steps.length).toBeGreaterThan(2);
    expect(result!.tools.length).toBeGreaterThan(0);
  });

  test('composes full edition workflow', () => {
    const result = composer.compose('publish full edition');
    expect(result).not.toBeNull();
    expect(result!.goal).toContain('full edition');
    expect(result!.steps.length).toBeGreaterThan(5);
  });

  test('composes lovable site workflow', () => {
    const result = composer.compose('create mini-site for my book');
    expect(result).not.toBeNull();
    expect(result!.goal.toLowerCase()).toContain('lovable');
  });

  test('composes astro site workflow', () => {
    const result = composer.compose('generate astro industrial site');
    expect(result).not.toBeNull();
    expect(result!.goal.toLowerCase()).toContain('astro');
  });

  test('returns null for unknown goal', () => {
    const result = composer.compose('xyzzy frobnicator');
    expect(result).toBeNull();
  });

  test('formats composition as readable text', () => {
    const result = composer.compose('produce kindle version');
    expect(result).not.toBeNull();
    const formatted = composer.format(result!);
    expect(formatted).toContain('WORKFLOW COMPOSER');
    expect(formatted).toContain('Steps:');
  });

  test('includes missing inputs from state', () => {
    const result = composer.compose('produce kindle version');
    expect(result).not.toBeNull();
    // State has cover missing, so it should appear
    expect(result!.missing_inputs).toContain('cover image');
  });
});
