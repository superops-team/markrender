import { resolve, join } from 'path';
import { copyFileSync, readdirSync, statSync, existsSync, mkdirSync, readFileSync, writeFileSync, rmSync } from 'fs';

// 源目录和目标目录
const sourceDir = resolve('./dist');
const targetDir = resolve('../../app/editor/plugins/excalidraw');
const templateFile = resolve('./scripts/excalidraw-template.html');
const excalidrawNodeModulesDir = resolve('./node_modules/@excalidraw/excalidraw/dist/excalidraw-assets');

// 确保目标目录存在
if (!existsSync(targetDir)) {
  mkdirSync(targetDir, { recursive: true });
}

// 复制文件的函数
function copyFiles(src, dest) {
  if (!existsSync(src)) {
    console.error(`Source directory ${src} does not exist`);
    return;
  }

  const files = readdirSync(src);
  
  for (const file of files) {
    const srcPath = join(src, file);
    const destPath = join(dest, file);
    const stat = statSync(srcPath);
    
    if (stat.isDirectory()) {
      // 如果是目录，递归复制
      if (!existsSync(destPath)) {
        mkdirSync(destPath, { recursive: true });
      }
      copyFiles(srcPath, destPath);
    } else {
      // 特殊处理 index.html 文件，使用模板
      if (file === 'index.html') {
        handleIndexHtml(srcPath, destPath);
      } else {
        // 如果是其他文件，直接复制
        console.log(`Copying ${srcPath} to ${destPath}`);
        copyFileSync(srcPath, destPath);
      }
    }
  }
}

// 特殊处理 index.html 文件
function handleIndexHtml(srcPath, destPath) {
  if (!existsSync(srcPath)) {
    console.error(`Source index.html ${srcPath} not found`);
    return;
  }
  if (!existsSync(templateFile)) {
    console.error(`Template file ${templateFile} not found`);
    return;
  }

  // 读取构建生成的 index.html
  const srcContent = readFileSync(srcPath, 'utf8');
  
  // 查找构建生成的脚本和样式标签
  const scriptTags = srcContent.match(/<script[^>]*src="[^"]*"[^>]*><\/script>/g) || [];
  const linkTags = srcContent.match(/<link[^>]*href="[^"]*"[^>]*>/g) || [];
  
  // 读取模板文件
  let templateContent = readFileSync(templateFile, 'utf8');
  
  // 替换模板中的占位符
  templateContent = templateContent.replace('<!-- EXCALIDRAW_CSS_PLACEHOLDER -->', linkTags.join('\n    '));
  templateContent = templateContent.replace('<!-- EXCALIDRAW_JS_PLACEHOLDER -->', scriptTags.join('\n    '));
  
  // 写入目标文件
  console.log(`Generating ${destPath} from template`);
  writeFileSync(destPath, templateContent, 'utf8');
}

// 创建Excalidraw所需的资源目录结构并复制 node_modules 资产
function createExcalidrawAssetsStructure() {
  const assetsDir = join(targetDir, 'assets');
  const excalidrawAssetsDir = join(assetsDir, 'excalidraw-assets');

  // 确保excalidraw-assets目录存在
  if (!existsSync(excalidrawAssetsDir)) {
    console.log('Creating excalidraw-assets directory...');
    mkdirSync(excalidrawAssetsDir, { recursive: true });
  }

  // 复制 node_modules/@excalidraw/excalidraw/dist/excalidraw-assets 下的所有文件
  if (existsSync(excalidrawNodeModulesDir)) {
    console.log(`Copying Excalidraw assets from ${excalidrawNodeModulesDir} to ${excalidrawAssetsDir}...`);
    copyFiles(excalidrawNodeModulesDir, excalidrawAssetsDir);
  } else {
    console.warn(`Excalidraw assets directory ${excalidrawNodeModulesDir} not found. Ensure @excalidraw/excalidraw is installed.`);
  }

  // 复制 Vite 构建生成的 assets（包括 vendor.js 等）到 excalidraw-assets
  const viteAssetsDir = join(sourceDir, 'assets');
  if (existsSync(viteAssetsDir)) {
    const viteFiles = readdirSync(viteAssetsDir).filter(file => file.endsWith('.js') || file.endsWith('.css'));
    for (const file of viteFiles) {
      const srcPath = join(viteAssetsDir, file);
      const destPath = join(excalidrawAssetsDir, file);
      console.log(`Copying Vite asset ${srcPath} to ${destPath}`);
      copyFileSync(srcPath, destPath);
    }
  } else {
    console.warn(`Vite assets directory ${viteAssetsDir} not found.`);
  }
}

// 清理重复的资源目录
function cleanupDuplicateAssets() {
  const duplicateAssetsDir = join(targetDir, 'assets', 'excalidraw-assets', 'excalidraw-assets');
  if (existsSync(duplicateAssetsDir)) {
    console.log('Removing duplicate assets directory...');
    rmSync(duplicateAssetsDir, { recursive: true, force: true });
  }
}

// 执行部署操作
try {
  console.log('Deploying Excalidraw build to plugin directory...');
  copyFiles(sourceDir, targetDir);
  createExcalidrawAssetsStructure();
  cleanupDuplicateAssets();
  console.log('Deployment completed successfully!');
} catch (error) {
  console.error('Deployment failed:', error);
  process.exit(1);
}