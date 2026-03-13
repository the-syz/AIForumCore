import sys
import os

# 添加backend目录到Python搜索路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import init_db, close_db
from app.api.auth import register
from app.schemas.user import UserCreate
import asyncio

async def test_register_direct():
    # 初始化数据库
    await init_db()
    
    try:
        # 创建用户数据
        user_data = UserCreate(
            name="测试用户",
            student_id="20240001",
            grade="2024级",
            email="test@example.com",
            phone="13800138000",
            research_direction="人工智能",
            wechat="test_wechat",
            password="password123"
        )
        
        print("尝试直接调用注册函数...")
        result = await register(user_data)
        print(f"注册成功！结果: {result}")
    except Exception as e:
        print(f"注册失败，错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭数据库连接
        await close_db()

if __name__ == "__main__":
    asyncio.run(test_register_direct())
