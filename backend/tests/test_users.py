from fastapi.testclient import TestClient
from app.core.security import get_password_hash, create_access_token
from app.models.user import User
import pytest

# 导入主应用
from main import app

client = TestClient(app)

@pytest.fixture
async def test_user():
    """创建测试用户"""
    user = await User.create(
        name="测试用户",
        student_id="20210001",
        password_hash=get_password_hash("password123")
    )
    yield user
    await user.delete()

@pytest.fixture
async def test_admin():
    """创建测试管理员用户"""
    user = await User.create(
        name="管理员用户",
        student_id="20210000",
        password_hash=get_password_hash("password123"),
        is_admin=True
    )
    yield user
    await user.delete()

@pytest.mark.asyncio
async def test_get_current_user(test_user):
    """测试获取当前用户信息"""
    # 生成token
    token = create_access_token(data={"sub": str(test_user.id)})
    
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["name"] == test_user.name

@pytest.mark.asyncio
async def test_update_current_user(test_user):
    """测试更新当前用户信息"""
    # 生成token
    token = create_access_token(data={"sub": str(test_user.id)})
    
    response = client.put(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "test@example.com",
            "phone": "13800138000"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["phone"] == "13800138000"

@pytest.mark.asyncio
async def test_list_users(test_admin):
    """测试获取用户列表（管理员）"""
    # 生成token
    token = create_access_token(data={"sub": str(test_admin.id)})
    
    response = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_user(test_admin, test_user):
    """测试获取用户详情（管理员）"""
    # 生成token
    token = create_access_token(data={"sub": str(test_admin.id)})
    
    response = client.get(
        f"/api/users/{test_user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["name"] == test_user.name

@pytest.mark.asyncio
async def test_update_user_role(test_admin, test_user):
    """测试修改用户权限（管理员）"""
    # 生成token
    token = create_access_token(data={"sub": str(test_admin.id)})
    
    response = client.put(
        f"/api/users/{test_user.id}/role",
        headers={"Authorization": f"Bearer {token}"},
        params={"role": "teacher", "is_admin": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "权限更新成功"

@pytest.mark.asyncio
async def test_delete_user(test_admin, test_user):
    """测试删除用户（管理员）"""
    # 生成token
    token = create_access_token(data={"sub": str(test_admin.id)})
    
    response = client.delete(
        f"/api/users/{test_user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "用户删除成功"

@pytest.mark.asyncio
async def test_batch_create_teachers(test_admin):
    """测试批量添加教师用户（管理员）"""
    # 生成token
    token = create_access_token(data={"sub": str(test_admin.id)})
    
    response = client.post(
        "/api/users/batch",
        headers={"Authorization": f"Bearer {token}"},
        json=[
            {
                "name": "教师1",
                "student_id": "20210002",
                "password": "password123"
            },
            {
                "name": "教师2",
                "student_id": "20210003",
                "password": "password123"
            }
        ]
    )
    assert response.status_code == 200
    data = response.json()
    assert "成功创建 2 个教师用户" in data["message"]
    
    # 清理测试数据
    await User.filter(student_id="20210002").delete()
    await User.filter(student_id="20210003").delete()
