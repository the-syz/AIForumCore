from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class PostBase(BaseModel):
    """经验贴基础模型"""
    title: str = Field(..., min_length=1, max_length=255, description="经验贴标题")
    content: str = Field(..., description="经验贴内容（Markdown格式）")
    category: str = Field(..., min_length=1, max_length=50, description="经验贴分类")

class PostCreate(PostBase):
    """经验贴创建模型"""
    is_draft: bool = Field(default=False, description="是否为草稿")

class PostUpdate(BaseModel):
    """经验贴更新模型"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    is_draft: Optional[bool] = None

class PostResponse(PostBase):
    """经验贴响应模型"""
    id: int
    author_id: int
    author_name: str
    created_at: datetime
    updated_at: datetime
    is_pinned: bool
    view_count: int
    like_count: int
    comment_count: int
    is_draft: bool = False
    attachments: List[str] = []
    
    class Config:
        from_attributes = True

class PostListResponse(BaseModel):
    """经验贴列表响应模型"""
    id: int
    title: str
    category: str
    author_name: str
    created_at: datetime
    updated_at: datetime
    is_pinned: bool
    view_count: int
    like_count: int
    comment_count: int
    
    class Config:
        from_attributes = True

class PostDraftResponse(BaseModel):
    """经验贴草稿响应模型"""
    id: int
    title: str
    content: str
    category: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PostPinRequest(BaseModel):
    """经验贴置顶请求模型"""
    is_pinned: bool = Field(..., description="是否置顶")
