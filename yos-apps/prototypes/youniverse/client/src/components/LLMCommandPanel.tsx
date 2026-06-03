// Y-OS Universe — LLMCommandPanel
// Natural language command input
// Mobile-optimized: 44px input height

import { useState, useRef } from 'react';

interface LLMCommandPanelProps {
  onCommand: (cmd: string) => void;
  isOpen: boolean;
  onToggle: () => void;
}

const EXAMPLES = [
  'Navigue vers Heart',
  'Ajoute une lune Vision à Crown',
  'Liste les lunes de Root',
  'Montre les alertes',
];

export default function LLMCommandPanel({ onCommand, isOpen, onToggle }: LLMCommandPanelProps) {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState<string[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);

  const submit = () => {
    const cmd = input.trim();
    if (!cmd) return;
    setHistory(h => [...h, `> ${cmd}`]);
    onCommand(cmd);
    setInput('');
  };

  return (
    <>
      {/* Toggle button */}
      <button
        onClick={onToggle}
        title="Panneau de commande LLM"
        style={{
          position: 'fixed',
          bottom: 68,
          right: 16,
          zIndex: 60,
          width: 48,
          height: 48,
          borderRadius: '50%',
          background: isOpen ? 'rgba(100, 80, 200, 0.9)' : 'rgba(40, 30, 80, 0.85)',
          border: '1px solid rgba(150, 100, 255, 0.4)',
          color: '#CCAAFF',
          fontSize: 18,
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backdropFilter: 'blur(8px)',
          transition: 'all 0.2s',
          boxShadow: isOpen ? '0 0 16px rgba(150, 100, 255, 0.4)' : 'none',
        }}
      >
        ⌘
      </button>

      {/* Panel */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          bottom: 124,
          right: 16,
          left: 16,
          zIndex: 60,
          background: 'rgba(8, 6, 20, 0.95)',
          backdropFilter: 'blur(16px)',
          border: '1px solid rgba(150, 100, 255, 0.3)',
          borderRadius: 12,
          padding: 16,
          maxHeight: '40vh',
          display: 'flex',
          flexDirection: 'column',
          gap: 10,
        }}>
          <div style={{
            fontSize: 11,
            color: '#9966FF',
            fontFamily: '"Space Mono", monospace',
            letterSpacing: '0.1em',
            marginBottom: 4,
          }}>
            NL → UNIVERS · Pipeline actif
          </div>

          {/* History */}
          {history.length > 0 && (
            <div style={{
              flex: 1,
              overflowY: 'auto',
              fontSize: 12,
              color: '#888899',
              fontFamily: 'monospace',
              maxHeight: 100,
            }}>
              {history.map((h, i) => (
                <div key={i} style={{ padding: '2px 0' }}>{h}</div>
              ))}
            </div>
          )}

          {/* Examples */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {EXAMPLES.map(ex => (
              <button
                key={ex}
                onClick={() => { setInput(ex); inputRef.current?.focus(); }}
                style={{
                  fontSize: 11,
                  color: '#9966FF',
                  background: 'rgba(150, 100, 255, 0.1)',
                  border: '1px solid rgba(150, 100, 255, 0.2)',
                  borderRadius: 4,
                  padding: '4px 8px',
                  cursor: 'pointer',
                  fontFamily: 'monospace',
                  whiteSpace: 'nowrap',
                }}
              >
                {ex}
              </button>
            ))}
          </div>

          {/* Input */}
          <div style={{ display: 'flex', gap: 8 }}>
            <input
              ref={inputRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && submit()}
              placeholder="Commande en langage naturel…"
              style={{
                flex: 1,
                height: 44,
                background: 'rgba(255,255,255,0.06)',
                border: '1px solid rgba(150, 100, 255, 0.3)',
                borderRadius: 8,
                color: '#FFFFFF',
                fontSize: 14,
                padding: '0 12px',
                outline: 'none',
                fontFamily: 'monospace',
              }}
            />
            <button
              onClick={submit}
              style={{
                width: 44,
                height: 44,
                background: 'rgba(150, 100, 255, 0.3)',
                border: '1px solid rgba(150, 100, 255, 0.5)',
                borderRadius: 8,
                color: '#CCAAFF',
                fontSize: 18,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              ▶
            </button>
          </div>
        </div>
      )}
    </>
  );
}
