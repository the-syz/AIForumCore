from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token, UserPasswordUpdate
from tortoise.exceptions import IntegrityError
from tortoise import Tortoise

router = APIRouter(tags=["认证"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 确保Tortoise ORM上下文是激活的
        from tortoise import Tortoise
        from app.core.database import TORTOISE_ORM
        
        # 检查Tortoise是否已经初始化
        if not Tortoise._inited:
            await Tortoise.init(config=TORTOISE_ORM)
            print("Tortoise ORM 初始化成功")
        
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
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取当前用户失败: {str(e)}")
        raise credentials_exception

async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """获取当前管理员用户"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return current_user

async def optional_get_current_user(token: str = Depends(oauth2_scheme)) -> User | None:
    """可选获取当前用户（即使没有token也不会报错）"""
    try:
        from tortoise import Tortoise
        from app.core.database import TORTOISE_ORM
        
        if not Tortoise._inited:
            await Tortoise.init(config=TORTOISE_ORM)
        
        payload = decode_access_token(token)
        if payload is None:
            return None
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        user = await User.get_or_none(id=int(user_id))
        return user
    except Exception:
        return None

# 版本2：完全可选，没有token也能通过
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request

class OptionalOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        try:
            return await super().__call__(request)
        except Exception:
            return None

optional_oauth2_scheme = OptionalOAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

async def optional_get_current_user_v2(token: Optional[str] = Depends(optional_oauth2_scheme)) -> User | None:
    """完全可选的当前用户获取（没有token也可以）"""
    if not token:
        return None
    try:
        from tortoise import Tortoise
        from app.core.database import TORTOISE_ORM
        
        if not Tortoise._inited:
            await Tortoise.init(config=TORTOISE_ORM)
        
        payload = decode_access_token(token)
        if payload is None:
            return None
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        user = await User.get_or_none(id=int(user_id))
        return user
    except Exception:
        return None

@router.post("/register")
async def register(user_data: UserCreate):
    """用户注册"""
    try:
        print(f"收到注册请求: {user_data}")
        
        # 确保Tortoise ORM上下文是激活的
        from tortoise import Tortoise
        from app.core.database import TORTOISE_ORM
        
        # 检查Tortoise是否已经初始化
        if not Tortoise._inited:
            await Tortoise.init(config=TORTOISE_ORM)
            print("Tortoise ORM 初始化成功")
        
        # 检查学号是否已存在
        existing_user = await User.filter(student_id=user_data.student_id).first()
        if existing_user:
            print(f"学号已存在: {user_data.student_id}")
            raise HTTPException(status_code=400, detail="学号已存在")
        
        # 检查密码长度
        password = user_data.password
        password_bytes = password.encode('utf-8')
        print(f"密码长度（字节）: {len(password_bytes)}")
        if len(password_bytes) > 72:
            print("密码长度超过72字节，正在截断...")
            password = password_bytes[:72].decode('utf-8', errors='ignore')
            print(f"截断后密码长度（字节）: {len(password.encode('utf-8'))}")
        
        # 确定角色和权限
        # 注册时只允许学生角色，教师角色只能在后台创建
        role = user_data.role if user_data.role in ["master", "phd", "graduate"] else "master"
        
        # 毕业生自动剥离管理员权限
        is_admin = False
        if role == "graduate":
            is_admin = False
            print(f"用户角色为毕业生，自动剥离管理员权限")
        
        print(f"用户角色: {role}, 管理员权限: {is_admin}")
        
        # 创建用户
        print(f"尝试创建用户: {user_data.name}, 学号: {user_data.student_id}")
        
        user = await User.create(
            name=user_data.name,
            student_id=user_data.student_id,
            grade=user_data.grade,
            email=user_data.email,
            phone=user_data.phone,
            research_direction=user_data.research_direction,
            wechat=user_data.wechat,
            password_hash=get_password_hash(password),
            role=role,
            is_admin=is_admin
        )
        print(f"用户创建成功: {user.id}")
        
        # 构建响应数据
        response_data = {
            "id": user.id,
            "name": user.name,
            "student_id": user.student_id,
            "grade": user.grade,
            "email": user.email,
            "phone": user.phone,
            "research_direction": user.research_direction,
            "wechat": user.wechat,
            "role": user.role,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
        print(f"构建响应数据: {response_data}")
        
        return response_data
    except HTTPException:
        raise
    except Exception as e:
        print(f"注册失败，错误: {str(e)}")
        import traceback
        traceback.print_exc()
        # 尝试重新初始化数据库
        try:
            from app.core.database import TORTOISE_ORM
            await Tortoise.init(config=TORTOISE_ORM)
            print("Tortoise ORM 重新初始化成功")
            
            # 检查密码长度
            password = user_data.password
            password_bytes = password.encode('utf-8')
            print(f"密码长度（字节）: {len(password_bytes)}")
            if len(password_bytes) > 72:
                print("密码长度超过72字节，正在截断...")
                password = password_bytes[:72].decode('utf-8', errors='ignore')
                print(f"截断后密码长度（字节）: {len(password.encode('utf-8'))}")
            
            # 再次尝试创建用户
            user = await User.create(
                name=user_data.name,
                student_id=user_data.student_id,
                grade=user_data.grade,
                email=user_data.email,
                phone=user_data.phone,
                research_direction=user_data.research_direction,
                wechat=user_data.wechat,
                password_hash=get_password_hash(password)
            )
            print(f"用户创建成功: {user.id}")
            response_data = {
                "id": user.id,
                "name": user.name,
                "student_id": user.student_id,
                "grade": user.grade,
                "email": user.email,
                "phone": user.phone,
                "research_direction": user.research_direction,
                "wechat": user.wechat,
                "role": user.role,
                "is_admin": user.is_admin,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            }
            return response_data
        except Exception as e2:
            print(f"重新初始化后仍然失败: {str(e2)}")
            raise HTTPException(status_code=500, detail=f"注册失败: {str(e2)}")

@router.post("/login", response_model=Token)
async def login(username: str = Form(...), password: str = Form(...), autoLogin: bool = Form(False)):
    """用户登录"""
    try:
        print(f"收到登录请求: {username}, autoLogin: {autoLogin}")
        
        # 确保Tortoise ORM上下文是激活的
        from tortoise import Tortoise
        from app.core.database import TORTOISE_ORM
        
        # 检查Tortoise是否已经初始化
        if not Tortoise._inited:
            await Tortoise.init(config=TORTOISE_ORM)
            print("Tortoise ORM 初始化成功")
        
        # 查找用户（支持学号/姓名登录）
        user = await User.filter(
            student_id=username
        ).first()
        print(f"根据学号查找用户: {user}")
        
        if not user:
            user = await User.filter(
                name=username
            ).first()
            print(f"根据姓名查找用户: {user}")
        
        if not user:
            print("用户不存在")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 验证密码
        print(f"验证密码: {password}")
        print(f"存储的密码哈希: {user.password_hash}")
        if not verify_password(password, user.password_hash):
            print("密码验证失败")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 根据autoLogin参数设置token有效期
        from datetime import timedelta
        if autoLogin:
            # 长期token：7天有效期
            expires_delta = timedelta(days=7)
            print("生成长期Token（7天）")
        else:
            # 短期token：2小时有效期
            expires_delta = timedelta(hours=2)
            print("生成短期Token（2小时）")
        
        # 生成Token
        print(f"生成Token for user: {user.id}")
        access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=expires_delta)
        print(f"Token生成成功: {access_token[:20]}...")
        
        # 构建用户信息
        from app.schemas.user import UserResponse
        user_response = UserResponse.model_validate(user)
        
        return {"access_token": access_token, "user": user_response}
    except HTTPException:
        raise
    except Exception as e:
        print(f"登录失败，错误: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")

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
