from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.api.auth import get_current_user, get_current_admin
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserCreate
from app.core.security import get_password_hash

router = APIRouter(tags=["用户"])

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

@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin)
):
    """获取用户列表（管理员）"""
    users = await User.all().offset(skip).limit(limit)
    return users

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
