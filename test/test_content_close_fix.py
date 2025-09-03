#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编辑器有内容时关闭按钮修复验证脚本
专门测试当编辑器有内容时的关闭行为
"""

import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class ContentCloseTestWindow(QMainWindow):
    """有内容时关闭测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✅ 编辑器有内容时关闭修复验证")
        self.setGeometry(100, 100, 900, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("✅ 编辑器有内容时关闭按钮修复验证")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # 问题描述
        problem_desc = QLabel("""
        🐛 用户反馈的具体问题：
        
        "你修改的版本当页面为空页面的时候能退出软件，但是当软件editor上有编辑的内容时就无法退出了"
        
        📋 问题分析：
        • 空页面时关闭正常 ✅
        • 有内容时关闭失效 ❌
        • 说明修复的条件判断可能有问题
        • 可能是超时机制没有正确触发
        """)
        problem_desc.setFont(QFont("Menlo", 11))
        problem_desc.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 8px;
                padding: 20px;
                color: #856404;
                line-height: 1.5;
            }
        """)
        layout.addWidget(problem_desc)
        
        # 修复要点
        fix_points = QLabel("""
        🔧 针对性修复要点：
        
        ✅ 1. 完善状态检查条件：
        • 检查 web_comm 是否存在且有效
        • 检查 document 是否存在且有 item_id
        • 检查 page_loaded 状态是否为 True
        • 只有所有条件满足才尝试保存
        
        ✅ 2. 增强超时保护：
        • 3秒超时定时器，无论保存是否成功
        • 超时后强制调用 _force_close()
        • 确保即使 WebCommunication 失败也能关闭
        
        ✅ 3. 改进回调处理：
        • save_markdown 回调中增加异常处理
        • 确保回调总是会调用 _cleanup_and_close()
        • 停止超时定时器避免重复关闭
        
        ✅ 4. 优化关闭流程：
        • 使用 _close_ready 标记避免重复处理
        • 通过 QTimer.singleShot 异步关闭父窗口
        • 避免直接调用 QApplication.quit()
        """)
        fix_points.setFont(QFont("Menlo", 11))
        fix_points.setStyleSheet("""
            QLabel {
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 8px;
                padding: 20px;
                color: #155724;
                line-height: 1.5;
            }
        """)
        layout.addWidget(fix_points)
        
        # 测试场景
        test_scenarios = QLabel("""
        🧪 重点测试场景：
        
        📝 场景1 - 有item_id的文档：
        • 打开或创建一个文档（有明确的item_id）
        • 编辑一些内容
        • 点击关闭按钮
        • 预期：应该保存内容后在3秒内关闭
        
        📝 场景2 - 无item_id但有内容：
        • 在编辑器中输入内容但未保存为文档
        • 点击关闭按钮
        • 预期：应该直接关闭（跳过保存）
        
        📝 场景3 - 页面未完全加载：
        • 在应用启动过程中快速点击关闭
        • 预期：应该直接关闭，不等待页面加载
        
        📝 场景4 - WebCommunication故障：
        • 模拟网络通信失败的情况
        • 预期：3秒后超时强制关闭
        """)
        test_scenarios.setFont(QFont("Menlo", 10))
        test_scenarios.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 20px;
                color: #495057;
                line-height: 1.4;
            }
        """)
        layout.addWidget(test_scenarios)
        
        # 验证步骤
        verification_steps = QLabel("""
        🔍 详细验证步骤：
        
        1️⃣ 启动应用测试：
        • 点击下方按钮启动 MarkRender
        • 观察应用是否正常启动
        
        2️⃣ 空状态测试：
        • 应用启动后立即点击关闭按钮
        • 确认能够正常关闭（已知正常）
        
        3️⃣ 有内容测试：
        • 选择或创建一个文档
        • 在编辑器中输入一些文字
        • 点击关闭按钮
        • 观察关闭时间（应该在3秒内）
        
        4️⃣ 日志观察：
        • 关注控制台日志输出
        • 确认是否有"退出前获取文档对象"日志
        • 确认是否有"强制关闭"或超时日志
        
        ✅ 成功标准：
        • 有内容时点击关闭按钮一次即可生效
        • 关闭时间不超过3秒
        • 内容被正确保存（如果有item_id）
        • 控制台无错误日志
        """)
        verification_steps.setFont(QFont("Menlo", 10))
        verification_steps.setStyleSheet("""
            QLabel {
                background-color: #e8f5e8;
                border: 1px solid #c3e6cb;
                border-radius: 8px;
                padding: 20px;
                color: #155724;
                line-height: 1.4;
            }
        """)
        layout.addWidget(verification_steps)
        
        # 启动测试按钮
        test_btn = QPushButton("🚀 启动MarkRender进行有内容关闭测试")
        test_btn.clicked.connect(self.start_main_app)
        test_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        layout.addWidget(test_btn)
        
    def start_main_app(self):
        """启动主应用进行测试"""
        try:
            print("🚀 启动MarkRender主应用...")
            print("📋 有内容关闭测试步骤：")
            print("1. 等待应用完全启动")
            print("2. 选择一个现有文档或创建新文档")
            print("3. 在编辑器中添加/修改一些内容")
            print("4. 点击红色关闭按钮")
            print("5. 观察关闭响应时间和行为")
            print("")
            print("🔍 观察要点：")
            print("• 点击关闭按钮后是否立即响应")
            print("• 关闭过程是否在3秒内完成")
            print("• 控制台是否输出相关保存日志")
            print("• 内容是否被正确保存")
            print("")
            print("⚠️  如果仍然无法关闭：")
            print("• 请等待3秒看是否有超时强制关闭")
            print("• 查看控制台是否有错误信息")
            print("• 记录具体的卡住状态")
            
            # 导入并启动主应用
            from main import MainWindow
            from PySide6.QtWidgets import QApplication
            
            # 创建主应用窗口
            main_window = MainWindow()
            main_window.show()
            
            print("✅ 主应用已启动，请进行有内容时的关闭测试")
            
        except Exception as e:
            print(f"❌ 启动主应用失败: {e}")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    print("🔧 编辑器有内容时关闭修复验证")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试目标: 验证有内容时关闭按钮是否正常工作")
    print("")
    
    window = ContentCloseTestWindow()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())