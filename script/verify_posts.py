import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import TORTOISE_ORM
from tortoise import Tortoise
import asyncio

async def verify_posts():
    await Tortoise.init(config=TORTOISE_ORM)
    
    conn = Tortoise.get_connection("default")
    
    print("查询经验贴数据...")
    result = await conn.execute_query("""
        SELECT p.id, p.title, p.category, p.author_id, u.name as author_name, 
               LEFT(p.content, 50) as content_preview
        FROM posts p
        LEFT JOIN users u ON p.author_id = u.id
        ORDER BY p.id DESC 
        LIMIT 10
    """)
    
    print("\n经验贴列表：")
    print("=" * 100)
    for row in result[1]:
        print(f"ID: {row['id']}")
        print(f"标题: {row['title']}")
        print(f"分类: {row['category']}")
        print(f"作者: {row['author_name']} (ID: {row['author_id']})")
        print(f"内容预览: {row['content_preview']}...")
        print("-" * 100)
    
    print("\n按分类统计：")
    stats = await conn.execute_query("""
        SELECT category, COUNT(*) as count
        FROM posts
        GROUP BY category
        ORDER BY count DESC
    """)
    
    for row in stats[1]:
        print(f"  {row['category']}: {row['count']}篇")
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(verify_posts())
