# AIForum 后端 API 文档

## 1. 简介

本文档描述了 AIForum 后端系统的 API 接口，包括认证、用户管理、论文管理、经验贴管理、下载中心、论坛功能和搜索功能等模块。

## 2. 认证

### 2.1 认证方式

系统使用 JWT (JSON Web Token) 进行身份认证。用户登录成功后，会获取到一个 JWT token，后续的请求需要在请求头中携带此 token。

### 2.2 认证流程

1. 用户通过 `/api/auth/login` 接口登录，获取 JWT token
2. 后续请求在请求头中携带 `Authorization: Bearer <token>`
3. 系统验证 token 有效性，确认用户身份

## 3. API 端点

### 3.1 认证模块

| 路径 | 方法 | 功能 | 请求体 (JSON) | 成功响应 (200 OK) |
|------|------|------|----------------|-------------------|
| `/api/auth/register` | POST | 用户注册 | `{"name": "用户名", "student_id": "学号", "password": "密码", "grade": "年级", "email": "邮箱", "phone": "电话", "research_direction": "研究方向", "wechat": "微信"}` | `{"id": 1, "name": "用户名", "student_id": "学号", ...}` |
| `/api/auth/login` | POST | 用户登录 | `{"username": "学号或姓名", "password": "密码"}` | `{"access_token": "JWT token", "user": {"id": 1, "name": "用户名", ...}}` |
| `/api/auth/logout` | POST | 用户登出 | N/A | `{"message": "登出成功"}` |
| `/api/auth/me` | GET | 获取当前用户信息 | N/A | `{"id": 1, "name": "用户名", ...}` |
| `/api/auth/change-password` | POST | 修改密码 | `{"old_password": "旧密码", "new_password": "新密码"}` | `{"message": "密码修改成功"}` |

### 3.2 用户模块

| 路径 | 方法 | 功能 | 请求体 (JSON) | 成功响应 (200 OK) |
|------|------|------|----------------|-------------------|
| `/api/users/me` | GET | 获取当前用户信息 | N/A | `{"id": 1, "name": "用户名", ...}` |
| `/api/users/me` | PUT | 更新当前用户信息 | `{"name": "新用户名", "email": "新邮箱", ...}` | `{"id": 1, "name": "新用户名", ...}` |
| `/api/users/` | GET | 获取用户列表（管理员） | N/A | `[{"id": 1, "name": "用户名", ...}]` |
| `/api/users/{user_id}` | GET | 获取用户详情（管理员） | N/A | `{"id": 1, "name": "用户名", ...}` |
| `/api/users/{user_id}/role` | PUT | 修改用户权限（管理员） | `{"role": "角色", "is_admin": true}` | `{"message": "权限更新成功"}` |
| `/api/users/{user_id}` | DELETE | 删除用户（管理员） | N/A | `{"message": "用户删除成功"}` |
| `/api/users/batch` | POST | 批量添加教师用户（管理员） | `[{"name": "教师名", "student_id": "工号", "password": "密码", ...}]` | `{"message": "成功创建 5 个教师用户"}` |

### 3.3 论文模块

| 路径 | 方法 | 功能 | 请求体 (Form Data) | 成功响应 (200 OK) |
|------|------|------|-------------------|-------------------|
| `/api/papers/` | POST | 上传论文 | `file: 文件, title: 标题, authors: 作者, abstract: 摘要, keywords: 关键词, doi: DOI, paper_type: 论文类型, category: 分类` | `{"id": 1, "title": "论文标题", ...}` |
| `/api/papers/` | GET | 获取论文列表 | N/A | `[{"id": 1, "title": "论文标题", ...}]` |
| `/api/papers/{paper_id}` | GET | 获取论文详情 | N/A | `{"id": 1, "title": "论文标题", ...}` |
| `/api/papers/{paper_id}` | PUT | 更新论文信息 | `{"title": "新标题", "authors": "新作者", ...}` | `{"id": 1, "title": "新标题", ...}` |
| `/api/papers/{paper_id}` | DELETE | 删除论文 | N/A | `{"message": "论文删除成功"}` |
| `/api/papers/{paper_id}/download` | GET | 下载论文 | N/A | 文件下载 |
| `/api/papers/search` | GET | 搜索论文 | N/A | `[{"id": 1, "title": "论文标题", ...}]` |

