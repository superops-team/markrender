import os
import shutil
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from .base import Base
from .db_manager import SingletonEngine
from datetime import datetime
import threading
from sqlalchemy import create_engine


class DBSchemaChecker:
    def __init__(self, db_path):
        self.db_path = db_path
        self.engine = SingletonEngine.get_instance(db_path)
        self.Session = sessionmaker(bind=self.engine)
        self.backup_dir = os.path.join(os.path.dirname(db_path), 'db_backups')

    def get_current_schema(self):
        """获取当前数据库的 Schema 信息"""
        inspector = inspect(self.engine)
        schema_info = {}
        for table_name in inspector.get_table_names():
            schema_info[table_name] = inspector.get_columns(table_name)
        return schema_info

    def get_expected_schema(self):
        """获取模型定义的期望 Schema 信息"""
        schema_info = {}
        for table in Base.metadata.tables.values():
            schema_info[table.name] = [{
                'name': column.name,
                'type': str(column.type),
                'nullable': column.nullable,
                'default': column.default
            } for column in table.columns]
        return schema_info

    def schema_changed(self):
        """检查数据库 Schema 是否发生变化"""
        current = self.get_current_schema()
        expected = self.get_expected_schema()
        return current != expected

    def backup_db(self):
        """备份当前数据库"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(
            self.backup_dir, f'db_backup_{timestamp}.db')
        shutil.copy2(self.db_path, backup_path)
        return backup_path

    def migrate_data(self, backup_path):
        """从备份数据库迁移数据到新数据库"""
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        # 创建备份数据库引擎和会话
        backup_engine = create_engine(f'sqlite:///{backup_path}')
        backup_session = sessionmaker(bind=backup_engine)()

        # 获取当前数据库会话
        current_session = self.Session()

        try:
            # 获取所有表名
            inspector = inspect(backup_engine)
            table_names = inspector.get_table_names()
            total_tables = len(table_names)

            for idx, table_name in enumerate(table_names, start=1):
                # 获取备份数据库中的数据
                backup_table = Base.metadata.tables.get(table_name)
                if backup_table:
                    rows = backup_session.execute(backup_table.select())

                    # 将数据插入到新数据库
                    for row in rows:
                        current_session.execute(
                            backup_table.insert().values(dict(row)))

                    # 显示迁移进度
                    progress = idx / total_tables * 100
                    self.show_upgrade_status(
                        f'正在迁移表 {table_name}，进度: {
                            progress:.1f}%')

            current_session.commit()
            self.show_upgrade_status('数据迁移完成')
        except Exception as e:
            current_session.rollback()
            self.show_upgrade_status(f'数据迁移失败: {e}')
        finally:
            backup_session.close()
            current_session.close()

    def show_upgrade_status(self, message=None):
        """显示数据库升级状态"""
        if message is None:
            message = '数据库升级中，请稍候...'
        print(message)

    def run_migration(self, backup_path):
        """执行数据迁移"""
        self.migrate_data(backup_path)
        self.show_upgrade_status('数据库升级完成')

    def run_check(self):
        """运行 Schema 检查，必要时执行备份和数据迁移"""
        if self.schema_changed():
            self.show_upgrade_status()
            backup_path = self.backup_db()
            # 移动老数据库到待迁移状态
            if os.path.exists(self.db_path):
                pending_migration_path = os.path.join(
                    self.backup_dir, f'pending_migration_{
                        os.path.basename(
                            self.db_path)}')
                # 关闭数据库连接
                self.engine.dispose()
                shutil.move(self.db_path, pending_migration_path)
            # 创建新数据库
            self.engine = SingletonEngine.get_instance(self.db_path)
            Base.metadata.create_all(self.engine)
            # 前台执行迁移，避免后台线程问题
            self.run_migration(backup_path)
