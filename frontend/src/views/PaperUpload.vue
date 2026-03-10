<template>
  <div class="paper-upload-container">
    <div class="upload-header">
      <el-button @click="goBack">返回</el-button>
      <h2>上传论文</h2>
    </div>
    
    <!-- 拖拽上传区域 -->
    <div class="upload-area">
      <el-upload
        class="upload-dragger"
        :auto-upload="false"
        :on-change="handleFileChange"
        drag
        multiple
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          <em>拖拽文件到此处</em> 或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            请上传 PDF 文件，大小不超过 20MB
          </div>
        </template>
      </el-upload>
      
      <!-- 上传进度 -->
      <el-progress
        v-if="uploadProgress > 0 && uploadProgress < 100"
        :percentage="uploadProgress"
        :status="uploadStatus"
        style="margin-top: 20px; width: 100%"
      />
      
      <!-- 上传按钮 -->
      <el-button
        type="primary"
        @click="uploadFiles"
        :loading="uploading"
        :disabled="selectedFiles.length === 0 || uploading"
        style="margin-top: 20px"
      >
        上传选中文件
      </el-button>
      
      <!-- 上传队列状态 -->
      <div v-if="uploading" class="upload-queue-status" style="margin-top: 20px">
        <h4>上传队列状态</h4>
        <p v-if="currentUploadIndex < uploadQueue.length">
          当前上传: {{ uploadQueue[currentUploadIndex]?.name }}
        </p>
        <p>已处理: {{ currentUploadIndex }} / {{ uploadQueue.length }}</p>
        <p v-if="uploadError" class="error-message">{{ uploadError }}</p>
      </div>
    </div>
    
    <!-- 文件列表 -->
    <div class="file-list-section" v-if="uploadedFiles.length > 0">
      <h3>已上传文件</h3>
      <el-table :data="uploadedFiles" style="width: 100%">
        <el-table-column prop="name" label="文件名" />
        <el-table-column prop="size" label="大小" width="100">
          <template #default="scope">
            {{ formatFileSize(scope.row.size) }}
          </template>
        </el-table-column>
        <el-table-column prop="uploadTime" label="上传时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    
    <!-- 解析进度对话框 -->
    <el-dialog
      v-model="showProgressDialog"
      title="论文解析进度"
      width="500px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <div class="progress-content">
        <el-steps :active="currentStep" finish-status="success">
          <el-step title="文件上传" description="正在上传文件" />
          <el-step title="论文解析" description="正在解析论文内容" />
          <el-step title="保存数据" description="正在保存论文信息" />
        </el-steps>
        
        <el-progress
          :percentage="parseProgress"
          :status="parseStatus"
          style="margin-top: 20px"
        />
        
        <p class="progress-message">{{ progressMessage }}</p>
      </div>
    </el-dialog>
    
    <!-- 论文信息编辑对话框 -->
    <el-dialog
      v-model="showEditDialog"
      :title="editingFile ? '编辑论文信息' : '论文信息'"
      width="800px"
    >
      <el-form :model="paperForm" :rules="paperRules" ref="paperFormRef" label-width="100px">
        <el-form-item label="论文标题" prop="title">
          <el-input v-model="paperForm.title" placeholder="请输入论文标题" />
        </el-form-item>
        
        <el-form-item label="作者" prop="authors">
          <el-input v-model="paperForm.authors" placeholder="请输入作者，多个作者用逗号分隔" />
        </el-form-item>
        
        <el-form-item label="摘要" prop="abstract">
          <el-input v-model="paperForm.abstract" type="textarea" :rows="4" placeholder="请输入论文摘要" />
        </el-form-item>
        
        <el-form-item label="关键词" prop="keywords">
          <el-input v-model="paperForm.keywords" placeholder="请输入关键词，多个关键词用逗号分隔" />
        </el-form-item>
        
        <el-form-item label="DOI" prop="doi">
          <el-input v-model="paperForm.doi" placeholder="请输入DOI" />
        </el-form-item>
        
        <el-form-item label="论文类型" prop="paper_type">
          <el-select v-model="paperForm.paper_type" placeholder="请选择论文类型">
            <el-option label="期刊论文" value="journal" />
            <el-option label="会议论文" value="conference" />
            <el-option label="学位论文" value="thesis" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="研究领域" prop="category">
          <el-input v-model="paperForm.category" placeholder="请输入研究领域" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSavePaper" :loading="savingPaper">保存</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 重试对话框 -->
    <el-dialog
      v-model="showRetryDialog"
      title="上传失败"
      width="600px"
    >
      <div>
        <p>以下文件上传失败：</p>
        <el-list>
          <el-list-item v-for="(file, index) in failedFiles" :key="index">
            <div class="file-info">
              <div class="file-name">{{ file.name }}</div>
              <div class="error-message">{{ file.errorMessage }}</div>
              <div class="error-type" v-if="file.errorType">错误类型：{{ file.errorType }}</div>
            </div>
          </el-list-item>
        </el-list>
        <p style="margin-top: 20px; color: #666;">是否重试上传这些文件？</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showRetryDialog = false">取消</el-button>
          <el-button type="primary" @click="retryFailedFiles">重试</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import http from '@/api/http'
