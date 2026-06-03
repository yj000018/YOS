// Y-OS Universe — L3Scene
// Satellite detail: satellite at center with children
// GSAP: zoom in from L2 satellite cloud distance → L3 close-up

import { useEffect, useRef } from 'react';
import { useThree } from '@react-three/fiber';
import * as THREE from 'three';
import gsap from 'gsap';
import type { SatelliteNode } from '../../types/cms';
import StarField from './StarField';

interface L3SceneProps {
  satellite: SatelliteNode;
}

export default function L3Scene({ satellite }: L3SceneProps) {
  const { camera, size } = useThree();
  const tweenRef = useRef<gsap.core.Tween | null>(null);

  useEffect(() => {
    const aspect = size.width / size.height;
    const fov = aspect < 0.75 ? 65 : 55;
    const camZ = aspect < 0.75 ? 10 : 8;
    const camY = camZ * 0.2;

    if ('fov' in camera) {
      (camera as THREE.PerspectiveCamera).fov = fov;
      (camera as THREE.PerspectiveCamera).updateProjectionMatrix();
    }

    if (tweenRef.current) { tweenRef.current.kill(); }

    // Start from L2 satellite cloud distance
    camera.position.set(0, camY * 4, camZ * 4);
    camera.lookAt(0, 0, 0);

    tweenRef.current = gsap.to(camera.position, {
      x: 0,
      y: camY,
      z: camZ,
      duration: 1.0,
      ease: 'power2.inOut',
      onUpdate: () => camera.lookAt(0, 0, 0),
      onComplete: () => { tweenRef.current = null; },
    });

    return () => { tweenRef.current?.kill(); };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [camera, satellite.id, size.width, size.height]);

  const children = satellite.children || [];
  const color = satellite.color || '#888888';

  return (
    <>
      <StarField />
      <ambientLight intensity={0.3} />
      <pointLight position={[10, 10, 10]} intensity={2} color="#FFF5E0" />

      {/* Central satellite */}
      <mesh>
        <sphereGeometry args={[1.2, 32, 32]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.4}
          roughness={0.5}
          metalness={0.3}
        />
      </mesh>

      {/* Glow shell */}
      <mesh>
        <sphereGeometry args={[1.5, 16, 16]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.15}
          side={THREE.BackSide}
          depthWrite={false}
        />
      </mesh>

      {/* Name label */}
      <group position={[0, 2.2, 0]}>
        <mesh>
          <planeGeometry args={[4, 0.6]} />
          <meshBasicMaterial color="#000000" transparent opacity={0.5} depthWrite={false} />
        </mesh>
      </group>

      {/* Children orbiting */}
      {children.map((child, i) => {
        const angle = (i / children.length) * Math.PI * 2;
        const r = 3.5;
        const x = Math.cos(angle) * r;
        const z = Math.sin(angle) * r;
        const childColor = child.color || color;
        const childSize = (child.size || 0.12) * 3;
        return (
          <group key={child.id} position={[x, 0, z]}>
            <mesh>
              <sphereGeometry args={[childSize, 16, 16]} />
              <meshStandardMaterial
                color={childColor}
                emissive={childColor}
                emissiveIntensity={0.3}
                roughness={0.6}
              />
            </mesh>
          </group>
        );
      })}
    </>
  );
}
