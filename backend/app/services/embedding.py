import os
import numpy as np
from typing import List, Union
from zhipuai import ZhipuAI
from app.services.api_key_manager import api_key_rotator

class EmbeddingService:
    """文本向量化服务"""
    
    def __init__(self):
        self.model = "embedding-3"
        self.dimension = 2048
    
    def get_embedding(self, text: str) -> np.ndarray:
        """获取单个文本的向量"""
        max_retries = 3
        for attempt in range(max_retries):
            api_key = api_key_rotator.get_next_key()
            try:
                client = ZhipuAI(api_key=api_key)
                response = client.embeddings.create(
                    model=self.model,
                    input=text
                )
                
                embedding = response.data[0].embedding
                api_key_rotator.record_usage(api_key, success=True)
                return np.array(embedding, dtype=np.float32)
                    
            except Exception as e:
                api_key_rotator.record_usage(api_key, success=False)
                if attempt == max_retries - 1:
                    raise e
                continue
        
        raise Exception("获取向量失败")
    
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """批量获取文本向量"""
        embeddings = []
        for text in texts:
            embedding = self.get_embedding(text)
            embeddings.append(embedding)
        return np.array(embeddings)

embedding_service = EmbeddingService()
