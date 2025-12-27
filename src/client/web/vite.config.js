import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Social API (Django) — avoids CORS in dev
      '/api/v1': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      // Vote API (Django) — avoids CORS in dev
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './tests/setup.js',
    css: true,
    exclude: ['**/node_modules/**', '**/dist/**', '**/tests/e2e/**'],
  },
})
