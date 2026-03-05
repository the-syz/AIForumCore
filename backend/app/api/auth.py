from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token, UserPasswordUpdate
from tortoise.exceptions import IntegrityError

router = APIRouter(tags=["认证"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    user = await User.get_or_none(id=int(user_id))
    if user is None:
        raise credentials_exception
    return user

async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """获取当前管理员用户"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return current_user

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """用户注册"""
    # 检查学号是否已存在
    existing_user = await User.filter(student_id=user_data.student_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="学号已存在")
    
    # 创建用户
    try:
        user = await User.create(
            name=user_data.name,
            student_id=user_data.student_id,
            grade=user_data.grade,
            email=user_data.email,
            phone=user_data.phone,
            research_direction=user_data.research_direction,
            wechat=user_data.wechat,
            password_hash=get_password_hash(user_data.password)
        )
        return user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="注册失败，请检查输入信息")

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """用户登录"""
    # 查找用户（支持学号/姓名登录）
    user = await User.filter(
        student_id=form_data.username
    ).first()
    
    if not user:
        user = await User.filter(
            name=form_data.username
        ).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 生成Token
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """用户登出"""
    # JWT是无状态的，登出只需客户端删除token即可
    return {"message": "登出成功"}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

@router.post("/change-password")
async def change_password(
    password_data: UserPasswordUpdate,
    current_user: User = Depends(get_current_user)
):
    """修改密码"""
    # 验证旧密码
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="旧密码错误")
    
    # 更新密码
    current_user.password_hash = get_password_hash(password_data.new_password)
    await current_user.save()
    
    return {"message": "密码修改成功"}
