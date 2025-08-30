const fs = require('fs');
const path = require('path');

// 部署脚本：将构建后的文件复制到PySide应用目录
const sourceDir = path.join(__dirname, '..', 'dist');
const targetDir = path.join(__dirname, '..', '..', '..', 'app', 'editor', 'plugins', 'tldraw');

// 确保目标目录存在
if (!fs.existsSync(targetDir)) {
  fs.mkdirSync(targetDir, { recursive: true });
}

// 复制文件
function copyFile(src, dest) {
  fs.copyFileSync(src, dest);
  console.log(`Copied: ${src} -> ${dest}`);
}

// 清空目标目录
if (fs.existsSync(targetDir)) {
  const files = fs.readdirSync(targetDir);
  files.forEach(file => {
    fs.unlinkSync(path.join(targetDir, file));
  });
}

// 复制所有文件
const files = fs.readdirSync(sourceDir);
files.forEach(file => {
  const srcPath = path.join(sourceDir, file);
  const destPath = path.join(targetDir, file);
  
  if (fs.statSync(srcPath).isDirectory()) {
    // 递归复制目录
    if (!fs.existsSync(destPath)) {
      fs.mkdirSync(destPath, { recursive: true });
    }
    const subFiles = fs.readdirSync(srcPath);
    subFiles.forEach(subFile => {
      const subSrcPath = path.join(srcPath, subFile);
      const subDestPath = path.join(destPath, subFile);
      copyFile(subSrcPath, subDestPath);
    });
  } else {
    copyFile(srcPath, destPath);
  }
});

console.log('TLDraw部署完成！');