from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DownloadBase(BaseModel):
    """下载中心基础模型"""
    title: str = Field(..., min_length=1, max_length=255, description="资源标题")
    description: Optional[str] = Field(None, description="资源描述")
    category: str = Field(..., min_length=1, max_length=50, description="资源分类")

class DownloadCreate(DownloadBase):
    """创建下载资源模型"""
    pass

class DownloadUpdate(BaseModel):
    """更新下载资源模型"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="资源标题")
    description: Optional[str] = Field(None, description="资源描述")
    category: Optional[str] = Field(None, min_length=1, max_length=50, description="资源分类")

class DownloadResponse(DownloadBase):
    """下载资源响应模型"""
    id: int
    file_path: str
    upload_time: datetime
    download_count: int
    uploader_id: int
    
    class Config:
        from_attributes = True