import { parsePaper, createPaper, updatePaper } from '@/api/papers'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'

const router = useRouter()

// 上传相关状态
const uploadUrl = '/api/papers/'
const uploadProgress = ref(0)
const uploadStatus = ref<'success' | 'exception' | 'warning' | ''>('')
const uploadedFiles = ref<any[]>([])
const selectedFiles = ref<any[]>([])
const uploadQueue = ref<any[]>([])
const failedFiles = ref<any[]>([])
const currentUploadIndex = ref(0)
const uploading = ref(false)
const uploadError = ref('')
const showRetryDialog = ref(false)

// 解析相关状态
const showProgressDialog = ref(false)
const currentStep = ref(0)
const parseProgress = ref(0)
const parseStatus = ref<'success' | 'exception' | 'warning' | ''>('')
const progressMessage = ref('')

// 编辑对话框状态
const showEditDialog = ref(false)
const paperFormRef = ref<any>(null)
const editingFile = ref<any>(null)
const savingPaper = ref(false)

// 论文表单
const paperForm = reactive({
  title: '',
  authors: '',
  abstract: '',
  keywords: '',
  doi: '',
  paper_type: '',
  category: ''
})

// 表单验证规则
const paperRules = {
  title: [{ required: true, message: '请输入论文标题', trigger: 'blur' }],
  authors: [{ required: true, message: '请输入作者', trigger: 'blur' }],
  abstract: [{ required: true, message: '请输入摘要', trigger: 'blur' }],
  keywords: [{ required: true, message: '请输入关键词', trigger: 'blur' }],
  paper_type: [{ required: true, message: '请选择论文类型', trigger: 'blur' }],
  category: [{ required: true, message: '请输入研究领域', trigger: 'blur' }]
}

// 返回论文列表页
const goBack = () => {
  router.push('/papers')
}

// 格式化文件大小
const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 处理文件选择
const handleFileChange = (file: any, fileList: any[]) => {
  // 验证文件类型和大小
  const isPDF = file.raw.type === 'application/pdf'
  const isLt20M = file.raw.size / 1024 / 1024 < 20

  if (!isPDF) {
    ElMessage.error('只能上传 PDF 文件!')
    return false
  }
  if (!isLt20M) {
    ElMessage.error('文件大小不能超过 20MB!')
    return false
  }

  // 添加到选中文件列表
  selectedFiles.value = fileList.map(item => item.raw)
}

// 上传文件
const uploadFiles = async () => {
  if (selectedFiles.value.length === 0) {
    ElMessage.warning('请先选择文件')
    return
  }

  // 将选中的文件添加到上传队列
  uploadQueue.value = [...selectedFiles.value]
  currentUploadIndex.value = 0
  uploadError.value = ''

  // 开始队列上传
  await processUploadQueue()

  // 清空选中文件列表
  selectedFiles.value = []
}

