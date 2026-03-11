from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
from app.api.auth import get_current_user, get_current_admin
from app.models.user import User
from app.models.paper import Paper
from app.schemas.paper import PaperCreate, PaperResponse, PaperUpdate, PaperListResponse, PaperSearchResponse
from app.services.files import FileService
from app.services.paper_parser import PaperParser
from app.services.knowledge_base import knowledge_base_service
import os
import difflib

router = APIRouter(tags=["论文"])
file_service = FileService()
paper_parser = PaperParser()

async def check_duplicate_paper(title: str, authors: str, doi: str) -> Optional[Paper]:
    """检查是否存在重复论文
    
    检查逻辑：
    1. 优先比对DOI号
    2. 然后比对标题相似度（90%以上）
    3. 最后比对作者相似度（70%以上）
    
    Args:
        title: 论文标题
        authors: 论文作者
        doi: 论文DOI号
    
    Returns:
        重复的论文对象，如果没有重复则返回None
    """
    # 1. 优先检查DOI号
    if doi:
        duplicate = await Paper.filter(doi=doi).first()
        if duplicate:
            return duplicate
    
    # 2. 检查标题和作者相似度
    all_papers = await Paper.all()
    for paper in all_papers:
        # 计算标题相似度
        title_similarity = difflib.SequenceMatcher(None, title.lower(), paper.title.lower()).ratio()
        
        # 如果标题相似度达到90%以上
        if title_similarity >= 0.9:
            # 计算作者相似度
            author_similarity = difflib.SequenceMatcher(None, authors.lower(), paper.authors.lower()).ratio()
            
            # 如果作者相似度达到70%以上
            if author_similarity >= 0.7:
                return paper
    
    return None

