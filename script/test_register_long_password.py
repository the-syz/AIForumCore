import requests
import json

# 测试注册功能，使用长密码
def test_register():
    url = "http://localhost:8000/api/auth/register"
    headers = {"Content-Type": "application/json"}
    data = {
        "name": "测试用户",
        "student_id": "20240009",
        "grade": "2024级",
        "email": "test9@example.com",
        "phone": "13800138008",
        "research_direction": "人工智能",
        "wechat": "test_wechat9",
        "password": "a" * 100  # 100个字符的密码
    }
    
    try:
        print("发送注册请求...")
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("注册成功！")
        else:
            print("注册失败！")
    except Exception as e:
        print(f"请求失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_register()
