/**
 * API client for backend communication
 */
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 second timeout for heavy operations
})

// Upload single image
export const uploadImage = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

// Upload multiple images
export const uploadImagesBatch = async (files) => {
  const formData = new FormData()
  files.forEach(file => {
    formData.append('files', file)
  })
  
  const response = await api.post('/embed/batch', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

// Project embeddings to 3D
export const projectTo3D = async () => {
  const response = await api.post('/project')
  return response.data
}

// Build kNN graph
export const buildGraph = async (k = 8) => {
  const response = await api.post('/graph', null, {
    params: { k }
  })
  return response.data
}

// Search by text
export const searchByText = async (query, k = 10) => {
  const response = await api.post('/search', {
    query,
    k
  })
  return response.data
}

// Search by image
export const searchByImage = async (file, k = 10) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post(`/search/image?k=${k}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

// Label clusters with Claude
export const labelClusters = async (clusterIds) => {
  const response = await api.post('/clusters/label', {
    cluster_ids: clusterIds
  })
  return response.data
}

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

// Health check
export const healthCheck = async () => {
  const response = await api.get('/')
  return response.data
}

export default api

