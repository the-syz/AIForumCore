import pytest
from fastapi.testclient import TestClient
import os
import tempfile
from app.core.security import create_access_token
from app.core.database import TORTOISE_ORM, Tortoise
from app.models.download import Download
from app.models.user import User
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
async def test_admin():
    """创建测试管理员用户"""
    user = await User.create(
        name="测试管理员",
        student_id="20210000",
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # password123的哈希值
        is_admin=True
    )
    yield user
    await user.delete()

@pytest_asyncio.fixture
def test_file_path():
    """创建测试文件"""
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("这是一个测试文件")
        temp_file_path = f.name
    
    yield temp_file_path
    
    # 清理临时文件
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

@pytest.mark.asyncio
async def test_create_download(test_admin, test_file_path):
    """测试上传下载资源（仅管理员）"""
    # 生成管理员token
    token = create_access_token(data={"sub": str(test_admin.id)})
    
    # 准备文件
    with open(test_file_path, "rb") as f:
        test_file = f.read()
    
    # 发送请求
    response = client.post(
        "/api/downloads/",
        data={
            "title": "测试资源",
            "description": "这是一个测试资源",
            "category": "测试"
        },
        files={
            "file": ("test.txt", test_file, "text/plain")
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "测试资源"
    assert data["description"] == "这是一个测试资源"
    assert data["category"] == "测试"
    assert "file_path" in data
    assert data["download_count"] == 0
    
    # 清理测试文件
    if os.path.exists(data["file_path"]):
        os.remove(data["file_path"])

@pytest.mark.asyncio
async def test_list_downloads():
    """测试获取下载资源列表"""
    # 发送请求
    response = client.get("/api/downloads/")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_download(test_admin, test_file_path):
    """测试获取下载资源详情"""
    # 生成管理员token
    token = create_access_token(data={"sub": str(test_admin.id)})
    
    # 先创建一个测试资源
    with open(test_file_path, "rb") as f:
        test_file = f.read()
    
    create_response = client.post(
        "/api/downloads/",
        data={
            "title": "测试资源",
            "description": "这是一个测试资源",
            "category": "测试"
        },
        files={
            "file": ("test.txt", test_file, "text/plain")
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    download_id = create_response.json()["id"]
    file_path = create_response.json()["file_path"]
    
    # 测试获取详情
    response = client.get(f"/api/downloads/{download_id}")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == download_id
    assert data["title"] == "测试资源"
    
    # 清理测试文件
    if os.path.exists(file_path):
        os.remove(file_path)

@pytest.mark.asyncio
async def test_update_download(test_admin, test_file_path):
    """测试更新下载资源（仅管理员）"""
    # 生成管理员token
    token = create_access_token(data={"sub": str(test_admin.id)})
    
    # 先创建一个测试资源
    with open(test_file_path, "rb") as f:
        test_file = f.read()
    
    create_response = client.post(
        "/api/downloads/",
        data={
            "title": "测试资源",
            "description": "这是一个测试资源",
            "category": "测试"
        },
        files={
            "file": ("test.txt", test_file, "text/plain")
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    download_id = create_response.json()["id"]
    file_path = create_response.json()["file_path"]
    
    # 测试更新
    update_data = {
        "title": "更新后的测试资源",
        "description": "这是更新后的测试资源",
        "category": "更新测试"
    }
    
    response = client.put(
        f"/api/downloads/{download_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == download_id
    assert data["title"] == "更新后的测试资源"
    assert data["description"] == "这是更新后的测试资源"
    assert data["category"] == "更新测试"
    
    # 清理测试文件
    if os.path.exists(file_path):
        os.remove(file_path)

@pytest.mark.asyncio
async def test_delete_download(test_admin, test_file_path):
    """测试删除下载资源（仅管理员）"""
    # 生成管理员token
    token = create_access_token(data={"sub": str(test_admin.id)})
    
    # 先创建一个测试资源
    with open(test_file_path, "rb") as f:
        test_file = f.read()
    
    create_response = client.post(
        "/api/downloads/",
        data={
            "title": "测试资源",
            "description": "这是一个测试资源",
            "category": "测试"
        },
        files={
            "file": ("test.txt", test_file, "text/plain")
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    download_id = create_response.json()["id"]
    file_path = create_response.json()["file_path"]
    
    # 测试删除
    response = client.delete(
        f"/api/downloads/{download_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 验证响应
    assert response.status_code == 200
    assert response.json()["message"] == "资源删除成功"
    
    # 验证资源已删除
    get_response = client.get(f"/api/downloads/{download_id}")
    assert get_response.status_code == 404
    
    # 清理测试文件（如果删除失败）
    if os.path.exists(file_path):
        os.remove(file_path)

@pytest.mark.asyncio
async def test_download_file(test_admin, test_file_path):
    """测试下载资源文件"""
    # 生成管理员token
    token = create_access_token(data={"sub": str(test_admin.id)})
    
    # 先创建一个测试资源
    with open(test_file_path, "rb") as f:
        test_file = f.read()
    
    create_response = client.post(
        "/api/downloads/",
        data={
            "title": "测试资源",
            "description": "这是一个测试资源",
            "category": "测试"
        },
        files={
            "file": ("test.txt", test_file, "text/plain")
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    download_id = create_response.json()["id"]
    file_path = create_response.json()["file_path"]
    
    # 测试下载
    response = client.get(f"/api/downloads/{download_id}/download")
    
    # 验证响应
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    
    # 验证下载次数已增加
    get_response = client.get(f"/api/downloads/{download_id}")
    assert get_response.status_code == 200
    assert get_response.json()["download_count"] == 1
    
    # 清理测试文件
    if os.path.exists(file_path):
        os.remove(file_path)
