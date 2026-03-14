# AIForum - 课题组学术交流平台

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green.svg)](https://fastapi.tiangolo.com/)
[![Vue](https://img.shields.io/badge/Vue.js-3.x-brightgreen.svg)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)

## 📖 项目简介

AIForum 是一个专为科研课题组设计的学术交流平台，旨在解决科研团队内部知识管理、论文共享、经验交流等实际需求。项目采用前后端分离架构，集成了基于 RAG 技术的智能问答系统，提供完整的学术资源管理和互动功能。

### 核心价值

- **效率提升**：学生可自主检索和下载论文，减少导师分发负担
- **知识复用**：经验贴沉淀问题解决方案，避免重复踩坑
- **协作增强**：评论、收藏等功能促进组内学术讨论
- **智能辅助**：AI 助手基于知识库提供智能问答，提升信息获取效率

## ✨ 主要功能

### 1. 论文管理
- 📄 支持 PDF、DOCX 格式论文上传
- 🔍 自动解析论文元数据（标题、作者、摘要、关键词等）
- 📑 论文列表展示、分类筛选、排序
- 💾 论文下载和收藏功能
- ✏️ 论文信息编辑和管理

### 2. 经验分享
- 📝 富文本编辑器支持图文混排
- 🏷️ 经验贴分类管理
- 👍 点赞、评论互动功能
- 📌 置顶功能（管理员）
- 📎 支持附件上传

### 3. 下载中心
- 📦 资源统一管理和分类
- 📥 资源上传和下载
- 🔍 资源检索功能

### 4. 用户管理
- 👥 学生、学生管理员、教师（管理员）三级角色
- 🔐 注册登录功能
- 👤 个人信息管理
- ⚙️ 用户权限管理（管理员）

### 5. AI 智能助手
- 🤖 基于 RAG 技术的智能问答
- 📚 引用相关文献回答问题
- 💬 对话历史记录
- 🔗 引用链接跳转

### 6. 全文搜索
- 🔎 支持论文、经验贴、下载中心的综合搜索
- ⚡ 快速检索，相关度排序
- 🎯 关键词高亮显示

## 🏗️ 技术架构

### 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue 3 | 3.x | 前端框架 |
| TypeScript | 5.x | 开发语言 |
| Element Plus | 2.x | UI 组件库 |
| Pinia | 2.x | 状态管理 |
| Vue Router | 4.x | 路由管理 |
| Vite | 5.x | 构建工具 |
| Axios | 1.x | HTTP 客户端 |

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.9+ | 开发语言 |
| FastAPI | 0.104+ | Web 框架 |
| Tortoise ORM | 0.20+ | 数据库 ORM |
| MySQL | 8.0 | 关系型数据库 |
| Redis | 6.x | 缓存和会话 |
| bcrypt | 4.x | 密码哈希 |
| python-jose | 3.x | JWT 认证 |

### AI 服务

| 技术 | 说明 |
|------|------|
| 智谱 GLM-4.5 | 对话模型 |
| 智谱 Embedding-3 | 文本嵌入模型 |
| FAISS | 向量数据库 |
| Free OCR API | OCR 识别（可选） |

### 部署架构

```
┌─────────────────────────────────────────────────────────────┐
│                    AIForum 系统架构                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   用户浏览器                                                 │
│       │                                                     │
│       ▼                                                     │
│   ┌─────────────┐                                          │
│   │   Nginx     │  ← 静态资源 + 反向代理                    │
│   │   (端口80)  │                                          │
│   └──────┬──────┘                                          │
│          │                                                  │
│          ├──────────────────┐                               │
│          ▼                  ▼                               │
│   ┌─────────────┐    ┌─────────────┐                       │
│   │  Frontend   │    │   Backend   │                       │
│   │  (Vue3)     │    │  (FastAPI)  │                       │
│   │  静态文件    │    │  (端口8000) │                       │
│   └─────────────┘    └──────┬──────┘                       │
│                             │                               │
│          ┌──────────────────┼──────────────────┐           │
│          ▼                  ▼                  ▼           │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│   │   MySQL     │    │   Redis     │    │  智谱AI API  │   │
│   │  (端口3306) │    │  (端口6379) │    │   (外部服务) │   │
│   └─────────────┘    └─────────────┘    └─────────────┘   │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐ │
│   │              文件存储 (uploads/)                      │ │
│   └─────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 快速开始

### 环境要求

- Docker 20.10+
- Docker Compose 2.x
- Git

### 部署步骤

#### 1. 克隆项目

```bash
git clone <repository-url>
cd AIForumCore
```

#### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入以下配置：

```env
# 数据库配置
MYSQL_ROOT_PASSWORD=your_secure_root_password
MYSQL_USER=aiforum
MYSQL_PASSWORD=your_secure_password

# JWT密钥（使用 openssl rand -hex 32 生成）
SECRET_KEY=your_secure_secret_key_at_least_32_characters

# 智谱AI API Key（支持5个Key轮换）
ZHIPU_API_KEY_1=your_zhipu_api_key_1
ZHIPU_API_KEY_2=your_zhipu_api_key_2
ZHIPU_API_KEY_3=your_zhipu_api_key_3
ZHIPU_API_KEY_4=your_zhipu_api_key_4
ZHIPU_API_KEY_5=your_zhipu_api_key_5

# OCR API Key（可选）
OCR_API_KEY=your_ocr_api_key

# 其他配置
DEBUG=false
```

#### 3. 启动服务

```bash
# 开发环境
docker-compose up -d

# 生产环境
docker-compose -f docker-compose.prod.yml up -d
```

#### 4. 初始化管理员账户

```bash
cd backend
python scripts/init_admin.py
```

#### 5. 访问应用

- 前端：http://localhost
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

### 本地开发

#### 后端开发

```bash
cd backend

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 📁 项目结构

```
AIForumCore/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic 模式
│   │   └── services/       # 业务逻辑
│   ├── data/               # 数据存储
│   ├── scripts/            # 辅助脚本
│   ├── tests/              # 测试文件
│   ├── main.py             # 应用入口
│   └── requirements.txt    # Python 依赖
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── api/            # API 调用
│   │   ├── components/     # 组件
│   │   ├── layouts/        # 布局
│   │   ├── router/         # 路由
│   │   ├── store/          # 状态管理
│   │   ├── views/          # 页面
│   │   └── main.ts         # 入口文件
│   ├── public/             # 静态资源
│   ├── nginx.conf          # Nginx 配置
│   └── package.json        # Node 依赖
├── docs/                   # 文档
│   ├── design/             # 设计文档
│   ├── tasks/              # 任务清单
│   └── 验收文档/           # 验收文档
├── scripts/                # 运维脚本
├── docker-compose.yml      # Docker Compose 配置
├── .env.example            # 环境变量示例
└── README.md               # 项目说明
```

## 🛠️ 维护指南

### 常见问题

#### 1. 服务无法启动

检查 Docker 容器状态：
```bash
docker-compose ps
```

查看日志：
```bash
docker-compose logs backend
docker-compose logs mysql
```

#### 2. 数据库连接失败

确认 MySQL 容器正在运行：
```bash
docker-compose exec mysql mysql -u aiforum -p
```

#### 3. AI 功能不工作

检查智谱 API Key 配置：
```bash
docker-compose exec backend python -c "import os; print(os.getenv('ZHIPU_API_KEY_1'))"
```

### 数据备份

```bash
# 备份数据库
docker-compose exec mysql mysqldump -u aiforum -p aiforum > backup.sql

# 备份上传文件
tar -czf uploads_backup.tar.gz backend/uploads/

# 备份向量数据库
tar -czf vector_index_backup.tar.gz backend/data/
```

### 数据恢复

```bash
# 恢复数据库
docker-compose exec -T mysql mysql -u aiforum -p aiforum < backup.sql

# 恢复上传文件
tar -xzf uploads_backup.tar.gz

# 恢复向量数据库
tar -xzf vector_index_backup.tar.gz
```

### 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose down
docker-compose build
docker-compose up -d
```

## 📚 相关文档

- [产品需求规格说明书](docs/PRD-产品需求规格说明书.md)
- [系统概要设计文档](docs/design/系统概要设计文档.md)
- [部署指南-容器化部署完整教程](docs/部署指南-容器化部署完整教程.md)
- [部署指南-Zeabur详细指南](docs/部署指南-Zeabur详细指南.md)
- [环境安装指南-Docker和Redis](docs/环境安装指南-Docker和Redis.md)
- [项目技术细节总结](docs/项目技术细节总结.md)

## 🔐 安全建议

1. **修改默认密码**：首次部署后立即修改所有默认密码
2. **JWT 密钥安全**：使用强随机密钥，定期更换
3. **API Key 保护**：不要将 API Key 提交到版本控制
4. **HTTPS 配置**：生产环境必须配置 HTTPS
5. **定期备份**：定期备份数据库和上传文件
6. **日志监控**：监控应用日志，及时发现异常

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👥 联系方式

如有问题，请提交 Issue 或联系项目维护者。

---

**祝您使用愉快！** 🎉
