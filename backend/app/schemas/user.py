from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional

# 允许的学生角色
STUDENT_ROLES = ["master", "phd", "graduate"]
# 所有角色
ALL_ROLES = ["master", "phd", "graduate", "teacher"]

class UserBase(BaseModel):
    """用户基础模型"""
    name: str = Field(..., min_length=1, max_length=50, description="用户名")
    student_id: str = Field(..., min_length=1, max_length=20, description="学号")
    grade: Optional[str] = Field(None, max_length=10, description="年级")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="电话")
    research_direction: Optional[str] = Field(None, max_length=255, description="研究方向")
    wechat: Optional[str] = Field(None, max_length=50, description="微信")
    role: Optional[str] = Field("master", description="用户角色: master(硕士), phd(博士), graduate(毕业生), teacher(教师)")
    
    @validator('role')
    def validate_role(cls, v):
        if v is None:
            return "master"
        if v not in ALL_ROLES:
            raise ValueError(f'无效的角色，必须是以下之一: {", ".join(ALL_ROLES)}')
        return v

class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=6, description="密码")

class UserLogin(BaseModel):
    """用户登录模型"""
    username: str = Field(..., description="用户名或学号")
    password: str = Field(..., description="密码")

class UserUpdate(BaseModel):
    """用户更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    student_id: Optional[str] = Field(None, min_length=1, max_length=20)
    grade: Optional[str] = Field(None, max_length=10)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    research_direction: Optional[str] = Field(None, max_length=255)
    wechat: Optional[str] = Field(None, max_length=50)

class UserPasswordUpdate(BaseModel):
    """用户密码更新模型"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码")

class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    role: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """令牌模型"""
    access_token: str
    user: UserResponse

class TokenData(BaseModel):
    """令牌数据模型"""
    user_id: Optional[str] = None
