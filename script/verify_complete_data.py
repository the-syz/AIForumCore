import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import init_db, close_db
from app.models.user import User
from app.models.paper import Paper
from app.models.post import Post
from tortoise import Tortoise
import asyncio

async def verify_complete_data():
    await init_db()
    
    try:
        conn = Tortoise.get_connection("default")
        
        print("=" * 60)
        print("论文详情:")
        print("=" * 60)
        papers = await conn.execute_query("SELECT id, title, authors, file_path, uploader_id FROM papers")
        for paper in papers[1]:
            print(f"ID: {paper['id']}")
            print(f"标题: {paper['title']}")
            print(f"作者: {paper['authors']}")
            print(f"文件路径: {paper['file_path']}")
            print(f"上传者ID: {paper['uploader_id']}")
            print("-" * 60)
        
        print("\n" + "=" * 60)
        print("经验贴详情:")
        print("=" * 60)
        posts = await conn.execute_query("SELECT id, title, category, author_id, LEFT(content, 100) as content_preview FROM posts")
        for post in posts[1]:
            print(f"ID: {post['id']}")
            print(f"标题: {post['title']}")
            print(f"分类: {post['category']}")
            print(f"作者ID: {post['author_id']}")
            print(f"内容预览: {post['content_preview']}...")
            print("-" * 60)
        
        print("\n" + "=" * 60)
        print("测试用户详情:")
        print("=" * 60)
        users = await conn.execute_query("SELECT id, name, student_id FROM users WHERE student_id = '20240010'")
        for user in users[1]:
            print(f"ID: {user['id']}")
            print(f"姓名: {user['name']}")
            print(f"学号: {user['student_id']}")
            print("-" * 60)
        
    except Exception as e:
        print(f"查询失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(verify_complete_data())
