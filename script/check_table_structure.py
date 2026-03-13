import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import init_db, close_db, TORTOISE_ORM
from tortoise import Tortoise
import asyncio

async def check_table_structure():
    await init_db()
    
    try:
        conn = Tortoise.get_connection("default")
        
        print("检查papers表结构...")
        papers_columns = await conn.execute_query("DESCRIBE papers")
        print("papers表字段:")
        for row in papers_columns[1]:
            print(f"  - {row['Field']}: {row['Type']}")
        
        print("\n检查posts表结构...")
        posts_columns = await conn.execute_query("DESCRIBE posts")
        print("posts表字段:")
        for row in posts_columns[1]:
            print(f"  - {row['Field']}: {row['Type']}")
        
    except Exception as e:
        print(f"检查失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(check_table_structure())
