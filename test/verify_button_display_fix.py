#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按钮显示修复验证脚本
验证移除重复高度设置后的按钮显示效果
"""

import sys
import os

def check_main_py_fix():
    """检查main.py修复"""
    main_py_path = "/Users/wanglichao/workspace/superops/larina/markrender/main.py"
    
    if not os.path.exists(main_py_path):
        print("❌ main.py文件不存在")
        return False
    
    with open(main_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否还有重复的高度设置
    button_controller_lines = []
    lines = content.split('\n')
    in_button_controller_section = False
    
    for i, line in enumerate(lines):
        if 'self.button_controller = ButtonController(' in line:
            in_button_controller_section = True
            button_controller_lines.append((i+1, line.strip()))
        elif in_button_controller_section:
            if 'title_bar_layout.addWidget(self.button_controller)' in line:
                button_controller_lines.append((i+1, line.strip()))
                break
            elif line.strip():
                button_controller_lines.append((i+1, line.strip()))
    
    print("🔍 ButtonController相关代码检查:")
    print("-" * 40)
    for line_num, line_content in button_controller_lines:
        print(f"  {line_num:3}: {line_content}")
    
    # 检查是否移除了重复设置
    has_duplicate_height = any('setFixedHeight(TOOLBAR_HEIGHT)' in line for _, line in button_controller_lines)
    
    if has_duplicate_height:
        print("\n❌ 仍存在重复的高度设置")
        return False
    else:
        print("\n✅ 已移除重复的高度设置")
        return True

def check_style_constants():
    """检查样式常量值"""
    try:
        # 添加项目路径
        sys.path.insert(0, "/Users/wanglichao/workspace/superops/larina/markrender")
        
        from app.preference.style_constants import TOOLBAR_HEIGHT, TOOLBAR_BUTTON_SIZE, TITLEBAR_HEIGHT
        
        print("📏 样式常量值检查:")
        print("-" * 40)
        print(f"  TITLEBAR_HEIGHT: {TITLEBAR_HEIGHT}px")
        print(f"  TOOLBAR_HEIGHT: {TOOLBAR_HEIGHT}px")
        print(f"  TOOLBAR_BUTTON_SIZE: {TOOLBAR_BUTTON_SIZE}px")
        
        # 计算合理性
        button_with_margin = TOOLBAR_BUTTON_SIZE + 4  # 假设上下各2px边距
        
        print(f"\n🧮 尺寸合理性分析:")
        print(f"  按钮尺寸: {TOOLBAR_BUTTON_SIZE}px")
        print(f"  预期最小容器高度: {button_with_margin}px (按钮 + 4px边距)")
        print(f"  实际容器高度: {TOOLBAR_HEIGHT}px")
        
        if TOOLBAR_HEIGHT >= button_with_margin:
            print(f"  ✅ 容器高度充足 ({TOOLBAR_HEIGHT}px >= {button_with_margin}px)")
        else:
            print(f"  ❌ 容器高度不足 ({TOOLBAR_HEIGHT}px < {button_with_margin}px)")
            print(f"  💡 建议调整TOOLBAR_HEIGHT到至少 {button_with_margin}px")
        
        # 检查标题栏高度
        if TITLEBAR_HEIGHT >= TOOLBAR_HEIGHT:
            print(f"  ✅ 标题栏高度充足 ({TITLEBAR_HEIGHT}px >= {TOOLBAR_HEIGHT}px)")
        else:
            print(f"  ❌ 标题栏高度不足 ({TITLEBAR_HEIGHT}px < {TOOLBAR_HEIGHT}px)")
            print(f"  💡 建议调整TITLEBAR_HEIGHT到至少 {TOOLBAR_HEIGHT}px")
            
        return True
        
    except ImportError as e:
        print(f"❌ 无法导入样式常量: {e}")
        return False
    except Exception as e:
        print(f"❌ 检查样式常量时出错: {e}")
        return False

def suggest_fixes():
    """提供修复建议"""
    print("\n💡 修复建议和验证步骤:")
    print("=" * 50)
    
    print("\n1. 立即验证:")
    print("  运行主程序: python main.py --debug")
    print("  观察右上角按钮是否完整显示")
    
    print("\n2. 如果按钮仍然显示不完整，检查:")
    print("  • CSS样式是否有padding/margin冲突")
    print("  • 是否有其他样式覆盖了setFixedSize设置")
    print("  • 父容器的布局约束是否合理")
    
    print("\n3. 调试方法:")
    print("  • 使用test/diagnose_button_display_issue.py进行详细诊断")
    print("  • 检查浏览器开发者工具（如果使用Web组件）")
    print("  • 临时增加边框样式来可视化容器边界")
    
    print("\n4. 可能的进一步修复:")
    print("  • 如果TOOLBAR_HEIGHT太小，考虑增加到28px或更大")
    print("  • 检查ButtonController的布局边距设置")
    print("  • 确认setFixedSize设置在样式表之后执行")

def main():
    """主函数"""
    print("🔧 按钮显示修复验证")
    print("=" * 50)
    
    # 检查main.py修复
    main_fix_ok = check_main_py_fix()
    
    # 检查样式常量
    constants_ok = check_style_constants()
    
    # 总结
    print("\n📊 修复状态总结:")
    print("-" * 30)
    if main_fix_ok:
        print("  ✅ main.py重复设置已修复")
    else:
        print("  ❌ main.py仍有问题")
        
    if constants_ok:
        print("  ✅ 样式常量检查完成")
    else:
        print("  ❌ 样式常量检查失败")
    
    if main_fix_ok and constants_ok:
        print("\n🎉 修复完成！建议立即测试主程序")
    else:
        print("\n⚠️  可能需要进一步修复")
    
    # 提供建议
    suggest_fixes()

if __name__ == "__main__":
    main()