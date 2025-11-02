#!/usr/bin/env python3
"""
测试递归修复的脚本
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl
import tempfile
import json

def test_js_recursion_fix():
    """测试JS递归修复"""
    app = QApplication(sys.argv)
    
    # 创建一个简单的HTML页面来测试JS脚本
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <h1>测试页面</h1>
        <script>
            // 模拟可能引起递归的问题
            window.editorState = {
                currentItemId: "test-item-1"
            };
            
            // 模拟localStorage
            window.localStorage = {
                length: 2,
                data: {
                    'excalidraw-test': 'test-data',
                    'other-key': 'other-data'
                },
                key: function(index) {
                    const keys = Object.keys(this.data);
                    return keys[index];
                },
                getItem: function(key) {
                    return this.data[key];
                },
                setItem: function(key, value) {
                    this.data[key] = value;
                },
                removeItem: function(key) {
                    delete this.data[key];
                }
            };
            
            console.log('测试页面加载完成');
        </script>
    </body>
    </html>
    """
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        temp_file = f.name
    
    try:
        # 创建Web视图
        view = QWebEngineView()
        page = QWebEnginePage(view)
        view.setPage(page)
        
        # 加载页面
        url = QUrl.fromLocalFile(temp_file)
        view.load(url)
        
        # 等待页面加载完成
        view.show()
        
        # 测试重置脚本
        reset_script = """
        (function() {
            try {
                console.log('开始重置页面状态');
                
                // 重置Markdown编辑器状态
                if (window.editorState) {
                    window.editorState.currentItemId = null;
                    console.log('Markdown编辑器状态已重置');
                }
                
                // 重置Excalidraw特定状态
                try {
                    // 安全地清空localStorage中的Excalidraw数据
                    if (typeof localStorage !== 'undefined') {
                        // 创建要删除的键的副本，避免在迭代时修改对象
                        const keysToRemove = [];
                        for (let i = 0; i < localStorage.length; i++) {
                            const key = localStorage.key(i);
                            if (key && (key.startsWith('excalidraw-') || key.includes('excalidraw'))) {
                                keysToRemove.push(key);
                            }
                        }
                        
                        // 删除收集到的键
                        keysToRemove.forEach(key => {
                            localStorage.removeItem(key);
                        });
                    }
                    
                    console.log('Excalidraw特定状态已重置');
                } catch (e) {
                    console.warn('重置Excalidraw特定状态时出错:', e);
                }
                
                console.log('页面状态重置完成');
                return JSON.stringify({ success: true, message: '页面状态重置完成' });
            } catch (error) {
                console.error('重置页面状态失败:', error);
                return JSON.stringify({ success: false, error: error.message });
            }
        })();
        """
        
        # 执行脚本
        def callback(result):
            print(f"脚本执行结果: {result}")
            app.quit()
        
        page.runJavaScript(reset_script, callback)
        
        # 运行应用
        app.exec()
        
    finally:
        # 清理临时文件
        os.unlink(temp_file)

if __name__ == "__main__":
    # 添加项目根目录到Python路径
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    test_js_recursion_fix()