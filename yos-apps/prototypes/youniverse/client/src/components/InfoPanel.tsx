// Y-OS Universe — InfoPanel
// Compact, repliable bottom drawer — full satellite detail display
// Shows: name, type badge, status, subtitle, description, tags, url, children count
// Mobile-optimized: 44px+ touch targets, readable at 14px+

import { useState } from 'react';
import type { PlanetNode, MoonNode, SatelliteNode } from '../types/cms';

type InfoTarget =
  | { type: 'planet'; data: PlanetNode }
  | { type: 'moon'; data: MoonNode }
  | { type: 'satellite'; data: SatelliteNode }
  | null;

interface InfoPanelProps {
  target: InfoTarget;
  onClose?: () => void;
}

const STATUS_ICONS: Record<string, string> = {
  active: '◉',
  dormant: '○',
  done: '✓',
  alert: '⚠',
  favorite: '★',
  recent: '◈',
};

const STATUS_LABELS: Record<string, string> = {
  active: 'Actif',
  dormant: 'Dormant',
  done: 'Terminé',
  alert: 'Alerte',
  favorite: 'Favori',
  recent: 'Récent',
};

const TYPE_ICONS: Record<string, string> = {
  doc: '📄',
  link: '🔗',
  tool: '⚙️',
  note: '📝',
  media: '🎬',
  task: '☑️',
  tagline: '💬',
};

