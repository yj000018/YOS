// Y-OS Universe — MoonObject
// Moon with procedural surface, scaled 2.5x for touch targets

import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface MoonObjectProps {
  name: string;
  color: string;
  emissive?: string;
  size?: number;
  position?: [number, number, number];
  onClick?: () => void;
  isSelected?: boolean;
}

const MOON_VERT = `
  varying vec3 vNormal;
  varying vec2 vUv;
  void main() {
    vNormal = normalize(normalMatrix * normal);
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const MOON_FRAG = `
  uniform vec3 uColor;
  uniform vec3 uEmissive;
  uniform float uTime;
  varying vec3 vNormal;
  varying vec2 vUv;

  float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
  float noise(vec2 p) {
    vec2 i = floor(p); vec2 f = fract(p);
    float a = hash(i), b = hash(i+vec2(1,0)), c = hash(i+vec2(0,1)), d = hash(i+vec2(1,1));
    vec2 u = f*f*(3.0-2.0*f);
    return mix(a,b,u.x) + (c-a)*u.y*(1.0-u.x) + (d-b)*u.x*u.y;
  }

  void main() {
    vec3 light = normalize(vec3(1.0, 0.8, 0.5));
    float diff = max(dot(vNormal, light), 0.0);

    float surface = noise(vUv * 6.0);
    float detail = noise(vUv * 14.0);
    vec3 col = uColor * (0.5 + 0.5 * surface);
    col += uEmissive * detail * 0.15;
    col *= (0.25 + 0.75 * diff);

    float rim = 1.0 - max(dot(vNormal, vec3(0,0,1)), 0.0);
    col += uColor * pow(rim, 4.0) * 0.3;

    gl_FragColor = vec4(col, 1.0);
  }
`;

export default function MoonObject({
  name,
  color,
  emissive,
  size = 0.6,
  position = [0, 0, 0],
  onClick,
  isSelected = false,
}: MoonObjectProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const timeRef = useRef(0);

  const uniforms = useMemo(() => ({
    uColor: { value: new THREE.Color(color) },
    uEmissive: { value: new THREE.Color(emissive || color) },
    uTime: { value: 0 },
  }), [color, emissive]);

  useFrame((_, delta) => {
    timeRef.current += delta;
    uniforms.uTime.value = timeRef.current;
    if (meshRef.current) meshRef.current.rotation.y += delta * 0.2;
  });

  // Scaled up 2.5x for touch targets
  const displaySize = size * 2.5;
  const hitSize = Math.max(displaySize * 1.3, 0.8);

  return (
    <group position={position}>
      {/* Invisible hit sphere */}
      <mesh onClick={onClick}>
        <sphereGeometry args={[hitSize, 8, 8]} />
        <meshBasicMaterial transparent opacity={0} depthWrite={false} />
      </mesh>

      <mesh ref={meshRef}>
        <sphereGeometry args={[displaySize, 32, 32]} />
        <shaderMaterial
          vertexShader={MOON_VERT}
          fragmentShader={MOON_FRAG}
          uniforms={uniforms}
        />
      </mesh>

      {/* Glow */}
      <mesh>
        <sphereGeometry args={[displaySize * 1.15, 16, 16]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={isSelected ? 0.2 : 0.08}
          side={THREE.BackSide}
          depthWrite={false}
        />
      </mesh>

      {isSelected && (
        <mesh rotation={[Math.PI / 2, 0, 0]}>
          <ringGeometry args={[displaySize * 1.3, displaySize * 1.5, 32]} />
          <meshBasicMaterial color={color} transparent opacity={0.8} side={THREE.DoubleSide} />
        </mesh>
      )}
    </group>
  );
}
