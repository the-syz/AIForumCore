#!/usr/bin/env python3
"""
测试论文解析服务
"""
import os
import sys

# 添加backend目录到Python搜索路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.services.paper_parser import PaperParser

# 测试文件路径
test_file = "tests/109-管壳式换热器研究与应用综述.pdf"

if not os.path.exists(test_file):
    print(f"测试文件不存在: {test_file}")
    sys.exit(1)

print(f"测试论文解析服务，文件: {test_file}")
print("=" * 80)

# 创建解析器实例
parser = PaperParser()

# 解析论文
print("正在解析论文...")
metadata = parser.parse(test_file)

# 打印解析结果
print("\n解析结果:")
print("=" * 80)
print(f"标题: {metadata.get('title', '未提取')}")
print(f"作者: {metadata.get('authors', '未提取')}")
print(f"摘要: {metadata.get('abstract', '未提取')}")
print(f"关键词: {metadata.get('keywords', '未提取')}")
print(f"DOI: {metadata.get('doi', '未提取')}")
print(f"论文类型: {metadata.get('paper_type', '未提取')}")

# 测试文本提取
print("\n文本提取测试:")
print("=" * 80)
text = parser.extract_text(test_file)
print(f"提取的文本长度: {len(text)} 字符")
print(f"前500字符: {text[:500]}...")

print("\n测试完成！")