@router.post("/", response_model=PaperResponse, status_code=status.HTTP_201_CREATED)
async def upload_paper(
    file: UploadFile = File(...),
    title: str = Form(...),
    authors: Optional[str] = Form(None),
    abstract: Optional[str] = Form(None),
    keywords: Optional[str] = Form(None),
    doi: Optional[str] = Form(None),
    paper_type: str = Form(default="journal"),
    category: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    """上传论文"""
    try:
        # 确保Tortoise ORM上下文是激活的
        from tortoise import Tortoise
        from app.core.database import TORTOISE_ORM
        
        # 检查Tortoise是否已经初始化
        if not Tortoise._inited:
            await Tortoise.init(config=TORTOISE_ORM)
            print("Tortoise ORM 初始化成功")
        
        # 验证文件
        if not file_service.validate_file(file):
            raise HTTPException(
                status_code=400, 
                detail={"message": "文件类型不支持或文件大小超过限制", "type": "file_validation"}
            )
        
        # 保存文件
        file_result = file_service.save_file(file, "paper")
        file_path = file_result["path"]
        print(f"文件保存成功: {file_path}")
        
        # 解析论文（如果失败，使用默认值）
        metadata = {}
        try:
            metadata = paper_parser.parse(file_path)
            print(f"论文解析结果: {metadata}")
        except Exception as e:
            print(f"论文解析失败，使用默认值: {str(e)}")
        
        # 确定最终使用的论文信息
        final_title = metadata.get('title', '') or title or '未命名论文'
        final_authors = metadata.get('authors', '') or authors or ''
        final_doi = metadata.get('doi', '') or doi or ''
        
        # 检查是否存在重复论文
        duplicate_paper = await check_duplicate_paper(final_title, final_authors, final_doi)
        if duplicate_paper:
            # 删除已保存的文件
            file_service.delete_file(file_path)
            raise HTTPException(
                status_code=400, 
                detail={
                    "message": f"论文已存在，重复论文ID: {duplicate_paper.id}", 
                    "type": "duplicate",
                    "duplicate_id": duplicate_paper.id
                }
            )
        
        # 创建论文记录
        paper = await Paper.create(
            title=final_title,
            authors=final_authors,
            abstract=abstract or metadata.get('abstract', ''),
            keywords=keywords or metadata.get('keywords', ''),
            doi=final_doi,
            paper_type=paper_type or metadata.get('paper_type', 'journal'),
            category=category,
            file_path=file_path,
            uploader_id=current_user.id
        )
        print(f"论文创建成功: {paper.id}")
        
        # 异步添加到知识库（不阻塞主流程）
        import asyncio
        try:
            asyncio.create_task(knowledge_base_service.add_paper(paper))
            print(f"论文已添加到知识库队列: {paper.id}")
        except Exception as kb_error:
            print(f"添加论文到知识库失败: {kb_error}")
        
        # 构建响应数据，确保包含完整的解析信息
        paper_data = {
            'id': paper.id,
            'title': final_title,
            'authors': final_authors,
            'abstract': abstract or metadata.get('abstract', ''),
            'keywords': keywords or metadata.get('keywords', ''),
            'doi': final_doi,
            'paper_type': paper_type or metadata.get('paper_type', 'journal'),
            'category': category,
            'file_path': file_path,
            'uploader_id': paper.uploader_id,
            'uploader_name': current_user.name,
            'upload_time': paper.upload_time,
            'download_count': paper.download_count,
            'favorite_count': paper.favorite_count,
            'view_count': paper.view_count,
            'like_count': paper.like_count
        }
        
        print(f"返回给前端的完整数据: {paper_data}")
        return paper_data
    except HTTPException:
        raise
    except Exception as e:
        print(f"上传论文失败，错误: {str(e)}")
        import traceback
        traceback.print_exc()
        # 区分不同类型的错误，返回更详细的错误信息
        error_message = f"上传论文失败: {str(e)}"
        error_type = "unknown"
        
        # 检查错误类型
        if "重复" in str(e):
            error_type = "duplicate"
        elif "文件类型" in str(e):
            error_type = "file_type"
        elif "文件大小" in str(e):
            error_type = "file_size"
        elif "数据库" in str(e):
            error_type = "database"
        elif "解析" in str(e):
            error_type = "parse"
        
        raise HTTPException(
            status_code=500, 
            detail={"message": error_message, "type": error_type}
        )

@router.get("/", response_model=List[PaperListResponse])
async def list_papers(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """获取论文列表"""
    query = Paper.all()
    
    if category:
        query = query.filter(category=category)
    
    papers = await query.offset(skip).limit(limit).order_by('-upload_time')
    return papers

@router.get("/{paper_id}", response_model=PaperResponse)
async def get_paper(
    paper_id: int,
    current_user: User = Depends(get_current_user)
):
    """获取论文详情"""
    paper = await Paper.get_or_none(id=paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    
    # 获取上传者信息
    uploader_name = None
    if paper.uploader_id:
        from app.models.user import User
        uploader = await User.get_or_none(id=paper.uploader_id)
        if uploader:
            uploader_name = uploader.name
    
    # 构建响应数据
    paper_data = {
        'id': paper.id,
        'title': paper.title,
        'authors': paper.authors,
        'abstract': paper.abstract,
        'keywords': paper.keywords,
        'doi': paper.doi,
        'paper_type': paper.paper_type,
        'category': paper.category,
        'file_path': paper.file_path,
        'uploader_id': paper.uploader_id,
        'uploader_name': uploader_name,
        'upload_time': paper.upload_time,
        'download_count': paper.download_count,
        'favorite_count': paper.favorite_count,
        'view_count': paper.view_count,
        'like_count': paper.like_count
    }
    
    return paper_data

@router.put("/{paper_id}", response_model=PaperResponse)
async def update_paper(
    paper_id: int,
    paper_data: PaperUpdate,
    current_user: User = Depends(get_current_user)
):
    """更新论文信息"""
    paper = await Paper.get_or_none(id=paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    
    # 只有上传者或管理员可以修改
    if paper.uploader_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 更新论文信息
    for field, value in paper_data.model_dump(exclude_unset=True).items():
        setattr(paper, field, value)
    await paper.save()
    
    # 异步更新知识库
    import asyncio
    try:
        asyncio.create_task(knowledge_base_service.update_paper(paper))
        print(f"论文已更新到知识库队列: {paper.id}")
    except Exception as kb_error:
        print(f"更新论文到知识库失败: {kb_error}")
    
    return paper

@router.delete("/{paper_id}")
async def delete_paper(
    paper_id: int,
    current_user: User = Depends(get_current_user)
):
    """删除论文"""
    paper = await Paper.get_or_none(id=paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    
    # 只有上传者或管理员可以删除
    if paper.uploader_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 删除文件
    file_service.delete_file(paper.file_path)
    
    # 异步从知识库删除
    import asyncio
    try:
        asyncio.create_task(knowledge_base_service.delete_paper(paper.id))
        print(f"论文已从知识库删除队列: {paper.id}")
    except Exception as kb_error:
        print(f"从知识库删除论文失败: {kb_error}")
    
    # 删除论文记录
    await paper.delete()
    
    return {"message": "论文删除成功"}

@router.get("/{paper_id}/download")
async def download_paper(
    paper_id: int,
    current_user: User = Depends(get_current_user)
):
    """下载论文"""
    paper = await Paper.get_or_none(id=paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    
    # 检查文件是否存在
    if not os.path.exists(paper.file_path):
        raise HTTPException(status_code=404, detail="论文文件不存在")
    
    # 增加下载次数
    paper.download_count += 1
    await paper.save()
    
    # 返回文件
    from fastapi.responses import FileResponse
    return FileResponse(paper.file_path, media_type='application/pdf')

@router.get("/search", response_model=List[PaperSearchResponse])
async def search_papers(
    keyword: str,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """搜索论文"""
    search_query = f"%{keyword}%"
    papers = await Paper.filter(
        (Paper.title.like(search_query)) |
        (Paper.authors.like(search_query)) |
        (Paper.abstract.like(search_query)) |
        (Paper.keywords.like(search_query)) |
        (Paper.doi.like(search_query))
    ).offset(skip).limit(limit).order_by('-upload_time')
    return papers

@router.post("/parse")
async def parse_paper(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """解析论文"""
    try:
        # 验证文件
        if not file_service.validate_file(file):
            raise HTTPException(
                status_code=400, 
                detail={"message": "文件类型不支持或文件大小超过限制", "type": "file_validation"}
            )
        
        # 保存临时文件
        file_result = file_service.save_file(file, "temp")
        file_path = file_result["path"]
        
        # 解析论文
        metadata = paper_parser.parse(file_path)
        
        # 删除临时文件
        file_service.delete_file(file_path)
        
        # 返回解析结果
        return metadata
    except Exception as e:
        print(f"解析论文失败，错误: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail={"message": f"解析论文失败: {str(e)}", "type": "parse"}
        )
