import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import init_db, close_db
from app.models.user import User
from app.models.paper import Paper
from app.models.post import Post
from tortoise import Tortoise
import asyncio

async def verify_data():
    await init_db()
    
    try:
        conn = Tortoise.get_connection("default")
        
        print("查询论文数据...")
        papers = await conn.execute_query("SELECT id, title, authors FROM papers")
        print(f"论文数量: {len(papers[1])}")
        for paper in papers[1]:
            print(f"  - ID: {paper['id']}, 标题: {paper['title']}")
        
        print("\n查询经验贴数据...")
        posts = await conn.execute_query("SELECT id, title, category FROM posts")
        print(f"经验贴数量: {len(posts[1])}")
        for post in posts[1]:
            print(f"  - ID: {post['id']}, 标题: {post['title']}, 分类: {post['category']}")
        
    except Exception as e:
        print(f"查询失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(verify_data())
