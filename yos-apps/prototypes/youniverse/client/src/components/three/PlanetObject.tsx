// Y-OS Universe — PlanetObject
// Procedural 3D planet with 4 material archetypes: crystal, gas, organic, rocky
// Mobile-optimized: larger sizes, proper touch targets via invisible hit sphere

import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import type { MaterialArchetype } from '../../types/cms';

interface PlanetObjectProps {
  name: string;
  color: string;
  glowColor?: string;
  emissive?: string;
  archetype?: MaterialArchetype;
  size?: number;
  position?: [number, number, number];
  onClick?: () => void;
  isSelected?: boolean;
  isFocused?: boolean;
}

// Procedural vertex/fragment shaders per archetype
const SHADERS: Record<MaterialArchetype, { vert: string; frag: string }> = {
  crystal: {
    vert: `
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;
      void main() {
        vNormal = normalize(normalMatrix * normal);
        vPosition = position;
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    frag: `
      uniform vec3 uColor;
      uniform vec3 uEmissive;
      uniform float uTime;
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;

      float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
      float noise(vec2 p) {
        vec2 i = floor(p); vec2 f = fract(p);
        float a = hash(i), b = hash(i+vec2(1,0)), c = hash(i+vec2(0,1)), d = hash(i+vec2(1,1));
        vec2 u = f*f*(3.0-2.0*f);
        return mix(a,b,u.x) + (c-a)*u.y*(1.0-u.x) + (d-b)*u.x*u.y;
      }

      void main() {
        vec3 light = normalize(vec3(1.0, 1.0, 0.5));
        float diff = max(dot(vNormal, light), 0.0);
        float spec = pow(max(dot(reflect(-light, vNormal), vec3(0,0,1)), 0.0), 32.0);

        // Crystal facets
        float facet = noise(vUv * 8.0 + uTime * 0.05);
        float facet2 = noise(vUv * 16.0 - uTime * 0.03);
        vec3 col = uColor * (0.4 + 0.6 * diff);
        col += uEmissive * 0.3 * facet;
        col += vec3(0.8, 0.9, 1.0) * spec * 0.8;
        col += uColor * facet2 * 0.2;

        // Rim glow
        float rim = 1.0 - max(dot(vNormal, vec3(0,0,1)), 0.0);
        col += uColor * pow(rim, 3.0) * 0.6;

        gl_FragColor = vec4(col, 1.0);
      }
    `,
  },
  gas: {
    vert: `
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;
      void main() {
        vNormal = normalize(normalMatrix * normal);
        vPosition = position;
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    frag: `
      uniform vec3 uColor;
      uniform vec3 uEmissive;
      uniform float uTime;
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;

      float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
      float noise(vec2 p) {
        vec2 i = floor(p); vec2 f = fract(p);
        float a = hash(i), b = hash(i+vec2(1,0)), c = hash(i+vec2(0,1)), d = hash(i+vec2(1,1));
        vec2 u = f*f*(3.0-2.0*f);
        return mix(a,b,u.x) + (c-a)*u.y*(1.0-u.x) + (d-b)*u.x*u.y;
      }
      float fbm(vec2 p) {
        float v = 0.0; float a = 0.5;
        for(int i=0;i<4;i++) { v += a*noise(p); p*=2.0; a*=0.5; }
        return v;
      }

      void main() {
        vec3 light = normalize(vec3(1.0, 0.8, 0.5));
        float diff = max(dot(vNormal, light), 0.0);

        // Gas bands
        float band = fbm(vec2(vUv.y * 6.0 + uTime * 0.02, vUv.x * 2.0));
        float band2 = fbm(vec2(vUv.y * 12.0 - uTime * 0.015, vUv.x * 3.0 + 1.0));
        vec3 col = mix(uColor, uEmissive * 1.5, band * 0.5);
        col = mix(col, uColor * 1.3, band2 * 0.3);
        col *= (0.3 + 0.7 * diff);

        // Atmosphere rim
        float rim = 1.0 - max(dot(vNormal, vec3(0,0,1)), 0.0);
        col += uColor * pow(rim, 2.0) * 0.5;

        gl_FragColor = vec4(col, 1.0);
      }
    `,
  },
  organic: {
    vert: `
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;
      void main() {
        vNormal = normalize(normalMatrix * normal);
        vPosition = position;
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    frag: `
      uniform vec3 uColor;
      uniform vec3 uEmissive;
      uniform float uTime;
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;

      float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
      float noise(vec2 p) {
        vec2 i = floor(p); vec2 f = fract(p);
        float a = hash(i), b = hash(i+vec2(1,0)), c = hash(i+vec2(0,1)), d = hash(i+vec2(1,1));
        vec2 u = f*f*(3.0-2.0*f);
        return mix(a,b,u.x) + (c-a)*u.y*(1.0-u.x) + (d-b)*u.x*u.y;
      }
      float fbm(vec2 p) {
        float v = 0.0; float a = 0.5;
        for(int i=0;i<4;i++) { v += a*noise(p); p*=2.0; a*=0.5; }
        return v;
      }

      void main() {
        vec3 light = normalize(vec3(1.0, 0.8, 0.3));
        float diff = max(dot(vNormal, light), 0.0);

        // Organic terrain
        float terrain = fbm(vUv * 5.0 + uTime * 0.01);
        float ocean = step(0.45, terrain);
        vec3 landColor = uColor * (0.6 + 0.4 * terrain);
        vec3 oceanColor = uEmissive * 0.5 + vec3(0.0, 0.1, 0.3);
        vec3 col = mix(oceanColor, landColor, ocean);
        col *= (0.3 + 0.7 * diff);

        // Clouds
        float cloud = fbm(vUv * 8.0 + uTime * 0.008);
        col = mix(col, vec3(0.9, 0.95, 1.0), smoothstep(0.6, 0.8, cloud) * 0.4);

        // Atmosphere
        float rim = 1.0 - max(dot(vNormal, vec3(0,0,1)), 0.0);
        col += vec3(0.3, 0.5, 1.0) * pow(rim, 2.5) * 0.4;

        gl_FragColor = vec4(col, 1.0);
      }
    `,
  },
  rocky: {
    vert: `
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;
      void main() {
        vNormal = normalize(normalMatrix * normal);
        vPosition = position;
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    frag: `
      uniform vec3 uColor;
      uniform vec3 uEmissive;
      uniform float uTime;
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;

      float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
      float noise(vec2 p) {
        vec2 i = floor(p); vec2 f = fract(p);
        float a = hash(i), b = hash(i+vec2(1,0)), c = hash(i+vec2(0,1)), d = hash(i+vec2(1,1));
        vec2 u = f*f*(3.0-2.0*f);
        return mix(a,b,u.x) + (c-a)*u.y*(1.0-u.x) + (d-b)*u.x*u.y;
      }
      float fbm(vec2 p) {
        float v = 0.0; float a = 0.5;
        for(int i=0;i<5;i++) { v += a*noise(p); p*=2.0; a*=0.5; }
        return v;
      }

      void main() {
        vec3 light = normalize(vec3(1.0, 0.7, 0.3));
        float diff = max(dot(vNormal, light), 0.0);

        // Rocky craters and terrain
        float rock = fbm(vUv * 6.0);
        float crater = 1.0 - smoothstep(0.0, 0.05, abs(rock - 0.5));
        vec3 col = uColor * (0.4 + 0.6 * rock);
        col = mix(col, uColor * 0.2, crater * 0.4);
        col *= (0.2 + 0.8 * diff);

        // Dust rim
        float rim = 1.0 - max(dot(vNormal, vec3(0,0,1)), 0.0);
        col += uEmissive * pow(rim, 3.0) * 0.4;

        gl_FragColor = vec4(col, 1.0);
      }
    `,
  },
};

// Archetype-to-material mapping for planets without explicit archetype
const COLOR_TO_ARCHETYPE: Record<string, MaterialArchetype> = {
  '#9B59B6': 'crystal',
  '#2471A3': 'gas',
  '#17A589': 'organic',
  '#27AE60': 'organic',
  '#F4D03F': 'gas',
  '#E67E22': 'rocky',
  '#C0392B': 'rocky',
};

function hexToRgb(hex: string): THREE.Color {
  return new THREE.Color(hex);
}

export default function PlanetObject({
  name,
  color,
  glowColor,
  emissive,
  archetype,
  size = 1.5,
  position = [0, 0, 0],
  onClick,
  isSelected = false,
  isFocused = false,
}: PlanetObjectProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const atmosphereRef = useRef<THREE.Mesh>(null);
  const timeRef = useRef(0);

  const resolvedArchetype: MaterialArchetype =
    archetype || COLOR_TO_ARCHETYPE[color] || 'rocky';

  const shader = SHADERS[resolvedArchetype];

  const uniforms = useMemo(() => ({
    uColor: { value: hexToRgb(color) },
    uEmissive: { value: hexToRgb(emissive || glowColor || color) },
    uTime: { value: 0 },
  }), [color, emissive, glowColor]);

  useFrame((_, delta) => {
    timeRef.current += delta;
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.15;
      uniforms.uTime.value = timeRef.current;
    }
    if (atmosphereRef.current) {
      atmosphereRef.current.rotation.y -= delta * 0.05;
    }
  });

  const planetSize = size;
  const atmosphereSize = planetSize * 1.18;
  // Touch hit target: at least 44px → in 3D units use a generous invisible sphere
  const hitSize = Math.max(planetSize * 1.4, 1.2);

  return (
    <group position={position}>
      {/* Invisible hit sphere for touch — ensures 44px+ touch target */}
      <mesh onClick={onClick}>
        <sphereGeometry args={[hitSize, 8, 8]} />
        <meshBasicMaterial transparent opacity={0} depthWrite={false} />
      </mesh>

      {/* Planet body with procedural shader */}
      <mesh ref={meshRef}>
        <sphereGeometry args={[planetSize, 64, 64]} />
        <shaderMaterial
          vertexShader={shader.vert}
          fragmentShader={shader.frag}
          uniforms={uniforms}
        />
      </mesh>

      {/* Atmosphere glow */}
      <mesh ref={atmosphereRef}>
        <sphereGeometry args={[atmosphereSize, 32, 32]} />
        <meshBasicMaterial
          color={glowColor || color}
          transparent
          opacity={isSelected ? 0.25 : 0.12}
          side={THREE.BackSide}
          depthWrite={false}
        />
      </mesh>

      {/* Selection ring */}
      {(isSelected || isFocused) && (
        <mesh rotation={[Math.PI / 2, 0, 0]}>
          <ringGeometry args={[planetSize * 1.35, planetSize * 1.5, 64]} />
          <meshBasicMaterial
            color={glowColor || color}
            transparent
            opacity={0.7}
            side={THREE.DoubleSide}
            depthWrite={false}
          />
        </mesh>
      )}
    </group>
  );
}
