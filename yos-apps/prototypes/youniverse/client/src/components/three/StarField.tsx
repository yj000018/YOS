// Y-OS Universe — StarField
// Particle-based background nebula + stars

import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export default function StarField() {
  const starsRef = useRef<THREE.Points>(null);
  const nebulaRef = useRef<THREE.Points>(null);

  const starGeom = useMemo(() => {
    const count = 2000;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const r = 80 + Math.random() * 120;
      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = r * Math.cos(phi);
      const brightness = 0.6 + Math.random() * 0.4;
      colors[i * 3] = brightness;
      colors[i * 3 + 1] = brightness;
      colors[i * 3 + 2] = brightness + Math.random() * 0.1;
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    g.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    return g;
  }, []);

  const nebulaGeom = useMemo(() => {
    const count = 300;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const nebulaColors = [
      [0.3, 0.1, 0.5],
      [0.1, 0.2, 0.5],
      [0.5, 0.1, 0.3],
    ];
    for (let i = 0; i < count; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const r = 60 + Math.random() * 80;
      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = r * Math.cos(phi);
      const nc = nebulaColors[Math.floor(Math.random() * nebulaColors.length)];
      colors[i * 3] = nc[0] + Math.random() * 0.1;
      colors[i * 3 + 1] = nc[1] + Math.random() * 0.1;
      colors[i * 3 + 2] = nc[2] + Math.random() * 0.1;
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    g.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    return g;
  }, []);

  useFrame((_, delta) => {
    if (starsRef.current) starsRef.current.rotation.y += delta * 0.003;
    if (nebulaRef.current) nebulaRef.current.rotation.y -= delta * 0.002;
  });

  return (
    <>
      <points ref={starsRef} geometry={starGeom}>
        <pointsMaterial
          size={0.4}
          vertexColors
          transparent
          opacity={0.9}
          sizeAttenuation
          depthWrite={false}
        />
      </points>
      <points ref={nebulaRef} geometry={nebulaGeom}>
        <pointsMaterial
          size={2.5}
          vertexColors
          transparent
          opacity={0.15}
          sizeAttenuation
          depthWrite={false}
        />
      </points>
    </>
  );
}
