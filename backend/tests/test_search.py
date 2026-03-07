import pytest
from fastapi.testclient import TestClient
from app.core.database import TORTOISE_ORM
from app.models.paper import Paper
from app.models.post import Post
from app.models.download import Download
from app.models.user import User
from tortoise import Tortoise

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

def test_search_papers(client):
    """测试搜索论文"""
    # 测试搜索
    response = client.get("/api/search/papers?keyword=Physics")
    
    assert response.status_code == 200, f"搜索失败: {response.text}"
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert isinstance(data["items"], list)

def test_search_posts(client):
    """测试搜索经验贴"""
    # 测试搜索
    response = client.get("/api/search/posts?keyword=VSCode")
    
    assert response.status_code == 200, f"搜索失败: {response.text}"
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert isinstance(data["items"], list)

def test_search_downloads(client):
    """测试搜索下载中心"""
    # 测试搜索
    response = client.get("/api/search/downloads?keyword=test")
    
    assert response.status_code == 200, f"搜索失败: {response.text}"
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert isinstance(data["items"], list)

def test_search_all(client):
    """测试综合搜索"""
    # 测试综合搜索
    response = client.get("/api/search/all?keyword=test")
    
    assert response.status_code == 200, f"搜索失败: {response.text}"
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert isinstance(data["items"], list)

def test_search_papers_pagination(client):
    """测试论文搜索分页"""
    # 测试第一页
    response = client.get("/api/search/papers?keyword=Physics&page=1&page_size=5")
    
    assert response.status_code == 200, f"搜索失败: {response.text}"
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 5

def test_search_posts_pagination(client):
    """测试经验贴搜索分页"""
    # 测试第一页
    response = client.get("/api/search/posts?keyword=VSCode&page=1&page_size=5")
    
    assert response.status_code == 200, f"搜索失败: {response.text}"
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 5

def test_search_empty_keyword(client):
    """测试空关键词搜索"""
    # 测试空关键词（应该返回所有结果）
    response = client.get("/api/search/papers?keyword=")
    
    # 空关键词应该返回所有结果
    assert response.status_code == 200, f"搜索失败: {response.text}"
    data = response.json()
    assert "total" in data
    assert "items" in data

def test_search_no_results(client):
    """测试无结果搜索"""
    # 测试一个不太可能存在的关键词
    response = client.get("/api/search/papers?keyword=xyzabc123nonexistent")
    
    assert response.status_code == 200, f"搜索失败: {response.text}"
    data = response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0
