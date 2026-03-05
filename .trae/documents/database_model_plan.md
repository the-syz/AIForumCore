# AIForum 数据库模型设计实施计划

## [x] 子任务 1：配置Tortoise ORM连接
- **Priority**: P0
- **Depends On**: 任务 1.3.1（数据库创建）
- **Description**:
  - 安装Tortoise ORM依赖
  - 配置数据库连接信息
  - 创建数据库初始化脚本
- **Success Criteria**:
  - Tortoise ORM依赖已安装
  - 数据库连接配置正确
  - 数据库初始化脚本已创建
- **Test Requirements**:
  - `programmatic` TR-1.1: 执行数据库初始化脚本无错误
  - `programmatic` TR-1.2: 数据库连接成功
- **Notes**: 使用环境变量中的数据库连接信息

## [x] 子任务 2：创建用户模型 (User)
- **Priority**: P0
- **Depends On**: 子任务 1
- **Description**:
  - 创建用户模型类
  - 定义用户字段（id, name, student_id, grade, email, phone, research_direction, wechat, password_hash, role, is_admin, created_at, updated_at）
  - 配置模型元数据
- **Success Criteria**:
  - 用户模型已创建
  - 字段定义正确
  - 模型关系配置正确
- **Test Requirements**:
  - `programmatic` TR-2.1: 模型能正确生成表结构
  - `programmatic` TR-2.2: 字段类型和约束正确
- **Notes**: 使用CharEnumField定义角色枚举

## [x] 子任务 3：创建论文模型 (Paper)
- **Priority**: P0
- **Depends On**: 子任务 1
- **Description**:
  - 创建论文模型类
  - 定义论文字段（id, title, authors, abstract, keywords, doi, paper_type, file_path, upload_time, user_id, like_count, favorite_count, view_count）
  - 配置与用户的关系
- **Success Criteria**:
  - 论文模型已创建
  - 字段定义正确
  - 与用户模型的关系配置正确
- **Test Requirements**:
  - `programmatic` TR-3.1: 模型能正确生成表结构
  - `programmatic` TR-3.2: 与用户模型的外键关系正确
- **Notes**: 支持不同类型的论文（期刊论文、学位论文等）

## [x] 子任务 4：创建经验贴模型 (Post)
- **Priority**: P0
- **Depends On**: 子任务 1
- **Description**:
  - 创建经验贴模型类
  - 定义经验贴字段（id, title, content, category, author_id, created_at, updated_at, is_pinned, view_count, like_count, comment_count）
  - 配置与用户的关系
- **Success Criteria**:
  - 经验贴模型已创建
  - 字段定义正确
  - 与用户模型的关系配置正确
- **Test Requirements**:
  - `programmatic` TR-4.1: 模型能正确生成表结构
  - `programmatic` TR-4.2: 与用户模型的外键关系正确
- **Notes**: 支持置顶功能和分类

## [x] 子任务 5：创建评论模型 (Comment)
- **Priority**: P0
- **Depends On**: 子任务 1, 子任务 4
- **Description**:
  - 创建评论模型类
  - 定义评论字段（id, content, user_id, post_id, parent_id, created_at, updated_at）
  - 配置与用户和经验贴的关系
- **Success Criteria**:
  - 评论模型已创建
  - 字段定义正确
  - 与用户和经验贴模型的关系配置正确
  - 支持评论回复功能
- **Test Requirements**:
  - `programmatic` TR-5.1: 模型能正确生成表结构
  - `programmatic` TR-5.2: 与用户和经验贴模型的外键关系正确
- **Notes**: 支持评论嵌套回复

## [x] 子任务 6：创建点赞和收藏模型 (Like, Favorite)
- **Priority**: P0
- **Depends On**: 子任务 1
- **Description**:
  - 创建点赞模型类
  - 创建收藏模型类
  - 定义字段（id, user_id, target_type, target_id, created_at）
  - 配置与用户的关系
- **Success Criteria**:
  - 点赞和收藏模型已创建
  - 字段定义正确
  - 与用户模型的关系配置正确
- **Test Requirements**:
  - `programmatic` TR-6.1: 模型能正确生成表结构
  - `programmatic` TR-6.2: 与用户模型的外键关系正确
- **Notes**: 支持对不同类型对象的点赞和收藏

## [x] 子任务 7：创建下载中心模型 (Download)
- **Priority**: P1
- **Depends On**: 子任务 1
- **Description**:
  - 创建下载中心模型类
  - 定义下载中心字段（id, title, description, file_path, upload_time, uploader_id, download_count, category）
  - 配置与用户的关系
- **Success Criteria**:
  - 下载中心模型已创建
  - 字段定义正确
  - 与用户模型的关系配置正确
- **Test Requirements**:
  - `programmatic` TR-7.1: 模型能正确生成表结构
  - `programmatic` TR-7.2: 与用户模型的外键关系正确
- **Notes**: 支持资源分类和下载次数统计

## [x] 子任务 8：创建AI对话模型 (AIConversation, AIMessage)
- **Priority**: P1
- **Depends On**: 子任务 1
- **Description**:
  - 创建AI对话模型类
  - 创建AI消息模型类
  - 定义字段（对话：id, user_id, topic, created_at, updated_at；消息：id, conversation_id, role, content, created_at）
  - 配置模型关系
- **Success Criteria**:
  - AI对话和消息模型已创建
  - 字段定义正确
  - 模型关系配置正确
- **Test Requirements**:
  - `programmatic` TR-8.1: 模型能正确生成表结构
  - `programmatic` TR-8.2: 模型间的关系配置正确
- **Notes**: 支持多轮对话和角色区分

## [x] 子任务 9：配置数据库初始化脚本
- **Priority**: P0
- **Depends On**: 所有模型创建完成
- **Description**:
  - 配置Tortoise ORM初始化
  - 配置自动表结构生成
  - 创建数据库初始化函数
- **Success Criteria**:
  - 数据库初始化脚本已配置
  - 自动表结构生成功能正常
- **Test Requirements**:
  - `programmatic` TR-9.1: 执行初始化脚本无错误
  - `programmatic` TR-9.2: 所有表结构正确生成
- **Notes**: 确保在应用启动时自动初始化数据库

## [x] 子任务 10：执行自动表结构生成
- **Priority**: P0
- **Depends On**: 子任务 9
- **Description**:
  - 执行数据库初始化
  - 验证表结构生成结果
  - 检查模型关系是否正确
- **Success Criteria**:
  - 所有表结构已生成
  - 模型关系配置正确
  - 数据库初始化成功
- **Test Requirements**:
  - `programmatic` TR-10.1: 数据库表结构生成成功
  - `programmatic` TR-10.2: 所有模型对应的表都已创建
- **Notes**: 确保数据库连接正常且权限足够