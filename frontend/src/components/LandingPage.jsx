/**
 * Landing Page Component
 * View-only mode - shows existing images or message
 */
import { useEffect } from 'react'
import { exportData } from '../api'
import { useStore } from '../store'
import AuthModal from './AuthModal'
import { supabase } from '../lib/supabase'

export default function LandingPage({ onComplete }) {
  const { setImages, setEdges, isAuthenticated, user, images } = useStore()
  
  // Show auth if not authenticated
  if (!isAuthenticated) {
    return <AuthModal onAuthSuccess={() => {}} />
  }
  
  // If we have images, automatically proceed
  useEffect(() => {
    if (images && images.length > 0) {
      // Small delay to show landing page briefly
      const timer = setTimeout(() => {
        onComplete()
      }, 500)
      return () => clearTimeout(timer)
    }
  }, [images, onComplete])
  
  const handleSignOut = async () => {
    await supabase.auth.signOut()
    window.location.reload()
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-950 via-blue-900 to-slate-900 overflow-y-auto">
      {/* Header */}
      <header className="p-8">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="text-4xl">🧭</div>
            <div>
              <h1 className="text-2xl font-bold text-white">Atlas of Images</h1>
              <p className="text-sm text-blue-300">Welcome, {user?.email}</p>
            </div>
          </div>
          <button
            onClick={handleSignOut}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded-lg transition-colors"
          >
            Sign Out
          </button>
        </div>
      </header>
      
      {/* Hero Section */}
      <div className="max-w-6xl mx-auto px-8 py-16">
        <div className="text-center mb-16">
          <h2 className="text-6xl font-bold text-white mb-6 leading-tight">
            Explore Your Images
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
            View and explore your existing 3D semantic map. 
            Discover hidden connections in your visual space.
          </p>
        </div>
        
        {/* Info Box */}
        <div className="max-w-3xl mx-auto">
          <div className="bg-slate-800/50 backdrop-blur-xl rounded-3xl shadow-2xl p-16 border border-blue-500/30">
            <div className="text-center">
              <div className="inline-block mb-6">
                <div className="text-8xl mb-2">🧭</div>
              </div>
              
              <h3 className="text-3xl font-bold text-white mb-4">
                View-Only Mode
              </h3>
              
              <p className="text-lg text-gray-300 mb-8">
                Image upload is disabled. You can explore your existing images in the 3D visualization.
              </p>
              
              {images && images.length > 0 ? (
                <div className="mt-8">
                  <p className="text-white text-xl mb-4">
                    Found {images.length} image{images.length !== 1 ? 's' : ''} in your collection
                  </p>
                  <button
                    onClick={onComplete}
                    className="
                      px-12 py-4 bg-gradient-to-r from-blue-600 via-blue-500 to-cyan-500
                      text-white text-xl font-bold rounded-full
                      shadow-lg shadow-blue-500/50 hover:shadow-xl hover:shadow-blue-500/70 
                      transform hover:scale-105
                      transition-all duration-200
                    "
                  >
                    🚀 Start Exploring
                  </button>
                </div>
              ) : (
                <p className="text-gray-400">
                  No images found. Please contact support if you expected to see images here.
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