### 3.4 经验贴模块

| 路径 | 方法 | 功能 | 请求体 (Form Data) | 成功响应 (200 OK) |
|------|------|------|-------------------|-------------------|
| `/api/posts/` | POST | 发布经验贴 | `title: 标题, content: 内容, category: 分类, is_draft: 是否草稿, files: 附件` | `{"id": 1, "title": "经验贴标题", ...}` |
| `/api/posts/` | GET | 获取经验贴列表 | N/A | `[{"id": 1, "title": "经验贴标题", ...}]` |
| `/api/posts/drafts` | GET | 获取当前用户的草稿 | N/A | `[{"id": 1, "title": "草稿标题", ...}]` |
| `/api/posts/{post_id}` | GET | 获取经验贴详情 | N/A | `{"id": 1, "title": "经验贴标题", ...}` |
| `/api/posts/{post_id}` | PUT | 更新经验贴 | `{"title": "新标题", "content": "新内容", ...}` | `{"id": 1, "title": "新标题", ...}` |
| `/api/posts/{post_id}` | DELETE | 删除经验贴 | N/A | `{"message": "经验贴删除成功"}` |
| `/api/posts/{post_id}/pin` | PUT | 置顶/取消置顶经验贴（管理员） | `{"is_pinned": true}` | `{"message": "置顶状态更新成功"}` |

### 3.5 下载中心模块

| 路径 | 方法 | 功能 | 请求体 (Form Data) | 成功响应 (200 OK) |
|------|------|------|-------------------|-------------------|
| `/api/downloads/` | POST | 上传下载资源（仅管理员） | `title: 标题, description: 描述, category: 分类, file: 文件` | `{"id": 1, "title": "资源标题", ...}` |
| `/api/downloads/` | GET | 获取下载资源列表 | N/A | `[{"id": 1, "title": "资源标题", ...}]` |
| `/api/downloads/{download_id}` | GET | 获取下载资源详情 | N/A | `{"id": 1, "title": "资源标题", ...}` |
| `/api/downloads/{download_id}` | PUT | 更新下载资源（仅管理员） | `{"title": "新标题", "description": "新描述", ...}` | `{"id": 1, "title": "新标题", ...}` |
| `/api/downloads/{download_id}` | DELETE | 删除下载资源（仅管理员） | N/A | `{"message": "资源删除成功"}` |
| `/api/downloads/{download_id}/download` | GET | 下载资源文件 | N/A | 文件下载 |

### 3.6 论坛模块

| 路径 | 方法 | 功能 | 请求体 (JSON) | 成功响应 (200 OK) |
|------|------|------|----------------|-------------------|
| `/api/forum/comments` | POST | 发表评论 | `{"content": "评论内容", "post_id": 帖子ID, "parent_id": 父评论ID}` | `{"id": 1, "content": "评论内容", ...}` |
| `/api/forum/comments` | GET | 获取评论列表 | N/A | `[{"id": 1, "content": "评论内容", ...}]` |
| `/api/forum/likes` | POST | 点赞/取消点赞 | `{"target_type": "post", "target_id": 目标ID}` | `{"message": "点赞成功"}` |
| `/api/forum/favorites` | POST | 收藏/取消收藏 | `{"target_type": "post", "target_id": 目标ID}` | `{"message": "收藏成功"}` |
| `/api/forum/favorites` | GET | 获取收藏列表 | N/A | `[{"id": 1, "target_type": "post", "target_id": 1, ...}]` |

### 3.7 搜索模块

| 路径 | 方法 | 功能 | 请求体 (Query) | 成功响应 (200 OK) |
|------|------|------|----------------|-------------------|
| `/api/search/papers` | GET | 搜索论文 | `keyword: 搜索关键词, page: 页码, page_size: 每页数量` | `{"total": 10, "page": 1, "page_size": 20, "items": [...]}` |
| `/api/search/posts` | GET | 搜索经验贴 | `keyword: 搜索关键词, page: 页码, page_size: 每页数量` | `{"total": 5, "page": 1, "page_size": 20, "items": [...]}` |
| `/api/search/downloads` | GET | 搜索下载中心 | `keyword: 搜索关键词, page: 页码, page_size: 每页数量` | `{"total": 3, "page": 1, "page_size": 20, "items": [...]}` |
| `/api/search/all` | GET | 综合搜索 | `keyword: 搜索关键词, page: 页码, page_size: 每页数量` | `{"total": 18, "page": 1, "page_size": 20, "items": [...]}` |

