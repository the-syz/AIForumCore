#!/usr/bin/env python3
"""添加测试数据到向量库"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.').resolve().parent / '.env'
load_dotenv(env_path)

from app.services.vector_db import vector_db
from app.services.embedding import embedding_service
import numpy as np

print("=== 添加测试数据到向量库 ===\n")

test_data = [
    {
        'type': 'paper',
        'id': 999,
        'title': '深度学习在计算机视觉中的应用',
        'content': '本文主要研究深度学习在计算机视觉领域的应用，包括卷积神经网络CNN、图像识别、目标检测等技术。实验结果表明，深度学习方法在图像分类任务上取得了显著的成果。'
    },
    {
        'type': 'paper',
        'id': 998,
        'title': '基于Transformer的自然语言处理研究',
        'content': 'Transformer架构彻底改变了自然语言处理领域。本文介绍了注意力机制、自注意力、多头注意力等核心概念，并探讨了BERT、GPT等预训练模型的应用。'
    },
    {
        'type': 'post',
        'id': 999,
        'title': '如何写好一篇学术论文',
        'content': '写好一篇学术论文需要注意以下几点：1. 选题要新颖有价值；2. 实验设计要严谨；3. 结果分析要深入；4. 写作要清晰流畅。建议大家多读顶会论文，学习写作技巧。'
    },
    {
        'type': 'post',
        'id': 998,
        'title': '研究生入学经验分享',
        'content': '考研是一个漫长的过程，需要做好充分准备。建议从大三下学期开始复习，数学和英语是重点，专业课要多做真题。保持良好的心态也很重要。'
    },
    {
        'type': 'download',
        'id': 999,
        'title': 'LaTeX论文模板',
        'content': '本模板适用于大多数计算机学科的会议和期刊论文，包含完整的标题、摘要、关键词、正文、参考文献等结构。'
    }
]

print(f"准备添加 {len(test_data)} 条测试数据...\n")

count = 0
for item in test_data:
    try:
        print(f"正在处理: {item['type']} - {item['title']}")
        text = f"{item['title']}\n{item['content']}"
        embedding = embedding_service.get_embedding(text)
        
        vector_db.add_vectors(
            vectors=embedding.reshape(1, -1),
            metadata_list=[item]
        )
        count += 1
        print(f"  ✓ 添加成功\n")
    except Exception as e:
        print(f"  ✗ 添加失败: {e}\n")

print(f"=== 完成 ===")
print(f"成功添加 {count} 条测试数据")
print(f"当前向量库总量: {vector_db.index.ntotal}")
print("\n现在可以测试AI对话了！试试问：")
print("  - 深度学习在计算机视觉中有什么应用？")
print("  - 如何写好一篇学术论文？")
print("  - 有LaTeX模板吗？")
