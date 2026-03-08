<template>
  <div class="paper-detail-container">
    <div class="paper-header">
      <el-button @click="goBack">返回</el-button>
      <h2>{{ paper?.title }}</h2>
    </div>
    
    <el-card v-if="paper" class="paper-card">
      <template #header>
        <div class="paper-meta">
          <span class="paper-authors">{{ paper.authors }}</span>
          <span class="paper-category">{{ paper.category }}</span>
        </div>
      </template>
      
      <div class="paper-content">
        <div class="paper-info">
          <p><strong>摘要：</strong>{{ paper.abstract }}</p>
          <p><strong>关键词：</strong>{{ paper.keywords }}</p>
          <p v-if="paper.doi"><strong>DOI：</strong>{{ paper.doi }}</p>
          <p><strong>上传时间：</strong>{{ formatDate(paper.upload_time) }}</p>
          <p><strong>下载次数：</strong>{{ paper.download_count }}</p>
          <p><strong>上传用户：</strong>{{ paper.uploader_name || '未知用户' }}</p>
        </div>
        
        <div class="paper-actions">
          <el-button type="primary" @click="handleDownload">下载论文</el-button>
        </div>
        
        <div class="paper-preview" v-if="paper.file_path">
          <h3>论文预览</h3>
          <div class="preview-content">
            <el-empty description="PDF 预览功能开发中" />
          </div>
        </div>
      </div>
    </el-card>
    
    <el-skeleton v-else :rows="10" animated />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPaperById, downloadPaper, deletePaper } from '@/api/papers'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const paper = ref<any>(null)

const paperId = computed(() => Number(route.params.id))

const isOwner = computed(() => {
  if (!paper.value || !userStore.userInfo) return false
  return paper.value.uploader_id === userStore.userInfo.id
})

const goBack = () => {
  router.push('/papers')
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

const handleDownload = async () => {
  try {
    await downloadPaper(paperId.value)
    ElMessage.success('下载成功')
  } catch (error) {
    ElMessage.error('下载失败')
  }
}

const handleEdit = () => {
  router.push(`/papers/edit/${paperId.value}`)
}

const handleDelete = async () => {
  try {
    await deletePaper(paperId.value)
    ElMessage.success('删除成功')
    router.push('/papers')
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const fetchPaperDetail = async () => {
  try {
    const data = await getPaperById(paperId.value)
    paper.value = data
  } catch (error) {
    ElMessage.error('获取论文详情失败')
  }
}

onMounted(() => {
  fetchPaperDetail()
})
</script>

<style scoped scss>
.paper-detail-container {
  .paper-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      margin: 0 0 0 20px;
      color: #333;
    }
  }
  
  .paper-card {
    margin-bottom: 20px;
    
    .paper-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .paper-authors {
        font-size: 16px;
        color: #666;
      }
      
      .paper-category {
        background-color: #ecf5ff;
        color: #409eff;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 12px;
      }
    }
    
    .paper-content {
      .paper-info {
        margin-bottom: 30px;
        
        p {
          margin: 10px 0;
          line-height: 1.5;
        }
      }
      
      .paper-actions {
        margin-bottom: 30px;
        display: flex;
        gap: 10px;
      }
      
      .paper-preview {
        h3 {
          margin-bottom: 20px;
          color: #333;
        }
        
        .preview-content {
          min-height: 400px;
          display: flex;
          justify-content: center;
          align-items: center;
          background-color: #f5f5f5;
          border-radius: 4px;
        }
      }
    }
  }
}
</style>