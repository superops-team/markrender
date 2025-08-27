#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TopBar按钮间距调试脚本

打印TopBar按钮的上下间距和布局信息，诊断按钮半隐藏遮挡问题
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer

from main import MainWindow
from app.preference.style_constants import *


class TopBarDebugger:
    """TopBar调试器"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        
    def print_design_constants(self):
        """打印设计常量"""
        print("🔧 设计常量信息:")
        print(f"  TITLEBAR_HEIGHT = {TITLEBAR_HEIGHT}px")
        print(f"  TOOLBAR_HEIGHT = {TOOLBAR_HEIGHT}px") 
        print(f"  TOOLBAR_BUTTON_SIZE = {TOOLBAR_BUTTON_SIZE}px")
        print(f"  SPACING_XS = {SPACING_XS}px")
        print(f"  SPACING_SM = {SPACING_SM}px")
        
    def print_title_bar_info(self):
        """打印标题栏信息"""
        title_bar = None
        button_controller = self.main_window.button_controller
        
        # 查找title_bar
        for child in self.main_window.findChildren(object):
            if hasattr(child, 'layout') and child.layout() and button_controller in [child.layout().itemAt(i).widget() for i in range(child.layout().count()) if child.layout().itemAt(i).widget()]:
                title_bar = child
                break
        
        if title_bar:
            print("\n📏 标题栏 (title_bar) 信息:")
            print(f"  总高度: {title_bar.height()}px")
            print(f"  固定高度: {title_bar.maximumHeight()}px")
            layout = title_bar.layout()
            if layout:
                margins = layout.contentsMargins()
                print(f"  布局边距: 左={margins.left()}px, 上={margins.top()}px, 右={margins.right()}px, 下={margins.bottom()}px")
                print(f"  布局间距: {layout.spacing()}px")
        
    def print_button_controller_info(self):
        """打印按钮控制器信息"""
        controller = self.main_window.button_controller
        
        print("\n🎛️ 按钮控制器 (ButtonController) 信息:")
        print(f"  容器高度: {controller.height()}px")
        print(f"  固定高度: {controller.maximumHeight()}px")
        print(f"  容器位置: x={controller.x()}, y={controller.y()}")
        print(f"  容器尺寸: w={controller.width()}, h={controller.height()}")
        
        layout = controller.layout()
        if layout:
            margins = layout.contentsMargins()
            print(f"  布局边距: 左={margins.left()}px, 上={margins.top()}px, 右={margins.right()}px, 下={margins.bottom()}px")
            print(f"  布局间距: {layout.spacing()}px")
            print(f"  对齐方式: {layout.alignment()}")
        
    def print_buttons_info(self):
        """打印按钮详细信息"""
        controller = self.main_window.button_controller
        
        print("\n🔘 工具按钮信息:")
        
        # 获取所有按钮
        buttons = [
            ("历史面板按钮", controller.history_btn),
            ("模式切换按钮", controller.mode_btn),
            ("导出按钮", controller.export_btn)
        ]
        
        for name, button in buttons:
            print(f"  {name}:")
            print(f"    按钮尺寸: {button.width()}×{button.height()}px")
            print(f"    固定尺寸: {button.maximumWidth()}×{button.maximumHeight()}px")
            print(f"    按钮位置: x={button.x()}, y={button.y()}")
            
            # 计算按钮在容器中的相对位置
            controller_height = controller.height()
            button_y = button.y()
            top_space = button_y
            bottom_space = controller_height - button_y - button.height()
            print(f"    上方空间: {top_space}px")
            print(f"    下方空间: {bottom_space}px")
            print(f"    垂直居中偏差: {abs(top_space - bottom_space)}px")
            
            # 检查按钮是否被遮挡
            if button_y < 0:
                print(f"    ⚠️  按钮上部被遮挡 {abs(button_y)}px")
            if button_y + button.height() > controller_height:
                print(f"    ⚠️  按钮下部被遮挡 {button_y + button.height() - controller_height}px")
            
            print()
    
    def calculate_optimal_spacing(self):
        """计算最优间距配置"""
        print("🧮 最优间距计算:")
        
        # 获取当前配置
        title_bar_height = TITLEBAR_HEIGHT
        toolbar_height = TOOLBAR_HEIGHT
        button_size = TOOLBAR_BUTTON_SIZE
        
        print(f"  当前配置:")
        print(f"    标题栏高度: {title_bar_height}px")
        print(f"    工具栏高度: {toolbar_height}px")
        print(f"    按钮尺寸: {button_size}×{button_size}px")
        
        # 计算理想间距
        if toolbar_height >= button_size:
            available_space = toolbar_height - button_size
            optimal_top_bottom = available_space / 2
            print(f"  理想配置:")
            print(f"    按钮上下各需间距: {optimal_top_bottom}px")
            
            # 检查title_bar是否有足够空间
            if title_bar_height >= toolbar_height:
                title_extra_space = title_bar_height - toolbar_height
                title_optimal_margin = title_extra_space / 2
                print(f"    标题栏上下边距: {title_optimal_margin}px")
            else:
                print(f"    ⚠️  标题栏高度不足！需要至少 {toolbar_height}px")
        else:
            print(f"    ❌ 工具栏高度不足！按钮 {button_size}px > 工具栏 {toolbar_height}px")
    
    def suggest_fixes(self):
        """建议修复方案"""
        print("\n💡 修复建议:")
        
        controller = self.main_window.button_controller
        layout = controller.layout()
        margins = layout.contentsMargins() if layout else None
        
        # 分析问题
        problems = []
        if controller.height() < TOOLBAR_BUTTON_SIZE:
            problems.append(f"工具栏高度 {controller.height()}px < 按钮尺寸 {TOOLBAR_BUTTON_SIZE}px")
        
        if margins:
            top_bottom_margin = margins.top() + margins.bottom()
            available_height = controller.height() - top_bottom_margin
            if available_height < TOOLBAR_BUTTON_SIZE:
                problems.append(f"扣除边距后可用高度 {available_height}px < 按钮尺寸 {TOOLBAR_BUTTON_SIZE}px")
        
        if problems:
            print("  发现问题:")
            for i, problem in enumerate(problems, 1):
                print(f"    {i}. {problem}")
            
            print("  建议方案:")
            
            # 方案1: 调整容器高度
            min_required_height = TOOLBAR_BUTTON_SIZE + (margins.top() + margins.bottom() if margins else 8)
            print(f"    方案1: 增加ButtonController高度到 {min_required_height}px")
            print(f"            (按钮{TOOLBAR_BUTTON_SIZE}px + 上下边距{margins.top() + margins.bottom() if margins else 8}px)")
            
            # 方案2: 减少边距
            if margins and margins.top() + margins.bottom() > 4:
                new_margin = 2
                print(f"    方案2: 减少布局边距到 {new_margin}px (当前: 上{margins.top()}px, 下{margins.bottom()}px)")
            
            # 方案3: 减小按钮尺寸
            max_button_size = controller.height() - (margins.top() + margins.bottom() if margins else 4)
            if max_button_size > 0:
                print(f"    方案3: 减小按钮尺寸到 {max_button_size}×{max_button_size}px")
        else:
            print("  ✅ 尺寸配置合理，检查其他可能原因:")
            print("    - 检查CSS样式是否有padding/margin冲突")
            print("    - 检查父容器是否有overflow hidden")
            print("    - 检查按钮是否有额外的样式偏移")


def main():
    """主函数"""
    print("🔍 TopBar按钮间距调试")
    print("=" * 60)
    
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 创建调试器
    debugger = TopBarDebugger(window)
    
    def run_debug():
        """运行调试分析"""
        try:
            print("📱 开始分析TopBar布局...")
            
            # 打印设计常量
            debugger.print_design_constants()
            
            # 打印标题栏信息
            debugger.print_title_bar_info()
            
            # 打印按钮控制器信息
            debugger.print_button_controller_info()
            
            # 打印按钮详细信息
            debugger.print_buttons_info()
            
            # 计算最优间距
            debugger.calculate_optimal_spacing()
            
            # 建议修复方案
            debugger.suggest_fixes()
            
            print("\n" + "=" * 60)
            print("🎯 调试分析完成")
            print("💡 请根据上述信息调整TopBar布局配置")
            
        except Exception as e:
            print(f"❌ 调试过程中出错: {e}")
            import traceback
            traceback.print_exc()
        
        # 关闭应用
        app.quit()
    
    # 延迟执行调试，确保窗口完全加载
    QTimer.singleShot(1000, run_debug)
    
    app.exec()


if __name__ == "__main__":
    main()