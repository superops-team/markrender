#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证数据驱动优化后的Sidebar间距效果
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from main import MainWindow
from utils.logger_utils import logger

def verify_optimized_spacing():
    """验证数据驱动优化后的间距效果"""
    app = QApplication.instance() or QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    def verify_optimization_results():
        """验证优化结果"""
        try:
            sidebar = window.sidebar
            layout = sidebar.layout()
            margins = layout.contentsMargins()
            
            logger.info("=" * 80)
            logger.info("数据驱动优化验证报告")
            logger.info("=" * 80)
            
            # 优化方案回顾
            logger.info("\n📋 应用的优化方案:")
            logger.info("   基于实测数据的发现:")
            logger.info("   - 按钮实际尺寸: 42x42px (非预期36x36px)")
            logger.info("   - 原始右间距: 2px (严重不足)")
            logger.info("   - 间距差值: 5px (不对称)")
            
            logger.info("\n🔧 实施的修正措施:")
            logger.info(f"   - 右边距调整: 7px → {margins.right()}px")
            logger.info(f"   - 总宽度调整: 53px → {sidebar.width()}px")
            logger.info(f"   - 保持左边距: {margins.left()}px (补偿边框扩展)")
            
            # 当前配置验证
            logger.info("\n📐 当前配置验证:")
            logger.info(f"   Sidebar总宽度: {sidebar.width()}px")
            logger.info(f"   布局边距: 左={margins.left()}px, 右={margins.right()}px")
            
            # 测量选中状态间距
            def measure_selected_state(button, name):
                """测量选中状态的实际间距"""
                button.setChecked(True)
                app.processEvents()
                
                btn_geometry = button.geometry()
                border_width = 1
                
                # 计算边框占用区域
                border_left_edge = btn_geometry.x() - border_width
                border_right_edge = btn_geometry.x() + btn_geometry.width() + border_width
                
                # 计算间距
                left_spacing = border_left_edge - 0
                right_spacing = sidebar.width() - border_right_edge
                
                logger.info(f"\n🎯 {name}按钮选中状态测量:")
                logger.info(f"   按钮实际尺寸: {btn_geometry.width()}x{btn_geometry.height()}px")
                logger.info(f"   边框左间距: {left_spacing}px")
                logger.info(f"   边框右间距: {right_spacing}px")
                logger.info(f"   间距差值: {abs(left_spacing - right_spacing)}px")
                
                return left_spacing, right_spacing, abs(left_spacing - right_spacing)
            
            # 测试所有按钮
            logger.info("\n📊 优化后间距测量:")
            
            # 先取消所有选中状态
            window.sidebar.file_browse_btn.setChecked(False)
            window.sidebar.import_btn.setChecked(False)
            window.sidebar.settings_btn.setChecked(False)
            
            # 测量Home按钮
            left1, right1, diff1 = measure_selected_state(window.sidebar.file_browse_btn, "Home")
            
            # 重置并测量Import按钮
            window.sidebar.file_browse_btn.setChecked(False)
            app.processEvents()
            left2, right2, diff2 = measure_selected_state(window.sidebar.import_btn, "Import")
            
            # 重置并测量Settings按钮
            window.sidebar.import_btn.setChecked(False) 
            app.processEvents()
            left3, right3, diff3 = measure_selected_state(window.sidebar.settings_btn, "Settings")
            
            # 优化效果评估
            logger.info("\n📈 优化效果评估:")
            
            avg_left = (left1 + left2 + left3) / 3
            avg_right = (right1 + right2 + right3) / 3
            avg_diff = (diff1 + diff2 + diff3) / 3
            
            logger.info(f"   平均左间距: {avg_left:.1f}px")
            logger.info(f"   平均右间距: {avg_right:.1f}px") 
            logger.info(f"   平均差值: {avg_diff:.1f}px")
            
            # 优化成功标准
            success_criteria = avg_diff <= 1.0  # 允许1px误差
            
            logger.info("\n🏆 优化结果评定:")
            if success_criteria:
                logger.info("   ✅ 优化成功!")
                logger.info("   - 间距差值在可接受范围内(≤1px)")
                logger.info("   - 数据驱动优化算法有效")
                logger.info("   - 边框对齐显著改善")
                result_status = "✅ 成功"
            else:
                logger.info("   ⚠️  需要进一步优化")
                logger.info(f"   - 当前差值 {avg_diff:.1f}px 超过目标1px")
                logger.info("   - 建议进一步调整边距配置")
                result_status = "⚠️ 需要调整"
            
            # 与理论值对比
            logger.info("\n🧮 理论值对比:")
            logger.info("   理论计算 (基于42px按钮):")
            theoretical_left = margins.left() - 1  # 8-1=7px
            theoretical_right = margins.right()    # 11px
            logger.info(f"   - 理论左间距: {theoretical_left}px")
            logger.info(f"   - 理论右间距: {theoretical_right}px")
            logger.info(f"   - 理论差值: {abs(theoretical_left - theoretical_right)}px")
            
            # 算法有效性验证
            theoretical_accuracy = abs(avg_left - theoretical_left) <= 1 and abs(avg_right - theoretical_right) <= 1
            
            logger.info("\n🎯 算法有效性:")
            if theoretical_accuracy:
                logger.info("   ✅ 理论计算与实测高度吻合")
                logger.info("   ✅ 数据驱动算法准确有效")
            else:
                logger.info("   ⚠️  理论与实测存在偏差，需要算法微调")
            
            # 最终总结
            logger.info("\n🎊 数据驱动优化总结:")
            logger.info(f"   优化状态: {result_status}")
            logger.info(f"   间距改善: 原5px差异 → 现{avg_diff:.1f}px差异")
            logger.info(f"   改善幅度: {((5 - avg_diff) / 5 * 100):.1f}%")
            
            if success_criteria and theoretical_accuracy:
                logger.info("   🏅 优化完全成功!")
                logger.info("   - 实现了像素级精确对齐")
                logger.info("   - 验证了数据驱动方法的有效性") 
                logger.info("   - 为后续类似问题提供了标准解决方案")
            
            logger.info("=" * 80)
            
            # 关闭应用
            window.close()
            
        except Exception as e:
            logger.error(f"验证优化效果时出错: {e}")
            import traceback
            logger.error(f"错误详情: {traceback.format_exc()}")
            window.close()
    
    # 延迟执行验证
    QTimer.singleShot(2000, verify_optimization_results)
    
    return app.exec()

if __name__ == "__main__":
    logger.info("开始验证数据驱动优化后的Sidebar间距效果...")
    verify_optimized_spacing()