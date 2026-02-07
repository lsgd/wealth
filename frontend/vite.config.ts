import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5000,
    proxy: {
      '/api': {
        target: 'http://localhost:8084',
        changeOrigin: true,
        timeout: 360000, // 6 min — discover flow polls for app 2FA approval
      },
    },
  },
})
