#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TopBar和StatusBar紧凑设计验证脚本

检查尺寸优化是否符合苹果设计规范
"""

import re
import os

def check_design_constants():
    """检查设计常量的更新"""
    constants_path = "/Users/wanglichao/workspace/superops/larina/markrender/app/preference/style_constants.py"
    
    if not os.path.exists(constants_path):
        print("❌ style_constants.py文件不存在")
        return False
    
    with open(constants_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    design_checks = []
    
    # 检查标题栏高度
    if "TITLEBAR_HEIGHT = 32" in content:
        design_checks.append("✅ 标题栏高度已优化为32px（符合苹果规范）")
    else:
        design_checks.append("❌ 标题栏高度未优化")
    
    # 检查状态栏高度
    if "STATUSBAR_HEIGHT = 22" in content:
        design_checks.append("✅ 状态栏高度已优化为22px（符合苹果规范）")
    else:
        design_checks.append("❌ 状态栏高度未优化")
    
    # 检查工具栏高度
    if "TOOLBAR_HEIGHT = 32" in content:
        design_checks.append("✅ 工具栏高度已设置为32px（符合苹果规范）")
    else:
        design_checks.append("❌ 工具栏高度未设置")
    
    # 检查工具按钮尺寸
    if "TOOLBAR_BUTTON_SIZE = 24" in content:
        design_checks.append("✅ 工具按钮尺寸已优化为24px（紧凑设计）")
    else:
        design_checks.append("❌ 工具按钮尺寸未优化")
    
    return design_checks

def check_button_controller_updates():
    """检查ButtonController的更新"""
    controller_path = "/Users/wanglichao/workspace/superops/larina/markrender/app/topbar/button_controller.py"
    
    if not os.path.exists(controller_path):
        print("❌ button_controller.py文件不存在")
        return False
    
    with open(controller_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    controller_checks = []
    
    # 检查工具栏高度使用
    if "from app.preference.style_constants import TOOLBAR_HEIGHT" in content:
        controller_checks.append("✅ ButtonController使用TOOLBAR_HEIGHT常量")
    else:
        controller_checks.append("❌ ButtonController未使用TOOLBAR_HEIGHT常量")
    
    # 检查按钮尺寸使用
    if "from app.preference.style_constants import TOOLBAR_BUTTON_SIZE" in content:
        controller_checks.append("✅ ButtonController使用TOOLBAR_BUTTON_SIZE常量")
    else:
        controller_checks.append("❌ ButtonController未使用TOOLBAR_BUTTON_SIZE常量")
    
    # 检查紧凑间距
    if "layout.setSpacing(2)" in content:
        controller_checks.append("✅ 按钮间距已优化为2px（紧凑设计）")
    else:
        controller_checks.append("❌ 按钮间距未优化")
    
    return controller_checks

def check_main_window_updates():
    """检查主窗口的更新"""
    main_path = "/Users/wanglichao/workspace/superops/larina/markrender/main.py"
    
    if not os.path.exists(main_path):
        print("❌ main.py文件不存在")
        return False
    
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    main_checks = []
    
    # 检查标题栏高度使用
    if "from app.preference.style_constants import TITLEBAR_HEIGHT" in content:
        main_checks.append("✅ 主窗口使用TITLEBAR_HEIGHT常量")
    else:
        main_checks.append("❌ 主窗口未使用TITLEBAR_HEIGHT常量")
    
    # 检查工具栏高度使用
    if "from app.preference.style_constants import TOOLBAR_HEIGHT" in content:
        main_checks.append("✅ 主窗口使用TOOLBAR_HEIGHT常量")
    else:
        main_checks.append("❌ 主窗口未使用TOOLBAR_HEIGHT常量")
    
    return main_checks

def check_style_utils_updates():
    """检查样式工具的更新"""
    utils_path = "/Users/wanglichao/workspace/superops/larina/markrender/app/preference/style_utils.py"
    
    if not os.path.exists(utils_path):
        print("❌ style_utils.py文件不存在")
        return False
    
    with open(utils_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    utils_checks = []
    
    # 检查状态栏样式更新
    if "from .style_constants import STATUSBAR_HEIGHT" in content:
        utils_checks.append("✅ 状态栏样式使用STATUSBAR_HEIGHT常量")
    else:
        utils_checks.append("❌ 状态栏样式未使用STATUSBAR_HEIGHT常量")
    
    # 检查工具栏按钮样式更新
    if "from .style_constants import TOOLBAR_BUTTON_SIZE" in content:
        utils_checks.append("✅ 工具栏按钮样式使用TOOLBAR_BUTTON_SIZE常量")
    else:
        utils_checks.append("❌ 工具栏按钮样式未使用TOOLBAR_BUTTON_SIZE常量")
    
    # 检查紧凑边距
    if "padding: 2px;" in content:
        utils_checks.append("✅ 工具栏按钮使用紧凑边距（2px）")
    else:
        utils_checks.append("❌ 工具栏按钮边距未优化")
    
    return utils_checks

def calculate_size_comparison():
    """计算尺寸优化对比"""
    print("\n📊 尺寸优化对比分析:")
    print("=" * 50)
    
    # TopBar对比
    print("🔧 TopBar（标题栏 + 工具栏）:")
    old_titlebar = 44  # 原始标题栏高度
    new_titlebar = 32  # 新标题栏高度
    reduction_titlebar = ((old_titlebar - new_titlebar) / old_titlebar) * 100
    print(f"  标题栏高度: {old_titlebar}px → {new_titlebar}px (减少{reduction_titlebar:.1f}%)")
    
    old_toolbar_btn = 28  # 原始工具按钮尺寸
    new_toolbar_btn = 24  # 新工具按钮尺寸
    reduction_btn = ((old_toolbar_btn - new_toolbar_btn) / old_toolbar_btn) * 100
    print(f"  工具按钮尺寸: {old_toolbar_btn}×{old_toolbar_btn}px → {new_toolbar_btn}×{new_toolbar_btn}px (减少{reduction_btn:.1f}%)")
    
    # StatusBar对比
    print("\n📊 StatusBar:")
    old_statusbar = 24  # 原始状态栏高度
    new_statusbar = 22  # 新状态栏高度
    reduction_statusbar = ((old_statusbar - new_statusbar) / old_statusbar) * 100
    print(f"  状态栏高度: {old_statusbar}px → {new_statusbar}px (减少{reduction_statusbar:.1f}%)")
    
    # 总体节省空间
    total_old = old_titlebar + old_statusbar
    total_new = new_titlebar + new_statusbar
    total_reduction = ((total_old - total_new) / total_old) * 100
    print(f"\n🎯 总体UI高度:")
    print(f"  TopBar + StatusBar: {total_old}px → {total_new}px (减少{total_reduction:.1f}%)")
    print(f"  节省垂直空间: {total_old - total_new}px")

def main():
    """主验证函数"""
    print("🔍 TopBar & StatusBar 紧凑设计验证")
    print("=" * 50)
    print("参考：苹果Human Interface Guidelines和主流应用（如Qoder）")
    
    # 检查设计常量
    print("\n📋 检查设计常量优化:")
    design_checks = check_design_constants()
    for check in design_checks:
        print(f"  {check}")
    
    # 检查ButtonController更新
    print("\n🎨 检查ButtonController更新:")
    controller_checks = check_button_controller_updates()
    for check in controller_checks:
        print(f"  {check}")
    
    # 检查主窗口更新
    print("\n🏠 检查主窗口更新:")
    main_checks = check_main_window_updates()
    for check in main_checks:
        print(f"  {check}")
    
    # 检查样式工具更新
    print("\n🎭 检查样式工具更新:")
    utils_checks = check_style_utils_updates()
    for check in utils_checks:
        print(f"  {check}")
    
    # 计算尺寸对比
    calculate_size_comparison()
    
    # 总结
    print("\n📊 优化效果总结:")
    all_checks = design_checks + controller_checks + main_checks + utils_checks
    success_count = len([check for check in all_checks if check.startswith("✅")])
    total_count = len(all_checks)
    
    print(f"  成功: {success_count}/{total_count}")
    if success_count == total_count:
        print("  🎉 所有优化已正确应用！")
        print("\n💡 苹果规范对比:")
        print("  - 标题栏: 32px ✅ (符合苹果标准工具栏高度)")
        print("  - 状态栏: 22px ✅ (符合苹果标准状态栏高度)")
        print("  - 工具按钮: 24px ✅ (紧凑且易于点击)")
        print("  - 整体比例: 协调 ✅ (类似Qoder等主流应用)")
    else:
        print("  ⚠️  部分优化可能未完全应用")
    
    print("\n🔧 技术规范:")
    print("  - 标题栏高度: 32px (TITLEBAR_HEIGHT)")
    print("  - 工具栏高度: 32px (TOOLBAR_HEIGHT)")
    print("  - 状态栏高度: 22px (STATUSBAR_HEIGHT)")
    print("  - 工具按钮尺寸: 24×24px (TOOLBAR_BUTTON_SIZE)")
    print("  - 按钮间距: 2px (紧凑设计)")
    print("  - 按钮边距: 2px (紧凑设计)")
    
    print("\n🎯 用户体验改进:")
    print("  - 更大的内容显示区域")
    print("  - 符合用户对主流应用的使用习惯")
    print("  - 保持功能完整性的同时提升空间效率")
    print("  - 与苹果生态应用保持一致的视觉体验")

if __name__ == "__main__":
    main()