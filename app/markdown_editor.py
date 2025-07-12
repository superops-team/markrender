from PySide6.QtGui import QKeySequence
from PySide6.QtCore import Qt
from PySide6 import QtWidgets
from utils.hash_utils import calculate_md5
from utils.logger_utils import logger


class MarkdownEditor(MTextEdit):
    def __init__(self, markdown_manager, parent=None):
        super().__init__(parent)
        self.initial_md5 = calculate_md5(self.toPlainText())
        self.setup_editor()
        logger.info("准备调用 setup_shortcuts 方法")
        self.setup_shortcuts()
        logger.info("setup_shortcuts 方法调用完成")
        self.parent = parent
        self.markdown_manager = markdown_manager

    def setup_editor(self):
        """配置编辑器基本属性"""
        self.setAcceptRichText(True)
        self.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)

        # 设置默认字体大小为 pt
        font = self.font()
        font.setPointSize(20)
        self.setFont(font)

    def setup_shortcuts(self):
        """设置保存快捷键"""
        from platform import system
        if system() == 'Darwin':  # macOS
            save_shortcut = QKeySequence(Qt.META | Qt.Key_S)
            # 显式禁用 Ctrl + S
            disable_shortcut = QKeySequence(Qt.CTRL | Qt.Key_S)
            self.save_action = self.addAction("Save")
            self.save_action.setShortcut(save_shortcut)
            # 设置禁用的快捷键为空操作
            dummy_action = self.addAction("")
            dummy_action.setShortcut(disable_shortcut)
            logger.info(f"macos保存快捷键已设置: {save_shortcut.toString()}")

        else:  # Windows 和 Linux
            save_shortcut = QKeySequence(Qt.CTRL | Qt.Key_S)
            self.save_action = self.addAction("Save")
            self.save_action.setShortcut(save_shortcut)
        self.save_action.triggered.connect(self.save_content)

    def save_content(self):
        """保存内容并更新初始MD5值，同时保存历史记录"""
        logger.info("触发保存操作，开始检查文件修改状态...")
        if not self.parent:
            logger.error("父对象未初始化，保存失败")
            MMessage.error('保存失败，父对象未初始化', parent=self, duration=1)
            return
        if not hasattr(self.parent, 'current_file'):
            logger.error("父对象缺少 current_file 属性，保存失败")
            MMessage.error('保存失败，检查初始化是否完成', parent=self, duration=1)
            return
        if not self.parent.current_file:
            logger.error("current_file 为空，保存失败")
            MMessage.error('保存失败，检查初始化是否完成', parent=self, duration=1)
            return
        old_content = self.toPlainText()
        logger.info("开始执行保存操作...")
        try:
            self.update_initial_md5()
            title = self.parent.current_file.get('title', '')
            logger.info(
                f"准备保存文件，标题: {title}, ID: {
                    self.parent.current_file.get(
                        'id', None)}")
            self.markdown_manager.save_markdown(
                title, self.toPlainText(), tags=self.parent.current_file.get(
                    'tags', None), render_style=self.parent.current_file.get(
                    'render_style', None), id=self.parent.current_file.get(
                    'id', None), file_path=self.parent.current_file.get(
                    'file_path', None), theme_id=self.parent.current_file.get(
                    'theme_id', None), converter=self.parent.current_file.get(
                    'converter', None), converter_start=self.parent.current_file.get(
                    'converter_start', None), converter_end=self.parent.current_file.get(
                    'converter_end', None), status=self.parent.current_file.get(
                    'status', None),)
            file_id = self.parent.current_file.get('id', None)
            self.markdown_manager.save_change_history(
                file_id, old_content, self.toPlainText())
            logger.info("保存操作执行成功")
            MMessage.success('文件已成功保存', self, duration=1, closable=True)
            # 新增更新历史列表的调用
            if self.parent and hasattr(self.parent, 'update_history_list'):
                self.parent.update_history_list()
        except Exception as e:
            logger.error(f"保存操作失败: {str(e)}", exc_info=True)
            MMessage.error(f'文件保存失败: {str(e)}', parent=self, duration=1)

    def mark_file_modified(self):
        """通过MD5值比较判断文件是否修改"""
        current_md5 = calculate_md5(self.toPlainText())
        return current_md5 != self.initial_md5

    def update_initial_md5(self):
        """更新初始MD5值"""
        self.initial_md5 = calculate_md5(self.toPlainText())

    def get_text_content(self):
        """获取编辑器内容"""
        return self.toPlainText()

    def set_text_content(self, content):
        """设置编辑器内容"""
        self.setPlainText(content)
        self.update_initial_md5()
