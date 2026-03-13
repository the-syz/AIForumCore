import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import init_db, close_db
from app.models.user import User
from tortoise import Tortoise
import asyncio

async def main():
    await init_db()
    
    try:
        user = await User.get_or_none(student_id="20240010")
        if not user:
            print("测试用户不存在")
            return
        
        print("上传论文...")
        conn = Tortoise.get_connection("default")
        
        await conn.execute_query(
            """INSERT INTO papers 
               (title, authors, file_path, user_id, paper_type, upload_time, like_count, favorite_count, view_count) 
               VALUES (%s, %s, %s, %s, %s, NOW(), 0, 0, 0)""",
            ["Physics-Informed Neural networks for heat transfer problems", 
             "Unknown", 
             r"f:\AIForumCore\backend\tests\126-Physics-Informed Neural networks for heat transfer problems.pdf",
             user.id,
             "journal"]
        )
        print("论文上传成功！")
        
        print("上传经验贴...")
        post_path = r"f:\AIForumCore\backend\tests\vscode配置latex教程.md"
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        await conn.execute_query(
            """INSERT INTO posts 
               (title, content, category, author_id, created_at, updated_at, is_pinned, view_count, like_count, comment_count) 
               VALUES (%s, %s, %s, %s, NOW(), NOW(), 0, 0, 0, 0)""",
            ["VSCode配置LaTeX教程", content, "工具教程", user.id]
        )
        print("经验贴上传成功！")
        
    except Exception as e:
        print(f"操作失败，错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(main())
