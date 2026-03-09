<template>
  <div class="download-detail-container">
    <div class="page-header">
      <el-button @click="router.push('/downloads')">返回列表</el-button>
      <h2>资源详情</h2>
    </div>
    
    <el-card v-loading="loading">
      <div class="resource-info">
        <h3>{{ download?.title }}</h3>
        <div class="meta-info">
          <span class="category"><el-tag>{{ download?.category }}</el-tag></span>
          <span class="upload-time">上传时间：{{ formatDate(download?.upload_time) }}</span>
          <span class="download-count">下载次数：{{ download?.download_count }}</span>
        </div>
        
        <div class="description">
          <h4>描述</h4>
          <p>{{ download?.description || '暂无描述' }}</p>
        </div>
        
        <div class="file-info">
          <h4>文件信息</h4>
          <p>文件名：{{ download?.file_name }}</p>
        </div>
        
        <div class="action-buttons">
          <el-button type="primary" size="large" @click="handleDownload" :loading="downloading">
            <el-icon><Download /></el-icon>
            下载资源
          </el-button>
          <el-button v-if="isAdmin" type="info" @click="handleEdit">
            <el-icon><Edit /></el-icon>
            编辑资源
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'
import { getDownloadById, downloadResource } from '@/api/downloads'
import { ElMessage } from 'element-plus'
import { Download, Edit } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const downloadId = Number(route.params.id)
const download = ref<any>(null)
const loading = ref(true)
const downloading = ref(false)

const isAdmin = userStore.isAdmin

const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const handleDownload = async () => {
  if (!download.value) return
  
  downloading.value = true
  try {
    await downloadResource(download.value.id)
    ElMessage.success('下载开始')
    // 刷新页面以更新下载次数
    loadDownloadDetail()
  } catch (error) {
    ElMessage.error('下载失败，请重试')
    console.error('下载资源失败:', error)
  } finally {
    downloading.value = false
  }
}

const handleEdit = () => {
  if (!download.value) return
  router.push(`/downloads/edit/${download.value.id}`)
}

const loadDownloadDetail = async () => {
  loading.value = true
  try {
    const data = await getDownloadById(downloadId)
    download.value = data
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
.download-detail-container {
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
  
  .resource-info {
    h3 {
      margin: 0 0 15px 0;
      color: #333;
      font-size: 20px;
      font-weight: 600;
    }
    
    .meta-info {
      display: flex;
      gap: 20px;
      margin-bottom: 20px;
      flex-wrap: wrap;
      
      .category {
        margin-right: 10px;
      }
      
      span {
        color: #666;
        font-size: 14px;
      }
    }
    
    .description {
      margin-bottom: 20px;
      
      h4 {
        margin: 0 0 10px 0;
        color: #333;
        font-size: 16px;
        font-weight: 500;
      }
      
      p {
        margin: 0;
        color: #666;
        line-height: 1.6;
      }
    }
    
    .file-info {
      margin-bottom: 30px;
      
      h4 {
        margin: 0 0 10px 0;
        color: #333;
        font-size: 16px;
        font-weight: 500;
      }
      
      p {
        margin: 0;
        color: #666;
      }
    }
    
    .action-buttons {
      display: flex;
      gap: 10px;
      margin-top: 20px;
    }
  }
}
</style>