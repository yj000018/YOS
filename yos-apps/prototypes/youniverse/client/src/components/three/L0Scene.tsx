// Y-OS Universe — L0Scene
// Solar system: Sun + 7 planets in Fibonacci spiral
// Chakra order: ROOT (red, closest) → SELF (violet, farthest)
// Top-down camera — bird's eye view, all orbits visible as circles
// FIXED positions — no animated orbits, no clustering

import { useEffect, useRef, useMemo } from 'react';
import { useThree } from '@react-three/fiber';
import * as THREE from 'three';
import gsap from 'gsap';
import type { CMSData, PlanetNode } from '../../types/cms';
import SunObject from './SunObject';
import PlanetObject from './PlanetObject';
import PlanetLabel from './PlanetLabel';
import OrbitRing from './OrbitRing';
import StarField from './StarField';

// Chakra order: ROOT → FLOW → POWER → HEART → VOICE → MIND → SELF
// (closest to sun → farthest from sun)
const CHAKRA_ORDER = ['root', 'flow', 'power', 'heart', 'voice', 'mind', 'self'];

// Fibonacci spiral: angle = i * golden_angle, radius grows with sqrt
const GOLDEN_ANGLE = Math.PI * (3 - Math.sqrt(5)); // ~137.5°
const BASE_RADIUS = 5;
const RADIUS_SCALE = 3.2;

function fibonacciPosition(index: number) {
  const angle = index * GOLDEN_ANGLE;
  const radius = BASE_RADIUS + RADIUS_SCALE * Math.sqrt(index + 1);
  return {
    x: Math.cos(angle) * radius,
    z: Math.sin(angle) * radius,
    radius,
  };
}

interface L0SceneProps {
  data: CMSData;
  onSelectPlanet: (planet: PlanetNode) => void;
  selectedPlanetId?: string | null;
  entryFrom?: 'in' | 'none';
}

function computeL0Camera(maxRadius: number, size: { width: number; height: number }) {
  const aspect = size.width / size.height;
  // Top-down: camera looks straight down
  // Need to see the full spiral — use the max radius to compute height
  const fov = aspect < 0.75 ? 75 : 65;
  const fovRad = (fov * Math.PI) / 180;
  const tanHalfFov = Math.tan(fovRad / 2);
  const viewDim = aspect < 1 ? maxRadius * 1.15 : maxRadius / Math.min(aspect, 1.2);
  const camY = (viewDim * 1.35) / tanHalfFov;
  // Slight tilt so it's not perfectly flat — adds depth perception
  const tiltX = camY * 0.12;
  const tiltZ = camY * 0.08;
  return { x: tiltX, y: camY, z: tiltZ, fov };
}

export default function L0Scene({ data, onSelectPlanet, selectedPlanetId, entryFrom = 'in' }: L0SceneProps) {
  const { camera, size } = useThree();
  const tweenRef = useRef<gsap.core.Tween | null>(null);

  // Sort planets into chakra order, compute Fibonacci positions
  const sortedPlanets = useMemo(() => {
    const ordered: PlanetNode[] = [];
    for (const cid of CHAKRA_ORDER) {
      const p = data.planets.find(pl => pl.id === cid);
      if (p) ordered.push(p);
    }
    // Add any planets not in CHAKRA_ORDER at the end
    for (const p of data.planets) {
      if (!ordered.includes(p)) ordered.push(p);
    }
    return ordered;
  }, [data.planets]);

  const planetPositions = useMemo(() => {
    return sortedPlanets.map((_, i) => fibonacciPosition(i));
  }, [sortedPlanets]);

  const maxRadius = useMemo(() => {
    return planetPositions.reduce((max, p) => Math.max(max, p.radius), 0);
  }, [planetPositions]);

  // GSAP entry animation + viewport-aware camera fit
  useEffect(() => {
    const target = computeL0Camera(maxRadius, size);

    if ('fov' in camera) {
      (camera as THREE.PerspectiveCamera).fov = target.fov;
      (camera as THREE.PerspectiveCamera).updateProjectionMatrix();
    }

    if (entryFrom === 'none') {
      camera.position.set(target.x, target.y, target.z);
      camera.lookAt(0, 0, 0);
      return;
    }

    if (tweenRef.current) { tweenRef.current.kill(); }

    // Start from higher up (zoomed out)
    camera.position.set(target.x * 0.5, target.y * 2.0, target.z * 0.5);
    camera.lookAt(0, 0, 0);

    tweenRef.current = gsap.to(camera.position, {
      x: target.x,
      y: target.y,
      z: target.z,
      duration: 1.4,
      ease: 'power2.inOut',
      onUpdate: () => camera.lookAt(0, 0, 0),
      onComplete: () => { tweenRef.current = null; },
    });

    return () => { tweenRef.current?.kill(); };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [camera, size.width, size.height, maxRadius]);

  return (
    <>
      <StarField />
      <ambientLight intensity={0.2} />
      {/* Top-down lighting */}
      <pointLight position={[0, 40, 0]} intensity={0.8} color="#FFF5E0" />

      {/* Sun at center */}
      <SunObject name={data.sun.name} />

      {/* Orbit rings — circular, visible from top-down */}
      {sortedPlanets.map((p, i) => (
        <OrbitRing
          key={`orbit-${p.id}`}
          radius={planetPositions[i].radius}
          color={p.color}
          opacity={0.1}
        />
      ))}

      {/* Planets — FIXED Fibonacci spiral positions */}
      {sortedPlanets.map((planet, i) => {
        const pos = planetPositions[i];
        const planetSize = (planet.size || 1.5) * 1.3;
        return (
          <group key={planet.id} position={[pos.x, 0, pos.z]}>
            <PlanetObject
              name={planet.name}
              color={planet.color || '#888888'}
              glowColor={planet.glowColor}
              emissive={planet.emissive}
              archetype={planet.archetype}
              size={planetSize}
              onClick={() => onSelectPlanet(planet)}
              isSelected={selectedPlanetId === planet.id}
            />
            <PlanetLabel
              text={planet.name}
              subtitle={planet.subtitle}
              color={planet.color || '#FFFFFF'}
              position={[0, 0, 0]}
              offset={[0, -(planetSize + 0.8), 0]}
            />
          </group>
        );
      })}
    </>
  );
}
