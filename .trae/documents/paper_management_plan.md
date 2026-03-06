# AIForum - 论文管理模块实现计划

## 任务概览
**任务编号**: T2-004
**任务名称**: 论文管理模块
**预估工时**: 2天
**优先级**: P0
**依赖关系**: 
- T2-001 数据库模型设计
- T2-002 用户认证模块
- T2-009 文件存储模块

## 实现计划

### [x] 任务1: 实现文件存储模块（T2-009）
- **优先级**: P0
- **Depends On**: 无
- **Description**: 创建 `app/services/files.py` 文件，实现文件上传、存储、下载功能
- **Success Criteria**: 文件存储模块功能正常，支持文件上传和下载
- **Test Requirements**:
  - `programmatic` TR-1.1: 文件上传功能正常
  - `programmatic` TR-1.2: 文件存储路径正确
  - `programmatic` TR-1.3: 文件验证功能正常
- **Status**: 完成

### [x] 任务2: 创建论文解析服务
- **优先级**: P0
- **Depends On**: 任务1
- **Description**: 创建 `app/services/paper_parser.py` 文件，实现论文解析功能（PDF/DOCX）
- **Success Criteria**: 论文解析功能正常，能够提取论文元数据
- **Test Requirements**:
  - `programmatic` TR-2.1: PDF文件解析正常
  - `programmatic` TR-2.2: DOCX文件解析正常
  - `programmatic` TR-2.3: 元数据提取正确
- **Status**: 完成

### [x] 任务3: 创建论文相关的schemas
- **优先级**: P0
- **Depends On**: 无
- **Description**: 创建 `app/schemas/paper.py` 文件，定义论文相关的请求和响应模型
- **Success Criteria**: schemas定义正确，支持论文相关的API操作
- **Test Requirements**:
  - `programmatic` TR-3.1: 论文创建模型定义正确
  - `programmatic` TR-3.2: 论文响应模型定义正确
  - `programmatic` TR-3.3: 论文更新模型定义正确
- **Status**: 完成

### [/] 任务4: 实现论文上传API
- **优先级**: P0
- **Depends On**: 任务1, 任务2, 任务3
- **Description**: 实现 `/papers` POST 接口，支持论文上传和解析
- **Success Criteria**: API正常响应，论文上传和解析成功
- **Test Requirements**:
  - `programmatic` TR-4.1: 返回201状态码
  - `programmatic` TR-4.2: 论文文件正确存储
  - `programmatic` TR-4.3: 论文元数据正确提取

### [ ] 任务5: 实现论文列表API
- **优先级**: P0
- **Depends On**: 任务3
- **Description**: 实现 `/papers` GET 接口，返回论文列表
- **Success Criteria**: API正常响应，返回正确的论文列表
- **Test Requirements**:
  - `programmatic` TR-5.1: 返回200状态码
  - `programmatic` TR-5.2: 返回论文列表符合预期格式
  - `programmatic` TR-5.3: 支持分页参数

### [ ] 任务6: 实现论文详情API
- **优先级**: P0
- **Depends On**: 任务3
- **Description**: 实现 `/papers/{paper_id}` GET 接口，返回指定论文的详细信息
- **Success Criteria**: API正常响应，返回正确的论文详情
- **Test Requirements**:
  - `programmatic` TR-6.1: 返回200状态码
  - `programmatic` TR-6.2: 返回论文详情符合预期格式
  - `programmatic` TR-6.3: 论文不存在时返回404状态码

### [ ] 任务7: 实现论文修改API
- **优先级**: P0
- **Depends On**: 任务3
- **Description**: 实现 `/papers/{paper_id}` PUT 接口，修改指定论文的信息
- **Success Criteria**: API正常响应，论文信息更新成功
- **Test Requirements**:
  - `programmatic` TR-7.1: 返回200状态码
  - `programmatic` TR-7.2: 返回更新后的论文信息
  - `programmatic` TR-7.3: 数据库中论文信息已更新

### [ ] 任务8: 实现论文删除API
- **优先级**: P0
- **Depends On**: 任务1
- **Description**: 实现 `/papers/{paper_id}` DELETE 接口，删除指定论文
- **Success Criteria**: API正常响应，论文删除成功
- **Test Requirements**:
  - `programmatic` TR-8.1: 返回200状态码
  - `programmatic` TR-8.2: 数据库中论文已删除
  - `programmatic` TR-8.3: 相关文件已删除

### [ ] 任务9: 实现论文下载API
- **优先级**: P0
- **Depends On**: 任务1
- **Description**: 实现 `/papers/{paper_id}/download` GET 接口，下载指定论文
- **Success Criteria**: API正常响应，论文下载成功
- **Test Requirements**:
  - `programmatic` TR-9.1: 返回200状态码
  - `programmatic` TR-9.2: 下载的文件内容正确
  - `programmatic` TR-9.3: 下载次数统计正确

### [ ] 任务10: 实现论文搜索功能
- **优先级**: P0
- **Depends On**: 任务3
- **Description**: 实现 `/papers/search` GET 接口，支持论文搜索
- **Success Criteria**: API正常响应，搜索结果正确
- **Test Requirements**:
  - `programmatic` TR-10.1: 返回200状态码
  - `programmatic` TR-10.2: 搜索结果符合预期
  - `programmatic` TR-10.3: 支持关键词搜索

### [ ] 任务11: 编写单元测试
- **优先级**: P1
- **Depends On**: 任务4-10
- **Description**: 编写 `tests/test_papers.py` 文件，测试所有论文管理API接口
- **Success Criteria**: 所有测试用例通过
- **Test Requirements**:
  - `programmatic` TR-11.1: 测试文件存在
  - `programmatic` TR-11.2: 所有测试用例通过

### [ ] 任务12: 注册路由到主应用
- **优先级**: P0
- **Depends On**: 任务4-10
- **Description**: 更新 `main.py` 文件，注册论文管理路由
- **Success Criteria**: 路由注册成功，应用启动正常
- **Test Requirements**:
  - `programmatic` TR-12.1: 应用启动无错误
  - `programmatic` TR-12.2: 路由可正常访问

## 技术实现要点
1. 使用 FastAPI 框架实现API接口
2. 使用 Tortoise ORM 进行数据库操作
3. 使用 PyPDF2 和 python-docx 解析论文文件
4. 使用文件存储服务管理论文文件
5. 实现 OCR 功能处理扫描版PDF
6. 遵循 RESTful API 设计规范
7. 实现适当的错误处理和数据验证

## 预期成果
- 完整的论文管理模块API
- 支持论文上传、解析、展示、下载等功能
- 支持论文搜索功能
- 完善的单元测试覆盖
