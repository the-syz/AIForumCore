import requests
import json

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
    # 登录获取token
    token_data = login("20240010", "123456")
    if token_data:
        print(f"获取到token: {token_data['access_token']}")
