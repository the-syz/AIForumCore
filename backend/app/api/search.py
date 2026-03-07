from fastapi import APIRouter, Query
from tortoise.queryset import Q
from typing import List, Optional
from app.models.paper import Paper
from app.models.post import Post
from app.models.download import Download
from app.schemas.search import SearchResult, PaperSearchItem, PostSearchItem, DownloadSearchItem

router = APIRouter(tags=["搜索"])

@router.get("/papers", response_model=SearchResult[PaperSearchItem])
async def search_papers(
    keyword: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量")
):
    """搜索论文"""
    search_query = f"%{keyword}%"
    
    # 构建查询条件
    query = Q(
        Q(title__icontains=keyword) |
        Q(authors__icontains=keyword) |
        Q(keywords__icontains=keyword) |
        Q(abstract__icontains=keyword) |
        Q(doi__icontains=keyword)
    )
    
    # 执行查询并排序
    papers = await Paper.filter(query).order_by(
        "-upload_time"
    ).offset((page-1)*page_size).limit(page_size).all()
    
    # 获取总数
    total = await Paper.filter(query).count()
    
    # 转换为搜索结果项
    items = [
        PaperSearchItem(
            id=paper.id,
            title=paper.title,
            authors=paper.authors,
            keywords=paper.keywords,
            abstract=paper.abstract,
            upload_time=paper.upload_time
        )
        for paper in papers
    ]
    
    return SearchResult(
        total=total,
        page=page,
        page_size=page_size,
        items=items
    )

@router.get("/posts", response_model=SearchResult[PostSearchItem])
async def search_posts(
    keyword: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量")
):
    """搜索经验贴"""
    # 构建查询条件
    query = Q(
        Q(title__icontains=keyword) |
        Q(content__icontains=keyword)
    )
    
    # 执行查询并排序
    posts = await Post.filter(query).order_by(
        "-created_at"
    ).offset((page-1)*page_size).limit(page_size).prefetch_related("author")
    
    # 获取总数
    total = await Post.filter(query).count()
    
    # 转换为搜索结果项
    items = [
        PostSearchItem(
            id=post.id,
            title=post.title,
            content=post.content[:200] + "..." if len(post.content) > 200 else post.content,
            created_at=post.created_at,
            author=post.author.name if post.author else None
        )
        for post in posts
    ]
    
    return SearchResult(
        total=total,
        page=page,
        page_size=page_size,
        items=items
    )

@router.get("/downloads", response_model=SearchResult[DownloadSearchItem])
async def search_downloads(
    keyword: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量")
):
    """搜索下载中心"""
    # 构建查询条件
    query = Q(
        Q(title__icontains=keyword) |
        Q(description__icontains=keyword) |
        Q(file_path__icontains=keyword)
    )
    
    # 执行查询并排序
    downloads = await Download.filter(query).order_by(
        "-upload_time"
    ).offset((page-1)*page_size).limit(page_size).all()
    
    # 获取总数
    total = await Download.filter(query).count()
    
    # 转换为搜索结果项
    items = [
        DownloadSearchItem(
            id=download.id,
            title=download.title,
            description=download.description,
            file_name=download.file_path.split("/")[-1] if download.file_path else "",
            download_count=download.download_count,
            upload_time=download.upload_time
        )
        for download in downloads
    ]
    
    return SearchResult(
        total=total,
        page=page,
        page_size=page_size,
        items=items
    )

@router.get("/all", response_model=SearchResult[dict])
async def search_all(
    keyword: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量")
):
    """综合搜索"""
    # 分别搜索不同类型的内容
    papers_query = Q(
        Q(title__icontains=keyword) |
        Q(authors__icontains=keyword) |
        Q(keywords__icontains=keyword) |
        Q(abstract__icontains=keyword) |
        Q(doi__icontains=keyword)
    )
    
    posts_query = Q(
        Q(title__icontains=keyword) |
        Q(content__icontains=keyword)
    )
    
    downloads_query = Q(
        Q(title__icontains=keyword) |
        Q(description__icontains=keyword) |
        Q(file_path__icontains=keyword)
    )
    
    # 执行查询
    papers = await Paper.filter(papers_query).limit(page_size).all()
    posts = await Post.filter(posts_query).limit(page_size).all()
    downloads = await Download.filter(downloads_query).limit(page_size).all()
    
    # 合并结果
    all_results = []
    
    # 添加论文结果
    for paper in papers:
        all_results.append({
            "id": paper.id,
            "title": paper.title,
            "type": "paper",
            "authors": paper.authors,
            "upload_time": paper.upload_time
        })
    
    # 添加经验贴结果
    for post in posts:
        await post.fetch_related("author")
        all_results.append({
            "id": post.id,
            "title": post.title,
            "type": "post",
            "author": post.author.name if post.author else None,
            "created_at": post.created_at
        })
    
    # 添加下载中心结果
    for download in downloads:
        all_results.append({
            "id": download.id,
            "title": download.title,
            "type": "download",
            "file_name": download.file_name,
            "download_count": download.download_count,
            "upload_time": download.upload_time
        })
    
    # 按时间排序
    all_results.sort(key=lambda x: x.get("upload_time", x.get("created_at")), reverse=True)
    
    # 分页
    start = (page-1) * page_size
    end = start + page_size
    paginated_results = all_results[start:end]
    
    return SearchResult(
        total=len(all_results),
        page=page,
        page_size=page_size,
        items=paginated_results
    )