## 4. 数据模型

### 4.1 用户模型 (User)

| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | int | 用户ID |
| name | str | 用户名 |
| student_id | str | 学号/工号 |
| grade | str | 年级 |
| email | str | 邮箱 |
| phone | str | 电话 |
| research_direction | str | 研究方向 |
| wechat | str | 微信 |
| password_hash | str | 密码哈希 |
| role | str | 角色 (student, student_admin, teacher) |
| is_admin | bool | 是否管理员 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### 4.2 论文模型 (Paper)

| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | int | 论文ID |
| title | str | 标题 |
| authors | str | 作者 |
| abstract | str | 摘要 |
| keywords | str | 关键词 |
| doi | str | DOI |
| paper_type | str | 论文类型 |
| category | str | 分类 |
| file_path | str | 文件路径 |
| uploader_id | int | 上传者ID |
| upload_time | datetime | 上传时间 |
| download_count | int | 下载次数 |

### 4.3 经验贴模型 (Post)

| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | int | 经验贴ID |
| title | str | 标题 |
| content | str | 内容 |
| category | str | 分类 |
| author_id | int | 作者ID |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |
| is_pinned | bool | 是否置顶 |
| is_draft | bool | 是否草稿 |
| view_count | int | 浏览次数 |
| like_count | int | 点赞次数 |
| comment_count | int | 评论次数 |

### 4.4 下载中心模型 (Download)

| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | int | 资源ID |
| title | str | 标题 |
| description | str | 描述 |
| category | str | 分类 |
| file_path | str | 文件路径 |
| file_name | str | 文件名 |
| uploader_id | int | 上传者ID |
| upload_time | datetime | 上传时间 |
| download_count | int | 下载次数 |

### 4.5 评论模型 (Comment)

| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | int | 评论ID |
| content | str | 评论内容 |
| user_id | int | 用户ID |
| post_id | int | 帖子ID |
| parent_id | int | 父评论ID |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### 4.6 点赞模型 (Like)

| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | int | 点赞ID |
| user_id | int | 用户ID |
| target_type | str | 目标类型 (post, paper, comment) |
| target_id | int | 目标ID |
| created_at | datetime | 创建时间 |

### 4.7 收藏模型 (Favorite)

| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | int | 收藏ID |
| user_id | int | 用户ID |
| target_type | str | 目标类型 (post, paper) |
| target_id | int | 目标ID |
| created_at | datetime | 创建时间 |

## 5. 错误处理

系统使用 HTTP 状态码来表示错误情况，常见的错误码如下：

| 状态码 | 描述 | 示例 |
|--------|------|------|
| 400 | 请求参数错误 | `{"detail": "学号已存在"}` |
| 401 | 未授权 | `{"detail": "用户名或密码错误"}` |
| 403 | 权限不足 | `{"detail": "权限不足"}` |
| 404 | 资源不存在 | `{"detail": "用户不存在"}` |
| 500 | 服务器内部错误 | `{"detail": "注册失败: 数据库连接错误"}` |

## 6. 注意事项

1. 所有需要认证的接口都需要在请求头中携带 `Authorization: Bearer <token>`
2. 文件上传接口的请求体使用 `multipart/form-data` 格式
3. 分页接口默认每页返回 20 条数据
4. 搜索接口支持关键词模糊搜索
5. 管理员接口需要用户具有管理员权限

## 7. 开发环境

- 后端框架：FastAPI
- 数据库：MySQL
- ORM：Tortoise ORM
- 认证：JWT
- 文件存储：本地文件系统

## 8. 部署

1. 安装依赖：`pip install -r requirements.txt`
2. 配置数据库连接：修改 `.env` 文件中的 `DATABASE_URL`
3. 启动服务：`uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

## 9. 测试

运行测试：`pytest tests/`
