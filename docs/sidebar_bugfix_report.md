# Sidebar按钮互斥效果Bug修复报告

## 问题描述

在实现Sidebar按钮互斥效果时，出现了一个AttributeError错误：
```
AttributeError: 'SidebarManager' object has no attribute 'button_group'
```

## 问题分析

### 错误原因
问题出现在按钮信号连接的时机。在`init_sidebar_button`方法中，按钮的`toggled`信号被连接到`on_button_toggled`槽函数，但此时`button_group`属性可能还没有被初始化。

### 详细分析
1. 在`__init__`方法中调用`init_ui`
2. 在`init_ui`方法中创建按钮并调用`init_sidebar_button`
3. `init_sidebar_button`方法中连接了按钮的`toggled`信号
4. 但是在信号连接时，`button_group`还未被创建（在`init_ui`方法的最后才创建）

## 修复方案

### 1. 提前初始化button_group属性
在`__init__`方法中提前初始化`button_group`属性，确保在按钮信号连接时该属性已存在。

### 2. 增加安全检查
在`on_button_toggled`方法中增加对`button_group`属性存在性的检查，防止在属性未初始化时访问。

## 修复实现

### 1. 在__init__方法中提前初始化
```python
def __init__(self, parent=None):
    super().__init__(parent)
    self.markdown_manager = MarkRenderManager()
    self.parent = parent
    self.app_style = AppStyle()  # 添加样式实例
    # 初始化按钮组
    self.button_group = []
    self.init_ui()
    # 设置侧边栏背景色和样式
    self.setStyleSheet(self.app_style.get_sidebar())
```

### 2. 在on_button_toggled方法中增加安全检查
```python
def on_button_toggled(self, button, checked, icon_name, toggle_slot):
    """统一处理按钮切换事件"""
    # 确保button_group已初始化
    if hasattr(self, 'button_group') and self.button_group:
        if checked:
            # 实现按钮互斥效果
            for other_button in self.button_group:
                if other_button != button and other_button.isChecked():
                    other_button.setChecked(False)
            
            # 更新图标为选中状态
            button.setIcon(QIcon(get_icon_path(icon_name, selected=True)))
        else:
            # 更新图标为非选中状态
            button.setIcon(QIcon(get_icon_path(icon_name, selected=False)))
    else:
        # 如果button_group未初始化，直接更新图标
        if checked:
            button.setIcon(QIcon(get_icon_path(icon_name, selected=True)))
        else:
            button.setIcon(QIcon(get_icon_path(icon_name, selected=False)))
    
    # 调用具体的处理函数
    toggle_slot(checked, icon_name)
```

## 测试验证

创建了测试脚本[test_sidebar_bugfix.py](file:///Users/bytedance/workspace/github/markrender/test/test_sidebar_bugfix.py)来验证修复效果：

1. 运行测试脚本，确认不再出现AttributeError错误
2. 验证按钮互斥效果正常工作
3. 验证默认状态正确设置
4. 验证按钮图标切换正常

## 修复效果

通过以上修复，解决了以下问题：

1. ✅ 消除了AttributeError错误
2. ✅ 保持了按钮互斥效果功能
3. ✅ 确保了默认状态正确性
4. ✅ 提高了代码的健壮性

## 总结

本次bug修复通过提前初始化属性和增加安全检查，解决了由于属性初始化时机不当导致的运行时错误。修复方案简单有效，没有影响原有功能，同时提高了代码的健壮性和容错能力。