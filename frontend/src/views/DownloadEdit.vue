<template>
  <div class="download-edit-container">
    <div class="page-header">
      <el-button @click="router.push('/downloads')">返回列表</el-button>
      <h2>编辑资源</h2>
    </div>
    
    <el-card v-loading="loading">
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
        
        <!-- 操作按钮 -->
        <el-form-item>
          <div class="form-actions">
            <el-button @click="router.push('/downloads')">取消</el-button>
            <el-button type="primary" @click="handleSubmit" :loading="submitting">保存</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getDownloadById, updateDownload } from '@/api/downloads'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()

const downloadId = Number(route.params.id)
const formRef = ref<InstanceType<typeof import('element-plus')['ElForm']>>()
const loading = ref(true)
const submitting = ref(false)

const form = ref({
  title: '',
  category: '',
  description: ''
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }]
}

const handleSubmit = () => {
  formRef.value.validate((valid: boolean) => {
    if (valid) {
      submitting.value = true
      updateDownload(downloadId, form.value).then(() => {
        ElMessage.success('资源更新成功')
        router.push(`/downloads/${downloadId}`)
      }).catch(error => {
        ElMessage.error('更新失败，请重试')
        console.error('更新资源失败:', error)
      }).finally(() => {
        submitting.value = false
      })
    }
  })
}

const loadDownloadDetail = async () => {
  loading.value = true
  try {
    const data = await getDownloadById(downloadId)
    form.value = {
      title: data.title,
      category: data.category,
      description: data.description
    }
  } catch (error) {
    ElMessage.error('获取资源详情失败')
    console.error('获取资源详情失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDownloadDetail()
})
</script>

<style scoped lang="scss">
.download-edit-container {
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
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
  }
}
</style>