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
          <p><strong>上传用户：</strong>
            <el-link v-if="paper.uploader_id" type="primary" @click="goToUserProfile(paper.uploader_id)">
              {{ paper.uploader_name || '未知用户' }}
            </el-link>
            <span v-else>{{ paper.uploader_name || '未知用户' }}</span>
          </p>
        </div>
        
        <div class="paper-actions">
          <el-button 
            :type="isLiked ? 'danger' : 'default'" 
            @click="handleLike"
          >
            <el-icon><Star /></el-icon>
            {{ isLiked ? '已点赞' : '点赞' }}
            <span v-if="likeCount > 0">({{ likeCount }})</span>
          </el-button>
          <el-button 
            :type="isFavorited ? 'success' : 'default'" 
            @click="handleFavorite"
          >
            <el-icon><Collection /></el-icon>
            {{ isFavorited ? '已收藏' : '收藏' }}
          </el-button>
          <el-button type="primary" @click="handleDownload">下载论文</el-button>
          <el-button type="warning" @click="addToAIChat">
            <el-icon><ChatDotRound /></el-icon>
            添加到AI对话
          </el-button>
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
import { toggleLike, toggleFavorite } from '@/api/forum'
import { useUserStore } from '@/store/user'
import { useTabsStore } from '@/store/tabs'
import { ElMessage } from 'element-plus'
import { Star, Collection, ChatDotRound } from '@element-plus/icons-vue'
import { useAIStore } from '@/store/ai'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const tabsStore = useTabsStore()
const aiStore = useAIStore()
const paper = ref<any>(null)
const isLiked = ref(false)
const isFavorited = ref(false)
const likeCount = ref(0)

const paperId = computed(() => Number(route.params.id))

const isOwner = computed(() => {
  if (!paper.value || !userStore.userInfo) return false
  return paper.value.uploader_id === userStore.userInfo.id
})

const goBack = () => {
  router.push('/papers')
}

const goToUserProfile = (userId: number) => {
  router.push(`/user/${userId}`)
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

const handleLike = async () => {
  if (!userStore.token) {
    ElMessage.warning('请先登录')
    return
  }
  try {
    await toggleLike('paper', paperId.value)
    isLiked.value = !isLiked.value
    if (isLiked.value) {
      likeCount.value++
      ElMessage.success('点赞成功')
    } else {
      likeCount.value--
      ElMessage.success('取消点赞成功')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleFavorite = async () => {
  if (!userStore.token) {
    ElMessage.warning('请先登录')
    return
  }
  try {
    await toggleFavorite('paper', paperId.value)
    isFavorited.value = !isFavorited.value
    ElMessage.success(isFavorited.value ? '收藏成功' : '取消收藏成功')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const addToAIChat = () => {
  if (!paper.value) return
  
  aiStore.addSelectedContent({
    type: 'paper',
    id: paper.value.id,
    title: paper.value.title
  })
  
  ElMessage.success('已添加到AI对话')
}

const fetchPaperDetail = async () => {
  try {
    const data = await getPaperById(paperId.value)
    paper.value = data
    likeCount.value = data.like_count || 0
    
    if (data.title) {
      const truncatedTitle = data.title.length > 20 ? data.title.substring(0, 20) + '...' : data.title
      tabsStore.updateTabTitle(route.path, truncatedTitle)
    }
  } catch (error) {
    console.error('获取论文详情失败:', error)
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
