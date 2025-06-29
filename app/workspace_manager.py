# -*- coding: utf-8 -*-
import os
from PySide6.QtWidgets import QComboBox, QPushButton, QHBoxLayout
from db.markdown_manager import MarkdownManager
from utils.logger_utils import logger


class WorkspaceManager:
    def __init__(self, parent):
        self.parent = parent
        self.workspaces = {"default": ""}
        self.current_workspace = "default"
        self.init_workspace_dir()
        self.setup_workspace_ui()

    def init_workspace_dir(self):
        """初始化工作区目录"""
        from platform import system
        if system() == 'Windows':
            self.workspace_dir = os.path.join(
                os.getenv('APPDATA'), 'markrender')
        elif system() == 'Darwin':
            self.workspace_dir = os.path.join(os.path.expanduser(
                '~'), 'Library', 'Application Support', 'markrender')
        else:
            self.workspace_dir = os.path.join(
                os.path.expanduser('~'), '.local', 'share', 'markrender')
        os.makedirs(self.workspace_dir, exist_ok=True)
        self.db_path = os.path.join(self.workspace_dir, 'default.db')
        self.markdown_history_manager = MarkdownManager(self.db_path)
        logger.info(f'数据库路径初始化完成，路径为: {self.db_path}')

    def setup_workspace_ui(self):
        """设置工作区UI组件"""
        self.workspace_combobox = QComboBox()
        self.workspace_combobox.addItems(list(self.workspaces.keys()))
        self.workspace_combobox.currentTextChanged.connect(
            self.switch_workspace)

        self.add_workspace_button = QPushButton("新增工作区")
        self.add_workspace_button.clicked.connect(self.add_workspace)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.workspace_combobox)
        self.layout.addWidget(self.add_workspace_button)

    def switch_workspace(self, workspace_name):
        """切换工作区"""
        self.current_workspace = workspace_name
        self.db_path = os.path.join(self.workspace_dir, f'{workspace_name}.db')
        self.markdown_history_manager = MarkdownManager(self.db_path)
        logger.info(f'已切换到工作区: {workspace_name}')

    def add_workspace(self):
        """新增工作区"""
        workspace_count = len(self.workspaces)
        new_workspace_name = f'workspace_{workspace_count}'
        self.workspaces[new_workspace_name] = ""
        self.workspace_combobox.addItem(new_workspace_name)
        logger.info(f'已新增工作区: {new_workspace_name}')
