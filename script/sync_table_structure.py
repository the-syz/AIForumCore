import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import init_db, close_db
from tortoise import Tortoise
import asyncio

async def sync_table_structure():
    await init_db()
    
    try:
        conn = Tortoise.get_connection("default")
        
        print("开始同步papers表结构...")
        
        # 检查category字段是否存在
        result = await conn.execute_query("SHOW COLUMNS FROM papers LIKE 'category'")
        if len(result[1]) == 0:
            print("添加category字段...")
            await conn.execute_query("ALTER TABLE papers ADD COLUMN category VARCHAR(100) NULL AFTER paper_type")
            print("category字段添加成功！")
        else:
            print("category字段已存在")
        
        # 检查download_count字段是否存在
        result = await conn.execute_query("SHOW COLUMNS FROM papers LIKE 'download_count'")
        if len(result[1]) == 0:
            print("添加download_count字段...")
            await conn.execute_query("ALTER TABLE papers ADD COLUMN download_count INT DEFAULT 0 AFTER view_count")
            print("download_count字段添加成功！")
        else:
            print("download_count字段已存在")
        
        # 检查外键字段名
        result = await conn.execute_query("SHOW COLUMNS FROM papers LIKE 'user_id'")
        if len(result[1]) > 0:
            print("重命名user_id为uploader_id...")
            await conn.execute_query("ALTER TABLE papers CHANGE COLUMN user_id uploader_id INT")
            print("外键字段重命名成功！")
        else:
            print("uploader_id字段已存在")
        
        print("\n验证表结构...")
        papers_columns = await conn.execute_query("DESCRIBE papers")
        print("papers表字段:")
        for row in papers_columns[1]:
            print(f"  - {row['Field']}: {row['Type']}")
        
        print("\n表结构同步完成！")
        
    except Exception as e:
        print(f"同步失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(sync_table_structure())
