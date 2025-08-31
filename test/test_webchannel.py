#!/usr/bin/env python3

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.editor.webengine import WebPageManager
from app.editor.channel import WebCommunicationManager
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

def main():
    app = QApplication(sys.argv)
    
    # 创建页面管理器和通信管理器
    page_manager = WebPageManager()
    page_id = 'test_page'
    comm_manager = WebCommunicationManager(page_id)
    
    # 创建页面
    view = page_manager.create_page(page_id, comm_manager)
    
    def test_communication():
        print('开始测试WebChannel通信...')
        print(f'页面对象是否设置: {comm_manager.page is not None}')
        
        # 测试JavaScript函数是否存在
        def check_function_exists(result):
            print(f'handlePythonMessage函数类型: {result}')
            
            if result == 'function':
                print('✅ handlePythonMessage函数已正确定义')
                # 测试发送消息到前端
                success1 = comm_manager.send_message('test', {'message': '这是一个测试消息'})
                print(f'发送测试消息结果: {success1}')
                
                success2 = comm_manager.send_message('setValue', {'content': '# 测试内容\n这是测试消息'})
                print(f'发送setValue消息结果: {success2}')
            else:
                print(f'❌ handlePythonMessage函数未定义，类型: {result}')
            
        view.page().runJavaScript('typeof window.handlePythonMessage', check_function_exists)
    
    # 加载简化的HTML文件
    success = page_manager.load_html(page_id, 'test_simple')
    print(f'加载HTML结果: {success}')
    
    # 等待3秒后测试通信
    QTimer.singleShot(3000, test_communication)
    
    # 10秒后退出应用
    QTimer.singleShot(10000, app.quit)
    
    app.exec()
    print('测试完成')

if __name__ == '__main__':
    main()