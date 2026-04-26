import process from 'node:process'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// Porta do Uvicorn em dev: padrão 8000, ou `set BACKEND_PORT=8040` (ex.: e2e com backend sem --reload)
const backPort = process.env.BACKEND_PORT || '8000'
const backTarget = `http://127.0.0.1:${backPort}`

// https://vite.dev/config/
export default defineConfig({
  plugins: [tailwindcss(), react()],
  server: {
    // Mesma origem que o Vite (ex.: 127.0.0.1:5173) — evita CORS no dev quando a API
    // usava http://localhost:8000 e a página 127.0.0.1:5173 (origens diferentes no browser).
    proxy: {
      '/api': {
        target: backTarget,
        changeOrigin: true,
      },
    },
  },
})
