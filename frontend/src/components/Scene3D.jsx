/**
 * Main 3D Scene Component
 * Renders the neural network visualization with nodes and edges
 */
import { useRef, useMemo, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera } from '@react-three/drei'
import * as THREE from 'three'
import { useStore } from '../store'

// Node component - represents a single image
function Node({ position, id, isSelected, isHovered, isSearchResult }) {
  const meshRef = useRef()
  const { setSelectedNode, setHoveredNode } = useStore()
  
  // Animation
  useFrame((state) => {
    if (meshRef.current) {
      // Gentle breathing animation
      const scale = 1 + Math.sin(state.clock.elapsedTime * 2 + position[0]) * 0.05
      meshRef.current.scale.setScalar(scale)
      
      // Rotate slightly if selected
      if (isSelected) {
        meshRef.current.rotation.y += 0.02
      }
    }
  })
  
  // Determine color and size based on state
  const color = isSelected 
    ? '#60a5fa'  // Bright blue when selected
    : isSearchResult 
    ? '#fbbf24'  // Yellow for search results
    : isHovered 
    ? '#93c5fd'  // Light blue on hover
    : '#3b82f6'  // Default blue
  
  const scale = isSelected ? 0.3 : isHovered ? 0.25 : 0.2
  
  return (
    <mesh
      ref={meshRef}
      position={position}
      scale={scale}
      onClick={(e) => {
        e.stopPropagation()
        setSelectedNode(id)
      }}
      onPointerOver={(e) => {
        e.stopPropagation()
        setHoveredNode(id)
        document.body.style.cursor = 'pointer'
      }}
      onPointerOut={() => {
        setHoveredNode(null)
        document.body.style.cursor = 'default'
      }}
    >
      <sphereGeometry args={[1, 16, 16]} />
      <meshStandardMaterial
        color={color}
        emissive={color}
        emissiveIntensity={isSelected ? 0.8 : isHovered ? 0.5 : 0.3}
        roughness={0.3}
        metalness={0.8}
      />
      
      {/* Glow effect */}
      <mesh scale={1.5}>
        <sphereGeometry args={[1, 16, 16]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={isSelected ? 0.3 : isHovered ? 0.2 : 0.1}
        />
      </mesh>
    </mesh>
  )
}

// Edge component - represents similarity connection between nodes
function Edge({ start, end, weight }) {
  const lineRef = useRef()
  
  const points = useMemo(() => {
    return [
      new THREE.Vector3(...start),
      new THREE.Vector3(...end)
    ]
  }, [start, end])
  
  const geometry = useMemo(() => {
    const geom = new THREE.BufferGeometry().setFromPoints(points)
    return geom
  }, [points])
  
  // Edge opacity based on similarity weight
  const opacity = Math.max(0.1, weight * 0.5)
  
  return (
    <line ref={lineRef} geometry={geometry}>
      <lineBasicMaterial
        color="#60a5fa"
        transparent
        opacity={opacity}
        linewidth={1}
      />
    </line>
  )
}

// Main scene content
function SceneContent() {
  const { images, edges, selectedNode, hoveredNode, searchResults } = useStore()
  const searchResultIds = useMemo(() => 
    new Set(searchResults.map(r => r.image_id)), 
    [searchResults]
  )
  
  // Filter edges to show only those connected to selected/hovered node
  const visibleEdges = useMemo(() => {
    if (!selectedNode && !hoveredNode) {
      // Show a subset of edges to avoid clutter
      return edges.filter((_, i) => i % 5 === 0).slice(0, 200)
    }
    
    const focusNode = selectedNode || hoveredNode
    return edges.filter(e => 
      e.source === focusNode || e.target === focusNode
    )
  }, [edges, selectedNode, hoveredNode])
  
  // Get image map for edge rendering
  const imageMap = useMemo(() => {
    const map = new Map()
    images.forEach(img => map.set(img.id, img))
    return map
  }, [images])
  
  return (
    <>
      {/* Ambient lighting */}
      <ambientLight intensity={0.3} />
      <pointLight position={[10, 10, 10]} intensity={1} />
      <pointLight position={[-10, -10, -10]} intensity={0.5} />
      
      {/* Nodes */}
      {images.map(image => (
        <Node
          key={image.id}
          id={image.id}
          position={image.coords}
          isSelected={selectedNode === image.id}
          isHovered={hoveredNode === image.id}
          isSearchResult={searchResultIds.has(image.id)}
        />
      ))}
      
      {/* Edges */}
      {visibleEdges.map((edge, i) => {
        const sourceImg = imageMap.get(edge.source)
        const targetImg = imageMap.get(edge.target)
        
        if (!sourceImg || !targetImg) return null
        
        return (
          <Edge
            key={`${edge.source}-${edge.target}-${i}`}
            start={sourceImg.coords}
            end={targetImg.coords}
            weight={edge.weight}
          />
        )
      })}
      
      {/* Background fog */}
      <fog attach="fog" args={['#0a0e1a', 10, 50]} />
    </>
  )
}

// Main Scene3D component
export default function Scene3D() {
  return (
    <Canvas
      style={{ width: '100%', height: '100%' }}
      gl={{ 
        antialias: true, 
        alpha: false,
        powerPreference: 'high-performance'
      }}
    >
      <PerspectiveCamera makeDefault position={[0, 0, 30]} fov={60} />
      
      <OrbitControls
        enableDamping
        dampingFactor={0.05}
        rotateSpeed={0.5}
        zoomSpeed={0.8}
        minDistance={5}
        maxDistance={100}
      />
      
      <SceneContent />
    </Canvas>
  )
}

