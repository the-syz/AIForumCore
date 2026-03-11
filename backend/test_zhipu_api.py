#!/usr/bin/env python3
"""测试AI服务"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
from dotenv import load_dotenv
env_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / '.env'
load_dotenv(env_path)

print("=== 测试智谱AI API ===")
print()

print("1. 测试环境变量...")
api_key = os.getenv('ZHIPU_API_KEY_1')
print(f"   ZHIPU_API_KEY_1: {api_key[:20] if api_key else 'NOT FOUND'}...")
print()

print("2. 测试向量化API...")
try:
    from zhipuai import ZhipuAI
    client = ZhipuAI(api_key=api_key)
    response = client.embeddings.create(
        model="embedding-3",
        input="测试文本"
    )
    print(f"   向量化成功，维度: {len(response.data[0].embedding)}")
except Exception as e:
    print(f"   向量化失败: {e}")
print()

print("3. 测试对话API...")
try:
    from zhipuai import ZhipuAI
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[{"role": "user", "content": "你好"}]
    )
    print(f"   对话成功: {response.choices[0].message.content[:50]}...")
except Exception as e:
    print(f"   对话失败: {type(e).__name__}: {e}")
print()

print("=== 测试完成 ===")
