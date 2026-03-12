"""
初始化管理员用户脚本
用于部署后创建第一个管理员账号

使用方法:
    python scripts/init_admin.py
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tortoise import Tortoise
from app.core.database import TORTOISE_ORM
from app.core.security import get_password_hash
from app.models.user import User


async def init_admin():
    """初始化管理员用户"""
    print("=" * 50)
    print("AIForum 管理员初始化脚本")
    print("=" * 50)
    
    await Tortoise.init(config=TORTOISE_ORM)
    
    existing_admin = await User.filter(is_admin=True).first()
    if existing_admin:
        print(f"\n管理员用户已存在: {existing_admin.name} (学号: {existing_admin.student_id})")
        print("如需创建新管理员，请先删除现有管理员或通过管理后台操作。")
        await Tortoise.close_connections()
        return
    
    print("\n请输入管理员信息:")
    print("-" * 30)
    
    name = input("姓名: ").strip()
    if not name:
        print("错误: 姓名不能为空")
        await Tortoise.close_connections()
        return
    
    student_id = input("工号/学号: ").strip()
    if not student_id:
        print("错误: 工号不能为空")
        await Tortoise.close_connections()
        return
    
    existing_user = await User.filter(student_id=student_id).first()
    if existing_user:
        print(f"错误: 工号 {student_id} 已存在")
        await Tortoise.close_connections()
        return
    
    password = input("密码 (默认为工号): ").strip()
    if not password:
        password = student_id
        print(f"使用工号作为默认密码")
    
    role_input = input("角色 (1=教师/2=学生管理员，默认1): ").strip()
    if role_input == "2":
        role = "master"
        print("将创建学生管理员账号")
    else:
        role = "teacher"
        print("将创建教师管理员账号")
    
    try:
        user = await User.create(
            name=name,
            student_id=student_id,
            password_hash=get_password_hash(password),
            role=role,
            is_admin=True,
            grade="教师" if role == "teacher" else "2024级"
        )
        
        print("\n" + "=" * 50)
        print("管理员创建成功!")
        print("=" * 50)
        print(f"  姓名: {user.name}")
        print(f"  工号: {user.student_id}")
        print(f"  角色: {'教师' if role == 'teacher' else '学生管理员'}")
        print(f"  权限: 管理员")
        print("=" * 50)
        print("\n请妥善保管账号信息，现在可以使用该账号登录系统。")
        
    except Exception as e:
        print(f"\n创建失败: {str(e)}")
    
    await Tortoise.close_connections()


async def create_default_admin():
    """创建默认管理员（非交互式，用于自动化部署）"""
    await Tortoise.init(config=TORTOISE_ORM)
    
    existing_admin = await User.filter(is_admin=True).first()
    if existing_admin:
        print(f"管理员已存在: {existing_admin.name}")
        await Tortoise.close_connections()
        return
    
    default_student_id = "admin"
    default_password = "admin123"
    
    user = await User.create(
        name="系统管理员",
        student_id=default_student_id,
        password_hash=get_password_hash(default_password),
        role="teacher",
        is_admin=True,
        grade="教师"
    )
    
    print("=" * 50)
    print("默认管理员创建成功!")
    print("=" * 50)
    print(f"  工号: {default_student_id}")
    print(f"  密码: {default_password}")
    print("=" * 50)
    print("请登录后立即修改密码!")
    
    await Tortoise.close_connections()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="初始化管理员用户")
    parser.add_argument("--default", action="store_true", help="创建默认管理员（非交互式）")
    args = parser.parse_args()
    
    if args.default:
        asyncio.run(create_default_admin())
    else:
        asyncio.run(init_admin())
