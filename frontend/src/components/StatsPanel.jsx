/**
 * Stats Panel Component
 * Displays statistics about the current dataset
 */
import { useState, useEffect } from 'react'
import { useStore } from '../store'
import { getStats } from '../api'

export default function StatsPanel() {
  const { images, edges } = useStore()
  const [backendStats, setBackendStats] = useState(null)
  
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const stats = await getStats()
        setBackendStats(stats)
      } catch (error) {
        console.error('Failed to fetch stats:', error)
      }
    }
    
    fetchStats()
    const interval = setInterval(fetchStats, 10000) // Update every 10s
    
    return () => clearInterval(interval)
  }, [])
  
  return (
    <div className="bg-neural-card/80 backdrop-blur-sm rounded-lg px-4 py-2 border border-gray-700">
      <div className="flex items-center space-x-6 text-sm">
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-neural-accent rounded-full animate-pulse-glow"></div>
          <span className="text-gray-400">Images:</span>
          <span className="text-white font-semibold">{images.length}</span>
        </div>
        
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse-glow"></div>
          <span className="text-gray-400">Edges:</span>
          <span className="text-white font-semibold">{edges.length}</span>
        </div>
        
        {backendStats && (
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse-glow"></div>
            <span className="text-gray-400">Embedding:</span>
            <span className="text-white font-semibold">{backendStats.embedding_dim}D</span>
          </div>
        )}
      </div>
    </div>
  )
}

