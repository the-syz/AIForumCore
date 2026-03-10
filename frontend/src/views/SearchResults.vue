<template>
  <div class="search-results-container">
    <div class="search-header">
      <el-button @click="goBack" class="back-button">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <div class="header-content">
        <h2>搜索结果</h2>
        <p v-if="keyword">搜索关键词: "{{ keyword }}"</p>
      </div>
    </div>

    <el-tabs v-model="activeTab" class="search-tabs">
      <el-tab-pane label="全部" name="all">
        <div v-if="loading" class="loading-section">
          <el-skeleton :rows="5" animated />
        </div>
        <div v-else-if="allResults.length === 0" class="empty-section">
          <el-empty description="未找到相关结果" />
        </div>
        <div v-else>
          <div v-if="paperResults.length > 0" class="result-section">
            <h3>论文 ({{ paperResults.length }})</h3>
            <div class="result-list">
              <el-card v-for="item in paperResults" :key="`paper-${item.id}`" class="result-item" @click="goToPaper(item.id)">
                <div class="result-title">{{ item.title }}</div>
                <div class="result-meta">
                  <span class="result-type">论文</span>
                  <span v-if="item.authors">{{ item.authors }}</span>
                  <span v-if="item.upload_time">{{ formatDate(item.upload_time) }}</span>
                </div>
              </el-card>
            </div>
          </div>

          <div v-if="postResults.length > 0" class="result-section">
            <h3>经验贴 ({{ postResults.length }})</h3>
            <div class="result-list">
              <el-card v-for="item in postResults" :key="`post-${item.id}`" class="result-item" @click="goToPost(item.id)">
                <div class="result-title">{{ item.title }}</div>
                <div class="result-meta">
                  <span class="result-type">经验贴</span>
                  <span v-if="item.author_name">{{ item.author_name }}</span>
                  <span v-if="item.created_at">{{ formatDate(item.created_at) }}</span>
                </div>
              </el-card>
            </div>
          </div>

          <div v-if="downloadResults.length > 0" class="result-section">
            <h3>下载资源 ({{ downloadResults.length }})</h3>
            <div class="result-list">
              <el-card v-for="item in downloadResults" :key="`download-${item.id}`" class="result-item" @click="goToDownload(item.id)">
                <div class="result-title">{{ item.title }}</div>
                <div class="result-meta">
                  <span class="result-type">下载资源</span>
                  <span v-if="item.category">{{ item.category }}</span>
                  <span v-if="item.upload_time">{{ formatDate(item.upload_time) }}</span>
                </div>
              </el-card>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="论文" name="papers">
        <div v-if="loading" class="loading-section">
          <el-skeleton :rows="5" animated />
        </div>
        <div v-else-if="paperResults.length === 0" class="empty-section">
          <el-empty description="未找到相关论文" />
        </div>
        <div v-else class="result-list">
          <el-card v-for="item in paperResults" :key="`paper-${item.id}`" class="result-item" @click="goToPaper(item.id)">
            <div class="result-title">{{ item.title }}</div>
            <div class="result-meta">
              <span v-if="item.authors">{{ item.authors }}</span>
              <span v-if="item.upload_time">{{ formatDate(item.upload_time) }}</span>
              <span v-if="item.download_count">下载: {{ item.download_count }}</span>
            </div>
          </el-card>
        </div>
      </el-tab-pane>

      <el-tab-pane label="经验贴" name="posts">
        <div v-if="loading" class="loading-section">
          <el-skeleton :rows="5" animated />
        </div>
        <div v-else-if="postResults.length === 0" class="empty-section">
          <el-empty description="未找到相关经验贴" />
        </div>
        <div v-else class="result-list">
          <el-card v-for="item in postResults" :key="`post-${item.id}`" class="result-item" @click="goToPost(item.id)">
            <div class="result-title">{{ item.title }}</div>
            <div class="result-meta">
              <span v-if="item.author_name">{{ item.author_name }}</span>
              <span v-if="item.created_at">{{ formatDate(item.created_at) }}</span>
              <span v-if="item.view_count">浏览: {{ item.view_count }}</span>
            </div>
          </el-card>
        </div>
      </el-tab-pane>

      <el-tab-pane label="下载资源" name="downloads">
        <div v-if="loading" class="loading-section">
          <el-skeleton :rows="5" animated />
        </div>
        <div v-else-if="downloadResults.length === 0" class="empty-section">
          <el-empty description="未找到相关资源" />
        </div>
        <div v-else class="result-list">
          <el-card v-for="item in downloadResults" :key="`download-${item.id}`" class="result-item" @click="goToDownload(item.id)">
            <div class="result-title">{{ item.title }}</div>
            <div class="result-meta">
              <span v-if="item.category">{{ item.category }}</span>
              <span v-if="item.upload_time">{{ formatDate(item.upload_time) }}</span>
              <span v-if="item.download_count">下载: {{ item.download_count }}</span>
            </div>
          </el-card>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchAll, searchPapers, searchPosts, searchDownloads } from '@/api/search'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const keyword = ref('')
const activeTab = ref('all')
const loading = ref(false)
const allResults = ref<any[]>([])
const paperResults = ref<any[]>([])
const postResults = ref<any[]>([])
const downloadResults = ref<any[]>([])

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const goToPaper = (id: number) => {
  router.push(`/papers/${id}`)
}

const goToPost = (id: number) => {
  router.push(`/posts/${id}`)
}

const goToDownload = (id: number) => {
  router.push(`/downloads/${id}`)
}

const goBack = () => {
  router.push('/')
}

const performSearch = async () => {
  if (!keyword.value) return
  
  loading.value = true
  try {
    const [allRes, papersRes, postsRes, downloadsRes] = await Promise.all([
      searchAll(keyword.value),
      searchPapers(keyword.value),
      searchPosts(keyword.value),
      searchDownloads(keyword.value)
    ])
    
    allResults.value = allRes.items || []
    paperResults.value = papersRes.items || []
    postResults.value = postsRes.items || []
    downloadResults.value = downloadsRes.items || []
  } catch (error) {
    ElMessage.error('搜索失败，请重试')
    console.error('搜索失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  const searchKeyword = route.query.q as string
  if (searchKeyword) {
    keyword.value = searchKeyword
    performSearch()
  }
})
</script>

<style scoped lang="scss">
.search-results-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  
  .search-header {
    margin-bottom: 30px;
    display: flex;
    align-items: center;
    gap: 20px;
    
    .back-button {
      flex-shrink: 0;
    }
    
    .header-content {
      flex: 1;
      
      h2 {
        margin: 0 0 10px;
        color: #333;
        font-size: 24px;
      }
      
      p {
        margin: 0;
        color: #666;
        font-size: 14px;
      }
    }
  }
  
  .search-tabs {
    :deep(.el-tabs__header) {
      margin-bottom: 20px;
    }
  }
  
  .loading-section,
  .empty-section {
    padding: 40px 0;
  }
  
  .result-section {
    margin-bottom: 30px;
    
    h3 {
      margin: 0 0 15px;
      color: #333;
      font-size: 18px;
      padding-bottom: 10px;
      border-bottom: 1px solid #eaeaea;
    }
  }
  
  .result-list {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }
  
  .result-item {
    cursor: pointer;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateX(5px);
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    }
    
    .result-title {
      font-size: 16px;
      font-weight: 600;
      color: #333;
      margin-bottom: 8px;
    }
    
    .result-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 15px;
      font-size: 13px;
      color: #999;
      
      .result-type {
        color: #409eff;
        font-weight: 500;
      }
    }
  }
}
</style>
