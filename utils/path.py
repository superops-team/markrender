import sys
import os

def get_icon_path(icon_name):
    '''
    获取图标路径
    '''
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'icons', icon_name)
    return os.path.join('icons', icon_name)