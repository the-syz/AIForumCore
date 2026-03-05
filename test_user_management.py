import requests

# 基础URL
BASE_URL = "http://localhost:8000/api"

def test_register():
    """测试用户注册"""
    url = f"{BASE_URL}/auth/register"
    data = {
        "name": "测试用户",
        "student_id": "20210001",
        "password": "password123"
    }
    response = requests.post(url, json=data)
    print(f"注册API响应状态码: {response.status_code}")
    print(f"注册API响应内容: {response.json()}")
    return response.json()

def test_login():
    """测试用户登录"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "20210001",
        "password": "password123"
    }
    response = requests.post(url, data=data)
    print(f"登录API响应状态码: {response.status_code}")
    print(f"登录API响应内容: {response.json()}")
    return response.json()

def test_get_current_user(token):
    """测试获取当前用户信息"""
    url = f"{BASE_URL}/users/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(f"获取当前用户信息API响应状态码: {response.status_code}")
    print(f"获取当前用户信息API响应内容: {response.json()}")
    return response.json()

def test_update_current_user(token):
    """测试更新当前用户信息"""
    url = f"{BASE_URL}/users/me"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "email": "test@example.com",
        "phone": "13800138000"
    }
    response = requests.put(url, headers=headers, json=data)
    print(f"更新当前用户信息API响应状态码: {response.status_code}")
    print(f"更新当前用户信息API响应内容: {response.json()}")
    return response.json()

if __name__ == "__main__":
    print("=== 测试用户管理API ===")
    
    # 注册用户
    print("\n1. 测试注册API...")
    register_result = test_register()
    
    # 登录获取token
    print("\n2. 测试登录API...")
    login_result = test_login()
    token = login_result.get("access_token")
    
    if token:
        # 获取当前用户信息
        print("\n3. 测试获取当前用户信息API...")
        test_get_current_user(token)
        
        # 更新当前用户信息
        print("\n4. 测试更新当前用户信息API...")
        test_update_current_user(token)
    else:
        print("登录失败，无法获取token")
