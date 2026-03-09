from tortoise import Tortoise
from app.core.database import TORTOISE_ORM
import asyncio

async def main():
    await Tortoise.init(config=TORTOISE_ORM)
    from app.models.user import User
    users = await User.all()
    print("Users in database:")
    for user in users:
        print(f"ID: {user.id}, Student ID: {user.student_id}, Name: {user.name}")
    await Tortoise.close()

if __name__ == "__main__":
    asyncio.run(main())