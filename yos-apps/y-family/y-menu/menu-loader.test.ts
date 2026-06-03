import { MenuLoader } from '../src/core/menu-loader';

const loader = new MenuLoader();

describe('MenuLoader', () => {
  test('loads root menu', () => {
    const menu = loader.load('root');
    expect(menu).not.toBeNull();
    expect(menu?.id).toBe('root');
  });

  test('loads book-factory root menu', () => {
    const menu = loader.load('book-factory.root');
    expect(menu).not.toBeNull();
    expect(menu?.id).toBe('book-factory.root');
  });

  test('loads book-factory build menu', () => {
    const menu = loader.load('book-factory.build');
    expect(menu).not.toBeNull();
    expect(menu?.id).toBe('book-factory.build');
  });

  test('returns null for non-existent menu', () => {
    const menu = loader.load('non-existent.menu');
    expect(menu).toBeNull();
  });

  test('all menu items have unique IDs within each menu', () => {
    const menus = [
      'root',
      'book-factory.root',
      'book-factory.import',
      'book-factory.design',
      'book-factory.build',
      'book-factory.website',
      'book-factory.distribution',
      'book-factory.release',
      'book-factory.diagnostics',
      'book-factory.sync',
    ];

    for (const menuId of menus) {
      const menu = loader.load(menuId);
      if (!menu) continue;
      const ids = menu.items.map(i => i.id);
      const uniqueIds = new Set(ids);
      expect(uniqueIds.size).toBe(ids.length);
    }
  });

  test('all menu items have required fields', () => {
    const menu = loader.load('book-factory.root');
    expect(menu).not.toBeNull();
    for (const item of menu!.items) {
      expect(item.id).toBeTruthy();
      expect(item.label).toBeTruthy();
      expect(item.action_type).toBeTruthy();
    }
  });
});
