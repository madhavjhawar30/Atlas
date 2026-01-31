/**
 * API client for backend communication
 */
import axios from 'axios'
import { supabase } from './lib/supabase'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 second timeout
})

// Add auth token to requests
api.interceptors.request.use(async (config) => {
  const { data: { session } } = await supabase.auth.getSession()
  if (session?.access_token) {
    config.headers.Authorization = `Bearer ${session.access_token}`
  }
  return config
})

// Export all data for visualization
export const exportData = async () => {
  const response = await api.get('/data/export')
  return response.data
}

// Get statistics
export const getStats = async () => {
  const response = await api.get('/stats')
  return response.data
}

// Health check (user-specific, requires auth)
export const healthCheck = async () => {
  const response = await api.get('/health/user')
  return response.data
}

// Generate image description using Google Gemini
export const describeImage = async (imageId) => {
  const response = await api.post(`/describe/image/${imageId}`)
  return response.data
}

// Get narration audio URL for an image
export const getNarrationUrl = (imageId) => {
  return `${import.meta.env.VITE_API_URL || 'http://localhost:8001'}/narrate/image/${imageId}`
}

// Get fresh signed URL for an image (useful when URLs expire)
export const getImageUrl = async (imageId, expiresIn = 3600) => {
  const response = await api.get(`/image/${imageId}/url`, {
    params: { expires_in: expiresIn }
  })
  return response.data
}

export default api

