/**
 * Upload Panel Component
 * Handles image upload and processing
 */
import { useRef, useState } from 'react'
import { uploadImagesBatch, projectTo3D, buildGraph, exportData } from '../api'
import { useStore } from '../store'

export default function UploadPanel() {
  const fileInputRef = useRef(null)
  const [isDragging, setIsDragging] = useState(false)
  const { setImages, setEdges, setLoading } = useStore()
  
  const handleFiles = async (files) => {
    if (!files || files.length === 0) return
    
    try {
      setLoading(true, 'Uploading images...')
      
      // Upload and embed
      const uploadResult = await uploadImagesBatch(Array.from(files))
      console.log('Upload result:', uploadResult)
      
      setLoading(true, 'Projecting to 3D space...')
      
      // Project to 3D
      await projectTo3D()
      
      setLoading(true, 'Building similarity graph...')
      
      // Build graph
      await buildGraph(8)
      
      setLoading(true, 'Loading visualization...')
      
      // Fetch and update data
      const data = await exportData()
      
      if (data.coords && data.coords.points) {
        const images = data.coords.points.map(point => ({
          id: point.id,
          coords: [point.x, point.y, point.z],
          thumb: data.meta?.[point.id]?.thumb || null,
          filename: data.meta?.[point.id]?.filename || 'Unknown',
          labels: data.meta?.[point.id]?.labels || []
        }))
        setImages(images)
      }
      
      if (data.graph && data.graph.edges) {
        setEdges(data.graph.edges)
      }
      
      setLoading(false)
      
    } catch (error) {
      console.error('Upload error:', error)
      setLoading(false)
      alert('Error uploading images: ' + error.message)
    }
  }
  
  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    
    const files = e.dataTransfer.files
    handleFiles(files)
  }
  
  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }
  
  const handleDragLeave = () => {
    setIsDragging(false)
  }
  
  const handleFileSelect = (e) => {
    const files = e.target.files
    handleFiles(files)
  }
  
  return (
    <div className="bg-neural-card rounded-lg p-4 shadow-xl border border-gray-700">
      <h3 className="text-lg font-semibold mb-3 text-white flex items-center">
        <span className="mr-2">📤</span>
        Upload Images
      </h3>
      
      <div
        className={`
          border-2 border-dashed rounded-lg p-6 text-center cursor-pointer
          transition-colors duration-200
          ${isDragging 
            ? 'border-neural-accent bg-neural-accent/10' 
            : 'border-gray-600 hover:border-neural-glow'
          }
        `}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="text-4xl mb-2">🖼️</div>
        <p className="text-sm text-gray-300 mb-1">
          Drag & drop images here
        </p>
        <p className="text-xs text-gray-500">or click to browse</p>
        
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept="image/*"
          onChange={handleFileSelect}
          className="hidden"
        />
      </div>
      
      <div className="mt-3 text-xs text-gray-500">
        <p>• Supports: JPG, PNG, WebP</p>
        <p>• Multiple images: Yes</p>
        <p>• Max size: 10MB per image</p>
      </div>
    </div>
  )
}

