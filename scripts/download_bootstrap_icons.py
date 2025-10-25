#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载Bootstrap Icons到指定路径
"""

import os
import requests
import zipfile
from io import BytesIO

def download_bootstrap_icons():
    """下载Bootstrap Icons到icons目录"""
    print("开始下载Bootstrap Icons...")
    
    # 创建icons目录
    icons_dir = "icons"
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
        print(f"创建目录: {icons_dir}")
    
    # Bootstrap Icons下载URL
    url = "https://github.com/twbs/icons/archive/refs/heads/main.zip"
    
    try:
        # 下载ZIP文件
        print("正在下载Bootstrap Icons...")
        response = requests.get(url)
        response.raise_for_status()
        
        # 解压ZIP文件
        print("正在解压Bootstrap Icons...")
        with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
            # 获取所有文件列表
            file_list = zip_file.namelist()
            
            # 筛选出icons目录下的SVG文件
            svg_files = [f for f in file_list if f.startswith("icons-main/icons/") and f.endswith(".svg")]
            
            # 提取SVG文件
            extracted_count = 0
            for svg_file in svg_files:
                # 获取文件名
                file_name = os.path.basename(svg_file)
                
                # 提取文件
                with zip_file.open(svg_file) as source, open(os.path.join(icons_dir, file_name), "wb") as target:
                    target.write(source.read())
                    extracted_count += 1
                    
                # 显示进度（每100个文件显示一次）
                if extracted_count % 100 == 0:
                    print(f"已提取 {extracted_count} 个图标...")
            
            print(f"成功提取 {extracted_count} 个图标到 {icons_dir} 目录")
            
        print("Bootstrap Icons下载完成!")
        
    except Exception as e:
        print(f"下载Bootstrap Icons时出错: {e}")

if __name__ == "__main__":
    download_bootstrap_icons()