#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按钮控制器修复效果验证脚本

检查关键修复是否已正确应用
"""

import re
import os

def check_main_py_fixes():
    """检查main.py中的修复"""
    main_py_path = "/Users/wanglichao/workspace/superops/larina/markrender/main.py"
    
    if not os.path.exists(main_py_path):
        print("❌ main.py文件不存在")
        return False
    
    with open(main_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixes_verified = []
    
    # 检查按钮控制器高度修复
    if "self.button_controller.setFixedHeight(36)" in content:
        fixes_verified.append("✅ 按钮控制器高度已修复为36px")
    else:
        fixes_verified.append("❌ 按钮控制器高度未修复")
    
    # 检查标题栏高度修复
    if "title_bar.setFixedHeight(44)" in content:
        fixes_verified.append("✅ 标题栏高度已调整为44px")
    else:
        fixes_verified.append("❌ 标题栏高度未调整")
    
    # 检查内边距修复
    if "title_bar_layout.setContentsMargins(10, 4, 10, 4)" in content:
        fixes_verified.append("✅ 标题栏内边距已优化")
    else:
        fixes_verified.append("❌ 标题栏内边距未优化")
    
    # 检查是否没有20px的冲突设置
    if "setFixedHeight(20)" not in content:
        fixes_verified.append("✅ 已移除20px的冲突设置")
    else:
        fixes_verified.append("❌ 仍存在20px的冲突设置")
    
    return fixes_verified

def check_button_controller_design():
    """检查按钮控制器的设计配置"""
    controller_path = "/Users/wanglichao/workspace/superops/larina/markrender/app/topbar/button_controller.py"
    
    if not os.path.exists(controller_path):
        print("❌ button_controller.py文件不存在")
        return False
    
    with open(controller_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    design_checks = []
    
    # 检查内部高度设计
    if "self.setFixedHeight(36)" in content:
        design_checks.append("✅ ButtonController内部高度设计为36px")
    else:
        design_checks.append("❌ ButtonController内部高度设计有问题")
    
    # 检查按钮尺寸
    if "button.setFixedSize(28, 28)" in content:
        design_checks.append("✅ 工具按钮尺寸设计为28×28px")
    else:
        design_checks.append("❌ 工具按钮尺寸设计有问题")
    
    # 检查布局间距
    if "layout.setSpacing(4)" in content:
        design_checks.append("✅ 按钮间距设计为4px")
    else:
        design_checks.append("❌ 按钮间距设计有问题")
    
    return design_checks

def main():
    """主验证函数"""
    print("🔍 右上角按钮控制器修复效果验证")
    print("=" * 50)
    
    # 检查main.py修复
    print("\n📋 检查main.py中的修复:")
    main_fixes = check_main_py_fixes()
    for fix in main_fixes:
        print(f"  {fix}")
    
    # 检查按钮控制器设计
    print("\n🎨 检查ButtonController设计配置:")
    design_checks = check_button_controller_design()
    for check in design_checks:
        print(f"  {check}")
    
    # 总结
    print("\n📊 修复效果总结:")
    all_checks = main_fixes + design_checks
    success_count = len([check for check in all_checks if check.startswith("✅")])
    total_count = len(all_checks)
    
    print(f"  成功: {success_count}/{total_count}")
    if success_count == total_count:
        print("  🎉 所有修复已正确应用！")
        print("\n💡 建议:")
        print("  - 启动应用程序: python main.py")
        print("  - 检查右上角是否显示3个工具按钮")
        print("  - 测试按钮的悬停和点击效果")
    else:
        print("  ⚠️  部分修复可能未完全应用")
    
    print("\n🔧 技术细节:")
    print("  - 按钮控制器内部设计: 36px高度")
    print("  - 标题栏容器配置: 44px高度")
    print("  - 内边距配置: 4px上下边距")
    print("  - 工具按钮尺寸: 28×28px")
    print("  - 按钮间距: 4px")

if __name__ == "__main__":
    main()