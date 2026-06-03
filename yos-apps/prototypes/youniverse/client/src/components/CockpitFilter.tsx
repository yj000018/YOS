// Y-OS Universe — CockpitFilter
// Filter bar: Tous / Alertes / Récents / Favoris / etc.
// Mobile: 44px touch targets, horizontal scroll

type FilterKey = 'all' | 'alert' | 'recent' | 'favorite' | 'active' | 'done' | 'dormant';

interface FilterOption {
  key: FilterKey;
  label: string;
  icon: string;
  color: string;
}

const FILTERS: FilterOption[] = [
  { key: 'all', label: 'Tous', icon: '⊙', color: '#FFFFFF' },
  { key: 'alert', label: 'Alertes', icon: '⚠', color: '#FF4444' },
  { key: 'recent', label: 'Récents', icon: '◈', color: '#00AAFF' },
  { key: 'favorite', label: 'Favoris', icon: '★', color: '#FFD700' },
  { key: 'active', label: 'Actifs', icon: '◉', color: '#00FF88' },
  { key: 'done', label: 'Terminés', icon: '✓', color: '#44FF44' },
  { key: 'dormant', label: 'Dormants', icon: '▤', color: '#666688' },
];

interface CockpitFilterProps {
  active: FilterKey;
  onChange: (key: FilterKey) => void;
}

export default function CockpitFilter({ active, onChange }: CockpitFilterProps) {
  return (
    <div style={{
      position: 'fixed',
      bottom: 0,
      left: 0,
      right: 0,
      zIndex: 40,
      display: 'flex',
      alignItems: 'center',
      padding: '0 8px',
      height: 56,
      background: 'rgba(4, 4, 12, 0.88)',
      backdropFilter: 'blur(10px)',
      borderTop: '1px solid rgba(255,255,255,0.06)',
      gap: 4,
      overflowX: 'auto',
      WebkitOverflowScrolling: 'touch',
    }}>
      {FILTERS.map(f => (
        <button
          key={f.key}
          onClick={() => onChange(f.key)}
          style={{
            flexShrink: 0,
            display: 'flex',
            alignItems: 'center',
            gap: 5,
            padding: '0 12px',
            height: 44,
            minWidth: 44,
            background: active === f.key ? f.color + '22' : 'transparent',
            border: active === f.key ? `1px solid ${f.color}66` : '1px solid transparent',
            borderRadius: 8,
            color: active === f.key ? f.color : '#666688',
            fontSize: 13,
            fontFamily: '"Space Mono", monospace',
            cursor: 'pointer',
            transition: 'all 0.15s',
            whiteSpace: 'nowrap',
          }}
        >
          <span style={{ fontSize: 14 }}>{f.icon}</span>
          <span style={{ fontSize: 12 }}>{f.label}</span>
        </button>
      ))}
    </div>
  );
}
