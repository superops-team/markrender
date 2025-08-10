import os
import json  # 添加json导入
import time

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QObject, Signal, Property, QTimer, Slot
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings

from db.settings_manager import SettingsManager
from db.markdown_manager import MarkdownManager
from app.editor.background import ThreadPoolManager, AutoSaveWorker, ContentLoader
from app.shortcut_manager import ShortcutManager  # 添加快捷键管理器导入
from app.app_style import AppStyle
from app.editor.channel import WebCommunicationManager
from utils import logger
from db import db_manager


class MarkdownDocument(QObject):
    text_changed = Signal(str)  # 文档内容变更信号
    content_changed = Signal(str)  # Web端内容变化时触发

    def __init__(self, file_id, file_name):
        super().__init__()
        self._file_id = file_id
        self.file_name = file_name
        self._text = ""
        self._suppress_change_notification = False
        # 新增防抖定时器，默认 200 毫秒
        self._debounce_timer = QTimer(self)
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.timeout.connect(self._emit_delayed_change)
        self._debounce_interval = 200

    @Slot(str)
    def on_content_changed(self, text):
        """Web 端内容变化时的处理"""
        if not self._suppress_change_notification:
            self._text = text
            self._debounce_timer.start(self._debounce_interval)

    def _emit_delayed_change(self):
        """延迟发射内容变化信号"""
        logger.debug(f"MarkdownDocument text updated, length: {len(self._text)}, first 20 chars: {self._text[:20]}")
        self.content_changed.emit(self._text)

    @property
    def file_id(self):
        return self._file_id

    @file_id.setter
    def file_id(self, value):
        if value != self._file_id:
            self.reset()
            self._file_id = value

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text
        self.text_changed.emit(text)  # 触发文档内部变更

    def reset(self):
        """重置文档状态"""
        self._text = ""
        self.text_changed.emit("")  # 发射清空内容的信号

    text = Property(str, get_text, set_text, notify=text_changed)


# 自定义 QWebEnginePage 类，拦截控制台日志和链接打开请求
class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        # 调用原有的处理方法，可根据需求修改处理逻辑
        super().javaScriptConsoleMessage(level, message, line_number, source_id)
        # 可以在这里添加自定义的日志记录逻辑
        logger.debug(f"JS Console: {message} (Line {line_number} in {source_id})", level)

    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        """
        重写导航请求方法，限制 URL 打开
        :param url: 请求的 URL
        :param nav_type: 导航类型
        :param is_main_frame: 是否为主框架
        :return: 是否允许导航
        """
        # 这里可以添加你的 URL 限制逻辑，以下是示例：
        # 只允许打开本地文件和特定域名的链接
        allowed_schemes = ['file']  # 允许 file 协议
        allowed_domains = ['example.com']  # 允许的域名列表

        if url.scheme() in allowed_schemes:
            return True
        if url.host() in allowed_domains:
            return True
        
        # 打印被阻止的 URL，方便调试
        logger.debug(f"Blocked navigation to: {url.toString()}")
        return False


