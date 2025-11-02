#!/usr/bin/env python3
"""
测试内容设置的脚本
"""

import sys
import os
import tempfile

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl

def test_content_setting():
    """测试内容设置"""
    app = QApplication(sys.argv)
    
    # 创建一个简单的HTML页面来测试内容设置
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <h1>测试页面</h1>
        <div id="content"></div>
        <script>
            // 模拟编辑器状态
            window.editorState = {
                editor: {
                    setValue: function(content) {
                        console.log('设置内容:', content);
                        document.getElementById('content').innerText = content;
                    },
                    getValue: function() {
                        return document.getElementById('content').innerText;
                    }
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
        
        # 测试设置内容
        test_content = "这是一个测试内容\n包含多行文本"
        
        set_content_script = f"""
        (function() {{
            try {{
                const content = {repr(test_content)};
                console.log('开始设置内容:', content);
                
                // 模拟延迟设置
                setTimeout(() => {{
                    try {{
                        if (window.editorState && window.editorState.editor && typeof window.editorState.editor.setValue === 'function') {{
                            window.editorState.editor.setValue(content);
                            console.log('内容设置完成');
                        }}
                    }} catch (e) {{
                        console.error('设置内容时出错:', e);
                    }}
                }}, 10);
                
                return JSON.stringify({{ success: true }});
            }} catch (error) {{
                console.error('设置内容失败:', error);
                return JSON.stringify({{ success: false, error: error.message }});
            }}
        }})();
        """
        
        # 执行脚本
        def callback(result):
            print(f"脚本执行结果: {result}")
            app.quit()
        
        page.runJavaScript(set_content_script, callback)
        
        # 运行应用
        app.exec()
        
    finally:
        # 清理临时文件
        os.unlink(temp_file)

if __name__ == "__main__":
    test_content_setting()