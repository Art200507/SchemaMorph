import { Canvas } from "@react-three/fiber";
import { FloatingBlob } from "./FloatingBlob";
import { OrbitControls } from "@react-three/drei";

export function ThreeDBackground() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-[#0a0015] via-[#1a0b2e] to-[#0a0015]" />

      {/* Background grid effect - positioned on right */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(236,72,153,0.08)_1px,transparent_1px),linear-gradient(90deg,rgba(236,72,153,0.08)_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_at_75%_50%,black_30%,transparent_75%)]" />

      {/* Quantum data streams effect - on right side */}
      <div className="absolute inset-0 opacity-20">
        <div
          className="absolute top-0 left-1/4 w-px h-full bg-gradient-to-b from-transparent via-pink-400 to-transparent animate-pulse"
          style={{ animationDuration: "3s" }}
        />
        <div
          className="absolute top-0 left-2/4 w-px h-full bg-gradient-to-b from-transparent via-fuchsia-400 to-transparent animate-pulse"
          style={{
            animationDuration: "2s",
            animationDelay: "0.5s",
          }}
        />
        <div
          className="absolute top-0 left-3/4 w-px h-full bg-gradient-to-b from-transparent via-pink-300 to-transparent animate-pulse"
          style={{
            animationDuration: "2.5s",
            animationDelay: "1s",
          }}
        />
      </div>

      {/* 3D Canvas - positioned on right half */}
      <div className="absolute right-0 top-0 w-1/2 h-full">
        <Canvas
          camera={{ position: [0, 0, 5], fov: 45 }}
          className="w-full h-full"
        >
        <ambientLight intensity={0.3} color="#ffffff" />
        <directionalLight
          position={[10, 10, 5]}
          intensity={1.5}
          color="#ff69f0"
        />
        <directionalLight
          position={[-10, 10, 5]}
          intensity={1.5}
          color="#ff69f0"
        />
        <directionalLight
          position={[0, -10, 5]}
          intensity={1.2}
          color="#e91e9e"
        />
        <pointLight
          position={[5, 5, 5]}
          intensity={4}
          color="#ff1493"
        />
        <pointLight
          position={[-5, 5, 5]}
          intensity={4}
          color="#ff1493"
        />
        <pointLight
          position={[0, -5, 5]}
          intensity={3.5}
          color="#e91e9e"
        />
        <spotLight
          position={[0, 10, 0]}
          intensity={4}
          angle={0.6}
          penumbra={1}
          color="#ffb3f0"
        />
        <spotLight
          position={[10, 0, 5]}
          intensity={3.5}
          angle={0.5}
          penumbra={1}
          color="#ff69f0"
        />
        <spotLight
          position={[-10, 0, 5]}
          intensity={3.5}
          angle={0.5}
          penumbra={1}
          color="#ff69f0"
        />

        <FloatingBlob />

        <OrbitControls
          enableZoom={false}
          enablePan={false}
          autoRotate
          autoRotateSpeed={0.5}
        />
      </Canvas>
      </div>

      {/* Glow effects - positioned on right */}
      <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-pink-500/30 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/3 w-96 h-96 bg-fuchsia-500/30 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute top-1/2 right-1/4 -translate-x-1/4 -translate-y-1/2 w-[500px] h-[500px] bg-pink-500/25 rounded-full blur-[100px] pointer-events-none animate-pulse" />

      {/* Digital baroque light rays - on right side */}
      <div className="absolute right-0 top-0 w-1/2 h-full overflow-hidden pointer-events-none opacity-15">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[2px] bg-gradient-to-r from-transparent via-pink-300 to-transparent rotate-45" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[2px] bg-gradient-to-r from-transparent via-fuchsia-300 to-transparent -rotate-45" />
      </div>
    </div>
  );
}
