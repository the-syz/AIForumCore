# 论文上传页面重写实现计划

## 任务分解与优先级

### [ ] 任务 1: 创建新的论文上传页面
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 创建新的 PaperUpload.vue 文件，实现大的拖拽上传区域
  - 支持拖拽文件和点击选择文件
  - 实现文件上传进度显示
  - 上传后生成文件列表
  - 保留上传框，支持继续上传
- **Success Criteria**:
  - 页面加载显示大的拖拽上传区域
  - 支持拖拽文件到区域上传
  - 支持点击区域选择文件上传
  - 上传过程显示进度条
  - 上传完成后在下方显示文件列表
  - 上传框保持可见，可继续上传新文件
- **Test Requirements**:
  - `programmatic` TR-1.1: 页面加载后显示拖拽上传区域
  - `programmatic` TR-1.2: 拖拽PDF文件到区域能触发上传
  - `programmatic` TR-1.3: 点击上传区域能打开文件选择对话框
  - `programmatic` TR-1.4: 上传过程显示实时进度
  - `programmatic` TR-1.5: 上传完成后文件显示在列表中
  - `human-judgement` TR-1.6: 界面美观，操作流畅

### [ ] 任务 2: 实现文件列表管理功能
- **Priority**: P0
- **Depends On**: 任务 1
- **Description**:
  - 在文件列表中显示已上传的文件信息
  - 每个文件右侧添加删除和编辑按钮
  - 实现文件删除功能
  - 实现文件编辑功能（打开论文信息对话框）
- **Success Criteria**:
  - 文件列表显示文件名、大小、上传时间等信息
  - 每个文件有删除和编辑按钮
  - 点击删除按钮能移除文件
  - 点击编辑按钮能打开论文信息对话框
- **Test Requirements**:
  - `programmatic` TR-2.1: 文件列表显示正确的文件信息
  - `programmatic` TR-2.2: 点击删除按钮能成功删除文件
  - `programmatic` TR-2.3: 点击编辑按钮能打开对话框
  - `human-judgement` TR-2.4: 文件列表布局美观，操作便捷

### [ ] 任务 3: 实现论文信息编辑对话框
- **Priority**: P0
- **Depends On**: 任务 2
- **Description**:
  - 创建论文信息编辑对话框组件
  - 包含论文标题、作者、摘要、关键词、DOI、论文类型、分类等字段
  - 支持表单验证
  - 实现保存功能
- **Success Criteria**:
  - 对话框包含所有必要的论文信息字段
  - 表单验证正常工作
  - 保存按钮能提交修改
  - 取消按钮能关闭对话框
- **Test Requirements**:
  - `programmatic` TR-3.1: 对话框包含所有必要字段
  - `programmatic` TR-3.2: 表单验证能正确提示错误
  - `programmatic` TR-3.3: 保存按钮能提交数据
  - `human-judgement` TR-3.4: 对话框布局合理，操作直观

### [ ] 任务 4: 实现论文自动解析功能
- **Priority**: P0
- **Depends On**: 任务 1
- **Description**:
  - 上传论文后自动调用后端解析服务
  - 解析完成后将提取的信息填充到编辑对话框中
  - 显示解析进度
- **Success Criteria**:
  - 上传完成后自动触发解析
  - 显示解析进度
  - 解析完成后填充论文信息到对话框
  - 解析失败时显示错误信息
- **Test Requirements**:
  - `programmatic` TR-4.1: 上传后自动开始解析
  - `programmatic` TR-4.2: 显示解析进度条
  - `programmatic` TR-4.3: 解析完成后填充信息
  - `programmatic` TR-4.4: 解析失败时显示错误提示

### [ ] 任务 5: 更新路由配置
- **Priority**: P1
- **Depends On**: 任务 1
- **Description**:
  - 确保论文上传路由指向新的上传页面
  - 确保导航菜单中的上传链接正确
- **Success Criteria**:
  - 访问 /papers/upload 路径显示新的上传页面
  - 导航菜单中的上传链接能正确跳转
- **Test Requirements**:
  - `programmatic` TR-5.1: 访问 /papers/upload 显示新页面
  - `programmatic` TR-5.2: 导航菜单点击上传能跳转

### [ ] 任务 6: 测试与优化
- **Priority**: P1
- **Depends On**: 任务 1-5
- **Description**:
  - 测试所有功能是否正常工作
  - 优化用户体验
  - 修复可能的 bug
- **Success Criteria**:
  - 所有功能正常工作
  - 界面美观，操作流畅
  - 无明显 bug
- **Test Requirements**:
  - `programmatic` TR-6.1: 所有功能测试通过
  - `human-judgement` TR-6.2: 用户体验良好
  - `human-judgement` TR-6.3: 界面美观

## 技术实现要点

1. **拖拽上传**：使用 Element Plus 的 el-upload 组件，设置 `drag` 属性
2. **文件列表**：使用响应式数组存储上传的文件信息
3. **编辑对话框**：使用 el-dialog 组件，包含论文信息表单
4. **自动解析**：上传完成后调用后端 API 解析论文，使用 Promise 处理异步操作
5. **进度显示**：使用 el-progress 组件显示上传和解析进度
6. **表单验证**：使用 Element Plus 的表单验证功能

## 预期效果

- 进入上传页面后，看到一个大的拖拽上传区域
- 可以拖拽 PDF 文件到区域上传，也可以点击选择文件
- 上传过程显示进度条
- 上传完成后，文件显示在下方的文件列表中
- 上传框保持可见，可继续上传新文件
- 每个文件右侧有删除和编辑按钮
- 点击编辑按钮，弹出论文信息对话框，自动填充解析后的信息
- 可以修改论文信息并保存

## 注意事项

- 确保文件类型验证（只允许 PDF）
- 确保文件大小限制（不超过 20MB）
- 处理上传和解析过程中的错误
- 确保界面响应式，在不同设备上都能正常显示
- 优化用户体验，提供清晰的反馈信息