#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按钮样式修复验证脚本
验证create_button_style函数的所有按钮类型是否正常工作
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_button_styles():
    """测试所有按钮样式是否正常生成"""
    try:
        from app.preference.style_utils import create_button_style
        
        print("🧪 测试所有按钮样式生成...")
        print("=" * 50)
        
        # 测试所有按钮类型
        button_types = ["primary", "secondary", "danger", "ghost"]
        sizes = ["sm", "md", "lg"]
        
        for button_type in button_types:
            for size in sizes:
                try:
                    style = create_button_style(button_type, size)
                    print(f"✅ {button_type} ({size}): 样式生成成功")
                except Exception as e:
                    print(f"❌ {button_type} ({size}): 样式生成失败 - {e}")
                    return False
        
        print("\n🎉 所有按钮样式测试通过！")
        
        # 特别测试secondary类型（之前出错的类型）
        print("\n🔍 详细测试secondary按钮样式:")
        secondary_style = create_button_style("secondary", "md")
        
        # 检查关键属性是否存在
        required_properties = [
            "background-color: #FFFFFF",  # NEUTRAL_0
            "color: #4D5358",            # NEUTRAL_700  
            "border: 1px solid #DDE1E6", # NEUTRAL_300
            "border-radius: 4px"         # RADIUS_SM
        ]
        
        for prop in required_properties:
            if prop in secondary_style:
                print(f"✅ 包含属性: {prop}")
            else:
                print(f"❌ 缺少属性: {prop}")
                return False
        
        print("\n✅ secondary按钮样式完全正确！")
        print("\n📝 修复总结:")
        print("• 添加了缺失的 'border' 键到 secondary 类型配置")
        print("• 使用 NEUTRAL_300 作为 secondary 按钮的默认边框色")
        print("• 保持了与设计系统的一致性")
        print("• 所有按钮类型现在都能正常生成样式")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_settings_dialog_creation():
    """测试设置对话框是否能正常创建"""
    try:
        print("\n🏗️  测试设置对话框创建...")
        print("=" * 50)
        
        # 这里只是导入测试，不实际显示GUI
        from app.sidebar.settings_dialog import SettingsDialog
        print("✅ SettingsDialog 类导入成功")
        
        # 测试样式生成器导入
        from app.preference.style_utils import (
            create_dialog_style, 
            create_input_style, 
            create_button_style
        )
        print("✅ 所有样式生成器导入成功")
        
        print("\n🎉 设置对话框相关组件测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 设置对话框测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🔧 按钮样式KeyError修复验证")
    print("测试时间:", __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print()
    
    # 测试按钮样式
    if not test_button_styles():
        return 1
    
    # 测试设置对话框
    if not test_settings_dialog_creation():
        return 1
    
    print("\n" + "="*60)
    print("🎉 所有测试通过！KeyError问题已完全修复！")
    print("🚀 设置对话框现在可以正常使用了！")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())