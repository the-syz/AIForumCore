import requests

# 测试根路径
try:
    print('测试根路径...')
    response = requests.get('http://localhost:8000/')
    print('根路径响应:', response.json())
except Exception as e:
    print('根路径测试失败:', str(e))

# 测试获取经验贴列表
try:
    print('测试获取经验贴列表...')
    response = requests.get('http://localhost:8000/api/posts/', params={
        'category': '',
        'skip': 0,
        'limit': 20
    })
    print('状态码:', response.status_code)
    print('响应内容:', response.json())
except Exception as e:
    print('获取经验贴列表失败:', str(e))