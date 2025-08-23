from sqlalchemy.orm import sessionmaker
from db.models import ExcalidrawBoard
from db.db_manager import SingletonEngine
from utils.logger_utils import logger  # 添加 logger 导入
from utils import time_utils

# 画板管理类
class ExcalidrawManager:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = SingletonEngine.get_db_path('data.db')
        else:
            self.db_path = db_path
        self.engine = SingletonEngine.get_instance(self.db_path)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def save_board(self, board_name, board_data, tags=None, board_type='', file_id=''):
        """保存画板"""
        with self.Session() as session:
            board = ExcalidrawBoard(
                board_name=board_name,
                board_data=board_data,
                tags=tags,
                board_type=board_type,
                file_id=file_id,
                created_at=time_utils.get_current_time(),
                updated_at=time_utils.get_current_time(),
                delete_at=None
            )
            session.add(board)
            session.commit()
            logger.info(f'已保存画板: {board.id}')
            return board.id
    
    def list_boards(self, name=None, tags=None, board_type=None):
        """列表画板"""
        with self.Session() as session:
            query = session.query(ExcalidrawBoard)
            if name:
                query = query.filter_by(board_name=name)
            if tags:
                query = query.filter(ExcalidrawBoard.tags.like(f'%{tags}%'))
            if board_type:
                query = query.filter_by(board_type=board_type)
            boards = query.all()
            return boards
    

    def get_board(self, board_name):
        """获取画板"""
        with self.Session() as session:
            board = session.query(ExcalidrawBoard).filter_by(board_name=board_name).first()
            if board:
                return board.board_data
            return None
    
    def delete_board(self, board_name):
        """删除画板"""
        with self.Session() as session:
            board = session.query(ExcalidrawBoard).filter_by(board_name=board_name).first()
            if board:
                session.delete(board)
                session.commit()
                logger.info(f'已删除画板: {board_name}')
                return True
            return False
    
    def update_board(self, board_name, board_data=None, tags=None, board_type=None):
        """更新画板"""
        with self.Session() as session:
            board = session.query(ExcalidrawBoard).filter_by(board_name=board_name).first()
            if board:
                if board_name:
                    board.board_name = board_name
                if board_data:
                    board.board_data = board_data
                if tags:
                    board.tags = tags
                if board_type:
                    board.board_type = board_type
                board.updated_at = time_utils.get_current_time()
                session.commit()
                logger.info(f'已更新画板: {board_name}')
                return True
            return False
    
    def get_board_by_file_id(self, file_id):
        """根据文件id获取画板"""
        with self.Session() as session:
            board = session.query(ExcalidrawBoard).filter_by(file_id=file_id).first()
            return board