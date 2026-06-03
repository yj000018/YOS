// Y-OS Universe — Breadcrumb
// Navigation trail: L0 > Planet > Moon > Satellite
// Mobile-optimized: 44px touch targets

interface BreadcrumbItem {
  label: string;
  level: number;
  color?: string;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  onNavigate: (level: number) => void;
  currentLevel: number;
}

export default function Breadcrumb({ items, onNavigate, currentLevel }: BreadcrumbProps) {
  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      zIndex: 50,
      display: 'flex',
      alignItems: 'center',
      padding: '0 16px',
      height: 52,
      background: 'rgba(4, 4, 12, 0.85)',
      backdropFilter: 'blur(10px)',
      borderBottom: '1px solid rgba(255,255,255,0.06)',
      gap: 0,
      overflowX: 'auto',
    }}>
      {/* Level badge */}
      <div style={{
        fontSize: 11,
        color: '#666688',
        fontFamily: '"Space Mono", monospace',
        marginRight: 12,
        flexShrink: 0,
        background: 'rgba(255,255,255,0.06)',
        padding: '3px 8px',
        borderRadius: 4,
      }}>
        L{currentLevel}
      </div>

      {items.map((item, i) => (
        <div key={i} style={{ display: 'flex', alignItems: 'center', flexShrink: 0 }}>
          {i > 0 && (
            <span style={{ color: '#333355', margin: '0 6px', fontSize: 14 }}>›</span>
          )}
          <button
            onClick={() => onNavigate(item.level)}
            style={{
              background: 'none',
              border: 'none',
              color: i === items.length - 1 ? (item.color || '#FFFFFF') : '#888899',
              fontSize: 13,
              fontFamily: '"Space Mono", monospace',
              fontWeight: i === items.length - 1 ? 700 : 400,
              cursor: i < items.length - 1 ? 'pointer' : 'default',
              padding: '8px 6px',
              minHeight: 44,
              letterSpacing: '0.05em',
              textTransform: 'uppercase',
              whiteSpace: 'nowrap',
            }}
          >
            {item.label}
          </button>
        </div>
      ))}
    </div>
  );
}
