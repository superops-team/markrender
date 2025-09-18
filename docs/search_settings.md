# 搜索设置功能说明

## 功能介绍

在 MarkRender 应用的通用设置中，我们新增了搜索设置功能，允许用户自定义搜索结果的排序条件。

## 设置选项

用户可以在"通用设置"中找到"搜索设置"部分，其中有以下三个排序选项：

1. **按创建时间** - 搜索结果按文件的创建时间排序
2. **按更新时间** - 搜索结果按文件的最后更新时间排序
3. **按名称排序** - 搜索结果按文件名称的字母顺序排序

## 默认设置

默认情况下，搜索结果将按名称排序。

## 使用方法

1. 打开应用的设置对话框（通过侧边栏的设置按钮）
2. 在"通用设置"选项卡中找到"搜索设置"部分
3. 选择您偏好的排序方式
4. 点击"保存"按钮保存设置

## 技术实现

搜索设置保存在应用的设置数据库中，键名为 `general`，其中包含一个 `search_sort` 字段，其值可以是：
- `created_time` 表示按创建时间排序
- `updated_time` 表示按更新时间排序
- `name` 表示按名称排序

### 数据加载

在 [MarkRenderManager](file:///Users/wanglichao/workspace/superops/larina/markrender/db/markrender_manager.py#L10-L456) 类的 [load_items](file:///Users/wanglichao/workspace/superops/larina/markrender/db/markrender_manager.py#L43-L62) 方法中，会读取设置中的排序条件，并相应地对数据进行排序：

- 当设置为 `created_time` 时，数据按创建时间降序排列
- 当设置为 `updated_time` 时，数据按更新时间降序排列
- 当设置为 `name` 时，数据按标题名称升序排列

## 代码结构

- 设置管理：`db/settings_manager.py`
- 设置界面：`app/sidebar/settings_dialog.py`
- 数据加载：`db/markrender_manager.py` 中的 [load_items](file:///Users/wanglichao/workspace/superops/larina/markrender/db/markrender_manager.py#L43-L62) 方法
- 设置存储：`db/models.py` 中的 `Settings` 模型