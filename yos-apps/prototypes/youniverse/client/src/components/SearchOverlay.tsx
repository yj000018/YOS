// Y-OS Universe — SearchOverlay (⌘K Command Palette)
// Full-text search across all planets, moons, and satellites
// Keyboard: ⌘K / Ctrl+K to open, Escape to close, ↑↓ to navigate, Enter to select
// Mobile: tap search icon to open

import { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import type { CMSData, PlanetNode, MoonNode, SatelliteNode } from '../types/cms';

interface SearchResult {
  id: string;
  name: string;
  description?: string;
  type: 'planet' | 'moon' | 'satellite';
  color: string;
  path: string; // e.g. "SELF > Identité > ..."
  nodeType?: string; // doc, link, tool, etc.
  status?: string;
  planet: PlanetNode;
  moon?: MoonNode;
  satellite?: SatelliteNode;
}

interface SearchOverlayProps {
  data: CMSData;
  isOpen: boolean;
  onClose: () => void;
  onNavigate: (result: SearchResult) => void;
}

function buildSearchIndex(data: CMSData): SearchResult[] {
  const results: SearchResult[] = [];

  for (const planet of data.planets) {
    results.push({
      id: planet.id,
      name: planet.name,
      description: planet.description,
      type: 'planet',
      color: planet.color || '#888888',
      path: planet.name,
      status: undefined,
      planet,
    });

    for (const moon of planet.moons || []) {
      results.push({
        id: moon.id,
        name: moon.name,
        description: moon.description,
        type: 'moon',
        color: moon.color || planet.color || '#888888',
        path: `${planet.name} › ${moon.name}`,
        status: undefined,
        planet,
        moon,
      });

      for (const sat of moon.satellites || []) {
        results.push({
          id: sat.id,
          name: sat.name,
          description: sat.description,
          type: 'satellite',
          color: sat.color || moon.color || '#888888',
          path: `${planet.name} › ${moon.name} › ${sat.name}`,
          nodeType: sat.type,
          status: sat.status,
          planet,
          moon,
          satellite: sat,
        });
      }
    }
  }

  return results;
}

const TYPE_ICONS: Record<string, string> = {
  planet: '🪐',
  moon: '🌙',
  satellite: '✦',
  doc: '📄',
  link: '🔗',
  tool: '⚙️',
  note: '📝',
  media: '🎬',
};

export default function SearchOverlay({ data, isOpen, onClose, onNavigate }: SearchOverlayProps) {
  const [query, setQuery] = useState('');
  const [selectedIdx, setSelectedIdx] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLDivElement>(null);

  const index = useMemo(() => buildSearchIndex(data), [data]);

  const results = useMemo(() => {
    if (!query.trim()) return index.slice(0, 20); // Show recent/all when empty
    const q = query.toLowerCase().trim();
    const terms = q.split(/\s+/);
    return index
      .filter(item => {
        const haystack = `${item.name} ${item.description || ''} ${item.path} ${item.nodeType || ''} ${item.status || ''}`.toLowerCase();
        return terms.every(t => haystack.includes(t));
      })
      .slice(0, 30);
  }, [query, index]);

  // Reset selection when results change
  useEffect(() => {
    setSelectedIdx(0);
  }, [results]);

  // Focus input when opened
  useEffect(() => {
    if (isOpen) {
      setQuery('');
      setSelectedIdx(0);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [isOpen]);

  // Scroll selected item into view
  useEffect(() => {
    if (listRef.current) {
      const el = listRef.current.children[selectedIdx] as HTMLElement;
      if (el) el.scrollIntoView({ block: 'nearest' });
    }
  }, [selectedIdx]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIdx(i => Math.min(i + 1, results.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIdx(i => Math.max(i - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (results[selectedIdx]) {
        onNavigate(results[selectedIdx]);
        onClose();
      }
    } else if (e.key === 'Escape') {
      onClose();
    }
  }, [results, selectedIdx, onNavigate, onClose]);

  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        zIndex: 200,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        paddingTop: 'max(60px, 10vh)',
      }}
    >
      {/* Backdrop */}
      <div
        onClick={onClose}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(2, 2, 10, 0.82)',
          backdropFilter: 'blur(8px)',
        }}
      />

      {/* Palette */}
      <div
        style={{
          position: 'relative',
          width: 'min(520px, calc(100vw - 32px))',
          maxHeight: '70vh',
          display: 'flex',
          flexDirection: 'column',
          background: 'rgba(12, 12, 28, 0.96)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: 12,
          boxShadow: '0 24px 80px rgba(0, 0, 0, 0.7), 0 0 1px rgba(255,255,255,0.1)',
          overflow: 'hidden',
        }}
        onKeyDown={handleKeyDown}
      >
        {/* Search input */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 10,
          padding: '14px 16px',
          borderBottom: '1px solid rgba(255,255,255,0.08)',
        }}>
          <span style={{ color: '#666688', fontSize: 18 }}>⌘</span>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Rechercher planètes, lunes, satellites…"
            style={{
              flex: 1,
              background: 'transparent',
              border: 'none',
              outline: 'none',
              color: '#EEEEFF',
              fontSize: 16,
              fontFamily: '"Space Mono", monospace',
              letterSpacing: '0.02em',
            }}
          />
          <kbd style={{
            fontSize: 11,
            color: '#555577',
            background: 'rgba(255,255,255,0.06)',
            padding: '2px 8px',
            borderRadius: 4,
            fontFamily: 'monospace',
          }}>
            ESC
          </kbd>
        </div>

        {/* Results */}
        <div
          ref={listRef}
          style={{
            overflowY: 'auto',
            maxHeight: '55vh',
            padding: '4px 0',
          }}
        >
          {results.length === 0 && (
            <div style={{
              padding: '24px 16px',
              textAlign: 'center',
              color: '#555577',
              fontSize: 13,
              fontFamily: '"Space Mono", monospace',
            }}>
              Aucun résultat pour « {query} »
            </div>
          )}
          {results.map((r, i) => (
            <div
              key={r.id}
              onClick={() => { onNavigate(r); onClose(); }}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 10,
                padding: '10px 16px',
                cursor: 'pointer',
                background: i === selectedIdx ? 'rgba(255,255,255,0.06)' : 'transparent',
                borderLeft: i === selectedIdx ? `3px solid ${r.color}` : '3px solid transparent',
                transition: 'background 0.1s',
                minHeight: 44,
              }}
            >
              {/* Color dot */}
              <div style={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                background: r.color,
                boxShadow: `0 0 6px ${r.color}66`,
                flexShrink: 0,
              }} />

              {/* Content */}
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <span style={{
                    color: '#EEEEFF',
                    fontSize: 14,
                    fontWeight: 600,
                    fontFamily: '"Space Mono", monospace',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                  }}>
                    {r.name}
                  </span>
                  <span style={{
                    fontSize: 10,
                    color: '#666688',
                    fontFamily: 'monospace',
                    textTransform: 'uppercase',
                    flexShrink: 0,
                  }}>
                    {TYPE_ICONS[r.nodeType || r.type] || '·'} {r.nodeType || r.type}
                  </span>
                </div>
                <div style={{
                  fontSize: 11,
                  color: '#555577',
                  fontFamily: 'monospace',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                  marginTop: 2,
                }}>
                  {r.path}
                </div>
              </div>

              {/* Status indicator */}
              {r.status && (
                <span style={{
                  fontSize: 10,
                  color: r.color,
                  opacity: 0.7,
                  flexShrink: 0,
                }}>
                  {r.status}
                </span>
              )}
            </div>
          ))}
        </div>

        {/* Footer hint */}
        <div style={{
          padding: '8px 16px',
          borderTop: '1px solid rgba(255,255,255,0.06)',
          display: 'flex',
          gap: 16,
          justifyContent: 'center',
        }}>
          {[
            { key: '↑↓', label: 'naviguer' },
            { key: '↵', label: 'sélectionner' },
            { key: 'esc', label: 'fermer' },
          ].map(h => (
            <span key={h.key} style={{ fontSize: 11, color: '#444466', fontFamily: 'monospace' }}>
              <kbd style={{
                background: 'rgba(255,255,255,0.06)',
                padding: '1px 5px',
                borderRadius: 3,
                marginRight: 4,
              }}>{h.key}</kbd>
              {h.label}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
