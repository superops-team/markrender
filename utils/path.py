import sys
import os

def get_icon_path(icon_name, selected=False):
    '''
    获取图标路径，支持选中状态
    Args:
        icon_name: 图标名称（不含后缀）
        selected: 是否选中状态
    Returns:
        图标路径
    '''
    full_name = f"{icon_name}.svg"
    if selected:
        full_name = f'{icon_name}-selected.svg'
    
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'icons', full_name)
    return os.path.join('icons', full_name)