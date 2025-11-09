import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // Set base path for GitHub Pages (replace YOUR_REPO_NAME with your actual repo name)
  // If your repo is at https://username.github.io/repo-name/, set base to '/repo-name/'
  // If your repo is at https://username.github.io/ (user/organization page), set base to '/'
  base: process.env.NODE_ENV === 'production' ? '/HackUMassXIII/' : '/',
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})

