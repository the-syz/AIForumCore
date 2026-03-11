from typing import Optional, Dict, Any, List
from app.models.paper import Paper
from app.models.post import Post
from app.models.download import Download
from app.services.embedding import embedding_service
from app.services.vector_db import vector_db
import pdfplumber
import PyPDF2
import os
import logging
import numpy as np

logger = logging.getLogger(__name__)

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
        logger.warning(f"pdfplumber提取失败，尝试PyPDF2: {e}")
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
        except Exception as e2:
            logger.warning(f"PyPDF2也失败: {e2}")
            text = ""
    return text[:10000]

class KnowledgeBaseService:
    """知识库管理服务"""
    
    @staticmethod
    async def add_paper(paper: Paper):
        """添加论文到知识库 - 仅使用数据库信息，不提取PDF全文"""
        try:
            full_text = f"{paper.title}\n{paper.authors or ''}\n{paper.abstract or ''}\n{paper.keywords or ''}"
            
            embedding = embedding_service.get_embedding(full_text[:5000])
            
            vector_db.add_vectors(
                vectors=embedding.reshape(1, -1),
                metadata_list=[{
                    'type': 'paper',
                    'id': paper.id,
                    'title': paper.title,
                    'content': (paper.abstract or paper.title)[:1000]
                }]
            )
            
            logger.info(f"✓ 论文已添加到知识库: {paper.title}")
        except Exception as e:
            logger.error(f"添加论文到知识库失败: {e}")
    
    @staticmethod
    async def add_post(post: Post):
        """添加经验贴到知识库"""
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
            
            logger.info(f"✓ 经验贴已添加到知识库: {post.title}")
        except Exception as e:
            logger.error(f"添加经验贴到知识库失败: {e}")
    
    @staticmethod
    async def add_download(download: Download):
        """添加下载资源到知识库"""
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
            
            logger.info(f"✓ 下载资源已添加到知识库: {download.title}")
        except Exception as e:
            logger.error(f"添加下载资源到知识库失败: {e}")
    
    @staticmethod
    async def sync_all():
        """全量同步知识库"""
        logger.info("=== 开始全量同步知识库 ===")
        
        vector_db.clear_all()
        
        all_metadata: List[Dict[str, Any]] = []
        all_vectors_list: List[np.ndarray] = []
        
        papers = await Paper.all()
        logger.info(f"发现 {len(papers)} 篇论文")
        for paper in papers:
            try:
                full_text = f"{paper.title}\n{paper.authors or ''}\n{paper.abstract or ''}\n{paper.keywords or ''}"
                
                embedding = embedding_service.get_embedding(full_text[:5000])
                all_vectors_list.append(embedding)
                all_metadata.append({
                    'type': 'paper',
                    'id': paper.id,
                    'title': paper.title,
                    'content': (paper.abstract or paper.title)[:1000]
                })
                logger.info(f"✓ 论文: {paper.title}")
            except Exception as e:
                logger.error(f"处理论文失败 {paper.title}: {e}")
        
        posts = await Post.filter(is_draft=False).all()
        logger.info(f"发现 {len(posts)} 篇经验贴")
        for post in posts:
            try:
                text = f"{post.title}\n{post.content}"
                embedding = embedding_service.get_embedding(text)
                all_vectors_list.append(embedding)
                all_metadata.append({
                    'type': 'post',
                    'id': post.id,
                    'title': post.title,
                    'content': post.content[:1000]
                })
                logger.info(f"✓ 经验贴: {post.title}")
            except Exception as e:
                logger.error(f"处理经验贴失败 {post.title}: {e}")
        
        downloads = await Download.all()
        logger.info(f"发现 {len(downloads)} 个下载资源")
        for download in downloads:
            try:
                text = f"{download.title}\n{download.description or ''}"
                embedding = embedding_service.get_embedding(text)
                all_vectors_list.append(embedding)
                all_metadata.append({
                    'type': 'download',
                    'id': download.id,
                    'title': download.title,
                    'content': download.description or download.title
                })
                logger.info(f"✓ 下载资源: {download.title}")
            except Exception as e:
                logger.error(f"处理下载资源失败 {download.title}: {e}")
        
        if all_vectors_list:
            all_vectors = np.array(all_vectors_list, dtype=np.float32)
            vector_db.add_vectors(all_vectors, all_metadata)
        
        logger.info(f"=== 全量同步完成，总计 {len(all_metadata)} 条向量 ===")
        return len(all_metadata)
    
    @staticmethod
    def get_stats() -> Dict[str, Any]:
        """获取知识库统计信息"""
        return {
            'total_vectors': vector_db.index.ntotal if vector_db._index else 0
        }
    
    @staticmethod
    async def delete_paper(paper_id: int):
        """从知识库删除论文"""
        try:
            vector_db.delete_by_type_and_id('paper', paper_id)
            logger.info(f"✓ 论文已从知识库删除: ID={paper_id}")
        except Exception as e:
            logger.error(f"从知识库删除论文失败: {e}")
    
    @staticmethod
    async def update_paper(paper: Paper):
        """更新论文在知识库中的信息"""
        try:
            await knowledge_base_service.delete_paper(paper.id)
            await knowledge_base_service.add_paper(paper)
            logger.info(f"✓ 论文已在知识库更新: {paper.title}")
        except Exception as e:
            logger.error(f"更新论文在知识库失败: {e}")
    
    @staticmethod
    async def delete_post(post_id: int):
        """从知识库删除经验贴"""
        try:
            vector_db.delete_by_type_and_id('post', post_id)
            logger.info(f"✓ 经验贴已从知识库删除: ID={post_id}")
        except Exception as e:
            logger.error(f"从知识库删除经验贴失败: {e}")
    
    @staticmethod
    async def update_post(post: Post):
        """更新经验贴在知识库中的信息"""
        try:
            await knowledge_base_service.delete_post(post.id)
            if not post.is_draft:
                await knowledge_base_service.add_post(post)
            logger.info(f"✓ 经验贴已在知识库更新: {post.title}")
        except Exception as e:
            logger.error(f"更新经验贴在知识库失败: {e}")
    
    @staticmethod
    async def delete_download(download_id: int):
        """从知识库删除下载资源"""
        try:
            vector_db.delete_by_type_and_id('download', download_id)
            logger.info(f"✓ 下载资源已从知识库删除: ID={download_id}")
        except Exception as e:
            logger.error(f"从知识库删除下载资源失败: {e}")
    
    @staticmethod
    async def update_download(download: Download):
        """更新下载资源在知识库中的信息"""
        try:
            await knowledge_base_service.delete_download(download.id)
            await knowledge_base_service.add_download(download)
            logger.info(f"✓ 下载资源已在知识库更新: {download.title}")
        except Exception as e:
            logger.error(f"更新下载资源在知识库失败: {e}")
    
    @staticmethod
    async def on_content_deleted():
        """内容删除后触发全量同步"""
        logger.info("检测到内容删除，触发全量同步...")
        try:
            await knowledge_base_service.sync_all()
        except Exception as e:
            logger.error(f"全量同步失败: {e}")

knowledge_base_service = KnowledgeBaseService()
