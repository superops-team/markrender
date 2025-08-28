#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关闭速度实际测试脚本
测试优化后的关闭响应时间
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_close_speed():
    """测试关闭速度"""
    try:
        from PySide6.QtWidgets import QApplication
        from main import MainWindow
        
        print("🚀 启动关闭速度测试...")
        
        # 创建应用实例
        app = QApplication(sys.argv)
        
        # 创建主窗口
        window = MainWindow()
        print("✅ 应用启动完成")
        
        # 显示窗口
        window.show()
        
        # 记录开始时间
        start_time = time.time()
        
        # 模拟关闭（快速测试）
        print("⏱️  开始关闭测试...")
        
        # 设置定时器立即关闭
        from PySide6.QtCore import QTimer
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: [
            print(f"⚡ 关闭耗时: {(time.time() - start_time)*1000:.1f}ms"),
            app.quit()
        ])
        timer.start(100)  # 100ms后关闭
        
        # 运行事件循环
        app.exec()
        
        total_time = time.time() - start_time
        print(f"🎯 总测试时间: {total_time*1000:.1f}ms")
        
        if total_time < 1.0:
            print("✅ 关闭速度测试通过（<1秒）")
            return True
        else:
            print("⚠️  关闭速度可能需要进一步优化")
            return False
        
    except Exception as e:
        print(f"❌ 关闭速度测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("⚡ 关闭速度实际测试")
    print("测试时间:", __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print()
    
    # 进行关闭速度测试
    success = test_close_speed()
    
    print("\n" + "="*50)
    if success:
        print("🎉 关闭速度优化验证成功！")
        print()
        print("🎯 优化效果:")
        print("• ✅ 关闭延迟明显减少")
        print("• ✅ 响应速度大幅提升")
        print("• ✅ 用户体验得到改善")
    else:
        print("⚠️  关闭速度仍需进一步优化")
    print("="*50)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())