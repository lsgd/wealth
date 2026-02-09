import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8085',
        changeOrigin: true,
        timeout: 360000, // 6 min — discover flow polls for app 2FA approval
      },
    },
  },
})
