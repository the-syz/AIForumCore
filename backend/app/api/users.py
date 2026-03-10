from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.api.auth import get_current_user, get_current_admin, optional_get_current_user_v2
from app.models.user import User
from app.models.paper import Paper
from app.models.post import Post
from app.schemas.user import UserResponse, UserUpdate, UserCreate
from app.core.security import get_password_hash, verify_password
from pydantic import BaseModel

router = APIRouter(tags=["用户"])

class PasswordUpdateRequest(BaseModel):
    old_password: str
    new_password: str

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """更新当前用户信息"""
    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    await current_user.save()
    return current_user

@router.post("/me/change-password")
async def change_password(
    data: PasswordUpdateRequest,
    current_user: User = Depends(get_current_user)
):
    """修改当前用户密码"""
    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="旧密码错误")
    
    current_user.password_hash = get_password_hash(data.new_password)
    await current_user.save()
    return {"message": "密码修改成功"}

@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin)
):
    """获取用户列表（管理员）"""
    users = await User.all().offset(skip).limit(limit)
    return users

@router.get("/{user_id}/public", response_model=UserResponse)
async def get_user_public(
    user_id: int,
    current_user: User = Depends(optional_get_current_user_v2)
):
    """获取用户公开信息（无需管理员权限）"""
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_admin)
):
    """获取用户详情（管理员）"""
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.get("/{user_id}/papers")
async def get_user_papers(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(optional_get_current_user_v2)
):
    """获取用户发布的论文列表"""
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    papers = await Paper.filter(uploader_id=user_id).offset(skip).limit(limit).order_by('-upload_time')
    return papers

@router.get("/{user_id}/posts")
async def get_user_posts(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(optional_get_current_user_v2)
):
    """获取用户发布的经验贴列表"""
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    posts = await Post.filter(author_id=user_id, is_draft=False).offset(skip).limit(limit).order_by('-created_at')
    
    response_data = []
    for post in posts:
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

@router.put("/{user_id}/role")
async def update_user_role(
    user_id: int,
    role: str,
    is_admin: bool,
    current_user: User = Depends(get_current_admin)
):
    """修改用户权限（管理员）"""
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 验证角色有效性
    valid_roles = ["master", "phd", "graduate", "teacher"]
    if role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"无效的角色，必须是以下之一: {', '.join(valid_roles)}")
    
    # 毕业生自动剥离管理员权限
    if role == "graduate":
        is_admin = False
    
    user.role = role
    user.is_admin = is_admin
    await user.save()
    return {"message": "权限更新成功"}

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin)
):
    """删除用户（管理员）"""
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    await user.delete()
    return {"message": "用户删除成功"}

@router.post("/batch")
async def batch_create_teachers(
    teachers: List[UserCreate],
    current_user: User = Depends(get_current_admin)
):
    """批量添加教师用户（管理员）"""
    created_users = []
    for teacher_data in teachers:
        # 检查学号是否已存在
        existing_user = await User.filter(student_id=teacher_data.student_id).first()
        if existing_user:
            continue
        
        # 创建教师用户
        user = await User.create(
            name=teacher_data.name,
            student_id=teacher_data.student_id,
            grade=teacher_data.grade,
            email=teacher_data.email,
            phone=teacher_data.phone,
            research_direction=teacher_data.research_direction,
            wechat=teacher_data.wechat,
            password_hash=get_password_hash(teacher_data.password),
            role="teacher",
            is_admin=False
        )
        created_users.append(user)
    
    return {"message": f"成功创建 {len(created_users)} 个教师用户"}

@router.post("/")
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_admin)
):
    """添加用户（管理员）"""
    # 检查学号是否已存在
    existing_user = await User.filter(student_id=user_data.student_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="学号已存在")
    
    # 确定角色和权限
    role = user_data.role if user_data.role else "master"
    is_admin = False
    
    # 毕业生自动剥离管理员权限
    if role == "graduate":
        is_admin = False
    
    user = await User.create(
        name=user_data.name,
        student_id=user_data.student_id,
        grade=user_data.grade,
        email=user_data.email,
        phone=user_data.phone,
        research_direction=user_data.research_direction,
        wechat=user_data.wechat,
        password_hash=get_password_hash(user_data.password),
        role=role,
        is_admin=is_admin
    )
    
    return user
