import os
import itertools
from typing import List, Dict, Optional
from datetime import datetime

class APIKeyRotator:
    """API Key轮询管理器"""
    
    def __init__(self):
        self._api_keys: Optional[List[str]] = None
        self._key_iter = None
        self._key_stats: Dict = {}
    
    def _ensure_initialized(self):
        """确保已初始化"""
        if self._api_keys is None:
            self._api_keys = self._load_api_keys()
            self._key_iter = itertools.cycle(self._api_keys)
            self._key_stats = {key: {'usage': 0, 'failures': 0, 'last_used': None} 
                              for key in self._api_keys}
    
    def _load_api_keys(self) -> List[str]:
        """加载API Keys"""
        keys = []
        for i in range(1, 6):
            key = os.getenv(f'ZHIPU_API_KEY_{i}')
            if key:
                keys.append(key)
        
        if not keys:
            key = os.getenv('ZHIPU_API_KEY')
            if key:
                keys.append(key)
        
        if not keys:
            raise ValueError("未配置智谱API Key，请在.env文件中配置ZHIPU_API_KEY_1到ZHIPU_API_KEY_5")
        
        return keys
    
    @property
    def api_keys(self) -> List[str]:
        """获取API Keys列表"""
        self._ensure_initialized()
        return self._api_keys
    
    def get_next_key(self) -> str:
        """获取下一个API Key"""
        self._ensure_initialized()
        return next(self._key_iter)
    
    def record_usage(self, key: str, success: bool = True):
        """记录API Key使用情况"""
        self._ensure_initialized()
        if key in self._key_stats:
            self._key_stats[key]['usage'] += 1
            self._key_stats[key]['last_used'] = datetime.now()
            if not success:
                self._key_stats[key]['failures'] += 1
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        self._ensure_initialized()
        return self._key_stats
    
    def get_available_key(self) -> str:
        """获取可用的API Key（带故障转移）"""
        self._ensure_initialized()
        max_retries = len(self._api_keys)
        for _ in range(max_retries):
            key = self.get_next_key()
            stats = self._key_stats[key]
            total = stats['usage']
            if total > 0 and stats['failures'] / total > 0.5:
                continue
            return key
        
        return self._api_keys[0]

api_key_rotator = APIKeyRotator()
