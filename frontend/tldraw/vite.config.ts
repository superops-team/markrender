import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react' // 添加react插件导入

// https://vite.dev/config/
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
        assetFileNames: (assetInfo: { name?: string }) => {
          if (assetInfo.name && typeof assetInfo.name === 'string' && assetInfo.name.endsWith('.css')) {
            return 'assets/index.css';
          }
          return `assets/[name].[ext]`;
        },
        
        // 自定义分块策略
        manualChunks: (id: string) => {
          if (id.includes('node_modules')) {
            return 'vendor';
          }
        },
      },
    },
  },
})