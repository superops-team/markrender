import json
import logging
from typing import Any, Dict, Union, Optional

logger = logging.getLogger(__name__)


class ExcalidrawDataHandler:
    """Excalidraw数据处理工具类"""
    
    @staticmethod
    def normalize_drawing_data(drawing_data: Union[str, Dict, Any]) -> str:
        """
        标准化Excalidraw绘图数据为JSON字符串
        
        Args:
            drawing_data: 原始绘图数据，可能是JSON字符串或字典对象
            
        Returns:
            str: 标准化的JSON字符串
            
        Raises:
            ValueError: 当数据格式无效时抛出
        """
        if not drawing_data:
            return ''
            
        try:
            # 如果drawing_data已经是字符串，验证其是否为有效的JSON
            if isinstance(drawing_data, str):
                if not drawing_data.strip():
                    return ''
                # 验证JSON格式并重新序列化以确保标准化
                parsed_data = json.loads(drawing_data)
                return json.dumps(parsed_data, ensure_ascii=False, separators=(',', ':'))
            else:
                # 如果是对象，直接序列化为JSON字符串
                return json.dumps(drawing_data, ensure_ascii=False, separators=(',', ':'))
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Excalidraw数据格式无效: {e}")
            raise ValueError(f"无效的Excalidraw数据格式: {str(e)}")
    
    @staticmethod
    def parse_drawing_data(drawing_data: Union[str, Dict, Any]) -> Dict:
        """
        解析Excalidraw绘图数据为字典对象
        
        Args:
            drawing_data: 原始绘图数据，可能是JSON字符串或字典对象
            
        Returns:
            Dict: 解析后的字典对象
            
        Raises:
            ValueError: 当数据格式无效时抛出
        """
        if not drawing_data:
            return {}
            
        try:
            # 如果drawing_data已经是字典对象，直接返回
            if isinstance(drawing_data, dict):
                return drawing_data
            # 如果是字符串，解析为字典对象
            elif isinstance(drawing_data, str):
                if not drawing_data.strip():
                    return {}
                parsed_data = json.loads(drawing_data)
                # 确保返回的是字典对象
                if isinstance(parsed_data, dict):
                    return parsed_data
                else:
                    return {"data": parsed_data}
            else:
                # 其他类型，尝试转换为字典
                return {"data": drawing_data}
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Excalidraw数据解析失败: {e}")
            raise ValueError(f"无法解析Excalidraw数据: {str(e)}")
    
    @staticmethod
    def get_elements_count(drawing_data: Union[str, Dict, Any]) -> int:
        """
        获取Excalidraw绘图中的元素数量
        
        Args:
            drawing_data: 绘图数据
            
        Returns:
            int: 元素数量
        """
        try:
            parsed_data = ExcalidrawDataHandler.parse_drawing_data(drawing_data)
            return len(parsed_data.get('elements', []))
        except Exception as e:
            logger.error(f"获取元素数量失败: {e}")
            return 0
    
    @staticmethod
    def validate_drawing_data(drawing_data: Union[str, Dict, Any]) -> bool:
        """
        验证Excalidraw绘图数据是否有效
        
        Args:
            drawing_data: 绘图数据
            
        Returns:
            bool: 数据是否有效
        """
        try:
            ExcalidrawDataHandler.parse_drawing_data(drawing_data)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def extract_metadata(drawing_data: Union[str, Dict, Any]) -> Dict:
        """
        从Excalidraw数据中提取元数据
        
        Args:
            drawing_data: 绘图数据
            
        Returns:
            Dict: 元数据字典
        """
        try:
            parsed_data = ExcalidrawDataHandler.parse_drawing_data(drawing_data)
            elements_count = len(parsed_data.get('elements', []))
            
            return {
                "elements_count": elements_count,
                "appState": parsed_data.get('appState', {}),
                "files": parsed_data.get('files', {}),
                "itemId": parsed_data.get('itemId', None)
            }
        except Exception as e:
            logger.error(f"提取元数据失败: {e}")
            return {}