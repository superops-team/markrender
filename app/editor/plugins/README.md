# 插件JS处理器架构说明

## 目录结构

```
plugins/
├── markdown/
│   ├── handler/
│   │   ├── getContent.js
│   │   ├── setValue.js
│   │   ├── reset.js
│   │   └── resetPageState.js
│   └── ...
├── excalidraw/
│   ├── handler/
│   │   ├── getContent.js
│   │   ├── setValue.js
│   │   ├── reset.js
│   │   └── resetPageState.js
│   └── ...
└── ...
```

## 架构说明

1. 每个插件目录下都有一个`handler`子目录，用于存放该插件专用的JS处理器文件
2. JS处理器文件名与BackendInterface中定义的action名称对应
3. JSScriptManager会优先从插件的handler目录加载特定页面类型的JS文件
4. 如果找不到特定页面类型的JS文件，则回退到通用的js_templates目录

## 处理器文件说明

- `getContent.js`: 获取编辑器内容
- `setValue.js`: 设置编辑器内容
- `reset.js`: 重置编辑器
- `resetPageState.js`: 重置页面状态

## 使用方式

在BackendInterface中，通过`send_message`或`send_message_sync`方法发送消息时，会自动根据当前的page_type加载对应的处理器文件。