import requests
import json

# 创建测试用户
def create_test_user():
    url = "http://localhost:8000/api/auth/register"
    headers = {"Content-Type": "application/json"}
    data = {
        "name": "测试用户",
        "student_id": "20240010",
        "grade": "2024级",
        "email": "test10@example.com",
        "phone": "13800138009",
        "research_direction": "人工智能",
        "wechat": "test_wechat10",
        "password": "123456"
    }
    
    try:
        print("创建测试用户...")
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("用户创建成功！")
            return response.json()
        else:
            print("用户创建失败！")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 登录获取token
def login(username, password):
    url = "http://localhost:8000/api/auth/login"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "username": username,
        "password": password
    }
    
    try:
        print("登录获取token...")
        response = requests.post(url, headers=headers, data=data, timeout=10)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("登录成功！")
            return response.json()
        else:
            print("登录失败！")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None

if __name__ == "__main__":
    # 创建测试用户
    user = create_test_user()
    if user:
        # 登录获取token
        token_data = login(user["student_id"], "123456")
        if token_data:
            print(f"获取到token: {token_data['access_token']}")
