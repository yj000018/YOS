// Y-OS Universe — useCameraTransition
// GSAP-powered cinematic camera transitions between hierarchy levels
// Usage: call animateCamera(targetPos, targetLookAt, onComplete?) from any scene component
//
// Architecture:
//   - Uses gsap.to() on camera.position and a lookAt target vector
//   - Duration 1.2s, power2.inOut easing for natural deceleration
//   - Kills any in-progress tween before starting a new one (no queuing)
//   - onComplete fires after animation ends (use to trigger state changes)

import { useCallback, useRef } from 'react';
import { useThree } from '@react-three/fiber';
import * as THREE from 'three';
import gsap from 'gsap';

interface CameraTarget {
  position: [number, number, number];
  lookAt?: [number, number, number];
  fov?: number;
  duration?: number;
  ease?: string;
  onComplete?: () => void;
}

export function useCameraTransition() {
  const { camera } = useThree();
  const tweenRef = useRef<gsap.core.Tween | null>(null);
  const lookAtRef = useRef(new THREE.Vector3(0, 0, 0));

  const animateCamera = useCallback((target: CameraTarget) => {
    const {
      position,
      lookAt = [0, 0, 0],
      fov,
      duration = 1.2,
      ease = 'power2.inOut',
      onComplete,
    } = target;

    // Kill any running tween immediately
    if (tweenRef.current) {
      tweenRef.current.kill();
      tweenRef.current = null;
    }

    const [tx, ty, tz] = position;
    const [lx, ly, lz] = lookAt;

    // Animate lookAt vector in parallel with position
    const lookAtTarget = { x: lx, y: ly, z: lz };
    const lookAtCurrent = {
      x: lookAtRef.current.x,
      y: lookAtRef.current.y,
      z: lookAtRef.current.z,
    };

    // FOV transition if specified
    if (fov && 'fov' in camera) {
      const cam = camera as THREE.PerspectiveCamera;
      gsap.to(cam, {
        fov,
        duration,
        ease,
        onUpdate: () => cam.updateProjectionMatrix(),
      });
    }

    // Animate lookAt
    gsap.to(lookAtCurrent, {
      x: lookAtTarget.x,
      y: lookAtTarget.y,
      z: lookAtTarget.z,
      duration,
      ease,
      onUpdate: () => {
        lookAtRef.current.set(lookAtCurrent.x, lookAtCurrent.y, lookAtCurrent.z);
        camera.lookAt(lookAtRef.current);
      },
    });

    // Animate position (primary tween — carries onComplete)
    tweenRef.current = gsap.to(camera.position, {
      x: tx,
      y: ty,
      z: tz,
      duration,
      ease,
      onComplete: () => {
        tweenRef.current = null;
        onComplete?.();
      },
    });
  }, [camera]);

  const killTransition = useCallback(() => {
    if (tweenRef.current) {
      tweenRef.current.kill();
      tweenRef.current = null;
    }
  }, []);

  return { animateCamera, killTransition };
}
