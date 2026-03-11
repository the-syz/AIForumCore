#!/usr/bin/env python3
"""测试完整RAG流程"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
from dotenv import load_dotenv
env_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / '.env'
load_dotenv(env_path)

print("=== 测试完整RAG流程 ===")
print()

print("1. 测试向量数据库...")
from app.services.vector_db import vector_db
print(f"   向量数据库维度: {vector_db.dimension}")
print(f"   当前向量数量: {vector_db.index.ntotal}")
print()

print("2. 测试向量化服务...")
from app.services.embedding import embedding_service
print(f"   模型: {embedding_service.model}")
print(f"   维度: {embedding_service.dimension}")
print()

print("3. 添加测试向量...")
import numpy as np
test_vector = embedding_service.get_embedding("这是一个测试文档，关于机器学习和深度学习的内容")
vector_db.add_vectors(
    vectors=test_vector.reshape(1, -1),
    metadata_list=[{
        'type': 'test',
        'id': 1,
        'title': '机器学习测试文档',
        'content': '这是一个测试文档，关于机器学习和深度学习的内容'
    }]
)
print(f"   添加后向量数量: {vector_db.index.ntotal}")
print()

print("4. 测试RAG服务...")
from app.services.rag import rag_service
try:
    result = rag_service.chat("什么是机器学习？")
    print(f"   RAG成功!")
    print(f"   回答: {result['answer'][:200]}...")
    print(f"   引用数: {len(result['references'])}")
except Exception as e:
    print(f"   RAG失败: {type(e).__name__}: {e}")
print()

print("=== 测试完成 ===")
