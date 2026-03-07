from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.api.auth import get_current_user
from app.models.user import User
from app.models.comment import Comment
from app.models.like import Like
from app.models.favorite import Favorite
from app.models.post import Post
from app.models.paper import Paper
from app.schemas.forum import CommentCreate, CommentResponse, LikeCreate, FavoriteCreate, FavoriteResponse
from tortoise import Tortoise

router = APIRouter(tags=["论坛"])

@router.post("/comments", response_model=CommentResponse)
async def create_comment(
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user)
):
    """发表评论"""
    try:
        # 确保Tortoise ORM上下文是激活的
        from tortoise import Tortoise
        from app.core.database import TORTOISE_ORM
        
        # 检查Tortoise是否已经初始化
        if not Tortoise._inited:
            await Tortoise.init(config=TORTOISE_ORM)
            print("Tortoise ORM 初始化成功")
        
        # 检查帖子是否存在
        post = await Post.get_or_none(id=comment_data.post_id)
        if not post:
            raise HTTPException(status_code=404, detail="帖子不存在")
        
        # 检查父评论是否存在（如果有）
        if comment_data.parent_id:
            parent_comment = await Comment.get_or_none(id=comment_data.parent_id)
            if not parent_comment:
                raise HTTPException(status_code=404, detail="父评论不存在")
        
        # 创建评论
        comment = await Comment.create(
            content=comment_data.content,
            user=current_user,
            post=post,
            parent_id=comment_data.parent_id
        )
        
        # 构建响应数据
        response_data = {
            "id": comment.id,
            "content": comment.content,
            "parent_id": comment.parent_id,
            "post_id": comment.post.id,
            "user_id": comment.user.id,
            "user_name": comment.user.name,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
            "replies": []
        }
        
        return response_data
    except HTTPException:
        raise
    except Exception as e:
        print(f"发表评论失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"发表评论失败: {str(e)}")

@router.get("/comments", response_model=List[CommentResponse])
async def list_comments(
    post_id: int = Query(..., description="帖子ID"),
    skip: int = 0,
    limit: int = 50
):
    """获取评论列表"""
    try:
        # 尝试重新初始化数据库
        try:
            from app.core.database import TORTOISE_ORM
            await Tortoise.init(config=TORTOISE_ORM)
        except Exception:
            pass
        
        # 检查帖子是否存在
        post = await Post.get_or_none(id=post_id)
        if not post:
            raise HTTPException(status_code=404, detail="帖子不存在")
        
        # 获取顶级评论（没有父评论的评论）
        top_level_comments = await Comment.filter(
            post_id=post_id,
            parent_id=None
        ).prefetch_related("user", "post").order_by("created_at").offset(skip).limit(limit).all()
        
        # 构建响应数据
        comments_data = []
        for comment in top_level_comments:
            # 获取评论的回复
            replies = await Comment.filter(parent_id=comment.id).prefetch_related("user", "post").order_by("created_at").all()
            
            # 构建回复数据
            replies_data = []
            for reply in replies:
                replies_data.append({
                    "id": reply.id,
                    "content": reply.content,
                    "parent_id": reply.parent_id,
                    "post_id": reply.post_id,
                    "user_id": reply.user.id,
                    "user_name": reply.user.name,
                    "created_at": reply.created_at,
                    "updated_at": reply.updated_at,
                    "replies": []
                })
            
            # 构建评论数据
            comment_data = {
                "id": comment.id,
                "content": comment.content,
                "parent_id": comment.parent_id,
                "post_id": comment.post_id,
                "user_id": comment.user.id,
                "user_name": comment.user.name,
                "created_at": comment.created_at,
                "updated_at": comment.updated_at,
                "replies": replies_data
            }
            comments_data.append(comment_data)
        
        return comments_data
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取评论列表失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取评论列表失败: {str(e)}")

@router.post("/likes")
async def toggle_like(
    like_data: LikeCreate,
    current_user: User = Depends(get_current_user)
):
    """点赞/取消点赞"""
    try:
        # 尝试重新初始化数据库
        try:
            from app.core.database import TORTOISE_ORM
            await Tortoise.init(config=TORTOISE_ORM)
        except Exception:
            pass
        
        # 检查目标是否存在
        if like_data.target_type == "post":
            target = await Post.get_or_none(id=like_data.target_id)
        elif like_data.target_type == "paper":
            target = await Paper.get_or_none(id=like_data.target_id)
        elif like_data.target_type == "comment":
            target = await Comment.get_or_none(id=like_data.target_id)
        else:
            raise HTTPException(status_code=400, detail="无效的目标类型")
        
        if not target:
            raise HTTPException(status_code=404, detail="目标不存在")
        
        # 检查是否已经点赞
        existing_like = await Like.filter(
            user_id=current_user.id,
            target_type=like_data.target_type,
            target_id=like_data.target_id
        ).first()
        
        if existing_like:
            # 取消点赞
            await existing_like.delete()
            return {"message": "取消点赞成功"}
        else:
            # 添加点赞
            await Like.create(
                user_id=current_user.id,
                target_type=like_data.target_type,
                target_id=like_data.target_id
            )
            return {"message": "点赞成功"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"点赞/取消点赞失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"点赞/取消点赞失败: {str(e)}")

@router.post("/favorites")
async def toggle_favorite(
    favorite_data: FavoriteCreate,
    current_user: User = Depends(get_current_user)
):
    """收藏/取消收藏"""
    try:
        # 尝试重新初始化数据库
        try:
            from app.core.database import TORTOISE_ORM
            await Tortoise.init(config=TORTOISE_ORM)
        except Exception:
            pass
        
        # 检查目标是否存在
        if favorite_data.target_type == "post":
            target = await Post.get_or_none(id=favorite_data.target_id)
        elif favorite_data.target_type == "paper":
            target = await Paper.get_or_none(id=favorite_data.target_id)
        else:
            raise HTTPException(status_code=400, detail="无效的目标类型")
        
        if not target:
            raise HTTPException(status_code=404, detail="目标不存在")
        
        # 检查是否已经收藏
        existing_favorite = await Favorite.filter(
            user_id=current_user.id,
            target_type=favorite_data.target_type,
            target_id=favorite_data.target_id
        ).first()
        
        if existing_favorite:
            # 取消收藏
            await existing_favorite.delete()
            return {"message": "取消收藏成功"}
        else:
            # 添加收藏
            await Favorite.create(
                user_id=current_user.id,
                target_type=favorite_data.target_type,
                target_id=favorite_data.target_id
            )
            return {"message": "收藏成功"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"收藏/取消收藏失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"收藏/取消收藏失败: {str(e)}")

@router.get("/favorites", response_model=List[FavoriteResponse])
async def list_favorites(
    target_type: Optional[str] = Query(None, description="目标类型: paper, post"),
    current_user: User = Depends(get_current_user)
):
    """获取收藏列表"""
    try:
        # 尝试重新初始化数据库
        try:
            from app.core.database import TORTOISE_ORM
            await Tortoise.init(config=TORTOISE_ORM)
        except Exception:
            pass
        
        # 构建查询
        query = Favorite.filter(user_id=current_user.id)
        
        # 如果指定了目标类型，过滤结果
        if target_type:
            query = query.filter(target_type=target_type)
        
        # 获取收藏列表
        favorites = await query.order_by("created_at").all()
        
        return favorites
    except Exception as e:
        print(f"获取收藏列表失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取收藏列表失败: {str(e)}")
