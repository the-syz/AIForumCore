import requests
import json

BASE_URL = "http://localhost:8000"

def login(username, password):
    url = f"{BASE_URL}/api/auth/login"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"username": username, "password": password}
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        if response.status_code == 200:
            return response.json()["access_token"]
        return None
    except Exception as e:
        print(f"登录失败: {e}")
        return None

def test_list_posts(token):
    """测试经验贴列表API"""
    url = f"{BASE_URL}/api/posts/posts/"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        print("测试经验贴列表API...")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"经验贴数量: {len(data)}")
            for post in data:
                print(f"  - ID: {post['id']}, 标题: {post['title']}, 分类: {post['category']}")
            return True
        return False
    except Exception as e:
        print(f"测试失败: {e}")
        return False

def test_get_post_detail(token, post_id):
    """测试经验贴详情API"""
    url = f"{BASE_URL}/api/posts/posts/{post_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        print(f"\n测试经验贴详情API (ID: {post_id})...")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"标题: {data['title']}")
            print(f"分类: {data['category']}")
            print(f"作者: {data['author_name']}")
            print(f"浏览量: {data['view_count']}")
            return True
        return False
    except Exception as e:
        print(f"测试失败: {e}")
        return False

def test_update_post(token, post_id):
    """测试经验贴修改API"""
    url = f"{BASE_URL}/api/posts/posts/{post_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        print(f"\n测试经验贴修改API (ID: {post_id})...")
        
        # 获取当前经验贴信息
        get_response = requests.get(url, headers=headers, timeout=10)
        if get_response.status_code != 200:
            print("获取经验贴信息失败")
            return False
        
        current_post = get_response.json()
        
        # 修改经验贴
        data = {
            "title": current_post['title'] + " (已修改)",
            "content": current_post['content'],
            "category": current_post['category']
        }
        
        response = requests.put(url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, json=data, timeout=10)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("经验贴修改成功")
            return True
        return False
    except Exception as e:
        print(f"测试失败: {e}")
        return False

def test_pin_post(token, post_id):
    """测试经验贴置顶API"""
    url = f"{BASE_URL}/api/posts/posts/{post_id}/pin"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        print(f"\n测试经验贴置顶API (ID: {post_id})...")
        response = requests.put(url, headers=headers, params={"is_pinned": True}, timeout=10)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("经验贴置顶成功")
            return True
        elif response.status_code == 403:
            print("权限不足（非管理员），符合预期")
            return True
        return False
    except Exception as e:
        print(f"测试失败: {e}")
        return False

def test_delete_post(token, post_id):
    """测试经验贴删除API"""
    url = f"{BASE_URL}/api/posts/posts/{post_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        print(f"\n测试经验贴删除API (ID: {post_id})...")
        response = requests.delete(url, headers=headers, timeout=10)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("经验贴删除成功")
            return True
        return False
    except Exception as e:
        print(f"测试失败: {e}")
        return False

def test_category_filter(token):
    """测试分类筛选功能"""
    url = f"{BASE_URL}/api/posts/posts/"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        print("\n测试分类筛选功能...")
        response = requests.get(url, headers=headers, params={"category": "工具教程"}, timeout=10)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"工具教程分类经验贴数量: {len(data)}")
            return True
        return False
    except Exception as e:
        print(f"测试失败: {e}")
        return False

if __name__ == "__main__":
    token = login("20240010", "123456")
    
    if not token:
        print("登录失败，无法继续测试")
        exit(1)
    
    print(f"登录成功，Token: {token[:30]}...")
    
    # 测试经验贴列表
    list_result = test_list_posts(token)
    
    # 测试分类筛选
    filter_result = test_category_filter(token)
    
    # 获取经验贴ID
    url = f"{BASE_URL}/api/posts/posts/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200 and len(response.json()) > 0:
        post_id = response.json()[0]['id']
        
        # 测试经验贴详情
        detail_result = test_get_post_detail(token, post_id)
        
        # 测试经验贴修改
        update_result = test_update_post(token, post_id)
        
        # 测试经验贴置顶
        pin_result = test_pin_post(token, post_id)
    else:
        print("没有经验贴数据，跳过详情、修改、置顶测试")
        detail_result = False
        update_result = False
        pin_result = False
    
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    print("=" * 60)
    print(f"经验贴列表API: {'✅ 通过' if list_result else '❌ 失败'}")
    print(f"分类筛选功能: {'✅ 通过' if filter_result else '❌ 失败'}")
    print(f"经验贴详情API: {'✅ 通过' if detail_result else '❌ 失败'}")
    print(f"经验贴修改API: {'✅ 通过' if update_result else '❌ 失败'}")
    print(f"经验贴置顶API: {'✅ 通过' if pin_result else '❌ 失败'}")
