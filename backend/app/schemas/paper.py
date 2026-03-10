from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PaperBase(BaseModel):
    """论文基础模型"""
    title: str = Field(..., min_length=1, max_length=255, description="论文标题")
    authors: Optional[str] = Field(None, max_length=255, description="作者")
    abstract: Optional[str] = Field(None, description="摘要")
    keywords: Optional[str] = Field(None, max_length=255, description="关键词")
    doi: Optional[str] = Field(None, max_length=100, description="DOI")
    paper_type: str = Field(default="journal", description="论文类型")
    category: Optional[str] = Field(None, max_length=50, description="分类")

class PaperCreate(PaperBase):
    """论文创建模型"""
    pass

class PaperUpdate(BaseModel):
    """论文更新模型"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    authors: Optional[str] = Field(None, max_length=255)
    abstract: Optional[str] = None
    keywords: Optional[str] = Field(None, max_length=255)
    doi: Optional[str] = Field(None, max_length=100)
    paper_type: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)

class PaperResponse(PaperBase):
    """论文响应模型"""
    id: int
    file_path: str
    uploader_id: int
    uploader_name: Optional[str] = None
    upload_time: datetime
    download_count: int
    favorite_count: int
    view_count: int
    like_count: int
    
    class Config:
        from_attributes = True

class PaperListResponse(BaseModel):
    """论文列表响应模型"""
    id: int
    title: str
    authors: Optional[str]
    upload_time: datetime
    download_count: int
    favorite_count: int
    
    class Config:
        from_attributes = True

class PaperSearchResponse(BaseModel):
    """论文搜索响应模型"""
    id: int
    title: str
    authors: Optional[str]
    abstract: Optional[str]
    upload_time: datetime
    
    class Config:
        from_attributes = True
