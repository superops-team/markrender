# MarkRender 测试文件索引

本目录包含 MarkRender 项目的所有测试文件，按功能分类如下：

## 🧪 测试文件分类

### 🔧 基础功能测试
- [`test_alignment.py`](test_alignment.py) - 基础对齐功能测试

### 📐 Sidebar对齐测试系列

#### 边框显示测试
- [`test_sidebar_border_fix.py`](test_sidebar_border_fix.py) - Sidebar选中状态左侧边框显示修复测试
- [`test_sidebar_border.py`](test_sidebar_border.py) - Sidebar边框显示基础测试

#### 间距对齐测试  
- [`test_sidebar_spacing_alignment.py`](test_sidebar_spacing_alignment.py) - Sidebar边框到左右两侧间距对齐优化测试
- [`test_sidebar_precise_alignment.py`](test_sidebar_precise_alignment.py) - Sidebar按钮精确对齐测试
- [`test_sidebar_alignment_v2.py`](test_sidebar_alignment_v2.py) - Sidebar对齐优化V2测试

#### 综合解决方案测试
- [`test_icon_center_border_align.py`](test_icon_center_border_align.py) - 图标居中与边框对齐综合解决方案测试
- [`test_smaller_sidebar_border.py`](test_smaller_sidebar_border.py) - 更小Sidebar边框测试

### 📊 数据测量与验证工具

#### 间距测量工具
- [`measure_sidebar_spacing.py`](measure_sidebar_spacing.py) - Sidebar间距精确测量工具
- [`verify_optimized_spacing.py`](verify_optimized_spacing.py) - 优化后间距验证工具

#### 综合验证工具
- [`final_verification.py`](final_verification.py) - 最终验证测试工具

## 🚀 如何运行测试

### 环境要求
确保已激活虚拟环境并安装所有依赖：
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### 运行单个测试
```bash
# 在项目根目录下运行
python test/test_sidebar_border_fix.py
```

### 运行测量工具
```bash
# 测量当前Sidebar间距
python test/measure_sidebar_spacing.py

# 验证优化效果  
python test/verify_optimized_spacing.py

# 最终综合验证
python test/final_verification.py
```

## 📋 测试文件说明

### 🎯 功能测试文件
**命名模式**: `test_*.py`  
**用途**: 验证特定功能的正确性，通常包含自动化测试逻辑

### 📏 测量工具文件  
**命名模式**: `measure_*.py`, `verify_*.py`  
**用途**: 精确测量UI元素尺寸和间距，验证优化效果

### ✅ 验证工具文件
**命名模式**: `*_verification.py`  
**用途**: 综合验证多个功能模块的集成效果

## 🔍 测试覆盖范围

### UI组件测试
- ✅ Sidebar按钮对齐
- ✅ 边框显示效果  
- ✅ 间距精确控制
- ✅ 选中状态反馈

### 布局测试
- ✅ 图标居中效果
- ✅ 边框与分割线对齐
- ✅ 响应式布局适配
- ✅ 像素级精确控制

### 交互测试
- ✅ 悬停状态变化
- ✅ 选中状态切换  
- ✅ 视觉反馈效果
- ✅ 用户体验优化

## 📊 测试报告

所有测试运行后会在控制台输出详细的测试报告，包括：
- 🎯 **测试目标**: 本次测试要验证的功能点
- 📐 **测量数据**: 精确的像素级测量结果  
- ✅ **验证结果**: 是否达到预期效果
- 🎨 **视觉效果**: 界面显示效果描述
- 📋 **技术分析**: 实现方案的技术细节

## 🔗 相关资源

- **文档**: 参见 [`../docs/`](../docs/) 目录查看相关技术文档
- **源代码**: 参见 [`../app/`](../app/) 目录查看被测试的源代码
- **工具脚本**: 参见 [`../utils/`](../utils/) 目录查看辅助工具

---

> 💡 **提示**: 建议按照测试的复杂度从简单到复杂的顺序运行测试文件，有助于理解整个优化过程的演进。