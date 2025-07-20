import os
from utils import logger
from PySide6 import QtWidgets
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6 import QtWebEngineCore  # Add this import
from PySide6.QtCore import QUrl, QObject, Signal, Property, QThread, QTimer, Slot
from PySide6.QtWebChannel import QWebChannel
from ..app_style import AppStyle
from PySide6.QtWebEngineCore import QWebEnginePage
from db.settings_manager import SettingsManager
from db.markdown_manager import MarkdownManager


class MarkdownDocument(QObject):
    def __init__(self, file_id, file_name):
        super().__init__()
        self._file_id = file_id
        self.file_name = file_name
        self._text = ""
        self._lines = []  # 存储按行分割后的文本
        self._page_size = 500  # 每页行数
        self._loaded_lines = 0  # 已加载的行数

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
        # 仅在文件 ID 变化时才 reset，这里调用 set_text 时应先设置正确的 file_id
        self._text = text
        # 添加调试日志确认数据更新
        logger.debug(f"MarkdownDocument text updated, length: {len(text)}, first 20 chars: {text[:20]}")
        self.text_changed.emit(text)

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

    def __init__(self, parent=None):
        super().__init__(parent)
        self.general_settings = SettingsManager().get_settings_dict('general') # 通用设置
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_save_condition)
        self.init_timer()

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


class MarkdownEditor(QtWidgets.QWidget):
    def __init__(self, parent=None, file_id="", file_name=""):
        super().__init__(parent)
        # Initialize document for WebChannel
        self.document = MarkdownDocument(file_id, file_name)
        self.markdown_manager = MarkdownManager()
        
        # 添加上次保存内容跟踪
        self.last_saved_text = None
        
        # 假设 history_panel 是 HistoryPanel 实例
        if hasattr(self.parent, 'history_panel'):
            self.parent.history_panel.history_item_selected.connect(self.update_markdown_content)
        
        # Setup GUI
        self.setup_ui()
        
        # 自动保存相关初始化
        self.document_modified = False
        self.init_auto_save()

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
        # 修改：添加初始状态检查
        if self.last_saved_text is None:
            self.last_saved_text = text
            return
        
        # 比较新内容与上次保存内容
        if text != self.last_saved_text:
            self.document_modified = True
    
    def get_markdown(self):
        js_code = """
                if (window.editor) {
                    window.editor.getMarkdown();
                } else {
                    '';
                }
        """
        def handle_markdown_content(content):
            self.document.set_text(content)
        self.preview.page().runJavaScript(js_code, handle_markdown_content)
        return self.document.get_text()

    @Slot()
    def auto_save_document(self):
        """自动保存文档内容"""
        logger.info(f"Auto-save triggered: {self.document.file_id}, modified: {self.document_modified}")
        if self.document.file_id:
            try:
                 # 保存成功后更新上次保存内容
                self.last_saved_text = self.get_markdown()
                self.markdown_manager.save_markdown(id=self.document.file_id, content=self.last_saved_text)
                self.document_modified = False
                logger.info(f"Auto-saved document: {self.document.file_id}, last: {self.last_saved_text[-20:-1]}")
            except Exception as e:
                logger.error(f"Auto-save failed: {str(e)}")
                # 新增：保存失败时仍标记为已修改
                self.document_modified = True

    def closeEvent(self, event):
        """窗口关闭时清理线程"""
        self.auto_save_thread.quit()
        self.auto_save_thread.wait()
        super().closeEvent(event)

    def setup_ui(self):
        # Web view for Cherry Markdown
        self.preview = QWebEngineView()
        # 创建自定义的 Page 实例
        page = CustomWebEnginePage(self.preview)
        self.preview.setPage(page)
        
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
            QtWebEngineCore.QWebEngineSettings.PluginsEnabled, False)
        self.preview.page().settings().setAttribute(
            QtWebEngineCore.QWebEngineSettings.JavascriptCanOpenWindows, False)
        self.preview.page().settings().setAttribute(
            QtWebEngineCore.QWebEngineSettings.LocalStorageEnabled, True)

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

