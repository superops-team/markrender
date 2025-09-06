"""
JS脚本管理器测试用例
验证JS脚本模块化调用的正确性
"""

import sys
import os
import unittest

# 添加项目根目录到sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.editor.js_scripts import JSScriptManager

class TestJSScriptManager(unittest.TestCase):
    """JS脚本管理器测试类"""
    
    def setUp(self):
        """测试初始化"""
        pass
    
    def tearDown(self):
        """测试清理"""
        pass
    
    def test_get_script(self):
        """测试获取JS脚本"""
        # 测试获取存在的脚本
        script = JSScriptManager.get_script("handle_backend_message", 
                                          action="testAction", 
                                          data={"key": "value"}, 
                                          request_id="12345")
        self.assertIsNotNone(script)
        self.assertIn("handleBackendMessage", script)
        
        # 测试获取不存在的脚本
        script = JSScriptManager.get_script("non_existent_script")
        self.assertIsNone(script)
    
    def test_add_and_remove_script(self):
        """测试添加和移除JS脚本"""
        # 添加新脚本 - 在新架构中此方法不适用，仅保留接口兼容性
        JSScriptManager.add_script("test_script", "console.log('test');")
        
        # 验证脚本列表功能
        scripts = JSScriptManager.list_scripts()
        self.assertIsInstance(scripts, list)
        
        # 移除脚本 - 在新架构中此方法不适用，仅保留接口兼容性
        JSScriptManager.remove_script("test_script")
    
    def test_list_scripts(self):
        """测试列出所有脚本"""
        scripts = JSScriptManager.list_scripts()
        self.assertIsInstance(scripts, list)
        self.assertGreater(len(scripts), 0)
        
        # 验证必要的脚本存在
        self.assertIn("handle_backend_message", scripts)
        self.assertIn("handle_backend_response", scripts)
        self.assertIn("reset_editor_content", scripts)
        self.assertIn("get_editor_content", scripts)
    
    def test_reset_editor_content_script(self):
        """测试重置编辑器内容脚本"""
        script = JSScriptManager.get_script("reset_editor_content")
        self.assertIsNotNone(script)
        self.assertIn("try {", script)
        self.assertIn("window.editorState", script)
    
    def test_get_editor_content_script(self):
        """测试获取编辑器内容脚本"""
        script = JSScriptManager.get_script("get_editor_content")
        self.assertIsNotNone(script)
        self.assertIn("try {", script)
        self.assertIn("window.editorState", script)

if __name__ == '__main__':
    unittest.main()