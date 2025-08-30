import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    rollupOptions: {
      output: {
        // 设置固定的入口JS文件名
        entryFileNames: 'assets/index.js',
        
        // 将所有依赖项打包到一个单独的vendor.js文件中
        chunkFileNames: 'assets/vendor.js',
        
        // 设置固定的资源文件名（CSS和其他资源）
        assetFileNames: (assetInfo) => {
          if (assetInfo.name && assetInfo.name.endsWith('.css')) {
            return 'assets/index.css';
          }
          return `assets/[name].[ext]`;
        },
        
        // 自定义分块策略，将所有node_modules中的模块放入vendor块
        manualChunks: (id) => {
          if (id.includes('node_modules')) {
            return 'vendor';
          }
        },
      },
    },
  },
})