class MarkdownEditor(QWidget):
    def __init__(self, parent=None, file_id="", file_name=""):
        super().__init__(parent)
        # 首先初始化web_comm
        self.web_comm = WebCommunicationManager.instance()
        # 然后再调用init_web_handlers()
        self.init_web_handlers()
        # 初始化线程池管理器
        self.thread_pool = ThreadPoolManager()
        # 连接线程池信号
        self.thread_pool.task_completed.connect(self.on_task_completed)
        self.thread_pool.task_failed.connect(self.on_task_failed)
        # Initialize document for WebChannel
        self.document = MarkdownDocument(file_id, file_name)
        # 注册文档到通信管理器
        if file_id:  # 确保file_id存在
            self.web_comm.document_map[file_id] = self.document
            self.file_id = file_id
        # 建立信号连接
        self.document.text_changed.connect(self.on_document_text_changed)  # 数据库读取后写入到前端
        self.markdown_manager = MarkdownManager()
        
        # 添加上次保存内容跟踪
        self.last_saved_text = None
        
        # 初始化快捷键管理器
        self.shortcut_manager = ShortcutManager(self)
        self.init_shortcuts()
        
        # 假设 history_panel 是 HistoryPanel 实例
        if hasattr(self.parent, 'history_panel'):
            self.parent.history_panel.history_item_selected.connect(self.update_markdown_content)
        
        # Setup GUI
        self.setup_ui()
        
        # 自动保存相关初始化
        self.document_modified = False
        self.init_auto_save()

    def setup_ui(self):
        # Web view for Cherry Markdown
        self.preview = QWebEngineView()
        # 创建自定义的 Page 实例
        page = CustomWebEnginePage(self.preview)
        self.preview.setPage(page)

        # 添加缓存设置
        cache_path = db_manager.get_user_data_dir() + '/web_cache'
        profile = self.preview.page().profile()
        profile.setCachePath(cache_path)
        profile.setPersistentStoragePath(db_manager.get_user_data_dir() + '/web_storage')
        profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
        # 设置缓存大小为 100MB
        profile.setHttpCacheMaximumSize(100 * 1024 * 1024)

        # 添加页面加载完成信号绑定
        self.preview.loadFinished.connect(self.on_page_loaded)

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.preview)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        self.setLayout(layout)

        # 设置圆角样式
        self.setStyleSheet(AppStyle().get_editor_parent() + AppStyle().get_editor_preview())

        # Setup WebChannel
        self.web_comm.attach_to_page(self.preview.page())
        
        # Load HTML file
        html_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "resources",
                "index.html"))
        self.preview.setUrl(QUrl.fromLocalFile(html_path))
        self.preview.page().settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, False)
        self.preview.page().settings().setAttribute(QWebEngineSettings.PluginsEnabled, False)
        self.preview.page().settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False) 
        self.preview.page().settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        self.preview.page().settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
        self.preview.page().settings().setAttribute(QWebEngineSettings.WebGLEnabled, True)
    
    @property
    def file_id(self):
        return self.document.file_id

    @file_id.setter
    def file_id(self, value):
        if value != self.document.file_id:
            if self.document.file_id:
                del self.web_comm.document_map[self.document.file_id]
            if value:
                self.document.file_id = value
                self.web_comm.document_map[value] = self.document
    
    def on_document_text_changed(self, text):
        """转发文档变更到前端"""
        self.web_comm.send_message("textChanged", {"content": text})
    
    def init_auto_save(self):
        """初始化自动保存功能"""
        self.general_settings = SettingsManager().get_settings_dict('general') or {}
        self.auto_save_enabled = self.general_settings.get('auto_save', True)
        self.auto_save_interval = self.general_settings.get('auto_save_interval', 30) * 1000
        
        if self.auto_save_enabled:
            self.auto_save_timer = QTimer(self)
            self.auto_save_timer.timeout.connect(self.submit_auto_save_task)
            self.auto_save_timer.start(self.auto_save_interval)

    def submit_auto_save_task(self):
        """提交自动保存任务"""
        if self.document_modified and self.document.file_id:
            task_id = f"auto_save_{self.document.file_id}_{int(time.time())}"
            save_worker = AutoSaveWorker(
                file_id=self.document.file_id,
                content=self.document.get_text()
            )
            self.thread_pool.submit_task(
                task_id=task_id,
                worker=save_worker,
                callback=self.on_auto_save_completed
            )
            logger.info(f"提交自动保存任务: {task_id}")

    def on_auto_save_completed(self, task_id, result):
        """自动保存完成回调"""
        if result:
            self.last_saved_text = self.document.get_text()
            self.document_modified = False
            logger.info(f"自动保存成功: {task_id}, save content: {self.last_saved_text[-10:-1]}")

    def on_document_modified(self, text, source="user"):
        """标记文档为已修改，source: user/program"""
        if self.last_saved_text is None:
            self.last_saved_text = text
            return
        
        # 程序更新不触发修改标记
        if source == "program":
            self.last_saved_text = text
            return
            
        # 使用更智能的比较，避免空格等微小变化
        if text.strip() != self.last_saved_text.strip():
            self.document_modified = True
    
    def init_shortcuts(self):
        """初始化快捷键连接"""
        # 连接保存快捷键
        self.shortcut_manager.save_requested.connect(self.save_document)
        
        # 连接其他快捷键
        self.shortcut_manager.new_file_requested.connect(self.create_new_file)
        self.shortcut_manager.open_file_requested.connect(self.open_file)
        self.shortcut_manager.find_requested.connect(self.show_find_dialog)
        
        # 注册默认快捷键
        self.shortcut_manager.register_default_shortcuts()

    def save_markdown_content(self, data):
        """线程安全的保存方法"""
        try:
            data = json.loads(data) if isinstance(data, str) else data
            content = data.get('content', '')
            if not self.document.file_id:
                return {"error": "无文件ID"}
            
            # 数据库操作通常是线程安全的
            success = self.markdown_manager.save_markdown(
                id=self.document.file_id,
                content=content,
            )
            
            return {
                "success": success,
                "file_id": self.document.file_id,
                "content_length": len(content)
            }
            
        except Exception as e:
            logger.error(f"保存失败: {str(e)}")
            return {"error": str(e)}

    def report_js_error(self, error_info):
        """线程安全的错误报告"""
        try:
            error_data = json.loads(error_info) if isinstance(error_info, str) else error_info
            logger.error(f'JS错误: {error_data}')
            return {"logged": True}
        except Exception as e:
            logger.error(f'处理JS错误失败: {str(e)}')
            return {"error": str(e)}

    def save_document(self):
        """手动保存当前文档"""
        if not self.document.file_id:
            logger.warning("无法保存：文档未关联文件ID")
            return False
        logger.info("快捷键触发保存动作")
        try:
            # 获取当前编辑内容
            def handle_save_content(content):
                if content:
                    # 保存到数据库
                    success = self.markdown_manager.save_markdown(
                        id=self.document.file_id, 
                        content=content
                    )
                    
                    if success:
                        self.last_saved_text = content
                        self.document_modified = False
                        logger.info(f"手动保存成功: {self.document.file_id}")
                    else:
                        logger.error("保存到数据库失败")
                        
            # 获取当前内容并保存
            self.get_markdown(handle_save_content)
            return True
            
        except Exception as e:
            logger.error(f"保存文档失败: {str(e)}")
            return False

    def create_new_file(self):
        """创建新文件（快捷键响应）"""
        if hasattr(self.parent.history_panel, 'create_new_markdown'):
            self.parent.history_panel.create_new_markdown()

    def open_file(self):
        """打开文件（快捷键响应）"""
        if hasattr(self.parent.sidebar_manager, 'handle_import'):
            self.parent.sidebar_manager.handle_import()

    def show_find_dialog(self):
        # 通过channel发送命令，而非直接调用runJavaScript
        self.web_comm.send_message("executeCommand", {
            "command": "find"
        })

    def update_theme(self, theme):
        # 通过channel发送主题更新请求
        self.web_comm.send_message("setTheme", {
            "theme": theme
        })

    def reset(self):
        self.document.file_id = ""
        self.document.file_name = ""
        self.document.reset()  # 调用文档的 reset 方法
        # 通过channel发送清空内容请求
        self.web_comm.send_message("setValue", {
            "content": ""
        })
        self.document.reset()  # 调用文档的 reset 方法
        # 执行 JavaScript 清空编辑区内容
        js_code = """
            if (window.editor) {
                window.editor.setValue('');
            }
        """
        self.preview.page().runJavaScript(js_code)

    def set_file_id(self, file_id):
        self.document.file_id = file_id
        # 通知前端当前文件ID
        if hasattr(self, 'web_comm') and self.web_comm:
            # 发送文件ID变更通知到前端
            self.web_comm.send_message('setCurrentFileId', {
                'file_id': file_id
            })
            logger.debug(f"已通知前端当前文件ID: {file_id}")
        else:
            logger.warning("web_comm未初始化，无法通知前端当前文件ID变更")

    def set_file_name(self, file_name):
        self.document.file_name = file_name

    def get_markdown(self, callback):
        """获取markdown内容"""
        # 设置5秒超时
        timeout_timer = QTimer()
        timeout_timer.setSingleShot(True)
        timeout_timer.timeout.connect(lambda: callback({
            'success': False,
            'error': '获取内容超时'
        }))
        timeout_timer.start(5000)

        # 发送获取请求
        self.web_comm.send_message(
            'getMarkdown',
            callback=lambda response: (
                timeout_timer.stop(),
                callback(response)
            )
        )

    def set_text_content(self, text_content):
        # 通过channel设置内容
        if not self.web_comm or not self.web_comm.page:
            logger.error("web_comm未初始化或页面未加载，无法设置内容")
            return

        # 检查页面是否已加载
        if not hasattr(self, 'page_loaded') or not self.page_loaded:
            # 页面未加载，延迟发送
            logger.warning("页面未加载，延迟设置内容")
            self.initial_content = text_content
            return

        # 添加回调机制确认消息发送状态
        def handle_set_value(response):
            if response.get('success'):
                self.last_saved_text = text_content
                logger.debug("内容已成功设置到前端")
            else:
                logger.error(f"设置内容失败: {response.get('error')}")

        self.web_comm.send_message("setValue", {
            "content": text_content
        }, handle_set_value)
        self.last_saved_text = text_content

    def resizeEvent(self, event):
        """窗口大小改变时触发，确保编辑区高度自适应"""
        super().resizeEvent(event)
        # 可以在这里添加额外的调整逻辑
        # 布局管理器会自动处理子部件的大小

    def handle_js_console_message(self, level, message, line_number, source_id):
        """处理 JavaScript 控制台消息"""
        level_map = {
            QWebEnginePage.InfoMessageLevel: "INFO",
            QWebEnginePage.WarningMessageLevel: "WARNING",
            QWebEnginePage.ErrorMessageLevel: "ERROR"
        }
        log_level = level_map.get(level, "UNKNOWN")
        logger.info(f"JS {log_level}: {message} at {source_id}:{line_number}")
    
    def on_page_loaded(self, success):
        """页面加载完成回调"""
        if success:
            self.page_loaded = True
            logger.debug("预览页面加载完成")
            # 如果有延迟发送的初始内容
            if hasattr(self, 'initial_content'):
                self.set_text_content(self.initial_content)
                del self.initial_content
        else:
            logger.error("预览页面加载失败")
            
            # 通过channel注册web端事件
            self.web_comm.send_message("registerEditorEvents", {})
            
            # 通过channel设置内容变化监听
            self.web_comm.send_message("setupContentChangeListener", {
                "callback": "contentChanged"
            })

    def update_markdown_content(self, item):
        """更新 Markdown 内容"""
        try:
            # 使用线程池提交内容加载任务
            loader = ContentLoader(item.file_id, self.markdown_manager)
            self.thread_pool.submit_task(f"load_{item.file_id}", loader, self.on_content_loaded)
        except Exception as e:
            logger.error(f"更新 Markdown 内容失败: {str(e)}")

    def on_content_loaded(self, content):
        """内容加载完成回调"""
        self.document.set_text(content)
        self.last_saved_text = content
        self.document_modified = False

    @Slot(str, object)
    def on_task_completed(self, task_id, result):
        """线程任务完成处理"""
        if task_id.startswith("load_content_"):
            self.on_content_loaded(result)
        elif task_id.startswith("auto_save_"):
            self.on_auto_save_completed(task_id, result)

    @Slot(str, str)
    def on_task_failed(self, task_id, error):
        """线程任务失败处理"""
        logger.error(f"任务 {task_id} 执行失败: {error}")

    def report_js_error(self, error_info):
        """接收并处理 JS 侧的错误信息"""
        try:
            error_data = json.loads(error_info)
            logger.error(f'收到 JS 错误: {error_data}')
        except json.JSONDecodeError:
            logger.error(f'解析 JS 错误信息失败: {error_info}')

    def closeEvent(self, event):
        # 1. 停止自动保存定时器
        if hasattr(self, 'auto_save_timer'):
            self.auto_save_timer.stop()
            logger.info("Auto-save timer stopped")

        # 2. 退出前保存文件
        if hasattr(self, 'web_comm') and self.document and self.document.file_id:
            logger.info(f"退出前获取文档对象: {self.document.file_id}")
            
            def save_markdown(response):
                content = response.get('content')
                logger.info(f"退出前保存文档对象: {self.document.file_id}, 内容长度: {len(content)}")
                if content:
                    self.markdown_manager.save_markdown(id=self.document.file_id, content=content)
                else:
                    logger.error(f"退出前保存文档对象失败: {self.document.file_id}, 错误信息: {response}")
                
                # 保存完成后再清理资源
                self._cleanup_resources()
            
            self.web_comm.send_message("getMarkdown", {}, callback=save_markdown)
            # 阻止事件默认处理，等待保存完成
            event.ignore()
            return
    
        # 如果没有需要保存的文档，直接清理资源
        self._cleanup_resources()
        
    def _cleanup_resources(self):
        # 3. 清理线程池资源
        if hasattr(self, 'thread_pool'):
            # 取消所有未完成任务
            self.thread_pool.cancel_all_tasks()
            # 等待当前任务完成（最多等待2秒）
            self.thread_pool.wait_for_completion(2000)
            logger.info("Thread pool resources cleaned up")

        # 4. 释放Web通信资源
        if hasattr(self, 'web_comm'):
            self.web_comm.cleanup()

    def init_web_handlers(self):
        """初始化Web发起请求处理器 - 线程安全版本"""
        # 使用异步处理，但确保线程安全
        self.web_comm.register_python_handler('autoSave', self.save_markdown_content, is_async=True)
        self.web_comm.register_python_handler('reportError', self.report_js_error, is_async=True)
