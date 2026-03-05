# AIForum 用户认证模块实施计划

## [/] 子任务 1：实现密码加密和验证
- **Priority**: P0
- **Depends On**: 任务 T2-001（数据库模型设计）
- **Description**:
  - 创建安全模块，实现密码哈希和验证功能
  - 使用passlib库进行bcrypt加密
  - 提供密码哈希生成和验证函数
- **Success Criteria**:
  - 密码加密功能正常
  - 密码验证功能正常
- **Test Requirements**:
  - `programmatic` TR-1.1: 密码哈希生成成功
  - `programmatic` TR-1.2: 密码验证正确
- **Notes**: 使用passlib[bcrypt]库

## [ ] 子任务 2：实现JWT Token生成和验证
- **Priority**: P0
- **Depends On**: 子任务 1
- **Description**:
  - 实现JWT Token生成功能
  - 实现JWT Token验证功能
  - 配置Token过期时间
  - 从环境变量获取密钥
- **Success Criteria**:
  - Token生成功能正常
  - Token验证功能正常
  - Token过期机制正常
- **Test Requirements**:
  - `programmatic` TR-2.1: Token生成成功
  - `programmatic` TR-2.2: Token验证正确
  - `programmatic` TR-2.3: 过期Token验证失败
- **Notes**: 使用python-jose库

## [ ] 子任务 3：创建用户相关的Schema
- **Priority**: P0
- **Depends On**: 任务 T2-001（数据库模型设计）
- **Description**:
  - 创建用户注册Schema
  - 创建用户登录Schema
  - 创建用户响应Schema
  - 创建用户更新Schema
- **Success Criteria**:
  - 所有Schema定义正确
  - 数据验证规则正确
- **Test Requirements**:
  - `programmatic` TR-3.1: Schema验证功能正常
  - `programmatic` TR-3.2: 数据类型和约束正确
- **Notes**: 使用Pydantic V2

## [ ] 子任务 4：实现用户注册API
- **Priority**: P0
- **Depends On**: 子任务 1, 子任务 3
- **Description**:
  - 实现用户注册接口
  - 验证学号唯一性
  - 密码加密存储
  - 返回用户信息
- **Success Criteria**:
  - 注册API正常工作
  - 学号重复时返回错误
  - 密码加密存储
- **Test Requirements**:
  - `programmatic` TR-4.1: 成功注册新用户
  - `programmatic` TR-4.2: 学号重复时返回400错误
- **Notes**: 验证请求数据的有效性

## [ ] 子任务 5：实现用户登录API
- **Priority**: P0
- **Depends On**: 子任务 1, 子任务 2, 子任务 3
- **Description**:
  - 实现用户登录接口
  - 支持学号/姓名登录
  - 验证密码正确性
  - 生成并返回JWT Token
- **Success Criteria**:
  - 登录API正常工作
  - 用户名或密码错误时返回错误
  - 成功登录返回Token
- **Test Requirements**:
  - `programmatic` TR-5.1: 正确凭据登录成功
  - `programmatic` TR-5.2: 错误凭据登录失败
  - `programmatic` TR-5.3: 登录成功返回Token
- **Notes**: 使用OAuth2PasswordRequestForm

## [ ] 子任务 6：实现密码修改API
- **Priority**: P0
- **Depends On**: 子任务 1, 子任务 2
- **Description**:
  - 实现密码修改接口
  - 验证当前密码
  - 设置新密码
- **Success Criteria**:
  - 密码修改API正常工作
  - 当前密码错误时返回错误
  - 密码修改成功
- **Test Requirements**:
  - `programmatic` TR-6.1: 正确当前密码修改成功
  - `programmatic` TR-6.2: 错误当前密码修改失败
- **Notes**: 需要用户登录状态

## [ ] 子任务 7：实现登出API
- **Priority**: P1
- **Depends On**: 子任务 2
- **Description**:
  - 实现用户登出接口
  - 处理Token失效
- **Success Criteria**:
  - 登出API正常工作
  - 登出后Token失效
- **Test Requirements**:
  - `programmatic` TR-7.1: 登出成功
  - `programmatic` TR-7.2: 登出后Token无法使用
- **Notes**: 可以使用Token黑名单

## [ ] 子任务 8：实现当前用户获取API
- **Priority**: P0
- **Depends On**: 子任务 2
- **Description**:
  - 实现获取当前用户信息接口
  - 从Token中提取用户信息
  - 返回用户详细信息
- **Success Criteria**:
  - 获取当前用户API正常工作
  - 未登录时返回错误
  - 成功返回用户信息
- **Test Requirements**:
  - `programmatic` TR-8.1: 登录状态下获取用户信息成功
  - `programmatic` TR-8.2: 未登录时返回401错误
- **Notes**: 使用依赖注入获取当前用户

## [ ] 子任务 9：配置OAuth2认证依赖
- **Priority**: P0
- **Depends On**: 子任务 2
- **Description**:
  - 配置OAuth2密码流
  - 创建认证依赖函数
  - 实现权限检查
- **Success Criteria**:
  - OAuth2配置正确
  - 认证依赖函数正常工作
  - 权限检查有效
- **Test Requirements**:
  - `programmatic` TR-9.1: 认证依赖正常工作
  - `programmatic` TR-9.2: 权限检查正确
- **Notes**: 用于保护需要认证的API

## [ ] 子任务 10：编写单元测试
- **Priority**: P1
- **Depends On**: 所有子任务
- **Description**:
  - 编写密码加密和验证测试
  - 编写JWT Token测试
  - 编写API功能测试
  - 编写边界情况测试
- **Success Criteria**:
  - 所有测试通过
  - 测试覆盖主要功能
  - 测试覆盖边界情况
- **Test Requirements**:
  - `programmatic` TR-10.1: 所有测试通过
  - `programmatic` TR-10.2: 测试覆盖率≥80%
- **Notes**: 使用pytest和pytest-asyncio