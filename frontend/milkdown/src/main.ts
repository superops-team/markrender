import { Crepe } from '@milkdown/crepe';
import { history } from '@milkdown/plugin-history';
import { clipboard } from '@milkdown/plugin-clipboard';
import { indent } from '@milkdown/plugin-indent';
import { cursor } from '@milkdown/plugin-cursor';

import '@milkdown/crepe/theme/common/style.css';
import '@milkdown/crepe/theme/frame.css';

const markdown = `
# Milkdown Editor Crepe test

- 支持工具栏
- 支持表格、代码块、emoji 等扩展
`;

await new Crepe({
  root: '#app',
  defaultValue: markdown,
  plugins: [
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
}).create();
