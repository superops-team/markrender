import { Crepe } from '@milkdown/crepe';
import { history } from '@milkdown/plugin-history';
import { clipboard } from '@milkdown/plugin-clipboard';
import { indent } from '@milkdown/plugin-indent';
import { cursor } from '@milkdown/plugin-cursor';
import { commonmark } from '@milkdown/preset-commonmark';
import { gfm } from '@milkdown/preset-gfm';

import '@milkdown/crepe/theme/common/style.css';
import '@milkdown/crepe/theme/frame.css';

const markdown = `
# Milkdown Editor Crepe test

- 支持工具栏
- 支持表格、代码块、emoji 等扩展
`;

// 使用异步函数包装顶层await
async function initEditor() {
  try {
    // 确保DOM元素存在
    const appElement = document.getElementById('app');
    if (!appElement) {
      console.error('App element not found');
      return;
    }

    const crepe = new Crepe({
      root: '#app',
      defaultValue: markdown,
      plugins: [
        commonmark,
        gfm,
        history,
        clipboard,
        indent,
        cursor,
      ],
      toolbar: {
        items: [
          ['bold', 'italic', 'strike'],
          ['heading', 'quote', 'link'],
          ['table', 'code', 'emoji'],
          ['undo', 'redo'],
        ],
      },
    });
    
    await crepe.create();
    console.log('Milkdown editor created successfully');
  } catch (error) {
    console.error('Failed to create Milkdown editor:', error);
    // 如果创建失败，尝试只使用最基本的配置
    try {
      const basicCrepe = new Crepe({
        root: '#app',
        defaultValue: markdown,
      });
      await basicCrepe.create();
      console.log('Basic Milkdown editor created successfully');
    } catch (basicError) {
      console.error('Failed to create basic Milkdown editor:', basicError);
    }
  }
}

// 确保DOM加载完成后再初始化编辑器
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initEditor);
} else {
  initEditor();
}