# Sidebar按钮互斥效果实现说明

## 需求分析

实现Sidebar按钮的互斥效果，确保同时只能选择一个按钮，并且默认展开quickpick按钮。

## 实现方案

### 1. 按钮组管理
创建一个按钮组来管理所有Sidebar按钮，实现互斥效果。

### 2. 互斥逻辑
当一个按钮被选中时，自动取消其他按钮的选中状态。

### 3. 默认状态
设置toggle_quickpick_btn为默认选中状态。

## 核心代码实现

### 1. 按钮组创建
```python
# 创建按钮组，实现互斥效果
self.button_group = [self.toggle_quickpick_btn, self.import_btn, self.settings_btn]
```

### 2. 互斥逻辑实现
```python
def on_button_toggled(self, button, checked, icon_name, toggle_slot):
    """统一处理按钮切换事件"""
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
    
    # 调用具体的处理函数
    toggle_slot(checked, icon_name)
```

### 3. 按钮处理函数优化
```python
def on_import_toggled(self, checked, icon_name="plus-square"):
    """处理导入按钮切换"""
    if checked:
        self.handle_import()
        # 导入完成后，自动切换回quickpick按钮
        self.toggle_quickpick_btn.setChecked(True)

def on_settings_toggled(self, checked, icon_name="settings"):
    """处理设置按钮切换"""
    if checked:
        self.show_settings_dialog()
        # 设置对话框关闭后，自动切换回quickpick按钮
        self.toggle_quickpick_btn.setChecked(True)
```

## 功能特点

### 1. 互斥效果
- 任何时候只有一个按钮处于选中状态
- 点击一个按钮会自动取消其他按钮的选中状态

### 2. 默认状态
- 默认选中toggle_quickpick_btn按钮
- quickpick面板默认展开

### 3. 自动回退
- 导入和设置操作完成后自动回退到quickpick按钮
- 保持用户体验的一致性

## 测试验证

创建了测试脚本[test_sidebar_mutual_exclusion.py](file:///Users/bytedance/workspace/github/markrender/test/test_sidebar_mutual_exclusion.py)来验证功能实现：

1. 按钮互斥效果验证
2. 默认状态验证
3. 自动回退功能验证

## 代码文件修改

### app/sidebar/sidebar_manager.py
1. 添加了button_group属性来管理按钮组
2. 修改了on_button_toggled方法实现互斥效果
3. 优化了on_import_toggled和on_settings_toggled方法，添加自动回退功能
4. 修改了settings按钮的处理方式，使用独立的处理函数

## 实现效果

通过以上修改，Sidebar按钮实现了以下效果：

1. ✅ 互斥效果：任何时候只有一个按钮处于选中状态
2. ✅ 默认展开：默认选中quickpick按钮，面板默认展开
3. ✅ 自动回退：导入和设置操作完成后自动回退到quickpick按钮
4. ✅ 视觉反馈：选中状态有明确的视觉反馈
5. ✅ 用户体验：操作流程自然，符合用户预期