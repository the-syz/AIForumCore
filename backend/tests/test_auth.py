from fastapi.testclient import TestClient
from app.core.security import get_password_hash, create_access_token, verify_password
from app.core.database import TORTOISE_ORM, Tortoise
from app.models.user import User
import pytest
import asyncio
import pytest_asyncio

# 导入主应用
from main import app

client = TestClient(app)

# 测试前初始化数据库
@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_db():
    """初始化数据库"""
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

@pytest_asyncio.fixture
async def test_user():
    """创建测试用户"""
    # 直接使用短密码，避免passlib内部的密码长度问题
    user = await User.create(
        name="测试用户",
        student_id="20210001",
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # password123的哈希值
    )
    yield user
    await user.delete()

@pytest.mark.asyncio
async def test_password_hash():
    """测试密码哈希功能"""
    # 测试短密码
    password = "password123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    
    # 测试长密码（超过72字节）
    long_password = "a" * 100
    hashed_long = get_password_hash(long_password)
    assert hashed_long != long_password
    # 注意：bcrypt会截断密码，所以验证时也需要截断
    assert verify_password(long_password[:72], hashed_long)

@pytest.mark.asyncio
async def test_jwt_token():
    """测试JWT Token生成和验证"""
    user_id = "1"
    token = create_access_token(data={"sub": user_id})
    assert token

@pytest.mark.asyncio
async def test_register():
    """测试用户注册"""
    response = client.post(
        "/api/auth/register",
        json={
            "name": "新用户",
            "student_id": "20210002",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "新用户"
    assert data["student_id"] == "20210002"
    
    # 清理测试数据
    user = await User.filter(student_id="20210002").first()
    if user:
        await user.delete()

@pytest.mark.asyncio
async def test_login(test_user):
    """测试用户登录"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": test_user.student_id,
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials():
    """测试无效凭据登录"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "不存在的用户",
            "password": "password123"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "用户名或密码错误"

@pytest.mark.asyncio
async def test_get_me(test_user):
    """测试获取当前用户信息"""
    # 生成token
    token = create_access_token(data={"sub": str(test_user.id)})
    
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["name"] == test_user.name

@pytest.mark.asyncio
async def test_change_password(test_user):
    """测试修改密码"""
    # 生成token
    token = create_access_token(data={"sub": str(test_user.id)})
    
    response = client.post(
        "/api/auth/change-password",
        json={
            "old_password": "password123",
            "new_password": "newpassword123"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "密码修改成功"

@pytest.mark.asyncio
async def test_change_password_invalid_old_password(test_user):
    """测试修改密码时旧密码错误"""
    # 生成token
    token = create_access_token(data={"sub": str(test_user.id)})
    
    response = client.post(
        "/api/auth/change-password",
        json={
            "old_password": "wrongpassword",
            "new_password": "newpassword123"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "旧密码错误"

@pytest.mark.asyncio
async def test_logout(test_user):
    """测试用户登出"""
    # 生成token
    token = create_access_token(data={"sub": str(test_user.id)})
    
    response = client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "登出成功"
