# 树形结构功能使用说明

## 概述

MarkRender 现在支持树形结构管理，允许用户将文档组织成文件夹和子文件夹的层次结构。

## 新增字段

在 `MarkRenderData` 模型中新增了以下字段以支持树形结构：

- `parent_id`: 父节点ID，用于建立节点间的父子关系
- `order`: 排序字段，用于控制同级节点的显示顺序
- `level`: 层级字段，表示节点在树中的深度
- `is_folder`: 是否为文件夹标识，0表示文件，1表示文件夹

## 新增接口

### 1. 创建文件夹

```python
def create_folder(self, title, parent_id=None):
    """
    创建文件夹
    Args:
        title: 文件夹标题
        parent_id: 父节点ID（可选）
    Returns:
        创建的文件夹ID
    """
```

### 2. 获取子节点

```python
def get_children(self, parent_id=None):
    """
    获取指定节点的子节点
    Args:
        parent_id: 父节点ID，None表示获取根节点
    Returns:
        子节点列表
    """
```

### 3. 移动节点

```python
def move_item(self, item_id, new_parent_id=None):
    """
    移动节点到新的父节点
    Args:
        item_id: 要移动的节点ID
        new_parent_id: 新的父节点ID
    """
```

### 4. 更新排序

```python
def update_order(self, item_id, new_order):
    """
    更新节点的排序
    Args:
        item_id: 节点ID
        new_order: 新的排序值
    """
```

### 5. 获取树形结构

```python
def get_tree_structure(self, parent_id=None):
    """
    获取树形结构数据
    Args:
        parent_id: 父节点ID，None表示获取根节点
    Returns:
        树形结构数据
    """
```

## 使用示例

### 创建文件夹结构

```python
from db.markrender_manager import MarkRenderManager

manager = MarkRenderManager()

# 创建根文件夹
root_folder_id = manager.create_folder("项目文档")

# 创建子文件夹
dev_folder_id = manager.create_folder("开发文档", parent_id=root_folder_id)
design_folder_id = manager.create_folder("设计文档", parent_id=root_folder_id)

# 创建文件并放入子文件夹
file_id = manager.save_item(
    title="API设计规范",
    content="# API设计规范\n...",
    parent_id=design_folder_id,
    page_type="markdown"
)
```

### 获取树形结构

```python
# 获取完整的树形结构
tree = manager.get_tree_structure()
print_tree(tree, 0)

def print_tree(nodes, level):
    for node in nodes:
        indent = "  " * level
        node_type = "📁" if node['is_folder'] else "📄"
        print(f"{indent}{node_type} {node['title']} (ID: {node['id']})")
        if 'children' in node and node['children']:
            print_tree(node['children'], level + 1)
```

### 移动节点

```python
# 将文件移动到另一个文件夹
manager.move_item(file_id, dev_folder_id)
```

### 更新排序

```python
# 更新节点排序
manager.update_order(dev_folder_id, 0)  # 开发文档排在前面
manager.update_order(design_folder_id, 1)  # 设计文档排在后面
```

## 注意事项

1. 数据库模式会自动更新以包含新的树形结构字段
2. 已有的数据会被保留，新字段会使用默认值
3. `parent_id` 字段允许为 NULL，表示根节点
4. `level` 字段会自动计算，根节点为 0，子节点为父节点层级 + 1
5. `is_folder` 字段用于区分文件和文件夹，0 表示文件，1 表示文件夹