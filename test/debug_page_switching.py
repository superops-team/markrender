#!/usr/bin/env python3
"""
调试页面切换问题的测试脚本
"""

import sys
import os
import time
import json
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.editor.js_scripts import JSScriptManager
from app.editor.backend_interface import BackendInterface
from utils import logger

class PageSwitchingTest:
    def __init__(self):
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.backend_interface = BackendInterface("markdown")
        self.view = None
        
    def setup_markdown_test_page(self):
        """设置Markdown测试页面"""
        print("=== 设置Markdown测试页面 ===")
        
        # 创建视图
        self.view = QWebEngineView()
        
        # 设置后端接口的页面引用
        self.backend_interface.set_page(self.view.page())
        
        # 加载测试HTML，模拟Markdown页面
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Markdown Test Page</title>
        </head>
        <body>
            <textarea id="editor" style="width: 100%; height: 300px;">初始Markdown内容</textarea>
            <script>
                // 模拟编辑器状态
                window.editorState = {
                    editor: {
                        getValue: function() {
                            return document.getElementById('editor').value;
                        },
                        setValue: function(content) {
                            document.getElementById('editor').value = content;
                        }
                    },
                    currentItemId: null
                };
                
                // 模拟handleBackendMessage函数
                window.handleBackendMessage = function(action, data, requestId) {
                    console.log('Markdown handleBackendMessage called:', action, data, requestId);
                    
                    switch(action) {
                        case 'setValue':
                            if (window.editorState.editor && typeof window.editorState.editor.setValue === 'function') {
                                window.editorState.editor.setValue(data.content || '');
                                return { success: true };
                            }
                            break;
                            
                        case 'getContent':
                            if (window.editorState.editor && typeof window.editorState.editor.getValue === 'function') {
                                const content = window.editorState.editor.getValue();
                                return { success: true, content: content };
                            }
                            break;
                            
                        case 'setCurrentItemId':
                            window.editorState.currentItemId = data.item_id;
                            return { success: true };
                            
                        default:
                            console.warn('未知的action类型:', action);
                            return { success: false, error: '未知的action类型' };
                    }
                    
                    return { success: false, error: '操作失败' };
                };
                
                console.log('Markdown测试页面已加载，handleBackendMessage函数已定义');
            </script>
        </body>
        </html>
        """
        
        self.view.setHtml(html_content)
        print("✅ Markdown测试页面已加载")
        return True
    
    def setup_excalidraw_test_page(self):
        """设置Excalidraw测试页面"""
        print("=== 设置Excalidraw测试页面 ===")
        
        # 创建视图
        self.view = QWebEngineView()
        
        # 设置后端接口的页面引用
        self.backend_interface.set_page(self.view.page())
        
        # 加载测试HTML，模拟Excalidraw页面
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Excalidraw Test Page</title>
        </head>
        <body>
            <div id="excalidraw-container">Excalidraw Container</div>
            <script>
                // 模拟Excalidraw函数
                window.loadExcalidrawData = function(content) {
                    console.log('loadExcalidrawData called with:', content);
                    window.currentExcalidrawData = content;
                    return true;
                };
                
                window.getExcalidrawData = function() {
                    console.log('getExcalidrawData called');
                    return window.currentExcalidrawData || '[]';
                };
                
                window.setCurrentItemId = function(itemId) {
                    console.log('setCurrentItemId called with:', itemId);
                    window.currentItemId = itemId;
                };
                
                // 初始化一些测试数据
                window.currentExcalidrawData = '[{"id":"test1","type":"rectangle"}]';
                
                // 模拟handleBackendMessage函数
                window.handleBackendMessage = function(action, data, requestId) {
                    console.log('Excalidraw handleBackendMessage called:', action, data, requestId);
                    
                    let result = { success: true };
                    
                    switch(action) {
                        case 'loadExcalidrawData':
                            if (typeof window.loadExcalidrawData === 'function') {
                                window.loadExcalidrawData(data.content);
                            }
                            break;
                            
                        case 'setCurrentItemId':
                            if (typeof window.setCurrentItemId === 'function') {
                                window.setCurrentItemId(data.item_id);
                            }
                            break;
                            
                        case 'setValue':
                            // 处理setValue消息，设置Excalidraw内容
                            if (typeof window.loadExcalidrawData === 'function') {
                                window.loadExcalidrawData(data.content);
                            }
                            break;
                            
                        case 'getContent':
                            // 处理getContent消息，获取Excalidraw内容
                            if (typeof window.getExcalidrawData === 'function') {
                                const content = window.getExcalidrawData();
                                result = { content: content };
                            }
                            break;
                            
                        default:
                            console.log('未知的后端消息类型:', action);
                    }
                    
                    return result;
                };
                
                console.log('Excalidraw测试页面已加载，handleBackendMessage函数已定义');
            </script>
        </body>
        </html>
        """
        
        self.view.setHtml(html_content)
        print("✅ Excalidraw测试页面已加载")
        return True
    
    def wait_for_result(self, timeout=2):
        """等待结果"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            self.app.processEvents()
            time.sleep(0.01)
    
    def test_handle_backend_message(self):
        """测试handle_backend_message模板"""
        print("=== 测试handle_backend_message模板 ===")
        
        # 测试模板渲染
        script = JSScriptManager.get_script("handle_backend_message", 
                                          action="setValue", 
                                          data={"content": "测试内容"}, 
                                          request_id="test123")
        if script:
            print("✅ handle_backend_message模板渲染成功")
            print("脚本内容预览:", script[:200] + "..." if len(script) > 200 else script)
        else:
            print("❌ handle_backend_message模板渲染失败")
            return False
            
        return True
    
    def test_get_content(self, page_type="markdown"):
        """测试获取内容"""
        print(f"=== 测试{page_type}获取内容 ===")
        
        result_data = {'value': None}
        
        def handle_result(result):
            print(f"获取内容结果: {result}")
            result_data['value'] = result
            
        # 发送getContent消息
        success = self.backend_interface.send_message(
            'getContent',
            callback=handle_result,
            item_id="test_item"
        )
        
        if not success:
            print("❌ 发送getContent消息失败")
            return False
            
        # 等待结果
        self.wait_for_result()
        
        result = result_data['value']
        if result and isinstance(result, dict) and result.get('success'):
            print("✅ 获取内容成功")
            print(f"   内容: {result.get('content')}")
            return True
        else:
            print("❌ 获取内容失败")
            return False
    
    def test_set_content(self, page_type="markdown"):
        """测试设置内容"""
        print(f"=== 测试{page_type}设置内容 ===")
        
        test_content = "这是通过setValue设置的新内容"
        if page_type == "excalidraw":
            test_content = '[{"id":"new1","type":"rectangle","x":100,"y":100}]'
            
        result_data = {'value': None}
        
        def handle_result(result):
            print(f"设置内容结果: {result}")
            result_data['value'] = result
            
        # 发送setValue消息
        success = self.backend_interface.send_message(
            'setValue',
            data={"content": test_content},
            callback=handle_result,
            item_id="test_item"
        )
        
        if not success:
            print("❌ 发送setValue消息失败")
            return False
            
        # 等待结果
        self.wait_for_result()
        
        result = result_data['value']
        if result and isinstance(result, dict) and result.get('success'):
            print("✅ 设置内容成功")
            return True
        else:
            print("❌ 设置内容失败")
            return False
    
    def test_page_switching_sequence(self):
        """测试页面切换序列：保存当前内容 -> 加载新内容"""
        print("=== 测试页面切换序列 ===")
        
        # 1. 获取当前内容（模拟保存当前页面）
        if not self.test_get_content("当前页面"):
            return False
            
        # 2. 设置新内容（模拟加载新页面内容）
        if not self.test_set_content("新页面"):
            return False
            
        # 3. 再次获取内容验证（确认新内容已设置）
        if not self.test_get_content("验证"):
            return False
            
        print("✅ 页面切换序列测试通过")
        return True
    
    def run_markdown_test(self):
        """运行Markdown测试"""
        print("开始Markdown页面切换功能测试...")
        
        # 测试模板
        if not self.test_handle_backend_message():
            return False
            
        # 设置页面
        if not self.setup_markdown_test_page():
            return False
            
        # 等待页面加载完成
        self.wait_for_result(1)
        
        # 测试页面切换序列
        if not self.test_page_switching_sequence():
            return False
            
        print("Markdown页面切换功能测试完成")
        return True
    
    def run_excalidraw_test(self):
        """运行Excalidraw测试"""
        print("开始Excalidraw页面切换功能测试...")
        
        # 设置页面
        if not self.setup_excalidraw_test_page():
            return False
            
        # 等待页面加载完成
        self.wait_for_result(1)
        
        # 测试页面切换序列
        if not self.test_page_switching_sequence():
            return False
            
        print("Excalidraw页面切换功能测试完成")
        return True

def main():
    print("开始调试页面切换问题...")
    
    # 测试Markdown页面
    print("\n" + "="*50)
    print("测试Markdown页面")
    print("="*50)
    test_manager = PageSwitchingTest()
    markdown_success = test_manager.run_markdown_test()
    
    # 测试Excalidraw页面
    print("\n" + "="*50)
    print("测试Excalidraw页面")
    print("="*50)
    test_manager2 = PageSwitchingTest()
    excalidraw_success = test_manager2.run_excalidraw_test()
    
    if markdown_success and excalidraw_success:
        print("\n🎉 所有测试通过！页面切换问题已修复。")
    else:
        print("\n❌ 部分测试失败，请检查代码。")

if __name__ == "__main__":
    main()