// 处理上传队列
const processUploadQueue = async () => {
  if (currentUploadIndex.value >= uploadQueue.value.length) {
    // 队列处理完成
    uploading.value = false
    uploadProgress.value = 0
    
    if (uploadedFiles.value.length > 0) {
      ElMessage.success(`成功上传 ${uploadedFiles.value.length} 个文件`)
      
      // 队列处理完成后，对已上传的文件进行解析
      for (const file of uploadedFiles.value) {
        if (!file.parsed) {
          await handleParsePaper(file)
          file.parsed = true
        } else {
          // 已经解析过的文件，直接打开编辑对话框
          await handleParsePaper(file)
        }
      }
    }
    
    if (failedFiles.value.length > 0) {
      // 显示重试对话框
      showRetryDialog.value = true
    }
    
    // 只清空上传队列，保留已上传文件列表
    uploadQueue.value = []
    
    return
  }

  uploading.value = true
  const currentFile = uploadQueue.value[currentUploadIndex.value]

  try {
    // 构建表单数据
    const formData = new FormData()
    formData.append('file', currentFile)
    formData.append('title', currentFile.name.replace('.pdf', ''))
    formData.append('authors', '')
    formData.append('abstract', '')
    formData.append('keywords', '')
    formData.append('doi', '')
    formData.append('paper_type', 'journal')
    formData.append('category', 'computer_vision')

    // 使用axios上传文件
    const response = await http.post('/papers/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        const percentage = Math.round((progressEvent.loaded / (progressEvent.total || 1)) * 100)
        uploadProgress.value = percentage
        uploadStatus.value = ''
      }
    })

    console.log('后端返回的完整响应:', response)

    // 添加到已上传文件列表
    const newFile = {
      id: response.id || uploadedFiles.value.length + 1,
      name: currentFile.name,
      size: currentFile.size,
      uploadTime: new Date().toLocaleString(),
      file_path: response.file_path,
      paper_id: response.id,
      parsed: true, // 标记为已解析，因为后端已经解析了
      // 保存后端返回的解析结果
      parsedData: {
        title: response.title || currentFile.name.replace('.pdf', ''),
        authors: response.authors || '',
        abstract: response.abstract || '',
        keywords: response.keywords || '',
        doi: response.doi || '',
        paper_type: response.paper_type || 'journal',
        category: response.category || ''
      }
    }
    console.log('构建的newFile对象:', newFile)
    uploadedFiles.value.push(newFile)

    ElMessage.success(`文件 ${currentFile.name} 上传成功`)
  } catch (error) {
    console.error('上传失败:', error)
    uploadError.value = `文件 ${currentFile.name} 上传失败`

    // 解析错误信息
    let errorMessage = `文件 ${currentFile.name} 上传失败`
    let errorType = 'unknown'
    
    if (error.code === 'ECONNABORTED') {
      // 超时错误
      errorMessage = `文件 ${currentFile.name} 上传超时，请检查网络连接或尝试上传较小的文件`
      errorType = 'timeout'
      ElMessage.warning(errorMessage)
    } else if (error.response?.data?.detail) {
      // 服务器返回的错误
      const detail = error.response.data.detail
      if (typeof detail === 'string') {
        errorMessage = detail
      } else if (Array.isArray(detail)) {
        errorMessage = detail.map(item => item.msg).join('; ')
      } else if (typeof detail === 'object') {
        // 处理对象格式的错误信息
        errorMessage = detail.message || '上传失败'
        errorType = detail.type || 'unknown'
      }
      
      // 检查错误类型
      if (error.response.data.error_type) {
        errorType = error.response.data.error_type
      }
      ElMessage.error(`文件 ${currentFile.name} 上传失败: ${errorMessage}`)
    } else {
      // 其他错误
      ElMessage.error(`文件 ${currentFile.name} 上传失败`)
    }
    
    // 将失败的文件添加到失败列表，包含错误信息
    failedFiles.value.push({
      ...currentFile,
      errorMessage,
      errorType
    })
  } finally {
    // 处理下一个文件
    currentUploadIndex.value++
    // 继续处理队列
    await processUploadQueue()
  }
}

