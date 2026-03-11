from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.api.auth import get_current_user
from app.models.user import User
from app.models.ai import AIConversation, AIMessage
from app.schemas.ai import (
    ChatRequest, ChatResponse,
    ConversationCreate, ConversationResponse,
    MessageResponse, ConversationHistoryResponse,
    SearchKnowledgeBaseRequest, SearchKnowledgeBaseResponse
)
from app.services.rag import rag_service
from app.services.vector_db import vector_db
from app.services.knowledge_base import knowledge_base_service
from app.api.auth import get_current_admin
import uuid

router = APIRouter(tags=["AI"])

@router.get("/debug/stats")
async def get_debug_stats(current_user: User = Depends(get_current_user)):
    """获取知识库调试信息"""
    return {
        "vector_count": vector_db.index.ntotal if vector_db._index else 0,
        "knowledge_base_stats": knowledge_base_service.get_stats()
    }

@router.post("/debug/search")
async def debug_search(
    request: SearchKnowledgeBaseRequest,
    current_user: User = Depends(get_current_user)
):
    """调试知识库搜索"""
    results = rag_service.search_knowledge_base(request.query, request.top_k or 3)
    return {"query": request.query, "results": results}

@router.post("/sync/all")
async def sync_all_knowledge_base(current_user: User = Depends(get_current_admin)):
    """全量同步知识库（仅管理员）"""
    try:
        count = await knowledge_base_service.sync_all()
        return {"message": "同步完成", "count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"同步失败: {str(e)}"
        )

@router.post("/clear")
async def clear_knowledge_base(current_user: User = Depends(get_current_admin)):
    """清空知识库（仅管理员）"""
    try:
        vector_db.clear_all()
        return {"message": "已清空知识库"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"清空失败: {str(e)}"
        )

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """AI对话"""
    try:
        conversation = None
        
        if request.conversation_id:
            conversation = await AIConversation.get_or_none(
                id=request.conversation_id,
                user=current_user
            )
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="对话不存在"
                )
        else:
            topic = request.message[:50] + "..." if len(request.message) > 50 else request.message
            conversation = await AIConversation.create(
                user=current_user,
                topic=topic
            )
        
        history_messages = []
        if conversation:
            messages = await AIMessage.filter(conversation=conversation).order_by('created_at').limit(10)
            for msg in messages:
                history_messages.append({
                    'role': msg.role,
                    'content': msg.content
                })
        
        await AIMessage.create(
            conversation=conversation,
            role='user',
            content=request.message
        )
        
        result = rag_service.chat(request.message, history_messages, selected_contents=request.selected_contents)
        
        await AIMessage.create(
            conversation=conversation,
            role='assistant',
            content=result['answer']
        )
        
        conversation.topic = request.message[:50] + "..." if len(request.message) > 50 else request.message
        await conversation.save()
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI对话失败: {str(e)}"
        )

@router.post("/search", response_model=SearchKnowledgeBaseResponse)
async def search_knowledge_base(
    request: SearchKnowledgeBaseRequest,
    current_user: User = Depends(get_current_user)
):
    """知识库检索"""
    try:
        results = rag_service.search_knowledge_base(request.query, request.top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"知识库搜索失败: {str(e)}"
        )

@router.post("/chat/new", response_model=ConversationResponse)
async def new_conversation(
    request: Optional[ConversationCreate] = None,
    current_user: User = Depends(get_current_user)
):
    """新建对话"""
    try:
        topic = request.topic if request and request.topic else "新对话"
        conversation = await AIConversation.create(
            user=current_user,
            topic=topic
        )
        return conversation
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建对话失败: {str(e)}"
        )

@router.get("/history")
async def get_chat_history(
    conversation_id: Optional[int] = None,
    current_user: User = Depends(get_current_user)
):
    """获取对话历史"""
    try:
        if conversation_id:
            conversation = await AIConversation.get_or_none(
                id=conversation_id,
                user=current_user
            )
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="对话不存在"
                )
            
            messages = await AIMessage.filter(conversation=conversation).order_by('created_at')
            return {
                "conversation": conversation,
                "messages": messages
            }
        else:
            conversations = await AIConversation.filter(
                user=current_user
            ).order_by('-updated_at').limit(10)
            return {"conversations": conversations}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取对话历史失败: {str(e)}"
        )

@router.delete("/conversation/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user)
):
    """删除对话"""
    try:
        conversation = await AIConversation.get_or_none(
            id=conversation_id,
            user=current_user
        )
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="对话不存在"
            )
        
        await conversation.delete()
        return {"message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除对话失败: {str(e)}"
        )
