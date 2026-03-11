from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    """对话请求模型"""
    message: str = Field(..., min_length=1, description="用户消息")
    conversation_id: Optional[int] = Field(None, description="对话ID，不传则创建新对话")
    selected_contents: Optional[List[dict]] = Field(None, description="选中的内容列表，用于限定搜索范围")

class ChatResponse(BaseModel):
    """对话响应模型"""
    answer: str = Field(..., description="AI回答")
    references: List[dict] = Field(default_factory=list, description="引用资料列表")

class ReferenceItem(BaseModel):
    """引用项模型"""
    type: str = Field(..., description="类型：paper/post/download")
    id: int = Field(..., description="ID")
    title: str = Field(..., description="标题")
    score: float = Field(..., description="相似度得分")

class ConversationCreate(BaseModel):
    """创建对话模型"""
    topic: Optional[str] = Field(None, max_length=255, description="对话主题")

class ConversationResponse(BaseModel):
    """对话响应模型"""
    id: int
    topic: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    """消息响应模型"""
    id: int
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationHistoryResponse(BaseModel):
    """对话历史响应模型"""
    conversation: ConversationResponse
    messages: List[MessageResponse]

class SearchKnowledgeBaseRequest(BaseModel):
    """知识库搜索请求模型"""
    query: str = Field(..., min_length=1, description="搜索查询")
    top_k: Optional[int] = Field(3, ge=1, le=10, description="返回结果数量")

class SearchKnowledgeBaseResponse(BaseModel):
    """知识库搜索响应模型"""
    results: List[ReferenceItem]
