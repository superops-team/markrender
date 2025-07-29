import os
from utils import logger
from db import db_manager
from PySide6 import QtWidgets
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6 import QtWebEngineCore
from PySide6.QtCore import QUrl, QObject, Signal, Property, QThread, QTimer, Slot, QStandardPaths
from PySide6.QtWebChannel import QWebChannel
from ..app_style import AppStyle
from PySide6.QtWebEngineCore import QWebEnginePage
from db.settings_manager import SettingsManager
from db.markdown_manager import MarkdownManager
import threading
from ..shortcut_manager import ShortcutManager  # 添加快捷键管理器导入


class MarkdownDocument(QObject):
    def __init__(self, file_id, file_name):
        super().__init__()
        self._file_id = file_id
        self.file_name = file_name
        self._text = ""
        self._suppress_change_notification = False  # 防止循环触发

    # 新增信号
    content_changed = Signal(str)  # Web端内容变化时触发
    
    @Slot(str)
    def on_content_changed(self, text):
        """Web端内容变化时的处理"""
        if not self._suppress_change_notification:
            self._text = text
            self.text_changed.emit(text)

    def set_text(self, text):
        """设置文本，避免循环触发"""
        self._suppress_change_notification = True
        self._text = text
        self.text_changed.emit(text)
        self._suppress_change_notification = False

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

    def reset(self):
        """重置文档状态"""
        self._text = ""
        self.text_changed.emit("")  # 发射清空内容的信号

    text_changed = Signal(str)
    text = Property(str, get_text, set_text, notify=text_changed)


# 自定义 QWebEnginePage 类，拦截控制台日志
class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        # 调用原有的处理方法，可根据需求修改处理逻辑
        super().javaScriptConsoleMessage(level, message, line_number, source_id)
        # 可以在这里添加自定义的日志记录逻辑
        print(f"JS Console: {message} (Line {line_number} in {source_id})", level)


class AutoSaveWorker(QObject):
    save_requested = Signal()
    cleanup_requested = Signal()
    cleanup_finished = Signal()  # 新增清理完成信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.general_settings = SettingsManager().get_settings_dict('general') or {}  # 通用设置，添加空字典回退
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_save_condition)
        self.init_timer()
        self.cleanup_requested.connect(self.cleanup)  # 连接信号和清理方法

    def init_timer(self):
        """根据设置初始化定时器"""
        self.auto_save_enabled = self.general_settings.get('auto_save_enabled', True)
        self.check_interval = self.general_settings.get('auto_save_interval', 30) * 1000  # 转换为毫秒

        if self.auto_save_enabled:
            self.timer.start(self.check_interval)
        else:
            self.timer.stop()

    def check_save_condition(self):
        """检查是否需要触发保存"""
        if self.auto_save_enabled:
            self.save_requested.emit()

    def update_settings(self):
        """更新设置并重启定时器"""
        self.init_timer()

    def cleanup(self):
        """清理定时器"""
        self.timer.stop()
        self.cleanup_finished.emit()  # 发射清理完成信号

