import json  # 添加json导入
import time

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QObject, Signal, Property, QTimer, Slot
from app.editor.background import ThreadPoolManager, AutoSaveWorker, ContentLoader
from app.preference import AppStyle
from app.editor.channel import WebCommunicationManager
from app.editor.webengine import WebPageManager  # 导入页面管理器
from utils import logger
from utils import time_utils
from db.markrender_manager import MarkRenderManager
from db.settings_manager import SettingsManager

from app.editor.export_manager import ExportManager


class MarkRenderDoc(QObject):
    text_changed = Signal(str)  # 内容变更信号
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
            # 通知编辑器有内容变化
            if hasattr(self, 'parent') and self.parent and hasattr(self.parent(), 'on_document_modified'):
                self.parent().on_document_modified(text, source="user")

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


class MarkRenderEditor(QWidget):
    def __init__(self, parent=None, file_id="", file_name=""):
        super().__init__(parent)
        # 初始化线程池管理器
        self.thread_pool = ThreadPoolManager()
        # 连接线程池信号
        self.thread_pool.task_completed.connect(self.on_task_completed)
        self.thread_pool.task_failed.connect(self.on_task_failed)
        
        # 初始化页面管理器
        self.page_manager = WebPageManager()
        self.page_id = f"markrender_{file_id}"  # 使用固定页面ID
        
        # 初始化文档
        self.document = MarkRenderDoc(file_id, file_name)
        # 注册文档到通信管理器
        if file_id:
            self.web_comm.document_map[file_id] = self.document
            self.file_id = file_id
            
        # 初始化其他组件
        self.markrender_manager = MarkRenderManager()
        self.last_saved_text = None
        
        # 建立信号连接
        self.document.text_changed.connect(self.on_document_text_changed)
        
        # 设置UI
        self.setup_ui()
        
        # 自动保存相关初始化
        self.document_modified = False
        self.init_auto_save()
    
    def get_id(self):
        return f"{self.page_id}"

    def setup_ui(self):
        # 创建页面管理器实例
        self.page_manager = WebPageManager()
        
        # 创建通信管理器（每个页面一个实例）
        self.web_comm = WebCommunicationManager(self.get_id())
        # 然后再调用init_web_handlers()
        self.init_web_handlers()
        
        # 创建布局
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        self.setLayout(layout)

        # 预加载常用页面类型
        from app.editor.webengine import PageType
        logger.info("开始预加载常用页面类型...")
        
        # 预加载页面
        self.page_manager.preload_page_type(PageType.MARKDOWN, self.web_comm)
        self.page_manager.preload_page_type(PageType.LANDING, self.web_comm)
        self.page_manager.preload_page_type(PageType.EXCALIDRAW, self.web_comm)
        
        # 初始创建默认的Markdown页面作为主显示区域
        self.preview = self.page_manager.get_or_create_page(
            page_id=self.get_id(),
            page_type=PageType.MARKDOWN,
            backend_interface=self.web_comm
        )
        
        if not self.preview:
            logger.error("创建Editor页面失败")
            return
        
        # 将通信管理器附加到页面管理器
        self.web_comm.attach_to_page_manager(self.page_manager)
        
        # 加载HTML文件，并在加载完成后初始化WebChannel
        success = self.page_manager.load_page_content(self.get_id(), PageType.MARKDOWN)
        if not success:
            logger.error("加载HTML文件失败")
            
        # 将预览组件添加到布局
        layout.addWidget(self.preview)
        
        # 设置样式
        self.setStyleSheet(AppStyle().get_editor_parent() + AppStyle().get_editor_preview())
        
        # 连接页面管理器信号
        self.page_manager.page_loaded.connect(self._on_page_loaded)
        self.page_manager.page_switched.connect(self._on_page_switched)
        
        logger.info("编辑器UI初始化完成")

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
            self.document_modified = False  # 初始化时不算修改
            return
        
        # 程序更新不触发修改标记
        if source == "program":
            self.last_saved_text = text
            self.document_modified = False
            return
        
        # 用户修改时检查内容是否真的发生了变化（忽略空格等微小变化）
        if text.strip() != self.last_saved_text.strip():
            self.document_modified = True
            logger.debug(f"文档已修改，新内容长度: {len(text)}")
        else:
            self.document_modified = False
            logger.debug("文档内容未变化")
    
    def _on_page_loaded(self, page_id, success):
        """页面加载完成回调"""
        if success:
            logger.info(f"页面加载成功: {page_id}")
        else:
            logger.error(f"页面加载失败: {page_id}")
    
    def _on_page_switched(self, from_page_id, to_page_id):
        """页面切换回调 - 优化版本，避免布局重排，添加转场效果"""
        logger.info(f"页面切换: {from_page_id} -> {to_page_id}")
        
        # 检查是否是相同的页面实例（智能复用情况）
        if (to_page_id in self.page_manager.pages and 
            from_page_id in self.page_manager.pages and
            self.page_manager.pages[to_page_id] is self.page_manager.pages.get(from_page_id)):
            logger.debug(f"相同页面实例复用，无需重排布局: {to_page_id}")
            return
        
        # 更新显示的页面
        if to_page_id in self.page_manager.pages:
            new_view = self.page_manager.pages[to_page_id]
            
            # 检查是否已经是当前显示的页面
            layout = self.layout()
            current_widget = layout.itemAt(0).widget() if layout.count() > 0 else None
            
            if current_widget is new_view:
                logger.debug(f"页面已是当前显示，无需切换: {to_page_id}")
                self.preview = new_view
                return
            
            # 只有在不同页面实例时才进行布局更新
            logger.debug(f"执行页面实例切换: {to_page_id}")
            
            # 使用简单的透明度动画实现转场效果
            self._perform_smooth_page_switch(layout, current_widget, new_view)
            
            logger.debug(f"页面显示切换完成: {to_page_id}")
    
    def _perform_smooth_page_switch(self, layout, old_widget, new_widget):
        """执行平滑的页面切换动画"""
        from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QTimer
        from PySide6.QtWidgets import QGraphicsOpacityEffect
        
        try:
            # 预先设置新页面为透明状态
            new_effect = QGraphicsOpacityEffect()
            new_effect.setOpacity(0.0)
            new_widget.setGraphicsEffect(new_effect)
            
            # 移除旧页面
            if old_widget and old_widget is not new_widget:
                old_item = layout.takeAt(0)
                if old_item:
                    old_item.widget().setParent(None)
            
            # 添加新页面
            layout.addWidget(new_widget)
            self.preview = new_widget
            new_widget.show()
            
            # 创建淡入动画
            self.fade_animation = QPropertyAnimation(new_effect, b"opacity")
            self.fade_animation.setDuration(200)  # 200ms的快速淡入
            self.fade_animation.setStartValue(0.0)
            self.fade_animation.setEndValue(1.0)
            self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            # 动画完成后清理效果
            def cleanup_effect():
                new_widget.setGraphicsEffect(None)
            
            self.fade_animation.finished.connect(cleanup_effect)
            self.fade_animation.start()
            
        except Exception as e:
            logger.warning(f"页面切换动画失败，使用默认切换: {e}")
            # 回退到直接切换
            if old_widget and old_widget is not new_widget:
                old_item = layout.takeAt(0)
                if old_item:
                    old_item.widget().setParent(None)
            layout.addWidget(new_widget)
            self.preview = new_widget
            new_widget.show()

    def save_markrender_content(self, data):
        """线程安全的保存方法"""
        try:
            data = json.loads(data) if isinstance(data, str) else data
            content = data.get('content', '')
            if not self.document.file_id:
                return {"error": "无文件ID"}
            
            # 数据库操作通常是线程安全的
            success = self.markrender_manager.save_item(
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
                    success = self.markrender_manager.save_item(
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
            self.get_content(handle_save_content)
            return True
            
        except Exception as e:
            logger.error(f"保存文档失败: {str(e)}")
            return False

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

    def get_content(self, callback):
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
            'getContent',
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
    
    def _on_page_loaded(self, success):
        """页面加载完成回调"""
        if success:            
            # 设置页面加载状态
            self.page_loaded = True
            logger.debug("WebChannel初始化完成")
            
            # 延迟发送消息，确保JavaScript完全初始化
            # 使用QTimer延迟300ms后发送
            def send_delayed_messages():
                try:
                    # 通过channel注册web端事件
                    self.web_comm.send_message("registerEditorEvents", {})
                    # 通过channel设置内容变化监听
                    self.web_comm.send_message("setupContentChangeListener", {
                        "callback": "contentChanged"
                    })
                except Exception as e:
                    logger.error(f"发送延迟消息失败: {e}")
            
            from PySide6.QtCore import QTimer
            QTimer.singleShot(300, send_delayed_messages)
        else:
            logger.error("页面加载失败")
            self.page_loaded = False

    def update_content(self, item):
        """更新页面内容"""
        try:
            # 使用线程池提交内容加载任务
            loader = ContentLoader(item.file_id, self.markrender_manager)
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

    def closeEvent(self, event):
        # 1. 停止自动保存定时器
        if hasattr(self, 'auto_save_timer'):
            self.auto_save_timer.stop()
            logger.debug("Auto-save timer stopped")

        # 2. 快速检查是否真的需要保存
        need_save = self._check_if_save_needed()
        
        if need_save:
            logger.info(f"检测到需要保存文档: {self.document.file_id}")
            self._perform_save_and_close(event)
        else:
            logger.debug("无需保存，直接关闭")
            self._cleanup_and_close()
    
    def _check_if_save_needed(self):
        """快速检查是否需要保存"""
        # 基本条件检查
        if not (hasattr(self, 'web_comm') and self.web_comm):
            return False
        if not (hasattr(self, 'document') and self.document and self.document.file_id):
            return False
        if not (hasattr(self, 'page_loaded') and self.page_loaded):
            return False
        
        # 检查是否有修改需要保存
        if hasattr(self, 'document_modified') and not self.document_modified:
            logger.debug("文档未修改，跳过保存")
            return False
            
        return True
    
    def _perform_save_and_close(self, event):
        """执行保存并关闭流程"""
        # 设置较短的超时定时器（1.5秒后强制关闭）
        if not hasattr(self, '_close_timeout_timer'):
            self._close_timeout_timer = QTimer()
            self._close_timeout_timer.setSingleShot(True)
            self._close_timeout_timer.timeout.connect(self._force_close)
        
        self._close_timeout_timer.start(1500)  # 1.5秒超时，减少延迟
        
        def save_content(response):
            # 停止超时定时器
            if hasattr(self, '_close_timeout_timer'):
                self._close_timeout_timer.stop()
                
            # 快速处理保存响应
            try:
                content = response.get('content', '') if response else ''
                if content and self.document.file_id:
                    self.markrender_manager.save_item(id=self.document.file_id, content=content)
                    logger.debug(f"文档已保存: {self.document.file_id}")
            except Exception as e:
                logger.error(f"保存文档时出错: {e}")
            
            # 保存完成后立即关闭
            self._cleanup_and_close()
        
        # 尝试快速获取内容并保存
        try:
            success = self.web_comm.send_message("getContent", {}, callback=save_content)
            if not success:
                logger.warning("发送getContent消息失败，1.5秒后强制关闭")
                self._cleanup_and_close()
                return
        except Exception as e:
            logger.error(f"发送getContent消息时出错: {e}")
            # 发送失败，停止超时定时器并直接关闭
            if hasattr(self, '_close_timeout_timer'):
                self._close_timeout_timer.stop()
            self._cleanup_and_close()
    
    def _force_close(self):
        """强制关闭 - 超时时调用"""
        logger.warning("关闭超时（1.5秒），强制清理资源并关闭")
        self._cleanup_and_close()
    
    def _cleanup_and_close(self):
        """清理资源并通知关闭"""
        try:
            self._cleanup_resources()
        except Exception as e:
            logger.error(f"清理资源时出错: {e}")
        
        # 标记编辑器已经准备好关闭
        self._close_ready = True
        
        # 通知父窗口编辑器已经准备好关闭，但不直接关闭父窗口
        # 让主窗口控制整个关闭流程，避免组件分离
        if self.parent() and hasattr(self.parent(), '_on_editor_close_ready'):
            self.parent()._on_editor_close_ready()
        elif self.parent():
            # 如果父窗口没有_on_editor_close_ready方法，则标记为准备关闭
            # 但不触发关闭，由父窗口自己控制关闭时机
            logger.info("编辑器已准备关闭，等待主窗口统一关闭")
        else:
            # 如果没有父窗口，直接退出应用
            from PySide6.QtWidgets import QApplication
            QTimer.singleShot(0, QApplication.quit)
        
    def _cleanup_resources(self):
        # 3. 清理线程池资源
        if hasattr(self, 'thread_pool'):
            # 取消所有未完成任务
            self.thread_pool.cancel_all_tasks()
            # 等待当前任务完成（最多等待2秒）
            self.thread_pool.wait_for_completion(500)
            logger.info("Thread pool resources cleaned up")

        # 4. 释放Web通信资源
        if hasattr(self, 'web_comm'):
            self.web_comm.cleanup()

    def init_web_handlers(self):
        """初始化Web发起请求处理器 - 线程安全版本"""
        # Markdown编辑器相关 - 使用异步处理，但确保线程安全
        self.web_comm.register_python_handler('autoSave', self.handle_set_content, is_async=True)
        self.web_comm.register_python_handler('contentChanged', self.handle_content_changed, is_async=False)
        self.web_comm.register_python_handler('getContent', self.handle_get_content, is_async=False)
        self.web_comm.register_python_handler('setValue', self.handle_set_content, is_async=False)
        self.web_comm.register_python_handler('setCurrentFileId', self.handle_set_file_id, is_async=False)
        
        # WebChannel基本通信相关
        self.web_comm.register_python_handler('frontendReady', self.handle_frontend_ready, is_async=False)
        
        # Excalidraw白板相关
        self.web_comm.register_python_handler('save_excalidraw_board', self.save_excalidraw_board, is_async=True)
        self.web_comm.register_python_handler('load_excalidraw_board', self.load_excalidraw_board, is_async=False)
        self.web_comm.register_python_handler('export_excalidraw_board', self.export_excalidraw_board, is_async=True)
        self.web_comm.register_python_handler('get_excalidraw_data', self.get_excalidraw_data, is_async=False)
        self.web_comm.register_python_handler('excalidrawDataResponse', self.handle_excalidraw_data_response, is_async=False)
        
        # Board/Excalidraw页面消息路由
        self.web_comm.register_python_handler('setBoardId', self.handle_set_board_id, is_async=False)
        
        # 通用错误处理
        self.web_comm.register_python_handler('reportError', self.handle_frontend_error, is_async=False)
        
        logger.info(f"已注册多个WebChannel消息处理器")

    def export_file(self, format):
        """
        导出指定格式的文件
        :param format: 导出文件的格式，支持 'html', 'md', 'pdf', 'epub'
        """
        content = self.document.get_text()
        export_manager = ExportManager(self, content)
        export_manager.export_file(format)
    
    # ========================= Excalidraw白板相关方法 =========================
    
    def save_excalidraw_board(self, data):
        """保存Excalidraw白板数据"""
        try:
            board_id = data.get('boardId')
            drawing_data = data.get('drawingData')  # JSON字符串格式
            metadata = data.get('metadata', {})
            
            if not board_id:
                return {"success": False, "error": "缺少boardId"}
            
            # 验证drawing_data是否是有效的JSON
            if drawing_data:
                try:
                    if isinstance(drawing_data, str):
                        json.loads(drawing_data)  # 验证JSON格式
                    else:
                        drawing_data = json.dumps(drawing_data)  # 转换为JSON字符串
                except (json.JSONDecodeError, TypeError) as e:
                    logger.error(f"Excalidraw数据格式无效: {e}")
                    return {"success": False, "error": "数据格式无效"}
            
            success = self.markrender_manager.save_item(
                id=board_id,
                content=drawing_data or '',
                page_type='excalidraw'  # 使用excalidraw类型
            )
            
            if success:
                logger.info(f"Excalidraw白板数据保存成功: {board_id}, 元素数量: {metadata.get('elementsCount', 0)}")
                return {
                    "success": True, 
                    "board_id": board_id,
                    "metadata": metadata
                }
            else:
                return {"success": False, "error": "数据库保存失败"}
                
        except Exception as e:
            logger.error(f"Excalidraw保存失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def load_excalidraw_board(self, data):
        """加载Excalidraw白板数据"""
        try:
            board_id = data.get('boardId')
            
            if not board_id:
                return {"success": False, "error": "缺少boardId"}
            
            # 从数据库加载数据
            board_data = self.markrender_manager.get_detail(board_id)
            
            if board_data and board_data.get('content'):
                # 验证和解析Excalidraw数据
                try:
                    if isinstance(board_data['content'], str):
                        parsed_data = json.loads(board_data['content'])
                    else:
                        parsed_data = board_data['content']
                    
                    logger.info(f"Excalidraw白板数据加载成功: {board_id}, 元素数量: {len(parsed_data.get('elements', []))}")
                    return {
                        "success": True,
                        "data": {
                            "drawingData": parsed_data,
                            "metadata": {
                                "timestamp": board_data.get('updated_at', ''),
                                "content_type": 'excalidraw',
                                "elements_count": len(parsed_data.get('elements', []))
                            }
                        }
                    }
                except (json.JSONDecodeError, TypeError) as e:
                    logger.error(f"Excalidraw数据解析失败: {e}")
                    return {"success": False, "error": "数据格式错误"}
            else:
                logger.info(f"Excalidraw白板数据不存在: {board_id}")
                return {"success": True, "data": None}  # 返回成功但数据为空
                
        except Exception as e:
            logger.error(f"Excalidraw加载失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def export_excalidraw_board(self, data):
        """导出Excalidraw白板"""
        try:
            board_id = data.get('boardId')
            export_format = data.get('format', 'png')
            image_data = data.get('imageData')  # Base64编码的图片数据
            
            if not board_id:
                return {"success": False, "error": "缺少boardId"}
            
            # 这里可以实现具体的导出逻辑
            # 目前先记录导出请求，后续可以扩展为真正的文件导出
            logger.info(f"Excalidraw白板导出请求: {board_id} -> {export_format}")
            
            if image_data:
                # 可以在这里实现将图片保存到文件系统的逻辑
                logger.info(f"收到图片数据，大小: {len(image_data)} 字符")
            
            return {
                "success": True,
                "board_id": board_id,
                "format": export_format,
                "message": f"白板已导出为 {export_format.upper()} 格式"
            }
            
        except Exception as e:
            logger.error(f"Excalidraw导出失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_excalidraw_data(self, data):
        """获取当前Excalidraw数据（用于实时同步）"""
        try:
            board_id = data.get('boardId')
            
            if not board_id:
                return {"success": False, "error": "缺少boardId"}
            
            # 这个方法主要用于前端主动请求当前数据
            # 具体的数据将由前端的JavaScript回调提供
            logger.debug(f"请求获取Excalidraw数据: {board_id}")
            
            return {
                "success": True,
                "message": "数据请求已发送到前端"
            }
            
        except Exception as e:
            logger.error(f"获取Excalidraw数据失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def handle_set_board_id(self, data):
        """处理设置BoardId消息"""
        try:
            board_id = data.get('id', '')
            page_id = data.get('id', '')
            title = data.get('title', '')
            
            logger.info(f"处理setBoardId消息: boardId={board_id}, pageId={page_id}, title={title}")
            
            if not board_id:
                return {"success": False, "error": "缺少boardId"}
            
            # 返回成功响应，确认消息已被正确处理
            return {
                "success": True,
                "boardId": board_id,
                "pageId": page_id,
                "message": f"Board ID 设置成功: {board_id}"
            }
            
        except Exception as e:
            logger.error(f"处理setBoardId消息失败: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
    
    def handle_excalidraw_data_response(self, data):
        """处理前端返回的Excalidraw数据"""
        try:
            elements = data.get('elements', [])
            files = data.get('files', {})
            
            logger.debug(f"收到Excalidraw数据响应: {len(elements)}个元素, {len(files)}个文件")
            
            # 这里可以处理接收到的数据，比如用于自动保存
            # 目前先记录日志
            return {
                "success": True,
                "elements_count": len(elements),
                "files_count": len(files)
            }
            
        except Exception as e:
            logger.error(f"处理Excalidraw数据响应失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    # ========================= 通用方法 =========================
    
    def handle_content_changed(self, data):
        """处理内容变化事件"""
        try:
            content = data.get('content', '')
            source = data.get('source', 'user')
            
            if hasattr(self, 'document') and self.document:
                self.document.set_text(content)
                self.on_document_modified(content, source)
                
            return {"success": True}
        except Exception as e:
            logger.error(f"处理内容变化失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def handle_get_content(self, data):
        """获取Markdown内容"""
        try:
            if hasattr(self, 'document') and self.document:
                content = self.document.get_text()
                return {"success": True, "content": content}
            else:
                return {"success": False, "error": "文档未初始化"}
        except Exception as e:
            logger.error(f"获取Markdown内容失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def handle_set_content(self, data):
        """设置内容值"""
        try:
            content = data.get('content', '')
            if hasattr(self, 'document') and self.document:
                self.document.set_text(content)
                return {"success": True}
            else:
                return {"success": False, "error": "文档未初始化"}
        except Exception as e:
            logger.error(f"设置内容失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def handle_frontend_ready(self, data):
        """处理前端就绪消息"""
        try:
            page_type = data.get('pageType', 'unknown')
            timestamp = data.get('timestamp', '')
            logger.info(f"收到前端就绪消息: pageType={page_type}, timestamp={timestamp}")
            
            # 返回成功响应
            return {
                "success": True,
                "message": "Frontend ready acknowledged",
                "serverTime": time_utils.now().isoformat(),
                "pageType": page_type
            }
        except Exception as e:
            logger.error(f"处理前端就绪消息失败: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
    
    def handle_set_file_id(self, data):
        """设置文件ID"""
        try:
            file_id = data.get('fileId')
            if file_id and hasattr(self, 'document') and self.document:
                self.document.file_id = file_id
                return {"success": True, "file_id": file_id}
            else:
                return {"success": False, "error": "无效的文件ID"}
        except Exception as e:
            logger.error(f"设置文件ID失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def handle_frontend_error(self, data):
        """处理前端错误报告"""
        try:
            error_info = {
                'message': data.get('message', ''),
                'source': data.get('source', ''),
                'line': data.get('line', 0),
                'column': data.get('column', 0),
                'stack': data.get('stack', ''),
                'page_type': data.get('pageType', 'unknown')
            }
            
            logger.error(f"前端错误[{error_info['page_type']}]: {error_info['message']} at {error_info['source']}:{error_info['line']}")
            
            if error_info['stack']:
                logger.error(f"错误堆栈: {error_info['stack']}")
            
            return {"success": True, "logged": True}
        except Exception as e:
            logger.error(f"处理前端错误失败: {str(e)}")
            return {"success": False, "error": str(e)}
