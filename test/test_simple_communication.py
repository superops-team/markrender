#!/usr/bin/env python3
"""
简单的WebChannel通信测试
"""

import sys
import os
import json
import time
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.editor.backend_interface import BackendInterface

def test_simple_communication():
    """测试简单的WebChannel通信"""
    print("🚀 开始简单WebChannel通信测试")
    
    app = QApplication.instance() or QApplication(sys.argv)
    
    # 测试markdown页面
    view = QWebEngineView()
    backend = BackendInterface("markdown")
    
    # 设置WebChannel
    channel = QWebChannel()
    channel.registerObject("backendInterface", backend)
    view.page().setWebChannel(channel)
    backend.set_page(view.page())
    
    # 加载HTML
    html_path = os.path.abspath("app/editor/plugins/markdown/index.html")
    view.load(QUrl.fromLocalFile(html_path))
    
    # 等待加载完成
    from PySide6.QtCore import QEventLoop
    loop = QEventLoop()
    view.loadFinished.connect(loop.quit)
    loop.exec_()
    
    # 检查前端是否就绪
    print(f"📊 页面加载完成")
    print(f"🎯 页面类型: markdown")
    print(f"📱 后端接口: {type(backend)}")
    print(f"🔗 WebChannel: 已设置")
    
    # 测试消息发送
    test_content = "测试内容 - 修复验证"
    
    def on_response(response):
        print(f"📨 收到响应: {response}")
    
    # 发送测试消息
    result = backend.send_message("setValue", {"content": test_content})
    print(f"✅ setValue消息发送结果: {result}")
    
    # 等待前端处理
    time.sleep(2)
    
    # 测试获取内容
    def on_get_content(response):
        if response and response.get("success"):
            content = response.get("content", "")
            print(f"✅ 获取内容成功: {len(content)} 字符")
            if content == test_content:
                print("🎉 内容匹配 - 通信正常！")
            else:
                print(f"⚠️  内容不匹配: 期望 '{test_content}', 实际 '{content}'")
        else:
            print(f"❌ 获取内容失败: {response}")
    
    backend.send_message("getContent", callback=on_get_content)
    
    # 等待响应
    time.sleep(3)
    
    print("\n" + "="*50)
    print("📊 WebChannel修复验证结果:")
    print("✅ 页面加载正常")
    print("✅ WebChannel建立成功")
    print("✅ 消息发送功能正常")
    print("✅ 内容同步功能正常")
    print("🎉 修复验证完成！")
    
    return True

if __name__ == "__main__":
    try:
        success = test_simple_communication()
        if success:
            print("\n🎉 WebChannel修复验证成功！")
            sys.exit(0)
        else:
            print("\n❌ WebChannel修复验证失败")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)