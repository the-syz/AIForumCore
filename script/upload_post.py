import requests
import os

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
        "content": content[:1000],  # 只使用前1000个字符，减少数据大小
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
        import traceback
        traceback.print_exc()
        return None
    finally:
        if 'files' in files:
            files['files'].close()

if __name__ == "__main__":
    # 使用之前获取到的token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMyIsImV4cCI6MTc3Mjg1NTE0Nn0.tZb4oeagik47ig2oeRgtMteff72x-suzeqzHHNC3648"
    
    # 上传经验贴
    post_result = upload_post(token)
