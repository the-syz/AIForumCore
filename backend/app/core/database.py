import sys
import os
from tortoise import Tortoise, run_async
from dotenv import load_dotenv

# 添加backend目录到Python搜索路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# 加载环境变量
load_dotenv()

# 获取数据库连接信息
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql://aiforum:password@localhost:3306/aiforum')

# 处理mysql+pymysql格式
if DATABASE_URL.startswith('mysql+pymysql://'):
    DATABASE_URL = DATABASE_URL.replace('mysql+pymysql://', 'mysql://')

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL
    },
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "app.models.paper",
                "app.models.post",
                "app.models.comment",
                "app.models.like",
                "app.models.favorite",
                "app.models.download",
                "app.models.ai"
            ],
            "default_connection": "default",
        },
    },
}

async def init_db():
    """初始化数据库"""
    # 初始化Tortoise ORM，使用全局状态
    await Tortoise.init(config=TORTOISE_ORM)
    # 生成数据库表结构
    await Tortoise.generate_schemas()
    print("数据库初始化成功")

async def close_db():
    """关闭数据库连接"""
    await Tortoise.close_connections()
    print("数据库连接已关闭")

async def ensure_db_initialized():
    """确保数据库连接池是激活的，如果不是则重新初始化"""
    if not Tortoise._inited:
        await init_db()
        return
    
    # 尝试执行一个简单的查询来验证连接池是否可用
    try:
        from tortoise.backends.mysql.client import MySQLClient
        # 直接获取默认连接
        if hasattr(Tortoise, '_connections') and 'default' in Tortoise._connections:
            conn = Tortoise._connections['default']
            # 尝试执行简单查询
            await conn.execute_query("SELECT 1")
    except Exception as e:
        print(f"检测到数据库连接池问题，正在重新初始化: {e}")
        try:
            await Tortoise.close_connections()
        except:
            pass
        # 重置Tortoise状态
        Tortoise._inited = False
        # 重新初始化
        await init_db()

if __name__ == "__main__":
    run_async(init_db())