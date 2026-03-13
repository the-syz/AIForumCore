import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import init_db, close_db
from tortoise import Tortoise
import asyncio

async def cleanup_data():
    await init_db()
    
    try:
        conn = Tortoise.get_connection("default")
        
        print("清理论文数据，只保留最新一条...")
        await conn.execute_query("DELETE FROM papers WHERE id NOT IN (SELECT max_id FROM (SELECT MAX(id) as max_id FROM papers) as tmp)")
        
        print("清理经验贴数据，只保留最新一条...")
        await conn.execute_query("DELETE FROM posts WHERE id NOT IN (SELECT max_id FROM (SELECT MAX(id) as max_id FROM posts) as tmp)")
        
        print("\n验证清理结果...")
        papers = await conn.execute_query("SELECT COUNT(*) as count FROM papers")
        posts = await conn.execute_query("SELECT COUNT(*) as count FROM posts")
        print(f"论文数量: {papers[1][0]['count']}")
        print(f"经验贴数量: {posts[1][0]['count']}")
        
        print("\n最终数据:")
        paper = await conn.execute_query("SELECT id, title, authors FROM papers")
        print(f"论文: ID={paper[1][0]['id']}, 标题={paper[1][0]['title']}")
        
        post = await conn.execute_query("SELECT id, title, category FROM posts")
        print(f"经验贴: ID={post[1][0]['id']}, 标题={post[1][0]['title']}")
        
    except Exception as e:
        print(f"清理失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(cleanup_data())
