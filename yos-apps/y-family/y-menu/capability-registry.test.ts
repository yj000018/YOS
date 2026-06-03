import { CapabilityRegistry } from '../src/core/capability-registry';

const registry = new CapabilityRegistry();

describe('CapabilityRegistry', () => {
  test('loads capabilities from YAML files', () => {
    registry.load();
    expect(registry.count()).toBeGreaterThan(0);
  });

  test('finds capability by ID', () => {
    const cap = registry.getById('book_factory.produce_kindle_ready_package');
    expect(cap).not.toBeUndefined();
    expect(cap?.title).toBe('Produce Kindle-ready package');
  });

  test('finds capabilities by module', () => {
    const caps = registry.getByModule('book-factory');
    expect(caps.length).toBeGreaterThan(10);
  });

  test('matches "produce kindle version" phrase', () => {
    const results = registry.findByPhrase('produce kindle version');
    expect(results.length).toBeGreaterThan(0);
    expect(results[0].score).toBeGreaterThan(0.3);
  });

  test('matches "create mini-site for my book" phrase', () => {
    const results = registry.findByPhrase('create mini-site for my book');
    expect(results.length).toBeGreaterThan(0);
    const titles = results.map(r => r.capability.title);
    const hasLovable = titles.some(t => t.toLowerCase().includes('lovable') || t.toLowerCase().includes('site'));
    expect(hasLovable).toBe(true);
  });

  test('matches "epub" phrase', () => {
    const results = registry.findByPhrase('epub');
    expect(results.length).toBeGreaterThan(0);
  });

  test('returns low-confidence results for unrelated phrase', () => {
    const results = registry.findByPhrase('xyzzy frobnicator');
    // May return some results but with low scores
    const highConfidence = results.filter(r => r.score > 0.5);
    expect(highConfidence.length).toBe(0);
  });

  test('all capabilities have required fields', () => {
    const all = registry.getAll();
    for (const cap of all) {
      expect(cap.id).toBeTruthy();
      expect(cap.title).toBeTruthy();
      expect(cap.module).toBeTruthy();
      expect(Array.isArray(cap.user_phrases)).toBe(true);
    }
  });
});
