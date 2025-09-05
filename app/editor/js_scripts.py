"""
JS脚本模块化管理
提供统一的JavaScript代码调用接口，避免将JavaScript代码写死在Python中
"""

from typing import Dict, Any, Optional
from utils import logger

class JSScriptManager:
    """JS脚本管理器"""
    
    # 预定义的JS脚本模板
    _scripts = {
        "handle_backend_message": """
            window.handleBackendMessage({action}, {data}, {request_id});
        """,
        
        "handle_backend_response": """
            window.handleBackendResponse({response});
        """,
        
        "reset_editor_content": r"""
            try {
                // 针对不同页面类型使用不同的编辑器对象
                if (window.editorState && window.editorState.editor) {
                    // Markdown页面使用Cherry Markdown编辑器
                    if (typeof window.editorState.editor.setValue === 'function') {
                        window.editorState.editor.setValue(%(content)s);
                    }
                } else if (window.editor) {
                    // 其他可能使用ace editor的页面
                    if (typeof window.editor.setValue === 'function') {
                        window.editor.setValue(%(content)s);
                        if (window.editor.session && typeof window.editor.session.setUndoManager === 'function') {
                            window.editor.session.setUndoManager(new ace.UndoManager());  // 重置 undo 栈，如果使用 ace editor
                        }
                    }
                } else if (window.ExcalidrawLib && typeof window.ExcalidrawLib.clearScene === 'function') {
                    // Excalidraw页面
                    window.ExcalidrawLib.clearScene();
                } else if (typeof window.updateScene === 'function') {
                    // Excalidraw的另一种清空方式
                    window.updateScene({ elements: [] });
                }
                // 额外: 清空任何本地存储或变量，如果适用
                if (typeof localStorage !== 'undefined') {
                    localStorage.clear();
                }
            } catch (error) {
                console.error('Reset editor failed:', error);
            }
        """,
        
        "get_editor_content": r"""
            try {
                if (window.editorState && window.editorState.editor && typeof window.editorState.editor.getValue === 'function') {
                    return window.editorState.editor.getValue();
                } else if (window.editor && typeof window.editor.getValue === 'function') {
                    return window.editor.getValue();
                } else if (typeof window.getSceneElements === 'function') {
                    const elements = window.getSceneElements();
                    return JSON.stringify(elements);
                }
                return "";
            } catch (error) {
                console.error('Get editor content failed:', error);
                return "";
            }
        """,
        
        "notify_channel_ready": r"""
            if (window.WebChannelManager && typeof window.WebChannelManager.notifyChannelReady === 'function') {
                window.WebChannelManager.notifyChannelReady();
            }
        """,
        
        "report_error": r"""
            if (window.WebChannelManager && typeof window.WebChannelManager.reportError === 'function') {
                window.WebChannelManager.reportError(%(error)s, %(source)s);
            }
        """
    }
    
    @classmethod
    def get_script(cls, script_name: str, **kwargs) -> Optional[str]:
        """获取JS脚本"""
        if script_name not in cls._scripts:
            logger.warning(f"JS脚本 {script_name} 未找到")
            return None
        
        script_template = cls._scripts[script_name]
        try:
            # 如果没有提供参数，直接返回模板
            if not kwargs:
                return script_template
            
            # 使用kwargs填充模板
            return script_template % kwargs
        except KeyError as e:
            logger.error(f"JS脚本 {script_name} 参数缺失: {e}")
            return script_template
        except Exception as e:
            logger.error(f"JS脚本 {script_name} 格式化失败: {e}")
            return script_template
    
    @classmethod
    def add_script(cls, script_name: str, script_content: str):
        """添加新的JS脚本"""
        cls._scripts[script_name] = script_content
    
    @classmethod
    def remove_script(cls, script_name: str):
        """移除JS脚本"""
        if script_name in cls._scripts:
            del cls._scripts[script_name]
    
    @classmethod
    def list_scripts(cls) -> list:
        """列出所有可用的JS脚本"""
        return list(cls._scripts.keys())