# 数据库模型使用指南 (Tortoise ORM)

## 📚 模型结构

```
app/models/
├── __init__.py
├── user.py      # 用户模型
├── paper.py     # 论文模型
├── post.py      # 经验贴模型
├── comment.py   # 评论模型
├── forum.py     # 点赞和收藏模型
├── download.py  # 下载中心模型
└── ai.py        # AI对话模型
```

## 🛠️ 基本操作

### 1. 查询数据

```python
# 查询所有用户
users = await User.all()

# 条件查询
user = await User.get(student_id="2024001")

# 过滤查询
users = await User.filter(role="student").all()

# 排序查询
users = await User.all().order_by("created_at")

# 分页查询
users = await User.all().offset(10).limit(20)

# 关联查询
posts = await Post.filter(author_id=user.id).all()
```

### 2. 创建数据

```python
# 创建用户
user = await User.create(
    name="张三",
    student_id="2024001",
    grade="2024级",
    password_hash=get_password_hash("123456")
)

# 创建论文
paper = await Paper.create(
    title="论文标题",
    authors="张三, 李四",
    upload_user=user  # 外键关联
)
```

### 3. 更新数据

```python
# 更新单个字段
user.name = "张三 (更新)"
await user.save()

# 批量更新
await User.filter(role="student").update(grade="2024级")
```

### 4. 删除数据

```python
# 删除单个对象
await user.delete()

# 批量删除
await User.filter(grade="2023级").delete()
```

### 5. 关联操作

```python
# 一对多关系
posts = await user.posts.all()

# 多对一关系
author = await post.author

# 外键查询
posts = await Post.filter(author__name="张三").all()
```

## 🔧 数据库初始化

### 1. 初始化数据库

```python
# 在 main.py 中使用 lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时
    await init_db()
    yield
    # 关闭时
    await close_db()

app = FastAPI(
    title="AIForum API",
    lifespan=lifespan
)
```

### 2. 自动生成表结构

```python
# app/core/database.py
async def init_db():
    """初始化数据库"""
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
```

## 📝 注意事项

1. **异步操作**：Tortoise ORM 所有操作都是异步的，需要使用 `await`
2. **事务**：复杂操作建议使用事务
3. **性能**：大量数据操作时使用 `in_bulk` 或 `bulk_create`
4. **索引**：对频繁查询的字段添加索引
5. **关系**：合理设计外键关系，避免循环依赖

## 🚀 示例：完整的CRUD操作

```python
# 创建用户
user = await User.create(
    name="测试用户",
    student_id="test123",
    password_hash=get_password_hash("123456")
)

# 查询用户
found_user = await User.get(student_id="test123")

# 更新用户
found_user.email = "test@example.com"
await found_user.save()

# 删除用户
await found_user.delete()
```

## 📞 常见问题

### Q: 如何处理事务？

**A:** 使用 `transaction` 上下文管理器：

```python
from tortoise.transactions import in_transaction

async with in_transaction() as conn:
    # 操作1
    user = await User.create(name="测试", using_db=conn)
    # 操作2
    await Paper.create(title="测试论文", upload_user=user, using_db=conn)
    # 如果有异常，会自动回滚
```

### Q: 如何添加索引？

**A:** 在模型中添加 `indexes`：

```python
class User(models.Model):
    # ...
    class Meta:
        table = "users"
        indexes = [
            ("student_id", True),  # 唯一索引
            ("role", False),      # 普通索引
        ]
```

### Q: 如何执行原生SQL？

**A:** 使用 `RawSQL`：

```python
from tortoise.expressions import RawSQL

users = await User.filter(
    RawSQL("student_id LIKE ?", ["2024%"])
).all()
```

## 🎯 最佳实践

1. **模型设计**：遵循数据库设计规范，合理设置字段类型和长度
2. **命名规范**：使用小写蛇形命名法
3. **代码组织**：按功能模块化组织模型
4. **错误处理**：合理处理数据库异常
5. **测试**：编写单元测试验证数据库操作

---

通过以上指南，你应该能够熟练使用 Tortoise ORM 进行数据库操作了！