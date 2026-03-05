# AIForum 数据库初始化实施计划

## [x] 任务 1.3.1：创建数据库和用户
- **Priority**: P1
- **Depends On**: 任务 1.1.1（基础开发工具安装）
- **Description**:
  - 登录 MySQL
  - 创建数据库：`CREATE DATABASE aiforum CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
  - 创建用户：`CREATE USER 'aiforum'@'localhost' IDENTIFIED BY 'password';`
  - 授权：`GRANT ALL PRIVILEGES ON aiforum.* TO 'aiforum'@'localhost';`
  - 刷新权限：`FLUSH PRIVILEGES;`
- **Success Criteria**:
  - 数据库 `aiforum` 已创建
  - 用户 `aiforum` 可正常登录
  - 用户有数据库操作权限
- **Test Requirements**:
  - `programmatic` TR-1.3.1.1: 执行 `SHOW DATABASES;` 能看到 aiforum 数据库
  - `programmatic` TR-1.3.1.2: 使用 aiforum 用户登录 MySQL 成功
  - `programmatic` TR-1.3.1.3: 执行 `SHOW GRANTS FOR 'aiforum'@'localhost';` 能看到授权信息
- **Notes**: 需要确保 MySQL 服务正在运行

## [x] 任务 1.3.2：配置Redis
- **Priority**: P1
- **Depends On**: 任务 1.1.1（基础开发工具安装）
- **Description**:
  - 启动 Redis 服务
  - 验证 Redis 连接：`redis-cli ping`
  - 配置 Redis 密码（可选）
  - 测试 Redis 基本操作
- **Success Criteria**:
  - Redis 服务正常运行
  - `redis-cli ping` 返回 `PONG`
  - 可进行基本的 set/get 操作
- **Test Requirements**:
  - `programmatic` TR-1.3.2.1: 执行 `redis-cli ping` 返回 `PONG`
  - `programmatic` TR-1.3.2.2: 执行 `redis-cli set test "Hello World"` 成功
  - `programmatic` TR-1.3.2.3: 执行 `redis-cli get test` 返回 `"Hello World"`
- **Notes**: 需要确保 Redis 服务正在运行