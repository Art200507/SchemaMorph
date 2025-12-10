import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { MeshDistortMaterial, shaderMaterial } from '@react-three/drei';
import * as THREE from 'three';

export function FloatingBlob() {
  const meshRef = useRef<THREE.Mesh>(null);
  const materialRef = useRef<any>(null);
  const timeRef = useRef(0);

  useFrame((state, delta) => {
    if (!meshRef.current) return;
    
    timeRef.current += delta;
    
    // Floating movement
    meshRef.current.position.y = Math.sin(timeRef.current * 0.5) * 0.5;
    meshRef.current.position.x = Math.cos(timeRef.current * 0.3) * 0.5;
    meshRef.current.position.z = Math.sin(timeRef.current * 0.4) * 0.3;
    
    // Rotation
    meshRef.current.rotation.x += delta * 0.2;
    meshRef.current.rotation.y += delta * 0.3;
    meshRef.current.rotation.z += delta * 0.1;
    
    // Animate material colors for holographic shift - Pink/Magenta
    if (materialRef.current) {
      const pulse = Math.sin(timeRef.current * 0.8) * 0.5 + 0.5;
      // Shift through pink and magenta hues
      materialRef.current.color.setHSL(0.85 + Math.sin(timeRef.current * 0.3) * 0.05, 1.0, 0.65 + pulse * 0.1); // Pink/Magenta base
      materialRef.current.emissive.setHSL(0.88 + Math.sin(timeRef.current * 0.4) * 0.04, 0.95, 0.4 + pulse * 0.2); // Magenta glow
    }
  });

  return (
    <mesh ref={meshRef} scale={1.5}>
      <sphereGeometry args={[1, 128, 128]} />
      <MeshDistortMaterial
        ref={materialRef}
        color="#ff69f0"
        attach="material"
        distort={0.7}
        speed={3}
        roughness={0.0}
        metalness={0.9}
        emissive="#e91e9e"
        emissiveIntensity={1.2}
        clearcoat={1.0}
        clearcoatRoughness={0.0}
        envMapIntensity={2.5}
        reflectivity={1.0}
      />
    </mesh>
  );
}