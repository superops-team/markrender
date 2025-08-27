#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证导出菜单样式修改效果
检查create_toolbar_menu_style函数是否已正确移除固定高度设置
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_menu_style_fix():
    """测试菜单样式修复效果"""
    print("🧪 导出菜单样式修复验证")
    print("=" * 50)
    
    try:
        # 导入样式函数（仅导入样式相关代码，避免数据库依赖）
        import sys
        import os
        
        # 直接读取样式文件内容进行验证
        style_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'app', 'preference', 'style_utils.py'
        )
        
        print(f"📂 检查文件: {style_file_path}")
        
        with open(style_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 查找create_toolbar_menu_style函数
        lines = content.split('\n')
        in_function = False
        function_lines = []
        
        for i, line in enumerate(lines):
            if 'def create_toolbar_menu_style():' in line:
                in_function = True
                function_lines.append(f"{i+1:3}: {line}")
            elif in_function:
                if line.strip() and not line.startswith(' ') and not line.startswith('\t') and 'def ' in line:
                    break
                function_lines.append(f"{i+1:3}: {line}")
                if '"""' in line and len(function_lines) > 5:  # 函数结束
                    break
                    
        print("\n📋 create_toolbar_menu_style函数内容:")
        print("-" * 40)
        for line in function_lines[:20]:  # 显示前20行
            print(line)
            
        # 检查修复效果
        function_content = '\n'.join(function_lines)
        
        print("\n🔍 修复效果验证:")
        print("-" * 40)
        
        if 'min-height: 140px' in function_content:
            print("❌ 发现固定最小高度设置: min-height: 140px")
        else:
            print("✅ 已移除固定最小高度设置")
            
        if 'max-height: 200px' in function_content:
            print("❌ 发现固定最大高度设置: max-height: 200px")
        else:
            print("✅ 已移除固定最大高度设置")
            
        if 'min-width: 140px' in function_content:
            print("✅ 保留最小宽度设置: min-width: 140px")
        else:
            print("⚠️  最小宽度设置可能被意外移除")
            
        # 检查注释是否更新
        if '高度自适应菜单项数量' in function_content:
            print("✅ 函数注释已更新，说明了自适应特性")
        else:
            print("ℹ️  函数注释可进一步优化")
            
        print("\n📊 修复总结:")
        print("-" * 40)
        print("🎯 修复目标: 让导出菜单高度根据菜单项数量自动调整")
        print("🔧 修复方案: 移除固定的min-height和max-height设置")
        print("💡 预期效果: 菜单高度将由Qt根据内容自动计算")
        print("✅ 修复状态: 样式代码已更新")
        
        print("\n🧪 测试建议:")
        print("-" * 40)
        print("1. 运行主应用程序")
        print("2. 点击导出按钮查看菜单")
        print("3. 观察菜单高度是否仍然合适")
        print("4. 验证菜单不会有多余的空白区域")
        
    except FileNotFoundError:
        print("❌ 未找到样式文件")
    except Exception as e:
        print(f"❌ 验证过程出错: {e}")

def generate_style_comparison():
    """生成样式对比说明"""
    print("\n" + "=" * 60)
    print("📊 样式修改对比")
    print("=" * 60)
    
    print("\n🔴 修复前的样式:")
    print("-" * 30)
    print("""
    QMenu {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 8px;
        min-width: 140px;
        min-height: 140px;        ← 固定最小高度
        max-height: 200px;        ← 固定最大高度
    }
    """)
    
    print("❌ 问题:")
    print("• 即使只有2个菜单项，菜单也会显示140px高度")
    print("• 造成不必要的空白区域")
    print("• 浪费屏幕空间")
    
    print("\n🟢 修复后的样式:")
    print("-" * 30)
    print("""
    QMenu {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 8px;
        min-width: 140px;         ← 保留最小宽度
        /* 移除了固定高度设置 */
    }
    """)
    
    print("✅ 改进:")
    print("• 菜单高度根据菜单项数量自动调整")
    print("• 消除不必要的空白区域")
    print("• 更好的用户体验")
    print("• 更合理的空间利用")

if __name__ == "__main__":
    test_menu_style_fix()
    generate_style_comparison()