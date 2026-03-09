<template>
  <div class="download-upload-container">
    <div class="page-header">
      <el-button @click="router.push('/downloads')">返回列表</el-button>
      <h2>上传资源</h2>
    </div>
    
    <el-card>
      <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
        <!-- 标题 -->
        <el-form-item label="标题" prop="title">
          <el-input 
            v-model="form.title" 
            placeholder="请输入资源标题" 
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
            <el-option label="科研资源" value="科研资源" />
            <el-option label="常用文件" value="常用文件" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        
        <!-- 描述 -->
        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="form.description" 
            placeholder="请输入资源描述" 
            type="textarea"
            :rows="4"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        
        <!-- 文件上传 -->
        <el-form-item label="文件" prop="file">
          <el-upload
            v-model:file-list="fileList"
            :auto-upload="false"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            :limit="1"
            :before-upload="beforeUpload"
            accept=".pdf,.doc,.docx,.xls,.xlsx,.zip,.rar"
          >
            <el-button type="primary" plain>选择文件</el-button>
            <template #tip>
              <div class="upload-tip">
                支持上传：PDF、Word、Excel、压缩包等格式
              </div>
            </template>
          </el-upload>
        </el-form-item>
        
        <!-- 操作按钮 -->
        <el-form-item>
          <div class="form-actions">
            <el-button @click="router.push('/downloads')">取消</el-button>
            <el-button type="primary" @click="handleSubmit" :loading="loading">上传</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { uploadDownload } from '@/api/downloads'
import { ElMessage } from 'element-plus'

const router = useRouter()
const formRef = ref<InstanceType<typeof import('element-plus')['ElForm']>>()
const loading = ref(false)

const form = ref({
  title: '',
  category: '',
  description: ''
})

const fileList = ref<any[]>([])
const selectedFile = ref<File | null>(null)

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }]
}

const handleFileChange = (file: any, newFileList: any[]) => {
  fileList.value = newFileList
  if (newFileList.length > 0) {
    selectedFile.value = newFileList[0].raw
  } else {
    selectedFile.value = null
  }
}

const handleFileRemove = (file: any, newFileList: any[]) => {
  fileList.value = newFileList
  selectedFile.value = null
}

const beforeUpload = (file: File) => {
  const maxSize = 50 * 1024 * 1024 // 50MB
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过50MB')
    return false
  }
  return true
}

const handleSubmit = () => {
  formRef.value.validate((valid: boolean) => {
    if (valid) {
      if (!selectedFile.value) {
        ElMessage.error('请选择文件')
        return
      }
      
      loading.value = true
      const formData = new FormData()
      formData.append('title', form.value.title)
      formData.append('category', form.value.category)
      formData.append('description', form.value.description)
      formData.append('file', selectedFile.value)
      
      uploadDownload(formData).then(() => {
        ElMessage.success('资源上传成功')
        router.push('/downloads')
      }).catch(error => {
        ElMessage.error('上传失败，请重试')
        console.error('上传资源失败:', error)
      }).finally(() => {
        loading.value = false
      })
    }
  })
}
</script>

<style scoped lang="scss">
.download-upload-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  
  .page-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    gap: 15px;
    
    h2 {
      margin: 0;
      color: #333;
      font-size: 22px;
      font-weight: 600;
    }
  }
  
  :deep(.el-card__body) {
    padding: 30px;
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
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
  }
}
</style>