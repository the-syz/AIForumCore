<template>
  <div class="file-upload">
    <el-upload
      class="upload-demo"
      :action="uploadUrl"
      :on-progress="handleProgress"
      :on-success="handleSuccess"
      :on-error="handleError"
      :before-upload="beforeUpload"
      :file-list="fileList"
      :auto-upload="false"
      ref="uploadRef"
    >
      <el-button type="primary">选择文件</el-button>
      <template #tip>
        <div class="el-upload__tip">
          请上传 PDF 文件，大小不超过 20MB
        </div>
      </template>
    </el-upload>
    
    <el-progress
      v-if="progress > 0 && progress < 100"
      :percentage="progress"
      :status="uploadStatus"
      style="margin-top: 10px"
    />
    
    <el-button
      type="primary"
      @click="submitUpload"
      :loading="submitting"
      :disabled="fileList.length === 0 || progress > 0 && progress < 100"
      style="margin-top: 10px"
    >
      上传
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  uploadUrl?: string
}>()

const emit = defineEmits<{
  (e: 'success', file: any): void
  (e: 'error', error: any): void
  (e: 'progress', percentage: number): void
}>()

const uploadRef = ref<any>(null)
const fileList = ref<any[]>([])
const progress = ref(0)
const submitting = ref(false)
const uploadStatus = ref<'success' | 'exception' | 'warning' | ''>('')

const uploadUrl = computed(() => props.uploadUrl || '/api/papers/')

const handleProgress = (event: any, file: any, fileList: any[]) => {
  const percentage = Math.round((event.loaded / event.total) * 100)
  progress.value = percentage
  uploadStatus.value = ''
  emit('progress', percentage)
}

const handleSuccess = (response: any, uploadFile: any, uploadFiles: any[]) => {
  progress.value = 100
  uploadStatus.value = 'success'
  submitting.value = false
  emit('success', uploadFile)
}

const handleError = (error: any, uploadFile: any, uploadFiles: any[]) => {
  progress.value = 0
  uploadStatus.value = 'exception'
  submitting.value = false
  emit('error', error)
}

const beforeUpload = (file: File) => {
  const isPDF = file.type === 'application/pdf'
  const isLt20M = file.size / 1024 / 1024 < 20

  if (!isPDF) {
    ElMessage.error('只能上传 PDF 文件!')
  }
  if (!isLt20M) {
    ElMessage.error('文件大小不能超过 20MB!')
  }
  return isPDF && isLt20M
}

const submitUpload = () => {
  submitting.value = true
  uploadRef.value.submit()
}
</script>

<style scoped scss>
.file-upload {
  .upload-demo {
    margin-bottom: 10px;
  }
}
</style>