import pytest
from fastapi.testclient import TestClient
from app.core.database import init_db, close_db
from app.models.user import User
from app.models.post import Post
import asyncio
import os
import shutil

# 导入应用
from main import app

# 测试客户端
client = TestClient(app)

# 测试前准备
@pytest.fixture(scope="module", autouse=True)
async def setup():
    """测试前初始化数据库"""
    await init_db()
    # 创建测试用户
    test_user = await User.create(
        name="测试用户",
        student_id="20240001",
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # 密码: 123456
    )
    # 创建管理员用户
    admin_user = await User.create(
        name="管理员",
        student_id="20240000",
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        is_admin=True
    )
    yield
    # 测试后清理
    await User.filter(student_id="20240001").delete()
    await User.filter(student_id="20240000").delete()
    await Post.filter().delete()
    await close_db()
    # 清理上传文件
    if os.path.exists("uploads"):
        shutil.rmtree("uploads")

# 获取测试token
def get_test_token():
    """获取测试用户的token"""
    response = client.post(
        "/api/auth/login",
        data={"username": "20240001", "password": "123456"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

# 获取管理员token
def get_admin_token():
    """获取管理员用户的token"""
    response = client.post(
        "/api/auth/login",
        data={"username": "20240000", "password": "123456"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

# 测试经验贴发布
def test_create_post():
    """测试经验贴发布功能"""
    token = get_test_token()
    
    # 测试发布经验贴
    response = client.post(
        "/api/posts/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "title": "测试经验贴",
            "content": "这是一篇测试经验贴\n\n**Markdown格式**",
            "category": "测试分类",
            "is_draft": False
        }
    )
    
    assert response.status_code == 201
    post_data = response.json()
    assert post_data["title"] == "测试经验贴"
    assert post_data["content"] == "这是一篇测试经验贴\n\n**Markdown格式**"
    assert post_data["category"] == "测试分类"
    assert post_data["is_draft"] == False

# 测试经验贴发布（带附件）
def test_create_post_with_attachment():
    """测试带附件的经验贴发布"""
    token = get_test_token()
    
    # 测试文件路径
    test_file_path = "tests/vscode配置latex教程.md"
    if not os.path.exists(test_file_path):
        pytest.skip("测试文件不存在")
    
    with open(test_file_path, "rb") as f:
        response = client.post(
            "/api/posts/",
            headers={"Authorization": f"Bearer {token}"},
            data={
                "title": "测试经验贴（带附件）",
                "content": "这是一篇带附件的测试经验贴",
                "category": "测试分类",
                "is_draft": False
            },
            files={"files": ("vscode配置latex教程.md", f, "text/markdown")}
        )
    
    assert response.status_code == 201
    post_data = response.json()
    assert post_data["title"] == "测试经验贴（带附件）"
    assert len(post_data["attachments"]) > 0

# 测试经验贴列表
def test_list_posts():
    """测试获取经验贴列表"""
    token = get_test_token()
    
    # 先发布两篇经验贴
    client.post(
        "/api/posts/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "title": "经验贴1",
            "content": "内容1",
            "category": "分类1",
            "is_draft": False
        }
    )
    
    client.post(
        "/api/posts/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "title": "经验贴2",
            "content": "内容2",
            "category": "分类2",
            "is_draft": False
        }
    )
    
    # 获取经验贴列表
    response = client.get(
        "/api/posts/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) >= 2

# 测试经验贴详情
def test_get_post():
    """测试获取经验贴详情"""
    token = get_test_token()
    
    # 先发布一篇经验贴
    create_response = client.post(
        "/api/posts/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "title": "测试详情",
            "content": "这是测试详情内容",
            "category": "测试分类",
            "is_draft": False
        }
    )
    
    post_id = create_response.json()["id"]
    
    # 获取经验贴详情
    response = client.get(
        f"/api/posts/{post_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    post_data = response.json()
    assert post_data["id"] == post_id
    assert post_data["title"] == "测试详情"
    assert post_data["content"] == "这是测试详情内容"

# 测试经验贴修改
def test_update_post():
    """测试修改经验贴"""
    token = get_test_token()
    
    # 先发布一篇经验贴
    create_response = client.post(
        "/api/posts/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "title": "待修改经验贴",
            "content": "原始内容",
            "category": "测试分类",
            "is_draft": False
        }
    )
    
    post_id = create_response.json()["id"]
    
    # 修改经验贴
    response = client.put(
        f"/api/posts/{post_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "已修改经验贴",
            "content": "修改后的内容",
            "category": "修改分类"
        }
    )
    
    assert response.status_code == 200
    post_data = response.json()
    assert post_data["title"] == "已修改经验贴"
    assert post_data["content"] == "修改后的内容"
    assert post_data["category"] == "修改分类"

# 测试经验贴删除
def test_delete_post():
    """测试删除经验贴"""
    token = get_test_token()
    
    # 先发布一篇经验贴
    create_response = client.post(
        "/api/posts/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "title": "待删除经验贴",
            "content": "内容",
            "category": "测试分类",
            "is_draft": False
        }
    )
    
    post_id = create_response.json()["id"]
    
    # 删除经验贴
    response = client.delete(
        f"/api/posts/{post_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == "经验贴删除成功"
    
    # 验证经验贴已删除
    detail_response = client.get(
        f"/api/posts/{post_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert detail_response.status_code == 404

# 测试经验贴置顶
def test_pin_post():
    """测试置顶经验贴"""
    admin_token = get_admin_token()
    
    # 先发布一篇经验贴
    create_response = client.post(
        "/api/posts/",
        headers={"Authorization": f"Bearer {admin_token}"},
        data={
            "title": "待置顶经验贴",
            "content": "内容",
            "category": "测试分类",
            "is_draft": False
        }
    )
    
    post_id = create_response.json()["id"]
    
    # 置顶经验贴
    response = client.put(
        f"/api/posts/{post_id}/pin",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"is_pinned": True}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == "置顶状态更新成功"

# 测试草稿功能
def test_draft功能():
    """测试草稿保存和加载功能"""
    token = get_test_token()
    
    # 保存草稿
    create_response = client.post(
        "/api/posts/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "title": "测试草稿",
            "content": "草稿内容",
            "category": "测试分类",
            "is_draft": True
        }
    )
    
    assert create_response.status_code == 201
    post_data = create_response.json()
    assert post_data["is_draft"] == True
    
    # 获取草稿列表
    response = client.get(
        "/api/posts/drafts",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    drafts = response.json()
    assert isinstance(drafts, list)
    assert len(drafts) >= 1
