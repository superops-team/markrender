import { defineConfig } from 'vite';
import { resolve } from 'path';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: './',
  plugins: [react()],
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    // 禁用代码压缩以避免 Excalidraw 初始化问题
    minify: false,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html')
      },
      output: {
        entryFileNames: 'assets/[name].[hash].js',
        chunkFileNames: 'assets/[name].[hash].js',
        assetFileNames: 'assets/[name].[hash].[ext]'
      }
    }
  },
  define: {
    // 定义全局变量，用于设置 Excalidraw 资源路径
    'process.env.EXCALIDRAW_ASSETS_PATH': JSON.stringify('./assets/'),
  },
  server: {
    port: 3002,
    // 确保静态资源正确服务
    fs: {
      allow: ['.', '../node_modules/@excalidraw/excalidraw']
    }
  }
});