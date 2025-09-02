#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关闭按钮优化验证脚本
验证关闭按钮反应速度和可靠性的优化效果
"""

import sys
import os
import time
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont

try:
    from main import MainWindow
    HAS_MODULES = True
except ImportError as e:
    print(f"⚠️  模块导入失败: {e}")
    HAS_MODULES = False

class CloseButtonTestWindow(QMainWindow):
    """关闭按钮优化测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.test_start_time = None
        self.test_results = []
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✅ 关闭按钮优化验证")
        self.setGeometry(100, 100, 900, 750)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("✅ 关闭按钮优化验证")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 问题描述
        problem_desc = QLabel("""
        🐛 原始问题：
        "点击关闭按钮后为什么有时没有反应需要再次点击一下"
        
        📋 问题分析：
        1. 异步保存阻塞关闭流程 - MarkdownEditor.closeEvent中的保存操作是异步的
        2. Web通信超时问题 - 如果Web引擎响应慢，回调函数可能不会被及时调用
        3. 资源清理不彻底 - _cleanup_resources方法没有强制关闭主窗口
        4. 缺少超时机制 - 保存过程没有超时保护，可能导致关闭流程永久挂起
        
        🔧 优化方案：
        • 添加关闭流程状态管理，防止重复关闭操作
        • 设置3秒保存超时机制，确保关闭流程不会无限等待
        • 添加强制关闭逻辑，超时后自动强制退出
        • 优化主窗口关闭流程，添加5秒主窗口关闭超时
        • 改进错误处理，确保异常情况下也能正常关闭
        """)
        problem_desc.setFont(QFont("Menlo", 11))
        problem_desc.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 15px;
                color: #856404;
            }
        """)
        layout.addWidget(problem_desc)
        
        # 优化详情
        optimization_desc = QLabel("""
        ⚡ 关键优化点：
        
        1. 📊 关闭流程状态管理：
           • _closing_in_progress标志防止重复关闭操作
           • _main_window_closing标志防止主窗口重复关闭
        
        2. ⏰ 超时保护机制：
           • 编辑器保存超时：3秒
           • 主窗口关闭超时：5秒
           • 超时后自动触发强制关闭
        
        3. 🔄 强制关闭逻辑：
           • _force_close()方法确保资源清理
           • _force_quit()方法作为最终保障
           • QTimer.singleShot确保在事件循环中执行
        
        4. 🛡️ 异常处理增强：
           • try-catch包围关键操作
           • 异常情况下也能正常关闭
           • 详细的日志记录便于调试
        
        5. 📞 回调机制优化：
           • 主窗口关闭完成回调
           • 编辑器与主窗口的协调关闭
           • 避免资源泄漏和僵尸进程
        """)
        optimization_desc.setFont(QFont("Menlo", 10))
        optimization_desc.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                border: 1px solid #bbdefb;
                border-radius: 4px;
                padding: 15px;
                color: #0d47a1;
            }
        """)
        layout.addWidget(optimization_desc)
        
        if HAS_MODULES:
            # 测试按钮
            test_btn = QPushButton("🧪 启动MarkRender进行关闭测试")
            test_btn.clicked.connect(self.start_close_test)
            test_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            layout.addWidget(test_btn)
        
        # 测试日志区域
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        self.log_text.setFont(QFont("Menlo", 10))
        self.log_text.setPlaceholderText("测试日志将在这里显示...")
        layout.addWidget(self.log_text)
        
        # 验证清单
        verification_desc = QLabel("""
        📋 验证清单 - 请测试以下场景：
        
        🔍 基本关闭测试：
        ☐ 启动MarkRender后立即点击关闭按钮
        ☐ 关闭按钮应该一次点击就能关闭应用
        ☐ 关闭过程应该在3-5秒内完成
        ☐ 不应该出现卡死或无响应现象
        
        📝 有内容时关闭测试：
        ☐ 在编辑器中输入一些内容
        ☐ 点击关闭按钮应该先保存内容再关闭
        ☐ 即使保存过程较慢，也应该在3秒内强制关闭
        ☐ 不应该需要多次点击关闭按钮
        
        🚫 异常情况测试：
        ☐ 网络断开或Web引擎异常时点击关闭
        ☐ 应该在5秒内强制退出应用
        ☐ 不应该出现僵尸进程或资源泄漏
        
        ⚡ 性能测试：
        ☐ 连续多次快速点击关闭按钮
        ☐ 应该只触发一次关闭流程
        ☐ 不应该出现重复关闭或错误
        
        ✅ 成功标准：
        ☐ 关闭按钮一次点击即可关闭应用
        ☐ 关闭过程响应迅速（<3秒）
        ☐ 各种异常情况下都能可靠关闭
        ☐ 没有资源泄漏或僵尸进程
        ☐ 用户体验流畅，无需多次点击
        
        💡 如果仍有问题：
        ☐ 检查日志中的错误信息
        ☐ 确认超时时间是否合适
        ☐ 验证Web通信是否正常
        ☐ 考虑进一步缩短超时时间
        """)
        verification_desc.setFont(QFont("Menlo", 10))
        verification_desc.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 15px;
                color: #333;
            }
        """)
        layout.addWidget(verification_desc)
        
    def log(self, message):
        """添加日志信息"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] {message}"
        self.log_text.append(log_entry)
        print(log_entry)  # 同时输出到控制台
        
    def start_close_test(self):
        """启动关闭测试"""
        if not HAS_MODULES:
            self.log("❌ 无法启动测试，模块导入失败")
            return
            
        try:
            self.log("🚀 启动MarkRender进行关闭测试...")
            self.test_start_time = time.time()
            
            # 创建MarkRender主窗口
            self.test_window = MainWindow()
            self.test_window.show()
            
            self.log("✅ MarkRender已启动")
            self.log("💡 现在请点击MarkRender窗口左上角的红色关闭按钮")
            self.log("🔍 观察关闭响应速度和可靠性")
            
            # 设置定时器监控关闭过程
            self.monitor_timer = QTimer()
            self.monitor_timer.timeout.connect(self.monitor_close_process)
            self.monitor_timer.start(500)  # 每500ms检查一次
            
        except Exception as e:
            self.log(f"❌ 启动测试失败: {e}")
            import traceback
            self.log(f"详细错误: {traceback.format_exc()}")
            
    def monitor_close_process(self):
        """监控关闭过程"""
        if not hasattr(self, 'test_window'):
            return
            
        # 检查测试窗口是否还存在
        if not self.test_window or not self.test_window.isVisible():
            elapsed = time.time() - self.test_start_time if self.test_start_time else 0
            self.log(f"🎉 MarkRender已关闭，耗时: {elapsed:.2f}秒")
            
            if elapsed < 1.0:
                self.log("⚡ 优秀！关闭速度非常快")
            elif elapsed < 3.0:
                self.log("✅ 良好！关闭速度正常")
            elif elapsed < 5.0:
                self.log("⚠️ 一般！关闭速度较慢但可接受")
            else:
                self.log("❌ 关闭速度过慢，可能仍有问题")
                
            self.monitor_timer.stop()
            delattr(self, 'test_window')
            self.test_start_time = None
            
            self.log("🔍 请尝试以下测试：")
            self.log("   1. 再次点击测试按钮，验证重复关闭")
            self.log("   2. 打开MarkRender，输入内容后关闭")
            self.log("   3. 快速多次点击关闭按钮")
            
        else:
            elapsed = time.time() - self.test_start_time if self.test_start_time else 0
            if elapsed > 10:  # 10秒还没关闭
                self.log("❌ 关闭过程超时，可能存在问题")
                self.monitor_timer.stop()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = CloseButtonTestWindow()
    window.show()
    
    print("✅ 关闭按钮优化验证已启动")
    print("🔧 主要优化：添加超时机制、状态管理、强制关闭逻辑")
    print("🧪 请点击测试按钮进行关闭按钮响应速度验证")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()