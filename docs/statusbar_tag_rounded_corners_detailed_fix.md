# Statusbar标签圆角样式详细修复说明

## 问题确认

Statusbar上的tag标签仍然显示为方形而不是圆角，尽管已经进行了初步修复。

## 深入分析

### 可能的原因
1. **Qt渲染机制**：某些Qt版本或平台上，样式表的圆角渲染可能需要特殊处理
2. **样式表优先级**：可能存在其他样式覆盖了圆角设置
3. **组件属性**：缺少必要的属性来启用样式表的圆角裁剪
4. **尺寸计算**：标签的宽度和高度比例可能不适合显示圆角效果

### 当前实现检查
```python
tag_label.setStyleSheet(f'''
    QLabel {{
        background-color: {PRIMARY_100};
        color: {PRIMARY_600};
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 11px;
        border: 1px solid {PRIMARY_200};
        min-height: 18px;
        min-width: 20px;
    }}
''')
# 启用样式表的圆角裁剪
tag_label.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
```

## 进一步优化方案

### 1. 增强圆角渲染
```python
# 启用抗锯齿渲染以获得更平滑的圆角
tag_label.setRenderHint(QPainter.RenderHint.Antialiasing, True)
tag_label.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
```

### 2. 使用自定义绘制方法
如果样式表方法仍然无法生效，可以考虑使用自定义绘制：

```python
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PySide6.QtCore import Qt, QRectF

class RoundedTagLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("background-color: transparent; border: none;")
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        
        # 绘制圆角矩形
        rect = QRectF(0, 0, self.width() - 1, self.height() - 1)
        path = QPainterPath()
        path.addRoundedRect(rect, 16, 16)  # 16px圆角
        
        # 绘制背景
        painter.fillPath(path, QBrush(QColor(PRIMARY_100)))
        
        # 绘制边框
        pen = QPen(QColor(PRIMARY_200), 1)
        painter.setPen(pen)
        painter.drawPath(path)
        
        # 绘制文字
        painter.setPen(QColor(PRIMARY_600))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())
```

### 3. 确保样式表正确应用
```python
def update_tags(self, tags):
    """更新标签列表"""
    # 清除现有标签
    while self.tags_layout.count() > 0:
        item = self.tags_layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
    
    # 添加新标签
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        for tag in tag_list:
            tag_label = QLabel(f"{tag}")
            # 使用更明确的样式表设置
            tag_label.setStyleSheet(f"""
                background-color: {PRIMARY_100};
                color: {PRIMARY_600};
                padding: 4px 12px;
                border-radius: 16px;
                font-size: 11px;
                border: 1px solid {PRIMARY_200};
                min-height: 20px;
                min-width: 25px;
            """)
            # 确保样式表生效
            tag_label.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
            tag_label.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
            self.tags_layout.addWidget(tag_label)
    else:
        # 如果没有标签，显示"无"消息
        no_tags_label = QLabel("无")
        no_tags_label.setStyleSheet("color: #999; font-size: 11px; font-style: italic;")
        self.tags_layout.addWidget(no_tags_label)
```

## 测试验证方法

### 1. 视觉检查
- 在不同操作系统和屏幕分辨率下检查圆角效果
- 检查标签在不同内容长度下的显示效果
- 验证标签在高DPI屏幕上的渲染质量

### 2. 代码验证
创建了测试脚本[test_statusbar_rounded_corners_detailed.py](file:///Users/bytedance/workspace/github/markrender/test/test_statusbar_rounded_corners_detailed.py)来详细验证修复效果：

1. 测试不同标签组合的圆角显示
2. 验证标签更新和清除功能
3. 检查标签在不同窗口大小下的表现

## 备用解决方案

如果样式表方法仍然无法实现圆角效果，可以考虑以下备用方案：

### 1. 使用Frame容器
```python
from PySide6.QtWidgets import QFrame

# 使用QFrame作为标签容器
tag_frame = QFrame()
tag_frame.setStyleSheet(f"""
    QFrame {{
        background-color: {PRIMARY_100};
        border: 1px solid {PRIMARY_200};
        border-radius: 16px;
        padding: 4px 12px;
    }}
""")
```

### 2. 使用QPushButton模拟标签
```python
from PySide6.QtWidgets import QPushButton

# 使用不可点击的按钮模拟标签
tag_button = QPushButton(tag)
tag_button.setFlat(True)
tag_button.setEnabled(False)
tag_button.setStyleSheet(f"""
    QPushButton {{
        background-color: {PRIMARY_100};
        color: {PRIMARY_600};
        border: 1px solid {PRIMARY_200};
        border-radius: 16px;
        padding: 4px 12px;
        font-size: 11px;
        min-height: 20px;
    }}
    QPushButton:disabled {{
        background-color: {PRIMARY_100};
        color: {PRIMARY_600};
        border: 1px solid {PRIMARY_200};
    }}
""")
```

## 总结

通过增强样式表设置和添加必要的Qt属性，应该能够解决Statusbar标签圆角样式不生效的问题。如果问题仍然存在，可以考虑使用自定义绘制或备用组件方案。

关键修复点：
1. ✅ 增加了`WA_StyledBackground`属性确保样式表生效
2. ✅ 调整了padding和尺寸以更好地显示圆角
3. ✅ 提供了多种备用解决方案
4. ✅ 创建了详细的测试验证脚本

这些改进应该能够确保Statusbar标签正确显示圆角样式。