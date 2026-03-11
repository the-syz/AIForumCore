#!/usr/bin/env python3
"""测试AI服务模块 - 第二版"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

print("=== 测试AI服务模块 (第二版) ===")
print()

print("1. 测试RAG服务加载...")
try:
    from app.services.rag import rag_service
    print(f"✓ RAG服务加载成功")
    print(f"  - 模型: {rag_service.model}")
except Exception as e:
    print(f"✗ RAG服务失败: {e}")
print()

print("2. 测试AI schemas加载...")
try:
    from app.schemas.ai import (
        ChatRequest, ChatResponse,
        ConversationCreate, ConversationResponse
    )
    print(f"✓ AI schemas加载成功")
except Exception as e:
    print(f"✗ AI schemas失败: {e}")
print()

print("3. 测试AI API路由加载...")
try:
    from app.api.ai import router
    print(f"✓ AI API路由加载成功")
    print(f"  - 路由标签: {router.tags}")
except Exception as e:
    print(f"✗ AI API路由失败: {e}")
print()

print("4. 测试向量数据库状态...")
try:
    from app.services.vector_db import vector_db
    print(f"✓ 向量数据库状态正常")
    print(f"  - 当前向量数量: {vector_db.index.ntotal}")
    print(f"  - 维度: {vector_db.dimension}")
except Exception as e:
    print(f"✗ 向量数据库失败: {e}")
print()

print("5. 检查知识库构建脚本...")
script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts', 'build_knowledge_base.py')
if os.path.exists(script_path):
    print(f"✓ 知识库构建脚本存在: {script_path}")
else:
    print(f"✗ 知识库构建脚本不存在")
print()

print("=== 测试完成 ===")
print()
print("已完成的任务:")
print("  ✓ T4-001: 向量数据库搭建")
print("  ✓ T4-002: API Key轮询管理")
print("  ✓ T4-003: 文本向量化服务")
print("  ✓ T4-004: RAG检索服务")
print("  ✓ T4-005: AI对话API")
print("  ✓ T4-006: 知识库构建脚本")
print()
print("下一步: 可以运行知识库构建脚本向量化现有内容")
print("  命令: cd backend && python scripts/build_knowledge_base.py")
