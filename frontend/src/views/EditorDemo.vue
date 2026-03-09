<template>
  <div class="editor-demo">
    <h1>UEditor 富文本编辑器示例</h1>
    
    <el-card class="editor-card">
      <template #header>
        <div class="card-header">
          <span>发布经验贴</span>
          <el-button type="primary" @click="handleSubmit">发布</el-button>
        </div>
      </template>
      
      <el-form :model="form" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="form.title" placeholder="请输入标题" />
        </el-form-item>
        
        <el-form-item label="分类">
          <el-select v-model="form.category" placeholder="请选择分类">
            <el-option label="学习经验" value="学习经验" />
            <el-option label="科研心得" value="科研心得" />
            <el-option label="工具教程" value="工具教程" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="内容">
          <UEditor
            ref="editorRef"
            v-model="form.content"
            :height="400"
            @ready="handleEditorReady"
          />
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="preview-card">
      <template #header>
        <span>内容预览</span>
      </template>
      <div class="preview-content" v-html="form.content"></div>
    </el-card>
    
    <el-card class="actions-card">
      <template #header>
        <span>编辑器操作</span>
      </template>
      <el-button-group>
        <el-button @click="getContent">获取内容</el-button>
        <el-button @click="getContentTxt">获取纯文本</el-button>
        <el-button @click="clearContent">清空内容</el-button>
        <el-button @click="setDemoContent">设置示例内容</el-button>
      </el-button-group>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import UEditor from '@/components/UEditor.vue'
import { ElMessage } from 'element-plus'

const editorRef = ref<InstanceType<typeof UEditor> | null>(null)

const form = reactive({
  title: '',
  category: '',
  content: ''
})

const handleEditorReady = (editor: any) => {
  console.log('Editor is ready:', editor)
}

const handleSubmit = () => {
  if (!form.title) {
    ElMessage.warning('请输入标题')
    return
  }
  if (!form.content) {
    ElMessage.warning('请输入内容')
    return
  }
  
  console.log('提交内容:', form)
  ElMessage.success('发布成功！')
}

const getContent = () => {
  const content = editorRef.value?.getContent()
  console.log('编辑器内容:', content)
  ElMessage.info('内容已打印到控制台')
}

const getContentTxt = () => {
  const text = editorRef.value?.getContentTxt()
  console.log('纯文本内容:', text)
  ElMessage.info('纯文本已打印到控制台')
}

const clearContent = () => {
  editorRef.value?.clearContent()
  form.content = ''
  ElMessage.success('内容已清空')
}

const setDemoContent = () => {
  const demoContent = `
    <h2>这是一个示例标题</h2>
    <p>这是一段示例内容，包含<strong>加粗</strong>、<em>斜体</em>、<u>下划线</u>等格式。</p>
    <ul>
      <li>列表项1</li>
      <li>列表项2</li>
      <li>列表项3</li>
    </ul>
    <blockquote>这是一段引用文字</blockquote>
  `
  editorRef.value?.setContent(demoContent)
  form.content = demoContent
  ElMessage.success('示例内容已设置')
}
</script>

<style scoped>
.editor-demo {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  color: #409EFF;
  margin-bottom: 20px;
}

.editor-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-card {
  margin-bottom: 20px;
}

.preview-content {
  min-height: 200px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.actions-card {
  margin-bottom: 20px;
}
</style>