// 处理论文解析
const handleParsePaper = async (file: any) => {
  showProgressDialog.value = true
  currentStep.value = 1
  parseProgress.value = 0
  progressMessage.value = '正在解析论文内容...'
  
  try {
    // 使用后端返回的解析结果
    const parsedData = file.parsedData || {
      title: file.name.replace('.pdf', ''),
      authors: '',
      abstract: '',
      keywords: '',
      doi: '',
      paper_type: 'journal',
      category: 'computer_vision'
    }
    console.log('使用后端解析结果:', parsedData)
    
    // 填充表单
    Object.assign(paperForm, parsedData)
    editingFile.value = file
    console.log('填充表单后:', paperForm)
    
    currentStep.value = 2
    parseProgress.value = 100
    progressMessage.value = '解析完成'
    
    await new Promise(resolve => setTimeout(resolve, 500))
    showProgressDialog.value = false
    
    // 打开编辑对话框
    showEditDialog.value = true
  } catch (error) {
    console.error('解析论文失败:', error)
    parseStatus.value = 'exception'
    progressMessage.value = '解析失败，请手动编辑论文信息'
    ElMessage.error('论文解析失败')
    
    // 3秒后关闭对话框
    setTimeout(() => {
      showProgressDialog.value = false
      // 打开编辑对话框让用户手动输入
      editingFile.value = file
      showEditDialog.value = true
    }, 3000)
  }
}

// 处理编辑文件
const handleEdit = (file: any) => {
  editingFile.value = file
  // 使用后端返回的解析结果
  const parsedData = file.parsedData || {
    title: file.name.replace('.pdf', ''),
    authors: '',
    abstract: '',
    keywords: '',
    doi: '',
    paper_type: 'journal',
    category: 'computer_vision'
  }
  // 填充表单
  Object.assign(paperForm, parsedData)
  showEditDialog.value = true
}

// 处理删除文件
const handleDelete = (file: any) => {
  const index = uploadedFiles.value.findIndex(f => f.id === file.id)
  if (index > -1) {
    uploadedFiles.value.splice(index, 1)
    ElMessage.success('文件删除成功')
  }
}

// 保存论文信息
const handleSavePaper = async () => {
  await paperFormRef.value.validate()
  
  savingPaper.value = true
  
  try {
    if (editingFile.value) {
      // 论文已经上传成功，使用updatePaper更新论文信息
      await updatePaper(editingFile.value.id, paperForm)
      ElMessage.success('论文信息保存成功')
      showEditDialog.value = false
    }
  } catch (error) {
    console.error('保存论文信息失败:', error)
    ElMessage.error('论文信息保存失败')
  } finally {
    savingPaper.value = false
  }
}

// 重试失败的文件
const retryFailedFiles = async () => {
  if (failedFiles.value.length === 0) return
  
  // 提取原始文件对象（移除错误信息）
  const filesToRetry = failedFiles.value.map(file => {
    // 直接返回原始文件对象，因为它已经包含了所有必要的属性
    return file
  })
  
  // 将失败的文件加入上传队列
  uploadQueue.value = filesToRetry
  currentUploadIndex.value = 0
  
  // 清空失败列表
  failedFiles.value = []
  
  // 关闭重试对话框
  showRetryDialog.value = false
  
  // 开始重试
  await processUploadQueue()
}
</script>

<style scoped scss>
.paper-upload-container {
  .upload-header {
    display: flex;
    align-items: center;
    margin-bottom: 30px;
    
    h2 {
      margin: 0 0 0 20px;
      color: #333;
    }
  }
  
  .upload-area {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 40px;
    margin-bottom: 30px;
    
    .upload-dragger {
      width: 100%;
      min-height: 300px;
    }
  }
  
  .file-list-section {
    margin-top: 30px;
    
    h3 {
      color: #333;
      margin-bottom: 15px;
    }
  }
  
  .progress-content {
    .progress-message {
      margin-top: 20px;
      text-align: center;
      color: #666;
    }
  }
  
  .upload-queue-status {
    background-color: #f0f9eb;
    border: 1px solid #e6f7ff;
    border-radius: 4px;
    padding: 15px;
    margin-top: 20px;
    
    h4 {
      margin: 0 0 10px 0;
      color: #333;
    }
    
    p {
      margin: 5px 0;
      color: #666;
    }
    
    .error-message {
      color: #f56c6c;
      font-weight: 500;
    }
  }
  
  .file-info {
    width: 100%;
    
    .file-name {
      font-weight: 500;
      margin-bottom: 5px;
    }
    
    .error-message {
      color: #f56c6c;
      font-size: 14px;
      margin-bottom: 3px;
    }
    
    .error-type {
      color: #909399;
      font-size: 12px;
    }
  }
}
</style>