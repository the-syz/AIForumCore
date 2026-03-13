import requests
import json

# 测试注册功能
def test_register():
    url = "http://localhost:8000/api/auth/register"
    headers = {"Content-Type": "application/json"}
    data = {
        "name": "测试用户",
        "student_id": "20240001",
        "grade": "2024级",
        "email": "test@example.com",
        "phone": "13800138000",
        "research_direction": "人工智能",
        "wechat": "test_wechat",
        "password": "password123"
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code != 200:
            print("注册失败！")
        else:
            print("注册成功！")
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    test_register()
