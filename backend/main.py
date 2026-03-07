# FastAPI 应用主文件

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

# 数据库初始化
from app.core.database import init_db, close_db

# API 路由
from app.api import auth, users, papers, posts, downloads


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
# app.include_router(forum.router, prefix="/api/forum", tags=["论坛"])
app.include_router(downloads.router, prefix="/api/downloads", tags=["下载中心"])
# app.include_router(search.router, prefix="/api/search", tags=["搜索"])
# app.include_router(ai.router, prefix="/api/ai", tags=["AI"])


@app.get("/")
async def root():
    """根路径"""
    return {"message": "Welcome to AIForum API"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
