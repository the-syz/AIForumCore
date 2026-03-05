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
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    print("数据库初始化成功")

if __name__ == "__main__":
    run_async(init_db())