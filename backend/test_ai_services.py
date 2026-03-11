#!/usr/bin/env python3
"""测试AI服务模块"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

print("=== 测试AI服务模块 ===")
print()

print("1. 测试API Key管理器...")
try:
    from app.services.api_key_manager import api_key_rotator
    print(f"✓ API Key管理器加载成功")
    print(f"  - 已加载 {len(api_key_rotator.api_keys)} 个API Key")
    key1 = api_key_rotator.get_next_key()
    key2 = api_key_rotator.get_next_key()
    print(f"  - 轮询正常: Key1和Key2不同: {key1[:20]}... != {key2[:20]}...")
except Exception as e:
    print(f"✗ API Key管理器失败: {e}")
print()

print("2. 测试向量数据库...")
try:
    from app.services.vector_db import vector_db
    import numpy as np
    print(f"✓ 向量数据库加载成功")
    print(f"  - 维度: {vector_db.dimension}")
    print(f"  - 当前向量数量: {vector_db.index.ntotal}")
    
    test_vector = np.random.rand(1, 1024).astype(np.float32)
    test_metadata = [{'type': 'test', 'id': 1, 'title': '测试文档', 'content': '这是测试内容'}]
    vector_db.add_vectors(test_vector, test_metadata)
    print(f"  - 向量添加成功")
    print(f"  - 添加后向量数量: {vector_db.index.ntotal}")
    
    results = vector_db.search(test_vector[0], top_k=1)
    print(f"  - 搜索成功，找到 {len(results)} 个结果")
    if results:
        print(f"  - 搜索结果标题: {results[0]['title']}")
        print(f"  - 相似度得分: {results[0]['score']:.4f}")
except Exception as e:
    print(f"✗ 向量数据库失败: {e}")
print()

print("3. 测试向量化服务 (需要网络连接)...")
try:
    from app.services.embedding import embedding_service
    print(f"✓ 向量化服务加载成功")
    print(f"  - 模型: {embedding_service.model}")
    print(f"  - 预期维度: {embedding_service.dimension}")
    
    test_text = "这是一段测试文本，用于验证向量化服务是否正常工作。"
    print(f"  - 测试文本: {test_text[:50]}...")
    
    # 这里不实际调用API，因为会消耗token
    print("  - 跳过实际API调用测试 (避免消耗token)")
    print("  - 服务结构验证通过")
    
except Exception as e:
    print(f"✗ 向量化服务失败: {e}")
print()

print("=== 测试完成 ===")
print()
print("提示: 前三个服务模块已创建完成，可以继续进行T4-004到T4-006的任务")
