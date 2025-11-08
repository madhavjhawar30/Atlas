/**
 * Webcam Mode Component
 * Live webcam embedding and positioning on the map
 */
import { useState, useRef, useEffect } from 'react'
import { searchByImage } from '../api'
import { useStore } from '../store'

export default function WebcamMode() {
  const [isActive, setIsActive] = useState(false)
  const [stream, setStream] = useState(null)
  const [error, setError] = useState(null)
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const intervalRef = useRef(null)
  
  const { setWebcamActive, setWebcamPosition, images } = useStore()
  
  const startWebcam = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 640, height: 480 } 
      })
      
      setStream(mediaStream)
      setError(null)
      setIsActive(true)
      setWebcamActive(true)
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream
      }
      
    } catch (err) {
      console.error('Webcam error:', err)
      setError('Failed to access webcam')
    }
  }
  
  const stopWebcam = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop())
    }
    setStream(null)
    setIsActive(false)
    setWebcamActive(false)
    setWebcamPosition(null)
    
    if (intervalRef.current) {
      clearInterval(intervalRef.current)
    }
  }
  
  const captureAndSearch = async () => {
    if (!videoRef.current || !canvasRef.current) return
    
    const video = videoRef.current
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    
    // Draw video frame to canvas
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    ctx.drawImage(video, 0, 0)
    
    // Convert to blob
    canvas.toBlob(async (blob) => {
      if (!blob) return
      
      try {
        // Search for similar images
        const file = new File([blob], 'webcam.jpg', { type: 'image/jpeg' })
        const results = await searchByImage(file, 1)
        
        if (results.results && results.results.length > 0) {
          const nearest = results.results[0]
          if (nearest.coords) {
            setWebcamPosition(nearest.coords)
          }
        }
      } catch (err) {
        console.error('Webcam search error:', err)
      }
    }, 'image/jpeg', 0.8)
  }
  
  useEffect(() => {
    if (isActive && images.length > 0) {
      // Capture and search every 2 seconds
      intervalRef.current = setInterval(captureAndSearch, 2000)
      
      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current)
        }
      }
    }
  }, [isActive, images])
  
  return (
    <div className="bg-neural-card rounded-lg p-4 shadow-xl border border-gray-700">
      <h3 className="text-lg font-semibold mb-3 text-white flex items-center">
        <span className="mr-2">📹</span>
        Live Mode
      </h3>
      
      {!isActive ? (
        <>
          <p className="text-sm text-gray-400 mb-3">
            Turn on your webcam to see your position on the map in real-time
          </p>
          
          <button
            onClick={startWebcam}
            disabled={images.length === 0}
            className="
              w-full py-2 bg-green-600 hover:bg-green-700
              text-white font-medium rounded-lg
              transition-colors duration-200
              disabled:opacity-50 disabled:cursor-not-allowed
            "
          >
            {images.length === 0 ? 'Upload images first' : 'Start Webcam'}
          </button>
          
          {error && (
            <p className="mt-2 text-xs text-red-400">{error}</p>
          )}
        </>
      ) : (
        <>
          <div className="mb-3 bg-neural-bg rounded-lg overflow-hidden">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full"
            />
          </div>
          
          <button
            onClick={stopWebcam}
            className="
              w-full py-2 bg-red-600 hover:bg-red-700
              text-white font-medium rounded-lg
              transition-colors duration-200
            "
          >
            Stop Webcam
          </button>
          
          <p className="mt-2 text-xs text-gray-500 flex items-center">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse mr-2"></span>
            Live • Updating every 2s
          </p>
        </>
      )}
      
      {/* Hidden canvas for capturing frames */}
      <canvas ref={canvasRef} className="hidden" />
      
      <div className="mt-3 text-xs text-gray-500">
        <p>💡 Move objects in view to explore the map</p>
      </div>
    </div>
  )
}

