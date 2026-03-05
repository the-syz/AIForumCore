# 数据库配置与初始化

from tortoise import Tortoise, run_async
from tortoise.config import Config
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql://root:password@localhost:3306/aiforum')

# Tortoise ORM 配置
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
                "app.models.forum",
                "app.models.download",
                "app.models.ai"
            ],
            "default_connection": "default",
        },
    },
}

async def init_db():
    """初始化数据库"""
    print("正在初始化数据库...")
    
    # 初始化 Tortoise ORM
    await Tortoise.init(config=TORTOISE_ORM)
    
    # 生成数据库表
    await Tortoise.generate_schemas()
    
    print("数据库初始化完成!")

async def close_db():
    """关闭数据库连接"""
    await Tortoise.close_connections()

# 同步初始化函数
def init_db_sync():
    """同步初始化数据库"""
    run_async(init_db())

# 示例：创建初始数据
async def create_initial_data():
    """创建初始数据"""
    from app.models.user import User
    
    # 检查是否已有管理员用户
    admin_count = await User.filter(role='teacher').count()
    
    if admin_count == 0:
        # 创建默认管理员用户
        admin = await User.create(
            name="管理员",
            student_id="admin",
            grade="",
            email="admin@example.com",
            password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # 密码: admin123
            role="teacher",
            is_admin=True
        )
        print(f"创建默认管理员用户: {admin.name}")

# 运行示例
if __name__ == "__main__":
    # 初始化数据库
    init_db_sync()
    
    # 创建初始数据
    run_async(create_initial_data())
    
    # 关闭连接
    run_async(close_db())
