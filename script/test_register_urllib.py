import urllib.request
import urllib.error
import json

# 测试注册功能
def test_register():
    url = "http://localhost:8000/api/auth/register"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "name": "测试用户",
        "student_id": "20240002",
        "grade": "2024级",
        "email": "test2@example.com",
        "phone": "13800138001",
        "research_direction": "人工智能",
        "wechat": "test_wechat2",
        "password": "password123"
    }
    
    try:
        req = urllib.request.Request(url, method="POST")
        for key, value in headers.items():
            req.add_header(key, value)
        
        data_bytes = json.dumps(data).encode("utf-8")
        req.add_header("Content-Length", str(len(data_bytes)))
        
        with urllib.request.urlopen(req, data=data_bytes) as response:
            status_code = response.getcode()
            response_text = response.read().decode("utf-8")
            print(f"响应状态码: {status_code}")
            print(f"响应内容: {response_text}")
            
            if status_code == 200:
                print("注册成功！")
            else:
                print("注册失败！")
    except urllib.error.HTTPError as e:
        print(f"HTTP错误: {e.code} - {e.reason}")
        try:
            error_content = e.read().decode("utf-8")
            print(f"错误内容: {error_content}")
        except:
            pass
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    test_register()
