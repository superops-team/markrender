#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// 获取当前文件目录
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🚀 开始部署 Excalidraw 到资源目录...\n');

// 路径配置
const sourceDir = path.join(__dirname, '../browser');
const targetDir = path.join(__dirname, '../../../app/editor/plugins/excalidraw');
const htmlTemplatePath = path.join(__dirname, '../../../app/editor/plugins/excalidraw/index.html');

// 确保目标目录存在
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`✅ 创建目录: ${dir}`);
  }
}

// 复制文件夹
function copyDir(src, dest) {
  ensureDir(dest);
  const entries = fs.readdirSync(src, { withFileTypes: true });
  
  for (let entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// 查找最新的JS文件
function findLatestJSFile(assetsDir) {
  const files = fs.readdirSync(assetsDir)
    .filter(file => file.startsWith('index-') && file.endsWith('.js'))
    .filter(file => {
      const stats = fs.statSync(path.join(assetsDir, file));
      return stats.size > 1000000; // 只考虑大于1MB的文件（主文件）
    })
    .sort((a, b) => {
      const statsA = fs.statSync(path.join(assetsDir, a));
      const statsB = fs.statSync(path.join(assetsDir, b));
      return statsB.mtime - statsA.mtime; // 按修改时间降序
    });
  
  return files[0] || null;
}

// 查找最新的CSS文件
function findLatestCSSFile(assetsDir) {
  const files = fs.readdirSync(assetsDir)
    .filter(file => file.startsWith('index-') && file.endsWith('.css'))
    .sort((a, b) => {
      const statsA = fs.statSync(path.join(assetsDir, a));
      const statsB = fs.statSync(path.join(assetsDir, b));
      return statsB.mtime - statsA.mtime;
    });
  
  return files[0] || null;
}

// 更新HTML模板
function updateHTMLTemplate(jsFile, cssFile) {
  try {
    let htmlContent = fs.readFileSync(htmlTemplatePath, 'utf8');
    
    // 更新JS文件引用 - 修复路径问题
    if (jsFile) {
      // 移除旧的JS引用
      htmlContent = htmlContent.replace(/<script[^>]*src="\.\/assets\/index-[^"]*\.js"[^>]*><\/script>/g, '');
      // 添加新的JS引用，确保路径正确
      const newJSScript = `    <script type="module" crossorigin src="./assets/${jsFile}"></script>`;
      // 在合适的位置插入新的JS引用
      htmlContent = htmlContent.replace('</head>', `    ${newJSScript}\n  </head>`);
      console.log(`✅ 更新JS文件引用: ${jsFile}`);
    }
    
    // 更新CSS文件引用
    if (cssFile) {
      // 移除旧的CSS引用
      htmlContent = htmlContent.replace(/<link[^>]*href="\.\/assets\/index-[^"]*\.css"[^>]*>/g, '');
      // 添加新的CSS引用，确保路径正确
      const newCSSLink = `    <link rel="stylesheet" crossorigin href="./assets/${cssFile}">`;
      // 在合适的位置插入新的CSS引用
      htmlContent = htmlContent.replace('</head>', `    ${newCSSLink}\n  </head>`);
      console.log(`✅ 更新CSS文件引用: ${cssFile}`);
    }
    
    fs.writeFileSync(htmlTemplatePath, htmlContent, 'utf8');
    console.log(`✅ HTML模板更新完成: ${htmlTemplatePath}`);
    
  } catch (error) {
    console.error(`❌ 更新HTML模板失败:`, error.message);
  }
}

// 主部署流程
try {
  console.log('📁 复制dist文件到目标目录...');
  copyDir(sourceDir, targetDir);
  console.log(`✅ 文件复制完成: ${sourceDir} -> ${targetDir}\n`);
  
  console.log('🔍 查找最新的资源文件...');
  const assetsDir = path.join(targetDir, 'assets');
  const latestJSFile = findLatestJSFile(assetsDir);
  const latestCSSFile = findLatestCSSFile(assetsDir);
  
  if (latestJSFile) {
    console.log(`📦 找到最新JS文件: ${latestJSFile}`);
  } else {
    console.warn('⚠️  未找到JS文件');
  }
  
  if (latestCSSFile) {
    console.log(`🎨 找到最新CSS文件: ${latestCSSFile}`);
  } else {
    console.warn('⚠️  未找到CSS文件');
  }
  
  console.log('\n📝 更新HTML模板...');
  updateHTMLTemplate(latestJSFile, latestCSSFile);
  
  console.log('\n🎉 部署完成！');
  console.log('💡 使用 npm run build-and-deploy 一键构建并部署');
  
} catch (error) {
  console.error('❌ 部署失败:', error);
  process.exit(1);
}