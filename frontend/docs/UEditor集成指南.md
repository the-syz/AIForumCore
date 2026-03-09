# UEditor 富文本编辑器集成指南

## 概述

UEditor是由百度web前端研发部开发的所见即所得富文本web编辑器，具有轻量、可定制、注重用户体验等特点。

## 当前项目中的文件结构

```
frontend/
├── public/
│   └── ueditor/              # UEditor核心文件
│       ├── _src/             # 源码文件
│       ├── _examples/        # 示例文件
│       ├── dialogs/          # 对话框资源
│       ├── lang/             # 语言包
│       ├── themes/           # 主题样式
│       ├── ueditor.config.js # 配置文件
│       ├── demo.html         # 演示页面
│       └── test.html         # 测试页面
├── src/
│   ├── components/
│   │   └── UEditor.vue      # Vue封装组件
│   ├── types/
│   │   └── ueditor.d.ts      # TypeScript类型声明
│   └── views/
│       └── EditorDemo.vue    # 使用示例
```

## 已准备好的内容

| 项目 | 状态 | 说明 |
|------|------|------|
| UEditor源码文件 | ✅ 已有 | `public/ueditor/` 目录 |
| Vue封装组件 | ✅ 已创建 | `src/components/UEditor.vue` |
| TypeScript类型声明 | ✅ 已创建 | `src/types/ueditor.d.ts` |
| 使用示例 | ✅ 已创建 | `src/views/EditorDemo.vue` |
| 测试页面 | ✅ 已创建 | `public/ueditor/test.html` |

## 快速开始

### 1. 测试UEditor

直接在浏览器中打开以下文件测试UEditor功能：

```
http://localhost:5173/ueditor/test.html
```

或者访问官方示例：

```
http://localhost:5173/ueditor/_examples/completeDemo.html
```

### 2. 在Vue组件中使用

#### 方式一：使用封装组件（推荐）

```vue
<template>
  <UEditor
    v-model="content"
    :height="400"
    :config="editorConfig"
    @ready="handleReady"
    @change="handleChange"
  />
</template>

<script setup>
import { ref } from 'vue'
import UEditor from '@/components/UEditor.vue'

const content = ref('')

const editorConfig = {
  serverUrl: '/api/upload/ueditor',  // 后端上传接口
  toolbars: [[
    'bold', 'italic', 'underline',
    'insertimage', 'link',
    'preview', 'fullscreen'
  ]]
}

const handleReady = (editor) => {
  console.log('编辑器已准备好', editor)
}

const handleChange = (newContent) => {
  console.log('内容已变化', newContent)
}
</script>
```

#### 方式二：直接使用（简单场景）

```vue
<template>
  <div>
    <script id="editor" type="text/plain"></script>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount } from 'vue'

let editor = null

onMounted(() => {
  // 加载UEditor脚本
  const loadScript = (src) => {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script')
      script.src = src
      script.onload = resolve
      script.onerror = reject
      document.head.appendChild(script)
    })
  }

  // 初始化编辑器
  const initEditor = async () => {
    await loadScript('/ueditor/ueditor.config.js')
    await loadScript('/ueditor/_examples/editor_api.js')
    await loadScript('/ueditor/lang/zh-cn/zh-cn.js')
    
    editor = UE.getEditor('editor', {
      serverUrl: '/api/upload/ueditor',  // 覆盖默认配置
      initialFrameWidth: '100%',
      initialFrameHeight: 400
    })
  }
  
  initEditor()
})

onBeforeUnmount(() => {
  if (editor) {
    editor.destroy()
  }
})
</script>
```

## ⚠️ 重要配置修改

### 1. 修改 `ueditor.config.js` 中的 `serverUrl`

UEditor默认的`serverUrl`指向PHP后端，需要修改为您的后端API：

**文件位置**: `public/ueditor/ueditor.config.js`

```javascript
// 当前配置（第31行）
serverUrl: URL + "php/controller.php",

// 修改为您的后端接口
serverUrl: "/api/upload/ueditor",
```

### 2. 或者通过组件配置覆盖（推荐）

如果不想修改UEditor源文件，可以在初始化编辑器时传入配置覆盖默认值：

```javascript
editor = UE.getEditor('editor', {
  serverUrl: '/api/upload/ueditor',  // 覆盖默认配置
  initialFrameWidth: '100%',
  initialFrameHeight: 400
})
```

封装好的 `UEditor.vue` 组件已支持通过 `config` prop 传入自定义配置。

### 3. 后端接口实现

