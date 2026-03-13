import requests
import os

# 上传论文
def upload_paper(token):
    url = "http://localhost:8000/api/papers/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 论文文件路径
    paper_path = r"f:\AIForumCore\backend\tests\126-Physics-Informed Neural networks for heat transfer problems.pdf"
    
    if not os.path.exists(paper_path):
        print(f"论文文件不存在: {paper_path}")
        return None
    
    # 准备表单数据
    data = {
        "title": "Physics-Informed Neural networks for heat transfer problems",
        "authors": "Unknown",
        "category": "人工智能"
    }
    
    # 准备文件
    files = {
        "file": open(paper_path, "rb")
    }
    
    try:
        print("上传论文...")
        response = requests.post(url, headers=headers, data=data, files=files, timeout=30)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 201:
            print("论文上传成功！")
            return response.json()
        else:
            print("论文上传失败！")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None
    finally:
        if 'file' in files:
            files['file'].close()

# 上传经验贴
def upload_post(token):
    url = "http://localhost:8000/api/posts/posts/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 经验贴文件路径
    post_path = r"f:\AIForumCore\backend\tests\vscode配置latex教程.md"
    
    if not os.path.exists(post_path):
        print(f"经验贴文件不存在: {post_path}")
        return None
    
    # 读取文件内容
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 准备表单数据
    data = {
        "title": "VSCode配置LaTeX教程",
        "content": content,
        "category": "工具教程"
    }
    
    # 准备文件
    files = {
        "files": open(post_path, "rb")
    }
    
    try:
        print("上传经验贴...")
        response = requests.post(url, headers=headers, data=data, files=files, timeout=30)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
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
        if 'files' in files:
            files['files'].close()

if __name__ == "__main__":
    # 使用之前获取到的token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMyIsImV4cCI6MTc3Mjg1NTE0Nn0.tZb4oeagik47ig2oeRgtMteff72x-suzeqzHHNC3648"
    
    # 上传论文
    paper_result = upload_paper(token)
    
    # 上传经验贴
    post_result = upload_post(token)
