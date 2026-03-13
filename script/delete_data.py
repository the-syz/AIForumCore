import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import init_db, close_db
from tortoise import Tortoise
import asyncio

async def delete_data():
    await init_db()
    
    try:
        conn = Tortoise.get_connection("default")
        
        print("删除论文数据...")
        await conn.execute_query("DELETE FROM papers")
        print("论文数据已删除！")
        
        print("删除经验贴数据...")
        await conn.execute_query("DELETE FROM posts")
        print("经验贴数据已删除！")
        
        print("\n验证删除结果...")
        papers = await conn.execute_query("SELECT COUNT(*) as count FROM papers")
        posts = await conn.execute_query("SELECT COUNT(*) as count FROM posts")
        print(f"论文数量: {papers[1][0]['count']}")
        print(f"经验贴数量: {posts[1][0]['count']}")
        
    except Exception as e:
        print(f"删除失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(delete_data())
