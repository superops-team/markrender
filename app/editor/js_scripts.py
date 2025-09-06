"""
JS脚本模块化管理
提供统一的JavaScript代码调用接口，避免将JavaScript代码写死在Python中
"""

import os
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, Undefined
from utils import logger

class JSScriptManager:
    """JS脚本管理器"""
    
    # 模板环境
    _template_env = None
    
    @classmethod
    def _get_template_env(cls):
        """获取模板环境"""
        if cls._template_env is None:
            template_dir = os.path.join(os.path.dirname(__file__), 'js_templates')
            cls._template_env = Environment(
                loader=FileSystemLoader(template_dir),
                trim_blocks=True,
                lstrip_blocks=True
            )
        return cls._template_env
    
    @classmethod
    def get_script(cls, script_name: str, **kwargs) -> Optional[str]:
        """获取JS脚本，使用Jinja2模板引擎渲染"""
        try:
            # 确保script_name以.js结尾
            if not script_name.endswith('.js'):
                script_name += '.js'
            
            # 处理参数，将Undefined对象转换为适当的默认值
            processed_kwargs = {}
            for key, value in kwargs.items():
                # 检查是否为Jinja2的Undefined对象
                if hasattr(value, '__class__') and 'Undefined' in value.__class__.__name__:
                    # 对于Undefined对象，根据变量名提供合理的默认值
                    if key in ['content', 'item_id', 'action', 'request_id', 'callback_id']:
                        processed_kwargs[key] = ''
                    elif key in ['data', 'response']:
                        processed_kwargs[key] = {}
                    else:
                        processed_kwargs[key] = None
                else:
                    processed_kwargs[key] = value
            
            # 获取模板环境
            env = cls._get_template_env()
            
            # 渲染模板
            template = env.get_template(script_name)
            script_content = template.render(**processed_kwargs)
            
            return script_content
        except Exception as e:
            logger.error(f"JS脚本 {script_name} 渲染失败: {e}")
            return None
    
    @classmethod
    def add_script(cls, script_name: str, script_content: str):
        """添加新的JS脚本 - 此方法在新架构中不适用，仅保留接口兼容性"""
        logger.warning("add_script方法在Jinja2模板架构中不适用")
    
    @classmethod
    def remove_script(cls, script_name: str):
        """移除JS脚本 - 此些方法在新架构中不适用，仅保留接口兼容性"""
        logger.warning("remove_script方法在Jinja2模板架构中不适用")
    
    @classmethod
    def list_scripts(cls) -> list:
        """列出所有可用的JS脚本"""
        try:
            template_dir = os.path.join(os.path.dirname(__file__), 'js_templates')
            if os.path.exists(template_dir):
                files = os.listdir(template_dir)
                return [f[:-3] if f.endswith('.js') else f for f in files]  # 移除.js后缀
            return []
        except Exception as e:
            logger.error(f"列出JS脚本失败: {e}")
            return []