需要在后端实现以下接口：

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/upload/ueditor?action=config` | GET | 返回编辑器配置 |
| `/api/upload/ueditor?action=uploadimage` | POST | 图片上传 |
| `/api/upload/ueditor?action=uploadfile` | POST | 文件上传 |
| `/api/upload/ueditor?action=listimage` | GET | 图片管理 |

#### 配置接口返回示例

```json
{
  "imageUrl": "/api/upload/ueditor?action=uploadimage",
  "fileUrl": "/api/upload/ueditor?action=uploadfile",
  "imageManagerUrl": "/api/upload/ueditor?action=listimage",
  "imageManagerListPath": "/uploads/images/",
  "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
  "fileAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".pdf", ".doc", ".docx"]
}
```

## 配置说明

### 基础配置

在 `ueditor.config.js` 中可以配置以下选项：

```javascript
{
  // UEditor资源路径
  UEDITOR_HOME_URL: '/ueditor/',
  
  // 服务器统一请求接口路径
  serverUrl: '/api/upload/ueditor',
  
  // 编辑器初始宽度
  initialFrameWidth: '100%',
  
  // 编辑器初始高度
  initialFrameHeight: 400,
  
  // 是否自动长高
  autoHeightEnabled: false,
  
  // 是否启用自动保存
  autoSaveEnabled: true,
  
  // 自动保存间隔（毫秒）
  saveInterval: 500,
  
  // 是否开启字数统计
  wordCount: true,
  
  // 允许的最大字符数
  maximumWords: 10000
}
```

### 工具栏配置

```javascript
toolbars: [[
  'fullscreen', 'source', '|', 'undo', 'redo', '|',
  'bold', 'italic', 'underline', 'fontborder', 'strikethrough', '|',
  'forecolor', 'backcolor', '|',
  'justifyleft', 'justifycenter', 'justifyright', '|',
  'insertorderedlist', 'insertunorderedlist', '|',
  'paragraph', 'fontfamily', 'fontsize', '|',
  'link', 'unlink', '|',
  'simpleupload', 'insertimage', 'emotion', '|',
  'inserttable', 'horizontal', '|',
  'preview', 'help'
]]
```

### 精简工具栏配置

如果只需要基本功能，可以使用精简配置：

```javascript
toolbars: [[
  'bold', 'italic', 'underline', '|',
  'forecolor', 'backcolor', '|',
  'justifyleft', 'justifycenter', 'justifyright', '|',
  'insertorderedlist', 'insertunorderedlist', '|',
  'link', 'insertimage', '|',
  'preview', 'fullscreen'
]]
```

## 常用API

### 获取内容

```javascript
// 获取HTML内容
const html = editor.getContent()

// 获取纯文本内容
const text = editor.getContentTxt()

// 获取带格式的纯文本
const plainText = editor.getPlainTxt()

// 获取完整的HTML
const allHtml = editor.getAllHtml()
```

### 设置内容

```javascript
// 设置内容
editor.setContent('<p>新内容</p>')

// 追加内容
editor.setContent('<p>追加内容</p>', true)
```

### 其他操作

```javascript
// 判断是否有内容
const hasContent = editor.hasContents()

// 清空内容
editor.setContent('')

// 获取焦点
editor.focus()

// 失去焦点
editor.blur()

// 禁用编辑器
editor.setDisabled()

// 启用编辑器
editor.setEnabled()

// 销毁编辑器
editor.destroy()
```

## 快速集成步骤总结

1. **修改配置文件** - 修改 `public/ueditor/ueditor.config.js` 中的 `serverUrl`，或在组件中传入配置覆盖

2. **在Vue中使用** - 导入封装好的组件：
   ```vue
   <template>
     <UEditor v-model="content" :height="400" />
   </template>
   
   <script setup>
   import UEditor from '@/components/UEditor.vue'
   import { ref } from 'vue'
   const content = ref('')
   </script>
   ```

3. **实现后端接口** - 实现图片上传等后端接口

4. **启动测试** - 访问 `http://localhost:5173/ueditor/test.html` 验证编辑器是否正常工作

## 注意事项

1. **安全警告**: UEditor提供的后端代码仅为DEMO作用，不可直接用于生产环境
2. **文件上传**: 需要自行实现后端上传接口
3. **XSS防护**: 前端展示用户输入内容时需要进行XSS过滤
4. **性能优化**: 编辑器较大，建议按需加载
5. **跨域问题**: 如果前后端分离部署，需要配置跨域

## 替代方案

如果UEditor不满足需求，可以考虑以下替代方案：

| 编辑器 | 特点 | 推荐场景 |
|--------|------|----------|
| TinyMCE | 现代化、功能强大、社区活跃 | 企业级应用 |
| Quill | 轻量级、模块化、易于扩展 | 现代Web应用 |
| wangEditor | 国产、轻量、适合国内场景 | 中文项目 |
| TipTap | 基于ProseMirror、现代化、可扩展性强 | Vue/React项目 |

## 相关链接

- [UEditor官网](http://ueditor.baidu.com)
- [UEditor文档](http://ueditor.baidu.com/doc)
- [UEditor GitHub](https://github.com/fex-team/ueditor)
- [FAQ Wiki](https://github.com/fex-team/ueditor/wiki/FAQ)
