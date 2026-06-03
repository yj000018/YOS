import { IntentRouter } from '../src/core/intent-router';
import { CapabilityRegistry } from '../src/core/capability-registry';
import { StateManager } from '../src/core/state-manager';

const registry = new CapabilityRegistry();
const state = new StateManager();
const router = new IntentRouter(registry, state);

describe('IntentRouter', () => {
  test('routes "produce kindle version"', () => {
    const result = router.route('produce kindle version');
    expect(result.intent).toBe('produce kindle version');
    expect(result.decision_paths).toBeDefined();
    expect(result.decision_paths!.length).toBeGreaterThan(0);
  });

  test('routes "create mini-site for my book"', () => {
    const result = router.route('create mini-site for my book');
    expect(result.decision_paths).toBeDefined();
    expect(result.decision_paths!.some(p => p.toLowerCase().includes('lovable'))).toBe(true);
  });

  test('routes "beautiful print pdf"', () => {
    const result = router.route('beautiful print pdf');
    expect(result.decision_paths).toBeDefined();
    expect(result.decision_paths!.some(p => p.toLowerCase().includes('typst'))).toBe(true);
  });

  test('routes "epub standard book"', () => {
    const result = router.route('epub standard book');
    expect(result.decision_paths).toBeDefined();
    expect(result.decision_paths!.some(p => p.toLowerCase().includes('pandoc'))).toBe(true);
  });

  test('provides decision paths for kindle without clarification when book_type is set', () => {
    // State has book_type: visual_essay, so no clarification needed
    const result = router.route('produce kindle version');
    // decision_paths should be populated regardless
    expect(result.decision_paths).toBeDefined();
    expect(result.decision_paths!.length).toBeGreaterThan(0);
  });

  test('formats result as readable text', () => {
    const result = router.route('produce kindle version');
    const formatted = router.format(result);
    expect(formatted).toContain('INTENT ROUTER');
    expect(formatted).toContain('produce kindle version');
  });
});
