// Y-OS Universe — SunObject
// Central sun with animated corona, bloom-ready emission, and light rays

import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface SunObjectProps {
  name?: string;
  onClick?: () => void;
  isSelected?: boolean;
}

const SUN_VERT = `
  varying vec3 vNormal;
  varying vec2 vUv;
  uniform float uTime;
  void main() {
    vNormal = normalize(normalMatrix * normal);
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const SUN_FRAG = `
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
  float fbm(vec2 p) {
    float v = 0.0; float a = 0.5;
    for(int i=0;i<4;i++) { v += a*noise(p); p*=2.0; a*=0.5; }
    return v;
  }

  void main() {
    // Solar surface
    float surface = fbm(vUv * 4.0 + uTime * 0.03);
    float surface2 = fbm(vUv * 8.0 - uTime * 0.02);

    vec3 coreColor = vec3(1.0, 0.95, 0.6);
    vec3 hotColor = vec3(1.0, 0.7, 0.1);
    vec3 coolColor = vec3(0.9, 0.3, 0.0);

    vec3 col = mix(hotColor, coreColor, surface);
    col = mix(col, coolColor, surface2 * 0.3);

    // Limb darkening
    float limb = max(dot(vNormal, vec3(0,0,1)), 0.0);
    col *= (0.4 + 0.6 * limb);

    // Bright core
    col += vec3(1.0, 1.0, 0.8) * pow(limb, 4.0) * 0.5;

    gl_FragColor = vec4(col, 1.0);
  }
`;

export default function SunObject({ name = 'Y', onClick, isSelected }: SunObjectProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const corona1Ref = useRef<THREE.Mesh>(null);
  const corona2Ref = useRef<THREE.Mesh>(null);
  const timeRef = useRef(0);

  const uniforms = useMemo(() => ({
    uTime: { value: 0 },
  }), []);

  useFrame((_, delta) => {
    timeRef.current += delta;
    uniforms.uTime.value = timeRef.current;
    if (meshRef.current) meshRef.current.rotation.y += delta * 0.05;
    if (corona1Ref.current) corona1Ref.current.rotation.z += delta * 0.02;
    if (corona2Ref.current) corona2Ref.current.rotation.z -= delta * 0.015;
  });

  return (
    <group>
      {/* Point light from sun */}
      <pointLight color="#FFF5E0" intensity={3} distance={80} decay={1.5} />

      {/* Hit sphere */}
      <mesh onClick={onClick}>
        <sphereGeometry args={[2.8, 8, 8]} />
        <meshBasicMaterial transparent opacity={0} depthWrite={false} />
      </mesh>

      {/* Sun body */}
      <mesh ref={meshRef}>
        <sphereGeometry args={[2.0, 64, 64]} />
        <shaderMaterial
          vertexShader={SUN_VERT}
          fragmentShader={SUN_FRAG}
          uniforms={uniforms}
        />
      </mesh>

      {/* Corona layer 1 */}
      <mesh ref={corona1Ref}>
        <sphereGeometry args={[2.5, 32, 32]} />
        <meshBasicMaterial
          color="#FF8C00"
          transparent
          opacity={0.15}
          side={THREE.BackSide}
          depthWrite={false}
        />
      </mesh>

      {/* Corona layer 2 */}
      <mesh ref={corona2Ref}>
        <sphereGeometry args={[3.2, 32, 32]} />
        <meshBasicMaterial
          color="#FFD700"
          transparent
          opacity={0.07}
          side={THREE.BackSide}
          depthWrite={false}
        />
      </mesh>

      {/* Selection indicator */}
      {isSelected && (
        <mesh rotation={[Math.PI / 2, 0, 0]}>
          <ringGeometry args={[2.6, 2.9, 64]} />
          <meshBasicMaterial color="#FFD700" transparent opacity={0.8} side={THREE.DoubleSide} />
        </mesh>
      )}
    </group>
  );
}
