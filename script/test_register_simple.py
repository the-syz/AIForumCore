import sys
import os

# 添加backend目录到Python搜索路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import init_db, close_db
from app.models.user import User
from app.core.security import get_password_hash
import asyncio

async def test_register_simple():
    # 初始化数据库
    await init_db()
    
    try:
        # 直接创建用户
        print("尝试创建用户...")
        
        # 生成密码哈希
        password_hash = get_password_hash("password123")
        print(f"密码哈希生成成功: {password_hash[:20]}...")
        
        # 创建用户
        user = await User.create(
            name="测试用户",
            student_id="20240003",
            grade="2024级",
            email="test3@example.com",
            phone="13800138002",
            research_direction="人工智能",
            wechat="test_wechat3",
            password_hash=password_hash
        )
        print(f"用户创建成功: {user.id}")
        
        # 测试查询用户
        user_from_db = await User.get(id=user.id)
        print(f"从数据库查询用户成功: {user_from_db.name}")
        
    except Exception as e:
        print(f"注册失败，错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭数据库连接
        await close_db()

if __name__ == "__main__":
    asyncio.run(test_register_simple())
