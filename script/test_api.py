import requests

# 测试API是否能正常访问
def test_api(token):
    # 测试获取当前用户信息
    url = "http://localhost:8000/api/auth/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        print("测试获取当前用户信息...")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("API访问成功！")
            return True
        else:
            print("API访问失败！")
            return False
    except Exception as e:
        print(f"请求失败: {e}")
        return False

if __name__ == "__main__":
    # 使用之前获取到的token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMyIsImV4cCI6MTc3Mjg1NTE0Nn0.tZb4oeagik47ig2oeRgtMteff72x-suzeqzHHNC3648"
    
    # 测试API
    test_api(token)
