import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173
  },
  define: {
    global: 'globalThis',
    'process.env': '{}',
    // 确保 Excalidraw 不使用 CDN
    'process.env.NODE_ENV': JSON.stringify('production')
  },
  build: {
    // 使用相对路径查找 assets
    assetsDir: 'assets',
    rollupOptions: {
      output: {
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name].[ext]',
        manualChunks: undefined // Disable manual chunks
      }
    },
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: null // Ensure no code splitting
      }
    }
  },
  // 配置基础路径为相对路径
  base: './',
  // 确保正确处理静态资源
  publicDir: 'public'
})