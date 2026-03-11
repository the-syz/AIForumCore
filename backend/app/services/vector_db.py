import os
import pickle
import numpy as np
import faiss
from typing import List, Dict, Any, Optional

class VectorDatabase:
    def __init__(self, dimension: int = 2048, index_path: str = "data/vector_index"):
        self.dimension = dimension
        self.index_path = index_path
        self._index: Optional[faiss.Index] = None
        self._metadata: Dict = {}
    
    def _ensure_initialized(self):
        """确保已初始化"""
        if self._index is None:
            self._load_or_create_index()
    
    def _load_or_create_index(self):
        """加载或创建索引"""
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        
        index_file = f"{self.index_path}.faiss"
        metadata_file = f"{self.index_path}.pkl"
        
        if os.path.exists(index_file) and os.path.exists(metadata_file):
            try:
                self._index = faiss.read_index(index_file)
                with open(metadata_file, 'rb') as f:
                    self._metadata = pickle.load(f)
                if self._index.d != self.dimension:
                    print(f"警告: 索引维度({self._index.d})与配置维度({self.dimension})不匹配，将创建新索引")
                    self._index = faiss.IndexFlatIP(self.dimension)
                    self._metadata = {}
            except Exception as e:
                print(f"加载索引失败: {e}，将创建新索引")
                self._index = faiss.IndexFlatIP(self.dimension)
                self._metadata = {}
        else:
            self._index = faiss.IndexFlatIP(self.dimension)
            self._metadata = {}
    
    @property
    def index(self) -> faiss.Index:
        """获取索引"""
        self._ensure_initialized()
        return self._index
    
    @property
    def metadata(self) -> Dict:
        """获取元数据"""
        self._ensure_initialized()
        return self._metadata
    
    def add_vectors(self, vectors: np.ndarray, metadata_list: List[Dict[str, Any]]):
        """添加向量"""
        self._ensure_initialized()
        faiss.normalize_L2(vectors)
        
        start_id = self._index.ntotal
        self._index.add(vectors)
        
        for i, metadata in enumerate(metadata_list):
            self._metadata[start_id + i] = metadata
        
        self._save_index()
    
    def search(self, query_vector: np.ndarray, top_k: int = 3) -> List[Dict[str, Any]]:
        """搜索相似向量"""
        self._ensure_initialized()
        query_vector = query_vector.reshape(1, -1)
        faiss.normalize_L2(query_vector)
        
        scores, indices = self._index.search(query_vector, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and idx in self._metadata:
                result = self._metadata[idx].copy()
                result['score'] = float(score)
                results.append(result)
        
        return results
    
    def rebuild_from_metadata(self, all_metadata_list: List[Dict[str, Any]], all_vectors: np.ndarray):
        """从元数据和向量完全重建索引"""
        self._ensure_initialized()
        
        self._index = faiss.IndexFlatIP(self.dimension)
        self._metadata = {}
        
        if len(all_vectors) > 0:
            self.add_vectors(all_vectors, all_metadata_list)
    
    def clear_all(self):
        """清空所有向量"""
        self._ensure_initialized()
        
        self._index = faiss.IndexFlatIP(self.dimension)
        self._metadata = {}
        self._save_index()
        print("已清空向量库")
    
    def delete_by_type_and_id(self, content_type: str, content_id: int):
        """根据类型和ID删除向量"""
        self._ensure_initialized()
        
        if self._index.ntotal == 0:
            return
        
        ids_to_keep = []
        for idx, metadata in self._metadata.items():
            if not (metadata.get('type') == content_type and metadata.get('id') == content_id):
                ids_to_keep.append(idx)
        
        if len(ids_to_keep) == self._index.ntotal:
            return
        
        if len(ids_to_keep) == 0:
            self.clear_all()
            return
        
        all_vectors = self._index.reconstruct_n(0, self._index.ntotal)
        new_vectors = all_vectors[ids_to_keep]
        new_metadata = [self._metadata[idx] for idx in ids_to_keep]
        
        self._index = faiss.IndexFlatIP(self.dimension)
        self._metadata = {}
        self.add_vectors(new_vectors, new_metadata)
        print(f"已删除{content_type} #{content_id}的向量")
    
    def _save_index(self):
        """保存索引"""
        self._ensure_initialized()
        faiss.write_index(self._index, f"{self.index_path}.faiss")
        with open(f"{self.index_path}.pkl", 'wb') as f:
            pickle.dump(self._metadata, f)

vector_db = VectorDatabase()
