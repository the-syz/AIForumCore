import redis

try:
    # 尝试连接到Redis服务器
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    # 测试连接
    response = r.ping()
    print(f"Redis连接测试: {response}")
    
    # 测试基本操作
    r.set('test', 'Hello World')
    value = r.get('test')
    print(f"Redis set/get测试: {value}")
    
    print("\n任务1.3.2 完成：Redis配置成功")
    
except Exception as e:
    print(f"错误: {e}")
    print("\n任务1.3.2 失败：Redis连接失败")