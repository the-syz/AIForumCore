import pytest
from fastapi.testclient import TestClient
from app.core.database import TORTOISE_ORM
from tortoise import Tortoise
import os

from main import app

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    """初始化数据库"""
    import asyncio
    asyncio.get_event_loop().run_until_complete(Tortoise.init(config=TORTOISE_ORM))
    yield
    asyncio.get_event_loop().run_until_complete(Tortoise.close_connections())

@pytest.fixture
def client():
    """创建测试客户端"""
    with TestClient(app) as c:
        yield c

def get_test_token(client):
    """获取测试用户的token (学号: 20240010)"""
    response = client.post(
        "/api/auth/login",
        data={"username": "20240010", "password": "123456"}
    )
    if response.status_code != 200:
        pytest.skip(f"登录失败: {response.text}")
    return response.json()["access_token"]

def get_admin_token(client):
    """获取管理员用户的token (学号: 20210000)"""
    response = client.post(
        "/api/auth/login",
        data={"username": "20210000", "password": "123456"}
    )
    if response.status_code != 200:
        pytest.skip(f"管理员登录失败: {response.text}")
    return response.json()["access_token"]

def test_create_post(client):
    """测试经验贴发布功能"""
    token = get_test_token(client)
    
    response = client.post(
        "/api/posts/posts/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "title": "测试经验贴",
            "content": "这是一篇测试经验贴\n\n**Markdown格式**",
            "category": "测试分类",
            "is_draft": False
        }
    )
    
    assert response.status_code == 201, f"发布失败: {response.text}"
    post_data = response.json()
    assert post_data["title"] == "测试经验贴"
    assert post_data["category"] == "测试分类"

def test_create_post_with_attachment(client):
    """测试带附件的经验贴发布"""
    token = get_test_token(client)
    
    test_file_path = "tests/vscode配置latex教程.md"
    if not os.path.exists(test_file_path):
        pytest.skip("测试文件不存在")
    
    with open(test_file_path, "rb") as f:
        file_content = f.read()
    
    response = client.post(
        "/api/posts/posts/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "title": "测试经验贴（带附件）",
            "content": "这是一篇带附件的测试经验贴",
            "category": "测试分类",
            "is_draft": False
        },
        files={"files": ("vscode配置latex教程.md", file_content, "text/markdown")}
    )
    
    assert response.status_code == 201, f"发布失败: {response.text}"
    post_data = response.json()
    assert post_data["title"] == "测试经验贴（带附件）"

def test_list_posts(client):
    """测试获取经验贴列表"""
    token = get_test_token(client)
    
    response = client.get(
        "/api/posts/posts/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"获取列表失败: {response.text}"
    posts = response.json()
    assert isinstance(posts, list)

def test_list_posts_with_category(client):
    """测试分类筛选"""
    token = get_test_token(client)
    
    response = client.get(
        "/api/posts/posts/?category=工具教程",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"分类筛选失败: {response.text}"
    posts = response.json()
    assert isinstance(posts, list)

def test_get_post(client):
    """测试获取经验贴详情"""
    token = get_test_token(client)
    
    # 先获取列表找到一个帖子
    list_response = client.get(
        "/api/posts/posts/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if list_response.status_code != 200 or len(list_response.json()) == 0:
        pytest.skip("没有可用的帖子")
    
    post_id = list_response.json()[0]["id"]
    
    response = client.get(
        f"/api/posts/posts/{post_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"获取详情失败: {response.text}"
    post_data = response.json()
    assert post_data["id"] == post_id

def test_update_post(client):
    """测试修改经验贴"""
    token = get_test_token(client)
    
    # 先发布一篇经验贴
    create_response = client.post(
        "/api/posts/posts/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "title": "待修改经验贴",
            "content": "原始内容",
            "category": "测试分类",
            "is_draft": False
        }
    )
    
    if create_response.status_code != 201:
        pytest.skip(f"创建帖子失败: {create_response.text}")
    
    post_id = create_response.json()["id"]
    
    # 修改经验贴
    response = client.put(
        f"/api/posts/posts/{post_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "已修改经验贴",
            "content": "修改后的内容",
            "category": "修改分类"
        }
    )
    
    assert response.status_code == 200, f"修改失败: {response.text}"
    post_data = response.json()
    assert post_data["title"] == "已修改经验贴"

def test_delete_post(client):
    """测试删除经验贴"""
    token = get_test_token(client)
    
    # 先发布一篇经验贴
    create_response = client.post(
        "/api/posts/posts/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "title": "待删除经验贴",
            "content": "内容",
            "category": "测试分类",
            "is_draft": False
        }
    )
    
    if create_response.status_code != 201:
        pytest.skip(f"创建帖子失败: {create_response.text}")
    
    post_id = create_response.json()["id"]
    
    # 删除经验贴
    response = client.delete(
        f"/api/posts/posts/{post_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"删除失败: {response.text}"

def test_pin_post(client):
    """测试置顶经验贴（管理员）"""
    admin_token = get_admin_token(client)
    
    # 先发布一篇经验贴
    create_response = client.post(
        "/api/posts/posts/",
        headers={"Authorization": f"Bearer {admin_token}"},
        data={
            "title": "待置顶经验贴",
            "content": "内容",
            "category": "测试分类",
            "is_draft": False
        }
    )
    
    if create_response.status_code != 201:
        pytest.skip(f"创建帖子失败: {create_response.text}")
    
    post_id = create_response.json()["id"]
    
    # 置顶经验贴
    response = client.put(
        f"/api/posts/posts/{post_id}/pin",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"is_pinned": True}
    )
    
    assert response.status_code == 200, f"置顶失败: {response.text}"

def test_draft(client):
    """测试草稿保存和加载功能"""
    token = get_test_token(client)
    
    # 保存草稿
    create_response = client.post(
        "/api/posts/posts/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "title": "测试草稿",
            "content": "草稿内容",
            "category": "测试分类",
            "is_draft": True
        }
    )
    
    assert create_response.status_code == 201, f"保存草稿失败: {create_response.text}"
    post_data = create_response.json()
    assert post_data["is_draft"] == True
    
    # 获取草稿列表
    response = client.get(
        "/api/posts/posts/drafts",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"获取草稿列表失败: {response.text}"
    drafts = response.json()
    assert isinstance(drafts, list)
