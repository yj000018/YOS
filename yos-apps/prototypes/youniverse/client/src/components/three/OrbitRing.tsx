// Y-OS Universe — OrbitRing
// Subtle orbit path visualization

import * as THREE from 'three';

interface OrbitRingProps {
  radius: number;
  color?: string;
  opacity?: number;
  inclination?: number;
}

export default function OrbitRing({
  radius,
  color = '#ffffff',
  opacity = 0.08,
  inclination = 0,
}: OrbitRingProps) {
  return (
    <mesh rotation={[Math.PI / 2 + inclination, 0, 0]}>
      <ringGeometry args={[radius - 0.03, radius + 0.03, 128]} />
      <meshBasicMaterial
        color={color}
        transparent
        opacity={opacity}
        side={THREE.DoubleSide}
        depthWrite={false}
      />
    </mesh>
  );
}