class MarkdownEditor(QtWidgets.QWidget):
    def __init__(self, parent=None, file_id="", file_name=""):
        super().__init__(parent)
        # Initialize document for WebChannel
        self.document = MarkdownDocument(file_id, file_name)
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
        profile = self.preview.page().profile()
        # cache_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.CacheLocation), "web_cache")
        cache_path = db_manager.get_user_data_dir() + '/web_cache'
        profile.setCachePath(cache_path)
        profile.setPersistentStoragePath(db_manager.get_user_data_dir() + '/web_storage')
        profile.setHttpCacheType(QtWebEngineCore.QWebEngineProfile.DiskHttpCache)

        # 添加页面加载完成信号绑定
        self.preview.loadFinished.connect(self.on_page_loaded)

        # 创建布局
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.preview)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        self.setLayout(layout)

        # 设置圆角样式
        self.setStyleSheet(AppStyle().get_editor_parent() + AppStyle().get_editor_preview())

        # Setup WebChannel
        self.channel = QWebChannel(self)
        self.channel.registerObject("document", self.document)
        self.preview.page().setWebChannel(self.channel)
        
        # 连接文档变化信号
        self.document.text_changed.connect(self.on_document_modified)
        
        # Load HTML file
        html_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "resources",
                "index.html"))
        self.preview.setUrl(QUrl.fromLocalFile(html_path))
        # Add these settings with corrected import
        self.preview.page().settings().setAttribute(
            QtWebEngineCore.QWebEngineSettings.ErrorPageEnabled, True)
        # 禁用不必要的功能
        self.preview.page().settings().setAttribute(
            QtWebEngineCore.QWebEngineSettings.PluginsEnabled, True)
        self.preview.page().settings().setAttribute(
            QtWebEngineCore.QWebEngineSettings.JavascriptCanOpenWindows, True)
        self.preview.page().settings().setAttribute(
            QtWebEngineCore.QWebEngineSettings.LocalStorageEnabled, True)

    def init_auto_save(self):
        """初始化自动保存功能"""
        # 创建后台线程
        self.auto_save_thread = QThread()
        self.auto_save_worker = AutoSaveWorker()
        
        # 移动工作对象到线程
        self.auto_save_worker.moveToThread(self.auto_save_thread)
        
        # 连接信号槽
        self.auto_save_worker.save_requested.connect(self.auto_save_document)
        
        # 启动线程
        self.auto_save_thread.start()

    @Slot(str)
    def on_document_modified(self, text):
        """标记文档为已修改"""
        if self.last_saved_text is None:
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
                        logger.info(f"手动保存成功: {self.document.file_name}")
                        
                        # 发送保存成功信号（如果需要）
                        if hasattr(self.parent(), 'on_file_saved'):
                            self.parent().on_file_saved(self.document.file_id)
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
        if hasattr(self.parent(), 'create_new_file'):
            self.parent().create_new_file()

    def open_file(self):
        """打开文件（快捷键响应）"""
        if hasattr(self.parent(), 'open_file_dialog'):
            self.parent().open_file_dialog()

    def show_find_dialog(self):
        """显示查找对话框（快捷键响应）"""
        js_code = """
            if (window.editor && window.editor.codemirror) {
                window.editor.codemirror.execCommand('find');
            }
        """
        self.preview.page().runJavaScript(js_code)

    @Slot()
    def auto_save_document(self):
        """自动保存文档内容（修复光标重置问题）"""
        logger.info(f"Auto-save triggered: {self.document.file_id}, modified: {self.document_modified}")
        if self.document.file_id and self.document_modified:
            try:
                # 直接获取内容保存，不重新设置document
                js_code = """
                    if (window.editor) {
                        window.editor.getMarkdown();
                    } else {
                        '';
                    }
                """
                def handle_auto_save(content):
                    if content and content != self.last_saved_text:
                        # 直接保存到数据库，不触发编辑器重载
                        success = self.markdown_manager.save_markdown(
                            id=self.document.file_id, 
                            content=content
                        )
                        if success:
                            self.last_saved_text = content
                            self.document_modified = False
                            logger.info(f"Auto-saved document: {self.document.file_id}")
                        else:
                            logger.error("自动保存到数据库失败")
                    else:
                        # 内容未变化，直接重置标记
                        self.document_modified = False
                        
                self.preview.page().runJavaScript(js_code, handle_auto_save)
            except Exception as e:
                logger.error(f"Auto-save failed: {str(e)}")
                self.document_modified = True

    def get_markdown(self, callback):
        """获取markdown内容（保持光标位置）"""
        js_code = """
            if (window.editor) {
                window.editor.getMarkdown();
            } else {
                '';
            }
        """
        def handle_markdown_content(content):
            # 只更新跟踪变量，不设置document内容
            self.last_saved_text = content
            callback(content)
        self.preview.page().runJavaScript(js_code, handle_markdown_content)
        return self.document.get_text()

    def closeEvent(self, event):
        """窗口关闭时清理"""
        # 先清理快捷键
        if hasattr(self, 'shortcut_manager'):
            self.shortcut_manager.clear_all_global_shortcuts()
            
        # 清理自动保存线程
        cleanup_finished = threading.Event()
        
        def on_cleanup_finished():
            cleanup_finished.set()
        
        self.auto_save_worker.cleanup_requested.connect(on_cleanup_finished)
        self.auto_save_worker.cleanup_requested.emit()
        
        cleanup_finished.wait(timeout=5)
        
        self.auto_save_thread.quit()
        self.auto_save_thread.wait()
        super().closeEvent(event)

    def export_to_browser(self):
        """导出当前内容到浏览器"""
        self.get_html_content(lambda html_content: self.export_html_to_browser(html_content))
    
    def export_html_to_browser(self, html_content):
        """导出 HTML 内容到浏览器"""
        if html_content:
            temp_file = os.path.join(QStandardPaths.writableLocation(QStandardPaths.TempLocation), "export.html")
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.preview.setUrl(QUrl.fromLocalFile(temp_file))
    
    def get_html_content(self, callback):
        """获取当前 HTML 内容"""
        js_code = """
            if (window.editor) {
                return window.editor.getValue();
            } else {
                return '';
            }
        """
        def handle_html_content(content):
            callback(content)
        self.preview.page().runJavaScript(js_code, handle_html_content)

    def update_theme(self, theme):
        """Switch the Cherry Markdown theme."""
        js_code = f"""
            if (window.editor) {
                window.editor.setTheme('{theme}')
            }
        """
        self.preview.page().runJavaScript(js_code)
        
    def update_auto_save_settings(self):
        """更新自动保存设置"""
        if hasattr(self, 'auto_save_worker'):
            self.auto_save_worker.update_settings()

    def reset(self):
        self.document.file_id = ""
        self.document.file_name = ""
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

    def set_file_name(self, file_name):
        self.document.file_name = file_name

    def set_text_content(self, text_content):
        self.document.set_text(text_content)
        # 新增：同步初始内容到last_saved_text
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
    
    def on_page_loaded(self, ok):
        """页面加载完成后初始化编辑器事件监听"""
        if ok:
            # 设置编辑器内容变化监听
            js_code = """
                if (window.editor) {
                    // 监听内容变化事件
                    window.editor.on('change', function() {
                        // 将编辑器内容同步到Python端document对象
                        document.text = window.editor.getValue();
                    });
                }
            """
            self.preview.page().runJavaScript(js_code)

    def update_markdown_content(self, item):
        """更新 Markdown 内容"""
        try:
            content = self.markdown_manager.get_markdown_content(item['id'])
            self.document.set_text(content)
            self.last_saved_text = content
            self.document_modified = False
            logger.info(f"成功更新 Markdown 内容，ID: {item['id']}")
        except Exception as e:
            logger.error(f"更新 Markdown 内容失败: {str(e)}")

