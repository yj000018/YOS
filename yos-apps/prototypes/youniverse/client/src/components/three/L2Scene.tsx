// Y-OS Universe — L2Scene
// Moon focus: moon at center, satellites in Fibonacci cloud
// GSAP: zoom in from L1 moon orbit distance → L2 fit

import { useEffect, useRef } from 'react';
import { useThree } from '@react-three/fiber';
import * as THREE from 'three';
import gsap from 'gsap';
import type { MoonNode, SatelliteNode } from '../../types/cms';
import MoonObject from './MoonObject';
import SatelliteCloud from './SatelliteCloud';
import PlanetLabel from './PlanetLabel';
import StarField from './StarField';

interface L2SceneProps {
  moon: MoonNode;
  onSelectSatellite: (sat: SatelliteNode) => void;
}

export default function L2Scene({ moon, onSelectSatellite }: L2SceneProps) {
  const { camera, size } = useThree();
  const tweenRef = useRef<gsap.core.Tween | null>(null);

  useEffect(() => {
    const aspect = size.width / size.height;
    const fov = aspect < 0.75 ? 65 : 55;
    const camZ = aspect < 0.75 ? 18 : 14;
    const camY = camZ * 0.2;

    if ('fov' in camera) {
      (camera as THREE.PerspectiveCamera).fov = fov;
      (camera as THREE.PerspectiveCamera).updateProjectionMatrix();
    }

    if (tweenRef.current) { tweenRef.current.kill(); }

    // Start from L1 moon orbit distance (much farther out)
    camera.position.set(0, camY * 3, camZ * 3.5);
    camera.lookAt(0, 0, 0);

    tweenRef.current = gsap.to(camera.position, {
      x: 0,
      y: camY,
      z: camZ,
      duration: 1.2,
      ease: 'power2.inOut',
      onUpdate: () => camera.lookAt(0, 0, 0),
      onComplete: () => { tweenRef.current = null; },
    });

    return () => { tweenRef.current?.kill(); };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [camera, moon.id, size.width, size.height]);

  const satellites = moon.satellites || [];

  return (
    <>
      <StarField />
      <ambientLight intensity={0.25} />
      <pointLight position={[15, 15, 15]} intensity={1.5} color="#FFF5E0" />

      {/* Central moon */}
      <MoonObject
        name={moon.name}
        color={moon.color || '#888888'}
        emissive={moon.emissive}
        size={(moon.size || 0.6) * 1.8}
        isSelected
      />
      <PlanetLabel
        text={moon.name}
        subtitle={moon.subtitle}
        color={moon.color || '#FFFFFF'}
        position={[0, 0, 0]}
        offset={[0, (moon.size || 0.6) * 1.8 * 2.5 + 1.2, 0]}
      />

      {/* Satellite cloud */}
      {satellites.length > 0 && (
        <SatelliteCloud
          satellites={satellites}
          moonColor={moon.color || '#888888'}
          onSelect={onSelectSatellite}
        />
      )}
    </>
  );
}
