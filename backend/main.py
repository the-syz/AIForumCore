# FastAPI 应用主文件

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

# 数据库初始化
from app.core.database import init_db, close_db

# API 路由
from app.api import auth, users, papers, posts, downloads, forum, search, editor


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    print("正在初始化数据库...")
    await init_db()
    print("数据库初始化完成")
    yield
    # 关闭时
    print("正在关闭数据库连接...")
    await close_db()
    print("数据库连接已关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title="AIForum API",
    description="AI论坛后端API",
    version="1.0.0",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:80"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户"])
app.include_router(papers.router, prefix="/api/papers", tags=["论文"])
app.include_router(posts.router, prefix="/api/posts", tags=["经验贴"])
# app.include_router(comments.router, prefix="/api/comments", tags=["评论"])
app.include_router(downloads.router, prefix="/api/downloads", tags=["下载中心"])
app.include_router(forum.router, prefix="/api/forum", tags=["论坛"])
app.include_router(search.router, prefix="/api/search", tags=["搜索"])
app.include_router(editor.router, prefix="/api", tags=["富文本编辑器"])
# app.include_router(ai.router, prefix="/api/ai", tags=["AI"])


@app.get("/")
async def root():
    """根路径"""
    return {"message": "Welcome to AIForum API"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


# 临时路由：生成经验贴数据
@app.get("/api/generate-posts")
async def generate_posts():
    """生成经验贴数据"""
    try:
        from app.models.post import Post
        # 定义经验贴数据
        posts_data = [
            # 学习经验
            {
                "title": "高效学习方法分享",
                "content": "在大学学习中，我总结了一些高效的学习方法：\n1. 制定合理的学习计划\n2. 采用番茄工作法提高专注度\n3. 定期复习巩固知识\n4. 积极参与课堂讨论\n5. 利用多种学习资源\n\n这些方法帮助我在学习中取得了不错的成绩，希望对大家有所帮助。",
                "category": "学习经验",
                "author_id": 23
            },
            {
                "title": "如何准备期末考试",
                "content": "期末考试是对一学期学习成果的检验，以下是我的备考经验：\n1. 提前规划复习时间\n2. 整理课堂笔记和重点内容\n3. 做历年真题熟悉考试题型\n4. 组建学习小组互相帮助\n5. 保持良好的作息和心态\n\n通过这些方法，我在期末考试中取得了优异的成绩。",
                "category": "学习经验",
                "author_id": 25
            },
            # 科研经验
            {
                "title": "科研入门指南",
                "content": "对于刚进入科研领域的同学，我有以下建议：\n1. 选择感兴趣的研究方向\n2. 多阅读相关领域的论文\n3. 积极与导师和同学交流\n4. 学会使用科研工具和软件\n5. 保持耐心和毅力\n\n科研是一个长期的过程，需要不断积累和探索。",
                "category": "科研经验",
                "author_id": 38
            },
            {
                "title": "论文写作技巧",
                "content": "论文写作是科研的重要环节，以下是一些写作技巧：\n1. 明确研究问题和目标\n2. 构建清晰的论文结构\n3. 注意逻辑连贯和论证充分\n4. 规范引用和参考文献\n5. 反复修改和完善\n\n好的论文需要不断打磨和改进。",
                "category": "科研经验",
                "author_id": 23
            },
            # 生活经验
            {
                "title": "大学生活平衡指南",
                "content": "在大学生活中，如何平衡学习、社交和个人时间：\n1. 合理安排时间，制定日程表\n2. 学会说\"不\"，避免过度承诺\n3. 保持健康的生活习惯\n4. 培养兴趣爱好，丰富课余生活\n5. 建立良好的人际关系\n\n平衡的生活有助于提高学习效率和生活质量。",
                "category": "生活经验",
                "author_id": 25
            },
            {
                "title": "校园生活小贴士",
                "content": "在校园生活中，我总结了一些实用的小贴士：\n1. 熟悉校园环境和资源\n2. 学会使用图书馆和自习室\n3. 参加社团活动，拓展人脉\n4. 注意个人财物安全\n5. 保持积极乐观的心态\n\n这些小贴士帮助我更好地适应校园生活。",
                "category": "生活经验",
                "author_id": 38
            },
            # 其他
            {
                "title": "我的大学感悟",
                "content": "大学是人生中重要的成长阶段，我有以下感悟：\n1. 学会独立生活和思考\n2. 珍惜与同学和老师的相处时光\n3. 尝试新事物，挑战自己\n4. 明确未来目标，为之努力\n5. 保持好奇心和学习热情\n\n大学时光转瞬即逝，希望大家都能珍惜这段美好的时光。",
                "category": "其他",
                "author_id": 23
            },
            {
                "title": "未来规划分享",
                "content": "关于未来规划，我有以下建议：\n1. 了解自己的兴趣和优势\n2. 关注行业发展趋势\n3. 制定短期和长期目标\n4. 不断学习和提升自己\n5. 保持灵活性，适应变化\n\n未来充满不确定性，但有规划的人生会更加精彩。",
                "category": "其他",
                "author_id": 25
            }
        ]
        
        # 清空现有数据
        await Post.all().delete()
        
        # 创建经验贴
        created_posts = []
        for post_data in posts_data:
            post = await Post.create(
                title=post_data["title"],
                content=post_data["content"],
                category=post_data["category"],
                author_id=post_data["author_id"],
                is_pinned=False,
                is_draft=False,
                view_count=0,
                like_count=0,
                comment_count=0
            )
            created_posts.append(post)
        
        # 统计结果
        total = len(created_posts)
        categories = {}
        for post in created_posts:
            if post.category not in categories:
                categories[post.category] = 0
            categories[post.category] += 1
        
        return {
            "message": f"成功生成 {total} 篇经验贴",
            "total": total,
            "categories": categories
        }
    except Exception as e:
        return {
            "message": f"生成经验贴失败: {str(e)}",
            "error": str(e)
        }

# 简单测试路由
@app.get("/api/test")
async def test():
    """测试路由"""
    return {"message": "测试成功"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
