// Y-OS Universe — SatelliteCloud
// InstancedMesh with Fibonacci sphere distribution for performance
// Renders 100+ satellites efficiently

import { useRef, useMemo, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import type { SatelliteNode } from '../../types/cms';

interface SatelliteCloudProps {
  satellites: SatelliteNode[];
  moonColor: string;
  onSelect?: (sat: SatelliteNode) => void;
}

const STATUS_COLORS: Record<string, string> = {
  active: '#00FF88',
  alert: '#FF4444',
  favorite: '#FFD700',
  recent: '#00AAFF',
  dormant: '#666688',
  done: '#44FF44',
};

export default function SatelliteCloud({ satellites, moonColor, onSelect }: SatelliteCloudProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const timeRef = useRef(0);
  const count = satellites.length;

  // Fibonacci sphere distribution
  const positions = useMemo(() => {
    const pts: THREE.Vector3[] = [];
    const phi = Math.PI * (3 - Math.sqrt(5));
    for (let i = 0; i < count; i++) {
      const y = 1 - (i / (count - 1)) * 2;
      const r = Math.sqrt(1 - y * y);
      const theta = phi * i;
      pts.push(new THREE.Vector3(
        Math.cos(theta) * r * 5.5,
        y * 5.5,
        Math.sin(theta) * r * 5.5
      ));
    }
    return pts;
  }, [count]);

  const colors = useMemo(() => {
    return satellites.map(s => {
      const statusColor = s.status ? STATUS_COLORS[s.status] : null;
      return new THREE.Color(statusColor || s.color || moonColor);
    });
  }, [satellites, moonColor]);

  useEffect(() => {
    if (!meshRef.current) return;
    const dummy = new THREE.Object3D();
    for (let i = 0; i < count; i++) {
      dummy.position.copy(positions[i]);
      const s = (satellites[i].size || 0.18) * 1.5;
      dummy.scale.set(s, s, s);
      dummy.updateMatrix();
      meshRef.current.setMatrixAt(i, dummy.matrix);
      meshRef.current.setColorAt(i, colors[i]);
    }
    meshRef.current.instanceMatrix.needsUpdate = true;
    if (meshRef.current.instanceColor) meshRef.current.instanceColor.needsUpdate = true;
  }, [count, positions, colors, satellites]);

  useFrame((_, delta) => {
    timeRef.current += delta;
    if (!meshRef.current) return;
    // Slow rotation of the whole cloud
    meshRef.current.rotation.y += delta * 0.04;
    meshRef.current.rotation.x += delta * 0.01;
  });

  if (count === 0) return null;

  return (
    <instancedMesh
      ref={meshRef}
      args={[undefined, undefined, count]}
      onClick={(e) => {
        e.stopPropagation();
        const idx = e.instanceId;
        if (idx !== undefined && onSelect) onSelect(satellites[idx]);
      }}
    >
      <sphereGeometry args={[1, 8, 8]} />
      <meshStandardMaterial
        vertexColors
        emissive={new THREE.Color(moonColor)}
        emissiveIntensity={0.3}
        roughness={0.6}
        metalness={0.2}
      />
    </instancedMesh>
  );
}
