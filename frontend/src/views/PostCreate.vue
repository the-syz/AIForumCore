<template>
  <div class="post-create-container">
    <!-- 顶部操作栏 -->
    <div class="page-header">
      <h2>发布经验贴</h2>
      <div class="header-actions">
        <el-checkbox v-model="form.is_draft" size="large" style="margin-right: 20px;">保存为草稿</el-checkbox>
        <el-button @click="router.push('/posts')">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="loading">发布</el-button>
      </div>
    </div>
    
    <el-card>
      <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
        <!-- 标题 -->
        <el-form-item label="标题" prop="title">
          <el-input 
            v-model="form.title" 
            placeholder="请输入标题" 
            maxlength="100" 
            show-word-limit
            size="large"
          />
        </el-form-item>
        
        <!-- 分类 -->
        <el-form-item label="分类" prop="category">
          <el-select 
            v-model="form.category" 
            placeholder="请选择分类" 
            style="width: 200px"
            size="large"
          >
            <el-option label="学习经验" value="学习经验" />
            <el-option label="科研经验" value="科研经验" />
            <el-option label="生活经验" value="生活经验" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        
        <!-- 附件上传 -->
        <el-form-item label="附件">
          <el-upload
            action="#"
            :auto-upload="false"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            :on-preview="handleFilePreview"
            :file-list="fileList"
            :limit="5"
            multiple
          >
            <el-button type="primary" plain>选择文件</el-button>
            <template #tip>
              <div class="upload-tip">最多上传5个文件，支持图片、文档等格式</div>
            </template>
          </el-upload>
        </el-form-item>
        
        <!-- 富文本编辑器 -->
        <el-form-item label="内容" prop="content">
          <vue-ueditor-wrap
            v-model="form.content"
            editor-id="post-create-editor"
            :config="editorConfig"
            :editorDependencies="['ueditor.config.js', 'ueditor.all.js']"
            style="height: 450px"
          />
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { createPost } from '@/api/posts'
import { ElMessage } from 'element-plus'

const router = useRouter()
const formRef = ref<InstanceType<typeof import('element-plus')['ElForm']>>()
const loading = ref(false)

const form = ref({
  title: '',
  content: '',
  category: '',
  is_draft: false
})

const fileList = ref<any[]>([])

// 从本地存储加载草稿
const loadDraft = () => {
  const savedDraft = localStorage.getItem('postDraft')
  if (savedDraft) {
    try {
      const draft = JSON.parse(savedDraft)
      form.value = {
        title: draft.title || '',
        content: draft.content || '',
        category: draft.category || '',
        is_draft: draft.is_draft || false
      }
    } catch (error) {
      console.error('加载草稿失败:', error)
    }
  }
}

// 保存草稿到本地存储
const saveDraftToLocal = () => {
  const draftData = {
    title: form.value.title,
    content: form.value.content,
    category: form.value.category,
    is_draft: form.value.is_draft
  }
  localStorage.setItem('postDraft', JSON.stringify(draftData))
}

// 清除本地存储的草稿
const clearDraft = () => {
  localStorage.removeItem('postDraft')
}

// 监听表单变化，自动保存草稿
watch(
  [() => form.value.title, () => form.value.content, () => form.value.category],
  () => {
    saveDraftToLocal()
  },
  { deep: true }
)

// 组件挂载时加载草稿
onMounted(() => {
  loadDraft()
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }]
}

const editorConfig = {
  serverUrl: '/api/editor/upload',
  UEDITOR_HOME_URL: '/static/UEditorPlus/',
  UEDITOR_CORS_URL: '/static/UEditorPlus/',
  initialFrameWidth: '100%',
  initialFrameHeight: 450,
  autoHeightEnabled: false,
  autoFloatEnabled: true,
  wordCount: true,
  maximumWords: 10000
}

const handleFileChange = (file: any, newFileList: any[]) => {
  fileList.value = newFileList
}

const handleFileRemove = (file: any, newFileList: any[]) => {
  fileList.value = newFileList
}

const handleFilePreview = (file: any) => {
  console.log('文件预览:', file)
}

const handleSubmit = () => {
  formRef.value.validate((valid: boolean) => {
    if (valid) {
      loading.value = true
      const formData = new FormData()
      formData.append('title', form.value.title)
      formData.append('content', form.value.content)
      formData.append('category', form.value.category)
      formData.append('is_draft', form.value.is_draft.toString())
      
      fileList.value.forEach(file => {
        formData.append('files', file.raw)
      })
      
      createPost(formData).then(() => {
        ElMessage.success(form.value.is_draft ? '草稿保存成功' : '经验贴发布成功')
        clearDraft() // 提交成功后清除本地草稿
        router.push('/posts')
      }).catch(error => {
        ElMessage.error('发布失败，请重试')
        console.error('发布经验贴失败:', error)
      }).finally(() => {
        loading.value = false
      })
    }
  })
}
</script>

<style scoped lang="scss">
.post-create-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      margin: 0;
      color: #333;
      font-size: 22px;
      font-weight: 600;
    }
    
    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
  }
  
  :deep(.el-card__body) {
    padding: 40px;
    min-height: 600px;
  }
  
  :deep(.el-form-item__label) {
    font-weight: 500;
    color: #333;
    font-size: 14px;
  }
  
  .upload-tip {
    font-size: 12px;
    color: #909399;
    margin-top: 8px;
  }
}
</style>