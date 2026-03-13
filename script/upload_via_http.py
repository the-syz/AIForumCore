import requests
import os
import json

BASE_URL = "http://localhost:8000"

def login(username, password):
    url = f"{BASE_URL}/api/auth/login"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"username": username, "password": password}
    
    try:
        print("登录获取token...")
        response = requests.post(url, headers=headers, data=data, timeout=10)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("登录成功！")
            return result["access_token"]
        else:
            print(f"登录失败: {response.text}")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def upload_paper(token):
    url = f"{BASE_URL}/api/papers/"
    headers = {"Authorization": f"Bearer {token}"}
    
    paper_path = r"f:\AIForumCore\backend\tests\126-Physics-Informed Neural networks for heat transfer problems.pdf"
    
    if not os.path.exists(paper_path):
        print(f"论文文件不存在: {paper_path}")
        return None
    
    data = {
        "title": "Physics-Informed Neural networks for heat transfer problems",
        "authors": "Unknown",
        "category": "人工智能"
    }
    
    files = {"file": ("paper.pdf", open(paper_path, "rb"), "application/pdf")}
    
    try:
        print("上传论文...")
        response = requests.post(url, headers=headers, data=data, files=files, timeout=120)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text[:500] if len(response.text) > 500 else response.text}")
        
        if response.status_code == 201:
            print("论文上传成功！")
            return response.json()
        else:
            print("论文上传失败！")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        files["file"][1].close()

def upload_post(token):
    url = f"{BASE_URL}/api/posts/posts/"
    headers = {"Authorization": f"Bearer {token}"}
    
    post_path = r"f:\AIForumCore\backend\tests\vscode配置latex教程.md"
    
    if not os.path.exists(post_path):
        print(f"经验贴文件不存在: {post_path}")
        return None
    
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    data = {
        "title": "VSCode配置LaTeX教程",
        "content": content,
        "category": "工具教程"
    }
    
    files = {"files": ("tutorial.md", open(post_path, "rb"), "text/markdown")}
    
    try:
        print("上传经验贴...")
        response = requests.post(url, headers=headers, data=data, files=files, timeout=60)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text[:200] if len(response.text) > 200 else response.text}")
        
        if response.status_code == 201:
            print("经验贴上传成功！")
            return response.json()
        else:
            print("经验贴上传失败！")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None
    finally:
        files["files"][1].close()

if __name__ == "__main__":
    token = login("20240010", "123456")
    
    if token:
        print(f"Token: {token[:30]}...")
        
        paper_result = upload_paper(token)
        post_result = upload_post(token)
        
        if paper_result and post_result:
            print("\n所有文件上传成功！")
        else:
            print("\n部分文件上传失败！")
