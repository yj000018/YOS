// Y-OS Universe — PlanetLabel
// HTML overlay labels via @react-three/drei Html
// SUBTLE: semi-transparent bg, small text, positioned BELOW planets
// Planet is the dominant visual — label is secondary

import { Html } from '@react-three/drei';

interface PlanetLabelProps {
  text: string;
  subtitle?: string;
  color?: string;
  position?: [number, number, number];
  offset?: [number, number, number];
}

export default function PlanetLabel({
  text,
  subtitle = '',
  color = '#FFFFFF',
  position = [0, 0, 0],
  offset = [0, -2, 0],
}: PlanetLabelProps) {
  const labelPos: [number, number, number] = [
    position[0] + offset[0],
    position[1] + offset[1],
    position[2] + offset[2],
  ];

  return (
    <group position={labelPos}>
      <Html
        center
        distanceFactor={undefined}
        zIndexRange={[100, 0]}
        style={{
          pointerEvents: 'none',
          userSelect: 'none',
          whiteSpace: 'nowrap',
        }}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 1,
            padding: '3px 8px',
            background: 'rgba(0, 0, 0, 0.45)',
            borderRadius: 4,
            backdropFilter: 'blur(4px)',
          }}
        >
          <span
            style={{
              color: color,
              fontSize: 12,
              fontWeight: 600,
              fontFamily: '"Space Mono", "Courier New", monospace',
              letterSpacing: '0.08em',
              lineHeight: 1.3,
              textShadow: '0 1px 2px rgba(0,0,0,0.7)',
            }}
          >
            {text}
          </span>
          {subtitle && (
            <span
              style={{
                color: 'rgba(255,255,255,0.55)',
                fontSize: 9,
                fontWeight: 400,
                fontFamily: '"Space Mono", "Courier New", monospace',
                lineHeight: 1.2,
                maxWidth: 140,
                overflow: 'hidden',
                textOverflow: 'ellipsis',
              }}
            >
              {subtitle.length > 22 ? subtitle.slice(0, 22) + '…' : subtitle}
            </span>
          )}
        </div>
      </Html>
    </group>
  );
}
