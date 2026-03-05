import requests

# 测试注册API
def test_register():
    url = "http://localhost:8000/api/auth/register"
    data = {
        "name": "测试用户",
        "student_id": "20210001",
        "password": "password123"
    }
    response = requests.post(url, json=data)
    print(f"注册API响应状态码: {response.status_code}")
    print(f"注册API响应内容: {response.json()}")

# 测试登录API
def test_login():
    url = "http://localhost:8000/api/auth/login"
    data = {
        "username": "20210001",
        "password": "password123"
    }
    response = requests.post(url, data=data)
    print(f"登录API响应状态码: {response.status_code}")
    print(f"登录API响应内容: {response.json()}")

if __name__ == "__main__":
    print("测试注册API...")
    test_register()
    print("\n测试登录API...")
    test_login()
