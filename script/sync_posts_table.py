import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import init_db, close_db
from tortoise import Tortoise
import asyncio

async def sync_posts_table():
    await init_db()
    
    try:
        conn = Tortoise.get_connection("default")
        
        print("开始同步posts表结构...")
        
        # 检查is_draft字段是否存在
        result = await conn.execute_query("SHOW COLUMNS FROM posts LIKE 'is_draft'")
        if len(result[1]) == 0:
            print("添加is_draft字段...")
            await conn.execute_query("ALTER TABLE posts ADD COLUMN is_draft TINYINT(1) DEFAULT 0 AFTER is_pinned")
            print("is_draft字段添加成功！")
        else:
            print("is_draft字段已存在")
        
        print("\n验证表结构...")
        posts_columns = await conn.execute_query("DESCRIBE posts")
        print("posts表字段:")
        for row in posts_columns[1]:
            print(f"  - {row['Field']}: {row['Type']}")
        
        print("\n表结构同步完成！")
        
    except Exception as e:
        print(f"同步失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(sync_posts_table())
