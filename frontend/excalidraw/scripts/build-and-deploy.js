#!/usr/bin/env node

/**
 * Excalidraw构建和部署脚本
 * 自动化解决浏览器白屏问题并确保Qt WebEngine兼容性
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// 获取当前文件目录
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.join(__dirname, '../../..');

console.log('🚀 开始Excalidraw构建和部署...\n');

// 路径配置
const sourceDir = path.join(__dirname, '../dist');
const targetDir = path.join(__dirname, '../../../app/editor/plugins/excalidraw');
const browserDir = path.join(__dirname, '../browser');
const htmlTemplatePath = path.join(targetDir, 'index.html');

// 确保目录存在
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

// 更新HTML模板（Qt WebEngine版本）
function updateHTMLTemplate(jsFile, cssFile) {
  try {
    let htmlContent = fs.readFileSync(htmlTemplatePath, 'utf8');
    
    // 确保webchannel-core.js引用存在
    if (!htmlContent.includes('webchannel-core.js')) {
      // 在qwebchannel.js引用后添加webchannel-core.js引用
      htmlContent = htmlContent.replace(
        '<script src="qrc:/qtwebchannel/qwebchannel.js"></script>',
        '<script src="qrc:/qtwebchannel/qwebchannel.js"></script>\n    <script src="./webchannel-core.js"></script>'
      );
      console.log('✅ 添加webchannel-core.js引用');
    }
    
    // 更新JS文件引用
    if (jsFile) {
      // 移除旧的JS引用
      htmlContent = htmlContent.replace(/<script[^>]*src="\.\/assets\/index-[^"]*\.js"[^>]*><\/script>/g, '');
      // 添加新的JS引用
      const newJSScript = `    <script type="module" crossorigin src="./assets/${jsFile}"></script>`;
      htmlContent = htmlContent.replace('</head>', `    ${newJSScript}\n  </head>`);
      console.log(`✅ 更新JS文件引用: ${jsFile}`);
    }
    
    // 更新CSS文件引用
    if (cssFile) {
      // 移除旧的CSS引用
      htmlContent = htmlContent.replace(/<link[^>]*href="\.\/assets\/index-[^"]*\.css"[^>]*>/g, '');
      // 添加新的CSS引用
      const newCSSLink = `    <link rel="stylesheet" crossorigin href="./assets/${cssFile}">`;
      htmlContent = htmlContent.replace('</head>', `    ${newCSSLink}\n  </head>`);
      console.log(`✅ 更新CSS文件引用: ${cssFile}`);
    }
    
    fs.writeFileSync(htmlTemplatePath, htmlContent, 'utf8');
    console.log(`✅ HTML模板更新完成: ${htmlTemplatePath}`);
    
  } catch (error) {
    console.error(`❌ 更新HTML模板失败:`, error.message);
  }
}

// 修复HTML文件（浏览器版本）
function fixHTMLFileForBrowser(htmlPath) {
  try {
    let htmlContent = fs.readFileSync(htmlPath, 'utf8');
    
    // 移除Qt特有的WebChannel引用
    htmlContent = htmlContent.replace(/<script src="qrc:\/qtwebchannel\/qwebchannel\.js"><\/script>/g, '');
    
    // 确保webchannel-core.js引用存在（使用相对路径）
    if (!htmlContent.includes('webchannel-core.js')) {
      // 在<head>中添加webchannel-core.js引用
      htmlContent = htmlContent.replace(
        '<head>',
        '<head>\n    <script src="./webchannel-core.js"></script>'
      );
      console.log('✅ 为浏览器版本添加webchannel-core.js引用');
    }
    
    // 添加浏览器兼容的WebChannel模拟
    const webChannelMock = `
    <!-- WebChannel模拟用于浏览器调试 -->
    <script>
      // 模拟QWebChannel对象
      if (typeof QWebChannel === 'undefined') {
        window.QWebChannel = function(transport, callback) {
          console.log('ℹ️ 浏览器模式: 使用WebChannel模拟');
          const mockBackend = {
            backendInterface: {
              dispatch_request: function(request) {
                console.log('📤 模拟发送请求:', request);
                // 返回模拟响应
                const requestData = JSON.parse(request);
                return Promise.resolve(JSON.stringify({
                  success: true,
                  requestId: requestData.requestId,
                  data: { message: '浏览器模拟响应' }
                }));
              },
              frontend_ready: function() {
                console.log('✅ 前端就绪(模拟)');
              },
              handle_web_response: function(response) {
                console.log('📥 收到Web响应(模拟):', response);
              }
            }
          };
          
          // 模拟异步初始化
          setTimeout(() => {
            callback(mockBackend);
          }, 100);
        };
      }
      
      // 确保window.qt对象存在
      if (!window.qt) {
        window.qt = {
          webChannelTransport: {}
        };
      }
    </script>`;
    
    // 在<head>标签中合适的位置插入WebChannel模拟
    htmlContent = htmlContent.replace('<head>', `<head>${webChannelMock}`);
    
    fs.writeFileSync(htmlPath, htmlContent, 'utf8');
    console.log(`✅ 浏览器版本HTML文件修复完成: ${htmlPath}`);
    
  } catch (error) {
    console.error(`❌ 修复浏览器版本HTML文件失败:`, error.message);
  }
}

// 主部署流程
try {
  console.log('📁 复制dist文件到目标目录...');
  copyDir(sourceDir, targetDir);
  console.log(`✅ 文件复制完成: ${sourceDir} -> ${targetDir}\n`);
  
  console.log('📁 生成浏览器兼容版本...');
  copyDir(sourceDir, browserDir);
  console.log(`✅ 浏览器版本生成完成: ${sourceDir} -> ${browserDir}\n`);
  
  console.log('🔍 查找最新的资源文件...');
  const assetsDir = path.join(targetDir, 'assets');
  const latestJSFile = findLatestJSFile(assetsDir);
  const latestCSSFile = findLatestCSSFile(assetsDir);
  
  if (latestJSFile) {
    console.log(`📦 找到最新JS文件: ${latestJSFile}`);
  } else {
    console.warn('⚠️ 未找到JS文件');
  }
  
  if (latestCSSFile) {
    console.log(`🎨 找到最新CSS文件: ${latestCSSFile}`);
  } else {
    console.warn('⚠️ 未找到CSS文件');
  }
  
  console.log('\n📝 更新Qt版本HTML模板...');
  updateHTMLTemplate(latestJSFile, latestCSSFile);
  
  console.log('\n📝 修复浏览器版本HTML文件...');
  const browserHtmlPath = path.join(browserDir, 'index.html');
  if (fs.existsSync(browserHtmlPath)) {
    fixHTMLFileForBrowser(browserHtmlPath);
  }
  
  console.log('\n🎉 Excalidraw构建和部署完成！');
  console.log('💡 使用方法:');
  console.log('   Qt版本: 直接在MarkRender应用中使用');
  console.log('   浏览器版本: cd frontend/excalidraw/browser && python -m http.server 8000');
  
} catch (error) {
  console.error('❌ 部署失败:', error);
  process.exit(1);
}