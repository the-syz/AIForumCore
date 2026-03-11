from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
from app.api.auth import get_current_user, get_current_admin
from app.models.user import User
from app.models.post import Post
from app.schemas.post import PostCreate, PostResponse, PostUpdate, PostListResponse, PostPinRequest, PostDraftResponse
from app.services.files import FileService
from app.services.knowledge_base import knowledge_base_service
import json

router = APIRouter(prefix="", tags=["经验贴"])
file_service = FileService()

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    category: str = Form(...),
    is_draft: bool = Form(default=False),
    attachments_json: str = Form(default=""),
    files: List[UploadFile] = File(default=[]),
    current_user: User = Depends(get_current_user)
):
    """发布经验贴"""
    try:
        from tortoise import Tortoise
        from app.core.database import TORTOISE_ORM
        
        if not Tortoise._inited:
            await Tortoise.init(config=TORTOISE_ORM)
            print("Tortoise ORM 初始化成功")
        
        attachments = []
        
        if attachments_json:
            try:
                attachments_data = json.loads(attachments_json)
                for item in attachments_data:
                    file_path = item.get('path', '')
                    file_name = item.get('name', '')
                    if file_path:
                        attachments.append({
                            "path": file_path,
                            "name": file_name
                        })
            except json.JSONDecodeError:
                print(f"解析附件JSON失败: {attachments_json}")
        
        for file in files:
            if file_service.validate_file(file):
                result = file_service.save_file(file, "attachment")
                attachments.append(result)
        
        post = await Post.create(
            title=title,
            content=content,
            category=category,
            is_draft=is_draft,
            author=current_user,
            attachments=attachments
        )
        
        # 异步添加到知识库（不阻塞主流程）
        if not is_draft:
            import asyncio
            try:
                asyncio.create_task(knowledge_base_service.add_post(post))
                print(f"经验贴已添加到知识库队列: {post.id}")
            except Exception as kb_error:
                print(f"添加经验贴到知识库失败: {kb_error}")
        
        response_data = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "category": post.category,
            "author_id": current_user.id,
            "author_name": current_user.name,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "is_pinned": post.is_pinned,
            "is_draft": post.is_draft,
            "view_count": post.view_count,
            "like_count": post.like_count,
            "comment_count": post.comment_count,
            "attachments": attachments
        }
        
        return response_data
    except HTTPException:
        raise
    except Exception as e:
        print(f"发布经验贴失败，错误: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"发布经验贴失败: {str(e)}")

@router.get("/", response_model=List[PostListResponse])
async def list_posts(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """获取经验贴列表"""
    try:
        # 尝试重新初始化数据库
        try:
            from tortoise import Tortoise
            from app.core.database import TORTOISE_ORM
            await Tortoise.init(config=TORTOISE_ORM)
        except Exception as e:
            print(f"Tortoise ORM 初始化失败: {str(e)}")
        
        query = Post.filter(is_draft=False)
        
        if category:
            query = query.filter(category=category)
        
        # 置顶帖排在前面
        posts = await query.order_by(
            "-is_pinned",
            "-created_at"
        ).offset(skip).limit(limit)
        
        # 构建响应
        response_data = []
        for post in posts:
            # 获取作者信息
            await post.fetch_related("author")
            author_name = post.author.name if post.author else "未知用户"
            
            response_data.append({
                "id": post.id,
                "title": post.title,
                "category": post.category,
                "author_id": post.author.id if post.author else 0,
                "author_name": author_name,
                "created_at": post.created_at,
                "updated_at": post.updated_at,
                "is_pinned": post.is_pinned,
                "view_count": post.view_count,
                "like_count": post.like_count,
                "comment_count": post.comment_count
            })
        
        return response_data
    except Exception as e:
        print(f"获取经验贴列表失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取经验贴列表失败: {str(e)}")

@router.get("/drafts", response_model=List[PostDraftResponse])
async def list_drafts(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的草稿"""
    drafts = await Post.filter(
        author=current_user,
        is_draft=True
    ).order_by("-updated_at")
    
    return drafts

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    current_user: User = Depends(get_current_user)
):
    """获取经验贴详情"""
    # 获取经验贴，包括作者信息
    post = await Post.get_or_none(id=post_id).prefetch_related("author")
    if not post:
        raise HTTPException(status_code=404, detail="经验贴不存在")
    
    # 检查权限：草稿只能由作者查看
    if post.is_draft and post.author.id != current_user.id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 增加浏览量
    post.view_count += 1
    await post.save()
    
    # 构建响应
    response_data = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "category": post.category,
        "author_id": post.author.id,
        "author_name": post.author.name,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "is_pinned": post.is_pinned,
        "is_draft": post.is_draft,
        "view_count": post.view_count,
        "like_count": post.like_count,
        "comment_count": post.comment_count,
        "attachments": post.attachments
    }
    
    return response_data

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user)
):
    """更新经验贴"""
    post = await Post.get_or_none(id=post_id).prefetch_related("author")
    if not post:
        raise HTTPException(status_code=404, detail="经验贴不存在")
    
    # 检查权限：只有作者或管理员可以修改
    if post.author.id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 更新经验贴
    update_data = post_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)
    await post.save()
    
    # 异步更新知识库
    import asyncio
    try:
        asyncio.create_task(knowledge_base_service.update_post(post))
        print(f"经验贴已更新到知识库队列: {post.id}")
    except Exception as kb_error:
        print(f"更新经验贴到知识库失败: {kb_error}")
    
    # 构建响应
    response_data = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "category": post.category,
        "author_id": current_user.id,
        "author_name": current_user.name,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "is_pinned": post.is_pinned,
        "is_draft": post.is_draft,
        "view_count": post.view_count,
        "like_count": post.like_count,
        "comment_count": post.comment_count,
        "attachments": []  # 这里可以添加附件处理逻辑
    }
    
    return response_data

@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user)
):
    """删除经验贴"""
    post = await Post.get_or_none(id=post_id).prefetch_related("author")
    if not post:
        raise HTTPException(status_code=404, detail="经验贴不存在")
    
    # 检查权限：只有作者或管理员可以删除
    if post.author.id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 异步从知识库删除
    import asyncio
    try:
        asyncio.create_task(knowledge_base_service.delete_post(post.id))
        print(f"经验贴已从知识库删除队列: {post.id}")
    except Exception as kb_error:
        print(f"从知识库删除经验贴失败: {kb_error}")
    
    # 删除经验贴
    await post.delete()
    
    return {"message": "经验贴删除成功"}

@router.put("/{post_id}/pin")
async def pin_post(
    post_id: int,
    pin_request: PostPinRequest,
    current_user: User = Depends(get_current_admin)
):
    """置顶/取消置顶经验贴（管理员）"""
    post = await Post.get_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="经验贴不存在")
    
    post.is_pinned = pin_request.is_pinned
    await post.save()
    
    return {"message": "置顶状态更新成功"}
