from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class CommentBase(BaseModel):
    """评论基础模型"""
    content: str = Field(..., min_length=1, description="评论内容")
    parent_id: Optional[int] = Field(None, description="父评论ID，用于回复")

class CommentCreate(CommentBase):
    """创建评论模型"""
    post_id: int = Field(..., description="帖子ID")

class CommentResponse(CommentBase):
    """评论响应模型"""
    id: int
    post_id: int
    user_id: int
    user_name: str
    created_at: datetime
    updated_at: datetime
    replies: List['CommentResponse'] = []
    
    class Config:
        from_attributes = True

# 更新前向引用
CommentResponse.model_rebuild()

class LikeCreate(BaseModel):
    """创建点赞模型"""
    target_type: str = Field(..., min_length=1, max_length=50, description="目标类型: paper, post, comment")
    target_id: int = Field(..., description="目标ID")

class FavoriteCreate(BaseModel):
    """创建收藏模型"""
    target_type: str = Field(..., min_length=1, max_length=50, description="目标类型: paper, post")
    target_id: int = Field(..., description="目标ID")

class FavoriteResponse(BaseModel):
    """收藏响应模型"""
    id: int
    target_type: str
    target_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
