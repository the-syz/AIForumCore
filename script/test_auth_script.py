#!/usr/bin/env python3
"""
认证模块测试脚本
"""

import asyncio
import sys
import os

# 添加backend目录到Python搜索路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from fastapi.testclient import TestClient
from app.core.security import get_password_hash, create_access_token, verify_password
from app.core.database import init_db, close_db
from app.models.user import User
from main import app

client = TestClient(app)

async def test_password_hash():
    """测试密码加密和验证"""
    print("测试密码加密和验证...")
    password = "password123"
    hashed_password = get_password_hash(password)
    assert hashed_password != password
    assert verify_password(password, hashed_password)
    assert not verify_password("wrongpassword", hashed_password)
    print("✓ 密码加密和验证测试通过")

async def test_jwt_token():
    """测试JWT Token生成和验证"""
    print("测试JWT Token生成和验证...")
    user_id = "1"
    token = create_access_token(data={"sub": user_id})
    assert token
    print("✓ JWT Token测试通过")

async def test_register():
    """测试用户注册"""
    print("测试用户注册...")
    response = client.post(
        "/api/auth/register",
        json={
            "name": "测试用户",
            "student_id": "20240001",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "测试用户"
    assert data["student_id"] == "20240001"
    print("✓ 用户注册测试通过")
    return data["id"]

async def test_login():
    """测试用户登录"""
    print("测试用户登录...")
    response = client.post(
        "/api/auth/login",
        data={
            "username": "20240001",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    print("✓ 用户登录测试通过")
    return data["access_token"]

async def test_get_me(token):
    """测试获取当前用户信息"""
    print("测试获取当前用户信息...")
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "测试用户"
    assert data["student_id"] == "20240001"
    print("✓ 获取当前用户信息测试通过")

async def test_change_password(token):
    """测试修改密码"""
    print("测试修改密码...")
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
    print("✓ 修改密码测试通过")

async def test_logout(token):
    """测试用户登出"""
    print("测试用户登出...")
    response = client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "登出成功"
    print("✓ 用户登出测试通过")

async def test_invalid_login():
    """测试无效凭据登录"""
    print("测试无效凭据登录...")
    response = client.post(
        "/api/auth/login",
        data={
            "username": "不存在的用户",
            "password": "password123"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "用户名或密码错误"
    print("✓ 无效凭据登录测试通过")

async def test_duplicate_register():
    """测试重复学号注册"""
    print("测试重复学号注册...")
    response = client.post(
        "/api/auth/register",
        json={
            "name": "重复用户",
            "student_id": "20240001",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "学号已存在"
    print("✓ 重复学号注册测试通过")

async def main():
    """主测试函数"""
    try:
        # 初始化数据库
        await init_db()
        print("数据库初始化成功")
        
        # 运行测试
        await test_password_hash()
        await test_jwt_token()
        user_id = await test_register()
        token = await test_login()
        await test_get_me(token)
        await test_change_password(token)
        await test_logout(token)
        await test_invalid_login()
        await test_duplicate_register()
        
        # 清理测试数据
        user = await User.filter(student_id="20240001").first()
        if user:
            await user.delete()
            print("测试数据清理成功")
        
        print("\n🎉 所有测试通过！")
        
    except Exception as e:
        print(f"测试失败: {e}")
    finally:
        # 关闭数据库连接
        await close_db()
        print("数据库连接已关闭")

if __name__ == "__main__":
    asyncio.run(main())
