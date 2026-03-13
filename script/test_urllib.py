import urllib.request
import urllib.error
import json

# 测试API是否能正常访问
def test_api():
    # 测试健康检查端点
    url = "http://localhost:8000/health"
    
    try:
        print("测试健康检查端点...")
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            status_code = response.getcode()
            response_text = response.read().decode("utf-8")
            print(f"响应状态码: {status_code}")
            print(f"响应内容: {response_text}")
            
            if status_code == 200:
                print("API访问成功！")
                return True
            else:
                print("API访问失败！")
                return False
    except urllib.error.HTTPError as e:
        print(f"HTTP错误: {e.code} - {e.reason}")
        return False
    except Exception as e:
        print(f"请求失败: {e}")
        return False

if __name__ == "__main__":
    # 测试API
    test_api()
