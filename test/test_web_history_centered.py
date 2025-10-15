#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web版本历史记录项居中测试
启动本地web服务器查看效果
"""

import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template_string
from PySide6.QtWidgets import QApplication, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QPainter

from app.history.history_item import HistoryItemWidget
from app.preference.app_style import AppStyle

app = Flask(__name__)

class MockHistoryRecord:
    """模拟历史记录对象"""
    def __init__(self, change_type, change_at):
        self.change_type = change_type
        self.change_at = change_at

def create_test_image():
    """创建测试图片"""
    app_qt = QApplication.instance() or QApplication(sys.argv)
    
    # 创建列表部件
    list_widget = QListWidget()
    list_widget.setSpacing(8)
    list_widget.setUniformItemSizes(True)
    
    # 应用样式
    app_style = AppStyle()
    list_widget.setStyleSheet(app_style.get_quickpick_panel())
    
    # 创建测试数据
    now = datetime.now()
    test_records = [
        MockHistoryRecord('content_create', now - timedelta(minutes=5)),
        MockHistoryRecord('content_update', now - timedelta(minutes=10)),
        MockHistoryRecord('title_update', now - timedelta(hours=1)),
        MockHistoryRecord('setting_update', now - timedelta(days=1)),
    ]
    
    # 添加到列表
    for i, record in enumerate(test_records):
        item_widget = HistoryItemWidget(record)
        list_item = QListWidgetItem(list_widget)
        list_item.setSizeHint(QSize(400, 40))
        list_widget.setItemWidget(list_item, item_widget)
        
        # 选中第一个项进行测试
        if i == 0:
            item_widget.set_selected(True)
    
    # 调整列表大小
    list_widget.resize(400, 200)
    list_widget.show()
    
    # 创建截图
    pixmap = QPixmap(list_widget.size())
    list_widget.render(pixmap)
    
    # 保存图片
    image_path = "/tmp/history_test.png"
    pixmap.save(image_path)
    
    return image_path

@app.route('/')
def index():
    """主页路由"""
    image_path = create_test_image()
    
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>历史记录项居中测试</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .test-image {
                max-width: 100%;
                height: auto;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin: 20px 0;
            }
            .status {
                padding: 10px;
                margin: 10px 0;
                border-radius: 4px;
            }
            .success {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .info {
                background-color: #d1ecf1;
                color: #0c5460;
                border: 1px solid #bee5eb;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>历史记录项居中测试</h1>
            <div class="status info">
                <strong>测试说明：</strong>此测试检查历史记录项中的change_type和change_at内容在选中时是否垂直居中显示。
            </div>
            
            <h2>测试结果：</h2>
            <img src="/static/history_test.png" alt="历史记录项测试截图" class="test-image">
            
            <h2>检查要点：</h2>
            <ul>
                <li>✅ 选中项的背景色是否正确应用</li>
                <li>✅ change_type文本是否垂直居中</li>
                <li>✅ change_at时间文本是否垂直居中</li>
                <li>✅ 文本颜色在选中状态下是否有足够对比度</li>
                <li>✅ 分割线是否正确显示</li>
            </ul>
            
            <div class="status success">
                <strong>状态：</strong>测试已完成，请检查截图中的居中效果。
            </div>
            
            <p><a href="/">刷新页面重新生成测试</a></p>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template)

@app.route('/static/history_test.png')
def serve_image():
    """提供测试图片"""
    image_path = create_test_image()
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    from flask import Response
    return Response(image_data, mimetype='image/png')

if __name__ == '__main__':
    print("启动Web测试服务器...")
    print("访问 http://localhost:8000 查看测试结果")
    app.run(host='0.0.0.0', port=8000, debug=True)