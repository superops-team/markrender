const fs = require('fs-extra');
const path = require('path');
const { execSync } = require('child_process');

// 源目录和目标目录
const srcDir = path.resolve(__dirname, '../dist');
const destDir = path.resolve(__dirname, '../../app/editor/plugins/excalidraw');

// 先运行构建命令
console.log('开始构建 Excalidraw 项目...');
try {
  execSync('npm run build', { stdio: 'inherit' });
  console.log('构建完成！');
} catch (error) {
  console.error('构建失败:', error);
  process.exit(1);
}

// 确保目标目录存在
fs.ensureDirSync(destDir);

// 复制文件
fs.copySync(srcDir, destDir, { overwrite: true});

// 更新 index.html 中的资源路径
const indexPath = path.join(destDir, 'index.html');
if (fs.existsSync(indexPath)) {
  let indexContent = fs.readFileSync(indexPath, 'utf-8');
  
  // 替换资源路径以适应插件目录结构
  indexContent = indexContent.replace(/\/assets\//g, './assets/');
  indexContent = indexContent.replace(/\/vite\.svg/g, './vite.svg');
  
  // 更新 window.EXCALIDRAW_ASSET_PATH
  indexContent = indexContent.replace(/window\.EXCALIDRAW_ASSET_PATH = "\/assets\/";/g, 'window.EXCALIDRAW_ASSET_PATH = "./assets/";');
  
  // 更新 CSS 链接
  const assetFiles = fs.readdirSync(path.join(destDir, 'assets'));
  const indexCssFiles = assetFiles.filter(file => file.startsWith('index.') && file.endsWith('.css'));
  
  if (indexCssFiles.length > 0) {
    const indexCssFile = indexCssFiles[0];
    // 更新现有的CSS链接
    indexContent = indexContent.replace(
      /<link rel="stylesheet" href="\.\/assets\/index\.[^"]+\.css"[^>]*>/,
      `<link rel="stylesheet" href="./assets/${indexCssFile}">`
    );
  }
  
  // 更新 JavaScript 文件引用
  const mainJsFiles = assetFiles.filter(file => file.startsWith('main.') && file.endsWith('.js') && !file.includes('test'));
  
  if (mainJsFiles.length > 0) {
    // 选择最大的 main.js 文件作为入口（通常是主应用文件）
    const mainJsFile = mainJsFiles.reduce((largest, current) => {
      const largestSize = fs.statSync(path.join(destDir, 'assets', largest)).size;
      const currentSize = fs.statSync(path.join(destDir, 'assets', current)).size;
      return currentSize > largestSize ? current : largest;
    });
    
    console.log(`选择的主JavaScript文件: ${mainJsFile}`);
    
    // 更新 script 标签
    indexContent = indexContent.replace(
      /<script type="module" crossorigin src="\.\/assets\/main\.[^"]+\.js"><\/script>/,
      `<script type="module" crossorigin src="./assets/${mainJsFile}"></script>`
    );
    
    // 更新 modulepreload 链接（如果存在）
    indexContent = indexContent.replace(
      /<link rel="modulepreload" crossorigin href="\.\/assets\/main\.[^"]+\.js">/g,
      `<link rel="modulepreload" crossorigin href="./assets/${mainJsFile}">`
    );
  }
  
  // 特殊处理：确保引用正确的主文件
  // 检查是否存在 main.js 文件（可能是复制过程中重命名的）
  if (assetFiles.includes('main.js')) {
    indexContent = indexContent.replace(
      /<script type="module" crossorigin src="\.\/assets\/main\.[^"]+\.js"><\/script>/,
      `<script type="module" crossorigin src="./assets/main.js"></script>`
    );
    
    indexContent = indexContent.replace(
      /<link rel="modulepreload" crossorigin href="\.\/assets\/main\.[^"]+\.js">/g,
      `<link rel="modulepreload" crossorigin href="./assets/main.js">`
    );
    console.log('使用重命名后的 main.js 文件');
  }
  
  fs.writeFileSync(indexPath, indexContent, 'utf-8');
  console.log('已更新 index.html 中的资源路径');
}

console.log('Excalidraw 部署完成！');