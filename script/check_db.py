import pymysql

# 尝试使用aiforum用户连接数据库
try:
    # 连接到aiforum用户
    conn = pymysql.connect(
        host="localhost",
        user="aiforum",
        password="password",
        database="aiforum"
    )
    cursor = conn.cursor()
    
    print("成功连接到aiforum数据库！")
    
    # 测试简单查询
    cursor.execute("SELECT 1;")
    result = cursor.fetchone()
    print(f"查询结果: {result}")
    
    cursor.close()
    conn.close()
    
    print("\n任务1.3.1 完成：数据库和用户创建成功")
    
except Exception as e:
    print(f"错误: {e}")
    print("\n任务1.3.1 失败：数据库或用户创建失败")