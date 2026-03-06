from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
from app.api.auth import get_current_user, get_current_admin
from app.models.user import User
from app.models.paper import Paper
from app.schemas.paper import PaperCreate, PaperResponse, PaperUpdate, PaperListResponse, PaperSearchResponse
from app.services.files import FileService
from app.services.paper_parser import PaperParser
import os

router = APIRouter(tags=["论文"])
file_service = FileService()
paper_parser = PaperParser()

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
    # 验证文件
    if not file_service.validate_file(file):
        raise HTTPException(status_code=400, detail="文件类型不支持或文件大小超过限制")
    
    # 保存文件
    file_path = file_service.save_file(file, "paper")
    
    # 解析论文
    metadata = paper_parser.parse(file_path)
    
    # 创建论文记录
    paper = await Paper.create(
        title=title or metadata.get('title', ''),
        authors=authors or metadata.get('authors', ''),
        abstract=abstract or metadata.get('abstract', ''),
        keywords=keywords or metadata.get('keywords', ''),
        doi=doi or metadata.get('doi', ''),
        paper_type=paper_type or metadata.get('paper_type', 'journal'),
        category=category,
        file_path=file_path,
        uploader_id=current_user.id
    )
    
    return paper

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
    return paper

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
