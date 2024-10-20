import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

// https://vitejs.dev/config/
const root = resolve(__dirname, 'src') // Points to the src directory
export default defineConfig({
  root,
  plugins: [react()],
  build: {
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(root, 'index.html'), // Points to src/index.html
        login: resolve(root, 'login', 'index.html'), // Points to src/about/index.html
      }
    }
  }
})
