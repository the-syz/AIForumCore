#!/usr/bin/env python3
"""构建知识库脚本 - 增强版，支持PDF全文提取"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

import asyncio
from app.models.paper import Paper
from app.models.post import Post
from app.models.download import Download
from app.services.embedding import embedding_service
from app.services.vector_db import vector_db
from app.core.database import init_db, close_db
import pdfplumber
import PyPDF2

def extract_pdf_text(pdf_path: str) -> str:
    """从PDF中提取文本内容"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
    except Exception as e:
        print(f"pdfplumber提取失败，尝试PyPDF2: {e}")
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
        except Exception as e2:
            print(f"PyPDF2也失败: {e2}")
            text = ""
    return text[:10000]

async def build_paper_vectors():
    """构建论文向量"""
    papers = await Paper.all()
    print(f"发现 {len(papers)} 篇论文")
    
    count = 0
    for paper in papers:
        try:
            full_text = f"{paper.title}\n{paper.authors or ''}\n{paper.abstract or ''}\n{paper.keywords or ''}"
            
            if paper.file_path and os.path.exists(paper.file_path):
                print(f"  正在提取PDF内容: {paper.file_path}")
                pdf_text = extract_pdf_text(paper.file_path)
                if pdf_text:
                    full_text += "\n\n" + pdf_text
                    print(f"  PDF内容提取成功，长度: {len(pdf_text)}")
            
            embedding = embedding_service.get_embedding(full_text[:15000])
            
            vector_db.add_vectors(
                vectors=embedding.reshape(1, -1),
                metadata_list=[{
                    'type': 'paper',
                    'id': paper.id,
                    'title': paper.title,
                    'content': (paper.abstract or paper.title)[:1000]
                }]
            )
            
            count += 1
            print(f"✓ 已处理论文 {count}/{len(papers)}: {paper.title[:30]}...")
        except Exception as e:
            print(f"✗ 处理论文失败 {paper.title}: {e}")
    
    print(f"已构建 {count} 篇论文的向量")
    return count

async def build_post_vectors():
    """构建经验贴向量"""
    posts = await Post.filter(is_draft=False).all()
    print(f"发现 {len(posts)} 篇经验贴")
    
    count = 0
    for post in posts:
        try:
            text = f"{post.title}\n{post.content}"
            
            embedding = embedding_service.get_embedding(text)
            
            vector_db.add_vectors(
                vectors=embedding.reshape(1, -1),
                metadata_list=[{
                    'type': 'post',
                    'id': post.id,
                    'title': post.title,
                    'content': post.content[:1000]
                }]
            )
            
            count += 1
            print(f"✓ 已处理经验贴 {count}/{len(posts)}: {post.title[:30]}...")
        except Exception as e:
            print(f"✗ 处理经验贴失败 {post.title}: {e}")
    
    print(f"已构建 {count} 篇经验贴的向量")
    return count

async def build_download_vectors():
    """构建下载中心向量"""
    downloads = await Download.all()
    print(f"发现 {len(downloads)} 个下载资源")
    
    count = 0
    for download in downloads:
        try:
            text = f"{download.title}\n{download.description or ''}"
            
            embedding = embedding_service.get_embedding(text)
            
            vector_db.add_vectors(
                vectors=embedding.reshape(1, -1),
                metadata_list=[{
                    'type': 'download',
                    'id': download.id,
                    'title': download.title,
                    'content': download.description or download.title
                }]
            )
            
            count += 1
            print(f"✓ 已处理下载资源 {count}/{len(downloads)}: {download.title[:30]}...")
        except Exception as e:
            print(f"✗ 处理下载资源失败 {download.title}: {e}")
    
    print(f"已构建 {count} 个下载资源的向量")
    return count

async def main():
    print("=== 开始构建知识库 ===")
    print()
    
    await init_db()
    
    try:
        total_count = 0
        
        print("1. 构建论文向量...")
        paper_count = await build_paper_vectors()
        total_count += paper_count
        print()
        
        print("2. 构建经验贴向量...")
        post_count = await build_post_vectors()
        total_count += post_count
        print()
        
        print("3. 构建下载中心向量...")
        download_count = await build_download_vectors()
        total_count += download_count
        print()
        
        print("=== 知识库构建完成 ===")
        print(f"总计构建 {total_count} 条向量")
        print(f"  - 论文: {paper_count}")
        print(f"  - 经验贴: {post_count}")
        print(f"  - 下载资源: {download_count}")
        print(f"当前向量库总量: {vector_db.index.ntotal}")
        
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(main())
