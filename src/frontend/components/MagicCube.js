// components/MagicCube.js
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { useMemo, useRef } from 'react';
import * as THREE from 'three';

// Function to create a texture with the number and background color
function createTextTexture(number, backgroundColor) {
  const size = 256;
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const context = canvas.getContext('2d');
  context.fillStyle = backgroundColor;
  context.fillRect(0, 0, size, size);

  if (number !== null) {
    context.font = 'bold 100px Arial';
    context.fillStyle = 'white';
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    context.fillText(number, size / 2, size / 2);
  }

  return new THREE.CanvasTexture(canvas);
}


// Helper function to generate a slightly brighter color palette
function generateColor(index) {
  const colors = [
    '#B22222', // Firebrick
    '#228B22', // Forest Green
    '#1E90FF', // Dodger Blue
    '#DAA520', // Goldenrod
    '#9932CC', // Dark Orchid
    '#20B2AA', // Light Sea Green
    '#CD5C5C', // Indian Red
    '#6A5ACD', // Slate Blue
    '#8B4513', // Saddle Brown
    '#4682B4', // Steel Blue
    '#2E8B57', // Sea Green
    '#A0522D', // Sienna
    '#6B8E23', // Olive Drab
    '#708090', // Slate Gray
    '#696969', // Dim Gray
  ];
  return colors[index % colors.length];
}


// Helper component to render each cube box with a texture that includes color and optionally a number
function CubeBox({ position, color, number, isVisible }) {
  const texture = useMemo(
    () => createTextTexture(isVisible ? number : null, color),
    [number, color, isVisible]
  );

  return (
    <mesh position={position}>
      <boxGeometry args={[0.9, 0.9, 0.9]} />
      <meshStandardMaterial attachArray="material" map={texture} />
    </mesh>
  );
}

// Optimized StarField component with reduced star count
function StarField() {
  const stars = useRef();
  const starPositions = useMemo(() => {
    const positions = [];
    for (let i = 0; i < 1000; i++) { // Reduced star count
      const x = THREE.MathUtils.randFloatSpread(200);
      const y = THREE.MathUtils.randFloatSpread(200);
      const z = THREE.MathUtils.randFloatSpread(200);
      positions.push(x, y, z);
    }
    return new Float32Array(positions);
  }, []);

  useFrame(() => {
    if (stars.current) {
      stars.current.rotation.y += 0.0005; // Slower rotation for efficiency
    }
  });

  return (
    <points ref={stars}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={starPositions.length / 3}
          array={starPositions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial color="#FFD700" size={0.5} sizeAttenuation />
    </points>
  );
}


export default function MagicCube({ cubeState }) {
  const cubeSize = 5;

  const positions = useMemo(
    () =>
      Array.from({ length: cubeSize * cubeSize * cubeSize }, (_, index) => [
        (index % cubeSize) - 2,
        Math.floor((index / cubeSize) % cubeSize) - 2,
        Math.floor(index / (cubeSize * cubeSize)) - 2,
      ]),
    [cubeSize]
  );

  return (
    <Canvas
      style={{ width: '100vw', height: '100vh', backgroundColor: '#000' }}
      camera={{ position: [10, 10, 10], fov: 50 }}
    >
      {/* Starry background */}
      <StarField />

      {/* Lighting and cube controls */}
      <ambientLight intensity={1.0} />
      <pointLight position={[10, 10, 10]} intensity={1.5} />
      <OrbitControls enableZoom={true} maxPolarAngle={Math.PI} minPolarAngle={0} />

      <group>
        {positions.map((position, index) => {
          const z = Math.floor(index / (cubeSize * cubeSize));
          const y = Math.floor((index % (cubeSize * cubeSize)) / cubeSize);
          const x = index % cubeSize;
          const number = cubeState[z]?.[y]?.[x] || null;

          const isVisible = x === 0 || x === cubeSize - 1 || y === 0 || y === cubeSize - 1 || z === 0 || z === cubeSize - 1;
          const color = generateColor(index);

          return (
            <CubeBox key={index} position={position} color={color} number={number} isVisible={isVisible} />
          );
        })}
      </group>
    </Canvas>
  );
}
