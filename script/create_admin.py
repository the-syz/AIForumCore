import sys
import os
import asyncio
from passlib.context import CryptContext

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.database import TORTOISE_ORM
from tortoise import Tortoise

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin():
    await Tortoise.init(config=TORTOISE_ORM)
    
    conn = Tortoise.get_connection("default")
    
    admin_data = {
        "name": "系统管理员",
        "student_id": "admin001",
        "email": "admin@aiforum.com",
        "password": "Admin@123456",
        "grade": "管理员",
        "role": "admin",
        "is_admin": True
    }
    
    password_hash = pwd_context.hash(admin_data["password"])
    
    try:
        await conn.execute_query(
            """INSERT INTO users 
               (name, student_id, email, password_hash, grade, role, is_admin, created_at, updated_at) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())""",
            [
                admin_data["name"],
                admin_data["student_id"],
                admin_data["email"],
                password_hash,
                admin_data["grade"],
                admin_data["role"],
                admin_data["is_admin"]
            ]
        )
        
        print("=" * 60)
        print("管理员用户创建成功！")
        print("=" * 60)
        print(f"用户名（学号）: {admin_data['student_id']}")
        print(f"密码: {admin_data['password']}")
        print(f"姓名: {admin_data['name']}")
        print(f"邮箱: {admin_data['email']}")
        print("=" * 60)
        print("请妥善保管登录信息！")
        
        result = await conn.execute_query(
            "SELECT id, name, student_id, is_admin, role FROM users WHERE student_id = %s",
            [admin_data["student_id"]]
        )
        
        if result[1]:
            user = result[1][0]
            print(f"\n用户ID: {user['id']}")
            print(f"角色: {user['role']}")
            print(f"管理员权限: {'是' if user['is_admin'] else '否'}")
        
    except Exception as e:
        if "Duplicate entry" in str(e):
            print("该学号已存在，尝试更新为管理员...")
            await conn.execute_query(
                "UPDATE users SET is_admin = 1, role = 'admin' WHERE student_id = %s",
                [admin_data["student_id"]]
            )
            print("已将用户更新为管理员！")
            print(f"学号: {admin_data['student_id']}")
            print(f"密码: {admin_data['password']}")
        else:
            print(f"创建失败: {str(e)}")
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(create_admin())