export default function InfoPanel({ target, onClose }: InfoPanelProps) {
  const [collapsed, setCollapsed] = useState(false);

  if (!target) return null;

  const { type, data } = target;

  const name = data.name;
  const subtitle = 'subtitle' in data ? data.subtitle : undefined;
  const description = 'description' in data ? data.description : undefined;
  const color = 'color' in data ? (data.color || '#888888') : '#888888';
  const status = 'status' in data ? data.status : undefined;
  const url = 'url' in data ? data.url : undefined;
  const tags = 'tags' in data ? data.tags : undefined;
  const nodeType = 'type' in data ? (data as SatelliteNode).type : undefined;
  const frequency = 'frequency' in data ? (data as PlanetNode).frequency : undefined;
  const element = 'element' in data ? (data as PlanetNode).element : undefined;
  const featured = 'featured' in data ? (data as SatelliteNode).featured : undefined;

  // Count children for context
  let childCount = 0;
  if (type === 'planet') {
    childCount = (data as PlanetNode).moons?.length ?? 0;
  } else if (type === 'moon') {
    childCount = (data as MoonNode).satellites?.length ?? 0;
  } else if (type === 'satellite') {
    childCount = (data as SatelliteNode).children?.length ?? 0;
  }

  const childLabel = type === 'planet' ? 'lunes' : type === 'moon' ? 'satellites' : 'éléments';

  return (
    <div
      style={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: 100,
        background: 'rgba(8, 8, 20, 0.94)',
        backdropFilter: 'blur(16px)',
        borderTop: `2px solid ${color}66`,
        borderRadius: '16px 16px 0 0',
        transition: 'transform 0.3s ease',
        transform: collapsed ? 'translateY(calc(100% - 52px))' : 'translateY(0)',
        maxHeight: '60vh',
        overflowY: 'auto',
      }}
    >
      {/* Handle bar — 44px touch target */}
      <div
        onClick={() => setCollapsed(c => !c)}
        style={{
          height: 52,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 20px',
          cursor: 'pointer',
          userSelect: 'none',
          minHeight: 44,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, flex: 1, minWidth: 0 }}>
          <div
            style={{
              width: 10,
              height: 10,
              borderRadius: '50%',
              background: color,
              boxShadow: `0 0 8px ${color}`,
              flexShrink: 0,
            }}
          />
          <span style={{
            color: '#FFFFFF',
            fontSize: 15,
            fontWeight: 700,
            fontFamily: '"Space Mono", monospace',
            letterSpacing: '0.08em',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
          }}>
            {name}
          </span>
          {featured && (
            <span style={{ color: '#FFD700', fontSize: 13 }}>★</span>
          )}
          {status && (
            <span style={{ color, fontSize: 13 }}>
              {STATUS_ICONS[status] || '·'}
            </span>
          )}
          {/* Type badge */}
          <span style={{
            fontSize: 10,
            color: '#888899',
            background: 'rgba(255,255,255,0.06)',
            padding: '2px 8px',
            borderRadius: 4,
            fontFamily: 'monospace',
            textTransform: 'uppercase',
            flexShrink: 0,
          }}>
            {nodeType ? `${TYPE_ICONS[nodeType] || ''} ${nodeType}` : type.toUpperCase()}
          </span>
        </div>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexShrink: 0 }}>
          <span style={{ color: '#666688', fontSize: 18 }}>{collapsed ? '▲' : '▼'}</span>
          {onClose && (
            <button
              onClick={(e) => { e.stopPropagation(); onClose(); }}
              style={{
                background: 'none',
                border: 'none',
                color: '#666688',
                fontSize: 20,
                cursor: 'pointer',
                padding: '4px 8px',
                minWidth: 44,
                minHeight: 44,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              ×
            </button>
          )}
        </div>
      </div>

      {/* Content */}
      {!collapsed && (
        <div style={{ padding: '0 20px 20px' }}>
          {/* Subtitle */}
          {subtitle && (
            <div style={{ color: color, fontSize: 13, marginBottom: 8, fontFamily: 'monospace', opacity: 0.85 }}>
              {subtitle}
            </div>
          )}

          {/* Status + child count row */}
          <div style={{ display: 'flex', gap: 12, marginBottom: 10, alignItems: 'center', flexWrap: 'wrap' }}>
            {status && (
              <span style={{
                fontSize: 12,
                color: color,
                background: `${color}18`,
                border: `1px solid ${color}44`,
                padding: '3px 10px',
                borderRadius: 4,
                fontFamily: 'monospace',
              }}>
                {STATUS_ICONS[status]} {STATUS_LABELS[status] || status}
              </span>
            )}
            {childCount > 0 && (
              <span style={{
                fontSize: 12,
                color: '#8888AA',
                background: 'rgba(255,255,255,0.05)',
                padding: '3px 10px',
                borderRadius: 4,
                fontFamily: 'monospace',
              }}>
                {childCount} {childLabel}
              </span>
            )}
            {frequency && (
              <span style={tagStyle('#FFD700')}>⚡ {frequency}</span>
            )}
            {element && (
              <span style={tagStyle('#88AAFF')}>◈ {element}</span>
            )}
          </div>

          {/* Description */}
          {description && (
            <p style={{
              color: '#CCCCDD',
              fontSize: 14,
              lineHeight: 1.65,
              marginBottom: 12,
              fontFamily: '"Space Grotesk", sans-serif',
            }}>
              {description}
            </p>
          )}

          {/* Tags */}
          {tags && tags.length > 0 && (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 12 }}>
              {tags.map(t => (
                <span key={t} style={tagStyle(color)}>{t}</span>
              ))}
            </div>
          )}

          {/* URL link */}
          {url && (
            <a
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 6,
                color: color,
                fontSize: 13,
                textDecoration: 'none',
                padding: '8px 14px',
                border: `1px solid ${color}44`,
                borderRadius: 6,
                minHeight: 44,
                fontFamily: 'monospace',
                background: `${color}0A`,
                transition: 'background 0.2s',
              }}
            >
              ↗ Ouvrir le lien
            </a>
          )}
        </div>
      )}
    </div>
  );
}

function tagStyle(color: string): React.CSSProperties {
  return {
    fontSize: 12,
    color,
    background: color + '18',
    border: `1px solid ${color}33`,
    padding: '3px 8px',
    borderRadius: 4,
    fontFamily: 'monospace',
  };
}
