#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sidebar按钮边框间距精确测量与优化算法分析
通过详细的几何计算和日志打印来分析实际间距，指导优化方案
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, QRect
from PySide6.QtGui import QPainter, QPen, QColor
from main import MainWindow
from utils.logger_utils import logger

def measure_sidebar_spacing():
    """精确测量sidebar按钮边框间距"""
    app = QApplication.instance() or QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    def detailed_spacing_analysis():
        """详细的间距分析"""
        try:
            # 获取sidebar相关组件
            sidebar = window.sidebar
            
            # 获取关键尺寸数据
            sidebar_width = sidebar.width()
            sidebar_geometry = sidebar.geometry()
            layout = sidebar.layout()
            margins = layout.contentsMargins()
            
            # 获取按钮信息
            home_btn = sidebar.file_browse_btn
            import_btn = sidebar.import_btn
            settings_btn = sidebar.settings_btn
            
            logger.info("=" * 80)
            logger.info("Sidebar按钮边框间距精确测量分析")
            logger.info("=" * 80)
            
            # === 1. 基础几何数据测量 ===
            logger.info("\n📐 基础几何数据测量:")
            logger.info(f"   Sidebar总宽度: {sidebar_width}px")
            logger.info(f"   Sidebar几何位置: x={sidebar_geometry.x()}, y={sidebar_geometry.y()}")
            logger.info(f"   Sidebar几何尺寸: w={sidebar_geometry.width()}, h={sidebar_geometry.height()}")
            logger.info(f"   布局边距: 左={margins.left()}px, 上={margins.top()}px, 右={margins.right()}px, 下={margins.bottom()}px")
            
            # === 2. 按钮几何数据分析 ===
            def analyze_button_geometry(button, button_name):
                """分析单个按钮的几何数据"""
                btn_geometry = button.geometry()
                btn_size = button.size()
                
                logger.info(f"\n🔍 {button_name}按钮几何分析:")
                logger.info(f"   按钮位置: x={btn_geometry.x()}, y={btn_geometry.y()}")
                logger.info(f"   按钮尺寸: w={btn_geometry.width()}, h={btn_geometry.height()}")
                logger.info(f"   按钮大小: {btn_size.width()}x{btn_size.height()}px")
                
                # 计算按钮相对于sidebar的位置
                btn_left_edge = btn_geometry.x()
                btn_right_edge = btn_geometry.x() + btn_geometry.width()
                sidebar_left_edge = 0  # sidebar内部坐标系
                sidebar_right_edge = sidebar_width
                
                # 计算实际间距
                left_spacing = btn_left_edge - sidebar_left_edge
                right_spacing = sidebar_right_edge - btn_right_edge
                
                logger.info(f"   按钮左边缘到sidebar左边缘: {left_spacing}px")
                logger.info(f"   按钮右边缘到sidebar右边缘: {right_spacing}px")
                
                return {
                    'button_name': button_name,
                    'geometry': btn_geometry,
                    'left_spacing': left_spacing,
                    'right_spacing': right_spacing,
                    'width': btn_geometry.width(),
                    'height': btn_geometry.height()
                }
            
            # 分析所有按钮（未选中状态）
            logger.info("\n🔢 未选中状态按钮间距测量:")
            home_btn.setChecked(False)
            import_btn.setChecked(False) 
            settings_btn.setChecked(False)
            
            # 强制刷新布局
            app.processEvents()
            
            unselected_data = []
            unselected_data.append(analyze_button_geometry(home_btn, "Home"))
            unselected_data.append(analyze_button_geometry(import_btn, "Import"))
            unselected_data.append(analyze_button_geometry(settings_btn, "Settings"))
            
            # === 3. 选中状态间距测量 ===
            def measure_selected_spacing(button, button_name):
                """测量选中状态的间距"""
                logger.info(f"\n🎯 {button_name}按钮选中状态测量:")
                
                # 设置为选中状态
                button.setChecked(True)
                app.processEvents()  # 确保样式生效
                
                # 重新获取几何数据
                btn_geometry = button.geometry()
                
                # 计算理论边框位置（考虑Qt边框向外扩展）
                # Qt中1px边框会向外扩展，所以实际占用空间更大
                border_width = 1  # 1px边框
                
                # 计算边框的实际占用区域
                border_left_edge = btn_geometry.x() - border_width
                border_right_edge = btn_geometry.x() + btn_geometry.width() + border_width
                border_top_edge = btn_geometry.y() - border_width
                border_bottom_edge = btn_geometry.y() + btn_geometry.height() + border_width
                
                # 计算边框到sidebar边缘的间距
                border_left_spacing = border_left_edge - 0  # 到sidebar左边缘
                border_right_spacing = sidebar_width - border_right_edge  # 到sidebar右边缘
                
                logger.info(f"   按钮几何位置: x={btn_geometry.x()}, y={btn_geometry.y()}")
                logger.info(f"   按钮几何尺寸: w={btn_geometry.width()}, h={btn_geometry.height()}")
                logger.info(f"   边框占用区域: 左={border_left_edge}, 右={border_right_edge}")
                logger.info(f"   边框左间距: {border_left_spacing}px")
                logger.info(f"   边框右间距: {border_right_spacing}px")
                logger.info(f"   间距差值: {abs(border_left_spacing - border_right_spacing)}px")
                
                # 间距对称性分析
                if border_left_spacing == border_right_spacing:
                    logger.info("   ✅ 完美对称: 左右间距完全一致")
                    alignment_status = "完美对称"
                elif abs(border_left_spacing - border_right_spacing) <= 0.5:
                    logger.info("   ⚠️  基本对称: 间距差异在0.5px以内")
                    alignment_status = "基本对称"
                else:
                    logger.info("   ❌ 不对称: 存在明显间距差异")
                    alignment_status = "不对称"
                
                return {
                    'button_name': button_name,
                    'geometry': btn_geometry,
                    'border_left_spacing': border_left_spacing,
                    'border_right_spacing': border_right_spacing,
                    'spacing_difference': abs(border_left_spacing - border_right_spacing),
                    'alignment_status': alignment_status
                }
            
            # 测量选中状态
            logger.info("\n🎯 选中状态边框间距测量:")
            selected_data = []
            
            # 依次测量每个按钮的选中状态
            for btn, name in [(home_btn, "Home"), (import_btn, "Import"), (settings_btn, "Settings")]:
                # 先取消所有选中状态
                home_btn.setChecked(False)
                import_btn.setChecked(False)
                settings_btn.setChecked(False)
                app.processEvents()
                
                # 测量当前按钮选中状态
                selected_data.append(measure_selected_spacing(btn, name))
            
            # === 4. 数据汇总分析 ===
            logger.info("\n📊 数据汇总分析:")
            
            # 未选中状态汇总
            logger.info("\n📋 未选中状态汇总:")
            for data in unselected_data:
                logger.info(f"   {data['button_name']}: 左间距={data['left_spacing']}px, 右间距={data['right_spacing']}px")
            
            # 选中状态汇总
            logger.info("\n📋 选中状态汇总:")
            for data in selected_data:
                logger.info(f"   {data['button_name']}: 边框左间距={data['border_left_spacing']}px, "
                           f"边框右间距={data['border_right_spacing']}px, 差值={data['spacing_difference']}px, "
                           f"状态={data['alignment_status']}")
            
            # === 5. 理论计算验证 ===
            logger.info("\n🧮 理论计算验证:")
            logger.info("   当前配置理论值:")
            logger.info(f"   - 布局左边距: {margins.left()}px")
            logger.info(f"   - 布局右边距: {margins.right()}px")
            logger.info(f"   - 按钮宽度: 36px (固定)")
            logger.info(f"   - 边框宽度: 1px (向外扩展)")
            
            theoretical_left = margins.left() - 1  # 边框向左扩展1px
            theoretical_right = margins.right()    # 右边距不变
            
            logger.info(f"   选中状态理论间距:")
            logger.info(f"   - 理论左间距: {margins.left()}px - 1px(边框) = {theoretical_left}px")
            logger.info(f"   - 理论右间距: {theoretical_right}px")
            logger.info(f"   - 理论差值: {abs(theoretical_left - theoretical_right)}px")
            
            # === 6. 优化算法建议 ===
            logger.info("\n🎯 优化算法建议:")
            
            # 分析实测数据和理论数据的差异
            actual_data = selected_data[0] if selected_data else None
            if actual_data:
                actual_left = actual_data['border_left_spacing']
                actual_right = actual_data['border_right_spacing']
                actual_diff = actual_data['spacing_difference']
                
                logger.info(f"   实测vs理论对比:")
                logger.info(f"   - 实测左间距: {actual_left}px vs 理论: {theoretical_left}px")
                logger.info(f"   - 实测右间距: {actual_right}px vs 理论: {theoretical_right}px")
                
                # 生成优化建议
                if actual_diff <= 0.5:
                    logger.info("   ✅ 当前对齐效果良好，无需调整")
                elif actual_left < actual_right:
                    # 左侧间距小于右侧，需要增加左边距
                    suggested_left_margin = margins.left() + actual_diff
                    logger.info(f"   📈 建议增加左边距: {margins.left()}px → {suggested_left_margin}px")
                elif actual_left > actual_right:
                    # 左侧间距大于右侧，需要减少左边距
                    suggested_left_margin = margins.left() - actual_diff
                    logger.info(f"   📉 建议减少左边距: {margins.left()}px → {suggested_left_margin}px")
                
                # 总宽度调整建议
                if actual_diff > 0.5:
                    logger.info(f"   🔧 同时建议调整总宽度以保持整体布局协调")
            
            # === 7. 算法优化公式 ===
            logger.info("\n🔬 算法优化公式:")
            logger.info("   边框对齐优化公式:")
            logger.info("   left_margin = base_margin + border_compensation")
            logger.info("   right_margin = base_margin")  
            logger.info("   total_width = left_margin + button_width + right_margin + border_expansion")
            logger.info("")
            logger.info("   其中:")
            logger.info("   - base_margin: 基础边距(通常7px)")
            logger.info("   - border_compensation: 边框补偿量(通常1px)")
            logger.info("   - border_expansion: 边框扩展量(Qt中为2px，左右各1px)")
            logger.info("   - button_width: 按钮宽度(36px)")
            
            logger.info("\n🎊 测量分析完成!")
            logger.info("=" * 80)
            
            # 关闭应用
            window.close()
            
        except Exception as e:
            logger.error(f"间距测量分析出错: {e}")
            import traceback
            logger.error(f"错误详情: {traceback.format_exc()}")
            window.close()
    
    # 延迟执行测量，确保窗口完全渲染
    QTimer.singleShot(2000, detailed_spacing_analysis)
    
    return app.exec()

if __name__ == "__main__":
    logger.info("开始Sidebar按钮边框间距精确测量...")
    measure_sidebar_spacing()