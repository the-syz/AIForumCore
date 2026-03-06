import pytest
from fastapi.testclient import TestClient
from app.core.database import init_db, close_db
from app.models.user import User
from app.models.paper import Paper
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
    yield
    # 测试后清理
    await User.filter(student_id="20240001").delete()
    await Paper.filter().delete()
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

# 测试论文上传
def test_upload_paper():
    """测试论文上传功能"""
    token = get_test_token()
    
    # 测试PDF文件上传
    test_file_path = "tests/109-管壳式换热器研究与应用综述.pdf"
    if not os.path.exists(test_file_path):
        pytest.skip("测试文件不存在")
    
    with open(test_file_path, "rb") as f:
        response = client.post(
            "/api/papers/",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("test.pdf", f, "application/pdf")},
            data={
                "title": "测试论文",
                "authors": "测试作者",
                "abstract": "测试摘要",
                "keywords": "测试,关键词",
                "paper_type": "journal",
                "category": "测试分类"
            }
        )
    
    assert response.status_code == 201
    paper_data = response.json()
    assert paper_data["title"] == "测试论文"
    assert paper_data["authors"] == "测试作者"
    assert "file_path" in paper_data

# 测试论文列表
def test_list_papers():
    """测试获取论文列表"""
    token = get_test_token()
    
    response = client.get(
        "/api/papers/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    papers = response.json()
    assert isinstance(papers, list)

# 测试论文详情
def test_get_paper():
    """测试获取论文详情"""
    token = get_test_token()
    
    # 先上传一篇论文
    test_file_path = "tests/109-管壳式换热器研究与应用综述.pdf"
    if not os.path.exists(test_file_path):
        pytest.skip("测试文件不存在")
    
    with open(test_file_path, "rb") as f:
        upload_response = client.post(
            "/api/papers/",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("test.pdf", f, "application/pdf")},
            data={"title": "测试论文"}
        )
    
    paper_id = upload_response.json()["id"]
    
    # 获取论文详情
    response = client.get(
        f"/api/papers/{paper_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    paper_data = response.json()
    assert paper_data["id"] == paper_id
    assert paper_data["title"] == "测试论文"

# 测试论文搜索
def test_search_papers():
    """测试论文搜索功能"""
    token = get_test_token()
    
    response = client.get(
        "/api/papers/search",
        headers={"Authorization": f"Bearer {token}"},
        params={"keyword": "测试"}
    )
    
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)

# 测试论文下载
def test_download_paper():
    """测试论文下载功能"""
    token = get_test_token()
    
    # 先上传一篇论文
    test_file_path = "tests/109-管壳式换热器研究与应用综述.pdf"
    if not os.path.exists(test_file_path):
        pytest.skip("测试文件不存在")
    
    with open(test_file_path, "rb") as f:
        upload_response = client.post(
            "/api/papers/",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("test.pdf", f, "application/pdf")},
            data={"title": "测试论文"}
        )
    
    paper_id = upload_response.json()["id"]
    
    # 下载论文
    response = client.get(
        f"/api/papers/{paper_id}/download",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

# 测试论文更新
def test_update_paper():
    """测试论文更新功能"""
    token = get_test_token()
    
    # 先上传一篇论文
    test_file_path = "tests/109-管壳式换热器研究与应用综述.pdf"
    if not os.path.exists(test_file_path):
        pytest.skip("测试文件不存在")
    
    with open(test_file_path, "rb") as f:
        upload_response = client.post(
            "/api/papers/",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("test.pdf", f, "application/pdf")},
            data={"title": "测试论文"}
        )
    
    paper_id = upload_response.json()["id"]
    
    # 更新论文
    response = client.put(
        f"/api/papers/{paper_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "更新后的测试论文"}
    )
    
    assert response.status_code == 200
    paper_data = response.json()
    assert paper_data["title"] == "更新后的测试论文"

# 测试论文删除
def test_delete_paper():
    """测试论文删除功能"""
    token = get_test_token()
    
    # 先上传一篇论文
    test_file_path = "tests/109-管壳式换热器研究与应用综述.pdf"
    if not os.path.exists(test_file_path):
        pytest.skip("测试文件不存在")
    
    with open(test_file_path, "rb") as f:
        upload_response = client.post(
            "/api/papers/",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("test.pdf", f, "application/pdf")},
            data={"title": "测试论文"}
        )
    
    paper_id = upload_response.json()["id"]
    
    # 删除论文
    response = client.delete(
        f"/api/papers/{paper_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == "论文删除成功"
    
    # 验证论文已删除
    detail_response = client.get(
        f"/api/papers/{paper_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert detail_response.status_code == 404
