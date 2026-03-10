
#!/usr/bin/env python3
"""
测试论文解析器的脚本
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.paper_parser import PaperParser

def test_paper_parser():
    """测试论文解析器"""
    print("=" * 60)
    print("开始测试论文解析器")
    print("=" * 60)
    
    parser = PaperParser()
    
    # 1. 测试获取客户端
    print("\n1. 测试获取智谱AI客户端...")
    client = parser.get_client()
    if client:
        print("✓ 成功获取智谱AI客户端")
    else:
        print("✗ 无法获取智谱AI客户端")
        return False
    
    # 2. 测试文本提取（用一个简单的测试文本）
    print("\n2. 测试AI解析功能...")
    test_text = """
    Deep Learning for Computer Vision: A Survey
    Authors: John Smith, Jane Doe, Bob Wilson
    Abstract: In this paper, we present a comprehensive survey of deep learning 
    techniques for computer vision applications. We review various convolutional 
    neural network architectures, including CNN, R-CNN, YOLO, and transformers.
    Keywords: deep learning, computer vision, CNN, transformers
    DOI: 10.1000/example123
    """
    
    print("测试文本:")
    print(test_text)
    
    try:
        metadata = parser.parse_with_ai(test_text)
        print("\nAI解析结果:")
        print(f"  标题: {metadata.get('title', 'N/A')}")
        print(f"  作者: {metadata.get('authors', 'N/A')}")
        print(f"  摘要: {metadata.get('abstract', 'N/A')[:100]}...")
        print(f"  关键词: {metadata.get('keywords', 'N/A')}")
        print(f"  DOI: {metadata.get('doi', 'N/A')}")
        print(f"  论文类型: {metadata.get('paper_type', 'N/A')}")
        
        if metadata.get('title'):
            print("✓ AI解析成功！")
            return True
        else:
            print("✗ AI解析失败，没有返回标题")
            return False
            
    except Exception as e:
        print(f"✗ AI解析发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_rule_based():
    """测试规则提取方法"""
    print("\n" + "=" * 60)
    print("测试规则提取方法")
    print("=" * 60)
    
    parser = PaperParser()
    
    test_text = """
    Deep Learning for Computer Vision: A Survey
    Authors: John Smith, Jane Doe, Bob Wilson
    Abstract: In this paper, we present a comprehensive survey of deep learning 
    techniques for computer vision applications. We review various convolutional 
    neural network architectures, including CNN, R-CNN, YOLO, and transformers.
    Keywords: deep learning, computer vision, CNN, transformers
    DOI: 10.1000/example123
    """
    
    print("\n测试规则提取:")
    title = parser.extract_title(test_text)
    print(f"  标题: {title}")
    
    authors = parser.extract_authors(test_text)
    print(f"  作者: {authors}")
    
    abstract = parser.extract_abstract(test_text)
    print(f"  摘要: {abstract[:100]}...")
    
    keywords = parser.extract_keywords(test_text)
    print(f"  关键词: {keywords}")
    
    doi = parser.extract_doi(test_text)
    print(f"  DOI: {doi}")
    
    return True

if __name__ == "__main__":
    print("论文解析器测试脚本\n")
    
    success1 = test_paper_parser()
    success2 = test_rule_based()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("✓ 所有测试通过！")
    else:
        print("✗ 部分测试失败，请检查上述错误信息")
    print("=" * 60)

