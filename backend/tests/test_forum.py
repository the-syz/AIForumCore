import pytest
from fastapi.testclient import TestClient
from app.core.database import TORTOISE_ORM
from app.models.user import User
from app.models.post import Post
from app.models.paper import Paper
from app.core.security import create_access_token
from tortoise import Tortoise
import pytest_asyncio

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

def test_create_comment(client):
    """测试发表评论"""
    token = get_test_token(client)
    
    # 先获取一个帖子
    list_response = client.get(
        "/api/posts/posts/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if list_response.status_code != 200 or len(list_response.json()) == 0:
        pytest.skip("没有可用的帖子")
    
    post_id = list_response.json()[0]["id"]
    
    # 准备评论数据
    comment_data = {
        "post_id": post_id,
        "content": "这是一个测试评论",
        "parent_id": None
    }
    
    # 发送请求
    response = client.post(
        "/api/forum/comments",
        json=comment_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 验证响应
    assert response.status_code == 200, f"发表评论失败: {response.text}"
    data = response.json()
    assert data["content"] == "这是一个测试评论"

def test_list_comments(client):
    """测试获取评论列表"""
    token = get_test_token(client)
    
    # 先获取一个帖子
    list_response = client.get(
        "/api/posts/posts/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if list_response.status_code != 200 or len(list_response.json()) == 0:
        pytest.skip("没有可用的帖子")
    
    post_id = list_response.json()[0]["id"]
    
    # 发送请求获取评论列表
    response = client.get(
        f"/api/forum/comments?post_id={post_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 验证响应
    assert response.status_code == 200, f"获取评论列表失败: {response.text}"
    data = response.json()
    assert isinstance(data, list)

def test_toggle_like_post(client):
    """测试点赞/取消点赞帖子"""
    token = get_test_token(client)
    
    # 先获取一个帖子
    list_response = client.get(
        "/api/posts/posts/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if list_response.status_code != 200 or len(list_response.json()) == 0:
        pytest.skip("没有可用的帖子")
    
    post_id = list_response.json()[0]["id"]
    
    # 准备点赞数据
    like_data = {
        "target_type": "post",
        "target_id": post_id
    }
    
    # 发送请求添加点赞
    response = client.post(
        "/api/forum/likes",
        json=like_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 验证响应
    assert response.status_code == 200, f"点赞失败: {response.text}"
    
    # 再次发送请求取消点赞
    response = client.post(
        "/api/forum/likes",
        json=like_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 验证响应
    assert response.status_code == 200, f"取消点赞失败: {response.text}"

def test_toggle_like_paper(client):
    """测试点赞/取消点赞论文"""
    token = get_test_token(client)
    
    # 先获取一个论文
    list_response = client.get(
        "/api/papers/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if list_response.status_code != 200 or len(list_response.json()) == 0:
        pytest.skip("没有可用的论文")
    
    paper_id = list_response.json()[0]["id"]
    
    # 准备点赞数据
    like_data = {
        "target_type": "paper",
        "target_id": paper_id
    }
    
    # 发送请求添加点赞
    response = client.post(
        "/api/forum/likes",
        json=like_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 验证响应
    assert response.status_code == 200, f"点赞失败: {response.text}"

def test_toggle_favorite_post(client):
    """测试收藏/取消收藏帖子"""
    token = get_test_token(client)
    
    # 先获取一个帖子
    list_response = client.get(
        "/api/posts/posts/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if list_response.status_code != 200 or len(list_response.json()) == 0:
        pytest.skip("没有可用的帖子")
    
    post_id = list_response.json()[0]["id"]
    
    # 准备收藏数据
    favorite_data = {
        "target_type": "post",
        "target_id": post_id
    }
    
    # 发送请求添加收藏
    response = client.post(
        "/api/forum/favorites",
        json=favorite_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 验证响应
    assert response.status_code == 200, f"收藏失败: {response.text}"
    
    # 再次发送请求取消收藏
    response = client.post(
        "/api/forum/favorites",
        json=favorite_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 验证响应
    assert response.status_code == 200, f"取消收藏失败: {response.text}"

def test_toggle_favorite_paper(client):
    """测试收藏/取消收藏论文"""
    token = get_test_token(client)
    
    # 先获取一个论文
    list_response = client.get(
        "/api/papers/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if list_response.status_code != 200 or len(list_response.json()) == 0:
        pytest.skip("没有可用的论文")
    
    paper_id = list_response.json()[0]["id"]
    
    # 准备收藏数据
    favorite_data = {
        "target_type": "paper",
        "target_id": paper_id
    }
    
    # 发送请求添加收藏
    response = client.post(
        "/api/forum/favorites",
        json=favorite_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 验证响应
    assert response.status_code == 200, f"收藏失败: {response.text}"

def test_list_favorites(client):
    """测试获取收藏列表"""
    token = get_test_token(client)
    
    # 发送请求获取收藏列表
    response = client.get(
        "/api/forum/favorites",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 验证响应
    assert response.status_code == 200, f"获取收藏列表失败: {response.text}"
    data = response.json()
    assert isinstance(data, list)
