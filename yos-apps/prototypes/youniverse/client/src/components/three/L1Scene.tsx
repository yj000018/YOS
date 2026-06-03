// Y-OS Universe — L1Scene
// Planet focus: planet at center, moons at FIXED evenly-spaced positions
// Top-down camera — bird's eye view, all moons clearly visible
// Each moon on its own orbit radius — NO animated orbits, NO clustering

import { useEffect, useRef, useMemo } from 'react';
import { useThree } from '@react-three/fiber';
import * as THREE from 'three';
import gsap from 'gsap';
import type { PlanetNode, MoonNode } from '../../types/cms';
import PlanetObject from './PlanetObject';
import MoonObject from './MoonObject';
import PlanetLabel from './PlanetLabel';
import OrbitRing from './OrbitRing';
import StarField from './StarField';

interface L1SceneProps {
  planet: PlanetNode;
  onSelectMoon: (moon: MoonNode) => void;
  selectedMoonId?: string | null;
}

function computeL1Camera(maxRadius: number, size: { width: number; height: number }) {
  const aspect = size.width / size.height;
  const fov = aspect < 0.75 ? 70 : 60;
  const fovRad = (fov * Math.PI) / 180;
  const tanHalfFov = Math.tan(fovRad / 2);
  const viewDim = aspect < 1 ? maxRadius / 1.0 : maxRadius / Math.min(aspect, 1.3);
  const camY = (viewDim * 1.25) / tanHalfFov;
  // Slight tilt for depth perception
  const tiltX = camY * 0.1;
  const tiltZ = camY * 0.06;
  return { x: tiltX, y: camY, z: tiltZ, fov };
}

export default function L1Scene({ planet, onSelectMoon, selectedMoonId }: L1SceneProps) {
  const { camera, size } = useThree();
  const tweenRef = useRef<gsap.core.Tween | null>(null);

  const moons = planet.moons || [];

  // Compute FIXED positions — evenly distributed angles, each on its own orbit
  const moonPositions = useMemo(() => {
    const n = moons.length;
    if (n === 0) return [];
    return moons.map((_, i) => {
      const angle = (i / n) * Math.PI * 2 - Math.PI / 2; // Start from top
      const radius = 3.5 + i * 2.2; // Distinct radius per moon
      return {
        x: Math.cos(angle) * radius,
        z: Math.sin(angle) * radius,
        radius,
      };
    });
  }, [moons]);

  const maxRadius = moonPositions.length > 0
    ? moonPositions[moonPositions.length - 1].radius
    : 8;

  // GSAP zoom-in from above
  useEffect(() => {
    const target = computeL1Camera(maxRadius, size);

    if ('fov' in camera) {
      (camera as THREE.PerspectiveCamera).fov = target.fov;
      (camera as THREE.PerspectiveCamera).updateProjectionMatrix();
    }

    if (tweenRef.current) { tweenRef.current.kill(); }

    // Start from higher up
    camera.position.set(target.x * 0.5, target.y * 2.5, target.z * 0.5);
    camera.lookAt(0, 0, 0);

    tweenRef.current = gsap.to(camera.position, {
      x: target.x,
      y: target.y,
      z: target.z,
      duration: 1.2,
      ease: 'power2.inOut',
      onUpdate: () => camera.lookAt(0, 0, 0),
      onComplete: () => { tweenRef.current = null; },
    });

    return () => { tweenRef.current?.kill(); };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [camera, planet.id, size.width, size.height, maxRadius]);

  const planetSize = (planet.size || 1.5) * 1.5;

  return (
    <>
      <StarField />
      <ambientLight intensity={0.2} />
      <pointLight position={[0, 30, 0]} intensity={1.2} color="#FFF5E0" />

      {/* Central planet */}
      <PlanetObject
        name={planet.name}
        color={planet.color || '#888888'}
        glowColor={planet.glowColor}
        emissive={planet.emissive}
        archetype={planet.archetype}
        size={planetSize}
        isSelected
      />
      <PlanetLabel
        text={planet.name}
        subtitle={planet.subtitle}
        color={planet.color || '#FFFFFF'}
        position={[0, 0, 0]}
        offset={[0, -(planetSize + 0.6), 0]}
      />

      {/* Moon orbit rings */}
      {moons.map((m, i) => (
        <OrbitRing
          key={`orbit-${m.id}`}
          radius={moonPositions[i]?.radius ?? 3.5 + i * 2.2}
          color={m.color || planet.color}
          opacity={0.1}
        />
      ))}

      {/* Moons — FIXED positions, no animation */}
      {moons.map((moon, i) => {
        const pos = moonPositions[i];
        if (!pos) return null;
        const moonSize = moon.size || 0.6;
        return (
          <group key={moon.id} position={[pos.x, 0, pos.z]}>
            <MoonObject
              name={moon.name}
              color={moon.color || planet.color || '#888888'}
              emissive={moon.emissive}
              size={moonSize}
              onClick={() => onSelectMoon(moon)}
              isSelected={selectedMoonId === moon.id}
            />
            <PlanetLabel
              text={moon.name}
              subtitle={moon.subtitle}
              color={moon.color || '#FFFFFF'}
              position={[0, 0, 0]}
              offset={[0, -(moonSize * 2 + 0.5), 0]}
            />
          </group>
        );
      })}
    </>
  );
}
