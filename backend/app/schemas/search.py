from pydantic import BaseModel
from typing import List, Optional, Generic, TypeVar, Any
from datetime import datetime

T = TypeVar('T')

class SearchResultItem(BaseModel):
    """搜索结果项"""
    id: int
    title: str
    type: str
    created_at: Optional[datetime] = None
    upload_time: Optional[datetime] = None
    author: Optional[str] = None
    description: Optional[str] = None

class SearchResult(BaseModel, Generic[T]):
    """搜索结果"""
    total: int
    page: int
    page_size: int
    items: List[T]

class PaperSearchItem(SearchResultItem):
    """论文搜索结果项"""
    type: str = "paper"
    authors: Optional[str] = None
    keywords: Optional[str] = None
    abstract: Optional[str] = None

class PostSearchItem(SearchResultItem):
    """经验贴搜索结果项"""
    type: str = "post"
    content: Optional[str] = None

class DownloadSearchItem(SearchResultItem):
    """下载中心搜索结果项"""
    type: str = "download"
    file_name: Optional[str] = None
    download_count: Optional[int] = None
