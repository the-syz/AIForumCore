#!/usr/bin/env python3
"""
测试同时解析多篇论文
"""
import os
import sys

# 添加backend目录到Python搜索路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.services.paper_parser import PaperParser

# 测试文件路径
test_files = [
    "tests/109-管壳式换热器研究与应用综述.pdf",  # 中文论文
    "tests/126-Physics-Informed Neural networks for heat transfer problems.pdf"  # 英文论文
]

# 创建解析器实例
parser = PaperParser()

print("测试同时解析多篇论文")
print("=" * 80)

for i, test_file in enumerate(test_files):
    if not os.path.exists(test_file):
        print(f"测试文件不存在: {test_file}")
        continue
    
    print(f"\n解析论文 {i+1}: {os.path.basename(test_file)}")
    print("-" * 80)
    
    # 解析论文
    print("正在解析...")
    metadata = parser.parse(test_file)
    
    # 打印解析结果
    print("\n解析结果:")
    print("=" * 60)
    print(f"标题: {metadata.get('title', '未提取')}")
    print(f"作者: {metadata.get('authors', '未提取')}")
    print(f"摘要: {metadata.get('abstract', '未提取')[:100]}..." if metadata.get('abstract') else "摘要: 未提取")
    print(f"关键词: {metadata.get('keywords', '未提取')}")
    print(f"DOI: {metadata.get('doi', '未提取')}")
    print(f"论文类型: {metadata.get('paper_type', '未提取')}")

print("\n测试完成！")
