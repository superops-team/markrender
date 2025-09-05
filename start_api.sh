#!/bin/bash

# 启动MarkRender API服务器的脚本

# 设置工作目录为项目根目录
cd "$(dirname "$0")"

# 检查是否安装了Python
if ! command -v python3 &> /dev/null
then
    echo "错误: 未找到Python3"
    exit 1
fi

# 检查是否安装了pip
if ! command -v pip &> /dev/null
then
    echo "错误: 未找到pip"
    exit 1
fi

# 安装依赖（如果需要）
echo "检查并安装依赖..."
pip install -r requirements.txt

# 启动API服务器
echo "启动MarkRender API服务器..."
python -m app.api.server --host 127.0.0.1 --port 8000

echo "API服务器已启动!"