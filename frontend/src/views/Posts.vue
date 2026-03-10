<template>
  <div class="posts-container">
    <div class="posts-header">
      <h2>经验贴</h2>
      <div class="posts-actions">
        <div class="search-box">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索经验贴标题、内容..."
            suffix-icon="el-icon-search"
            @keyup.enter="handleSearch"
          >
            <template #append>
              <el-button type="primary" @click="handleSearch">搜索</el-button>
            </template>
          </el-input>
        </div>
        <el-button v-if="isSearching" type="info" @click="handleReset">重置</el-button>
        <el-button type="primary" @click="handleCreate">发布经验贴</el-button>
      </div>
    </div>
    
    <!-- 搜索结果列表 -->
    <div v-if="isSearching" class="search-results">
      <div v-if="loading" class="loading-section">
        <el-skeleton :rows="5" animated />
      </div>
      <div v-else-if="posts.length === 0" class="empty-state">
        <el-empty description="未找到相关经验贴" />
      </div>
      <div v-else class="result-list">
        <el-card v-for="post in posts" :key="post.id" class="result-item" @click="handleView(post)">
          <div class="result-title">{{ post.title }}</div>
          <div class="result-meta">
            <span class="result-category">{{ post.category }}</span>
            <span class="result-author">{{ post.author_name }}</span>
            <span class="result-time">{{ formatDate(post.created_at) }}</span>
            <span class="result-views">浏览: {{ post.view_count }}</span>
          </div>
        </el-card>
      </div>
    </div>
    
    <!-- 分类分栏展示 -->
    <div v-else class="categories-container">
      <!-- 学习经验 -->
      <div class="category-section" v-if="getPostsByCategory('学习经验').length > 0">
        <div class="category-header">
          <h3>学习经验</h3>
        </div>
        <div class="post-cards">
          <el-card
            v-for="post in getPostsByCategory('学习经验')"
            :key="post.id"
            class="post-card"
            :class="{ 'pinned-post': post.is_pinned }"
          >
            <template #header>
              <div class="post-card-header">
                <router-link :to="`/posts/${post.id}`" class="post-title">
                  {{ post.title }}
                  <span v-if="post.is_pinned" class="pinned-badge">置顶</span>
                </router-link>
              </div>
            </template>
            <div class="post-meta">
              <span class="author">作者: {{ post.author_name }}</span>
              <span class="created-at">{{ formatDate(post.created_at) }}</span>
              <span class="view-count">浏览: {{ post.view_count }}</span>
              <span class="comment-count">评论: {{ post.comment_count }}</span>
            </div>
            <div class="post-actions">
              <el-button size="small" @click="handleView(post)">查看</el-button>
            </div>
          </el-card>
        </div>
      </div>
      
      <!-- 科研经验 -->
      <div class="category-section" v-if="getPostsByCategory('科研经验').length > 0">
        <div class="category-header">
          <h3>科研经验</h3>
        </div>
        <div class="post-cards">
          <el-card
            v-for="post in getPostsByCategory('科研经验')"
            :key="post.id"
            class="post-card"
            :class="{ 'pinned-post': post.is_pinned }"
          >
            <template #header>
              <div class="post-card-header">
                <router-link :to="`/posts/${post.id}`" class="post-title">
                  {{ post.title }}
                  <span v-if="post.is_pinned" class="pinned-badge">置顶</span>
                </router-link>
              </div>
            </template>
            <div class="post-meta">
              <span class="author">作者: {{ post.author_name }}</span>
              <span class="created-at">{{ formatDate(post.created_at) }}</span>
              <span class="view-count">浏览: {{ post.view_count }}</span>
              <span class="comment-count">评论: {{ post.comment_count }}</span>
            </div>
            <div class="post-actions">
              <el-button size="small" @click="handleView(post)">查看</el-button>
            </div>
          </el-card>
        </div>
      </div>
      
      <!-- 生活经验 -->
      <div class="category-section" v-if="getPostsByCategory('生活经验').length > 0">
        <div class="category-header">
          <h3>生活经验</h3>
        </div>
        <div class="post-cards">
          <el-card
            v-for="post in getPostsByCategory('生活经验')"
            :key="post.id"
            class="post-card"
            :class="{ 'pinned-post': post.is_pinned }"
          >
            <template #header>
              <div class="post-card-header">
                <router-link :to="`/posts/${post.id}`" class="post-title">
                  {{ post.title }}
                  <span v-if="post.is_pinned" class="pinned-badge">置顶</span>
                </router-link>
              </div>
            </template>
            <div class="post-meta">
              <span class="author">作者: {{ post.author_name }}</span>
              <span class="created-at">{{ formatDate(post.created_at) }}</span>
              <span class="view-count">浏览: {{ post.view_count }}</span>
              <span class="comment-count">评论: {{ post.comment_count }}</span>
            </div>
            <div class="post-actions">
              <el-button size="small" @click="handleView(post)">查看</el-button>
            </div>
          </el-card>
        </div>
      </div>
      
      <!-- 其他 -->
      <div class="category-section" v-if="getPostsByCategory('其他').length > 0">
        <div class="category-header">
          <h3>其他</h3>
        </div>
        <div class="post-cards">
          <el-card
            v-for="post in getPostsByCategory('其他')"
            :key="post.id"
            class="post-card"
            :class="{ 'pinned-post': post.is_pinned }"
          >
            <template #header>
              <div class="post-card-header">
                <router-link :to="`/posts/${post.id}`" class="post-title">
                  {{ post.title }}
                  <span v-if="post.is_pinned" class="pinned-badge">置顶</span>
                </router-link>
              </div>
            </template>
            <div class="post-meta">
              <span class="author">作者: {{ post.author_name }}</span>
              <span class="created-at">{{ formatDate(post.created_at) }}</span>
              <span class="view-count">浏览: {{ post.view_count }}</span>
              <span class="comment-count">评论: {{ post.comment_count }}</span>
            </div>
            <div class="post-actions">
              <el-button size="small" @click="handleView(post)">查看</el-button>
            </div>
          </el-card>
        </div>
      </div>
    </div>
    
    <!-- 无内容提示 -->
    <div v-if="!isSearching && posts.length === 0" class="empty-state">
      <el-empty description="暂无经验贴" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getPosts, deletePost } from '@/api/posts'
import { searchPosts } from '@/api/search'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'

interface Post {
  id: number
  title: string
  category: string
  author_id: number
  author_name: string
  created_at: string
  view_count: number
  comment_count: number
  is_pinned: boolean
}

const router = useRouter()
const userStore = useUserStore()
const posts = ref<Post[]>([])
const allPosts = ref<Post[]>([])
const searchKeyword = ref('')
const loading = ref(false)
const isSearching = ref(false)

// 检查是否有权限管理经验贴
const canManagePost = (post: Post) => {
  if (!userStore.userInfo) return false
  return userStore.userInfo.id === post.author_id || userStore.isAdmin
}

// 根据分类获取经验贴，置顶帖在前，按时间倒序
const getPostsByCategory = (category: string) => {
  return posts.value
    .filter(post => post.category === category)
    .sort((a, b) => {
      // 置顶帖优先
      if (a.is_pinned && !b.is_pinned) return -1
      if (!a.is_pinned && b.is_pinned) return 1
      // 时间倒序
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    })
}

// 搜索经验贴
const handleSearch = async () => {
  if (!searchKeyword.value.trim()) {
    handleReset()
    return
  }
  loading.value = true
  isSearching.value = true
  try {
    const response = await searchPosts(searchKeyword.value.trim())
    posts.value = response.items || []
  } catch (error) {
    ElMessage.error('搜索失败，请重试')
    console.error('搜索失败:', error)
  } finally {
    loading.value = false
  }
}

// 重置搜索
const handleReset = () => {
  searchKeyword.value = ''
  isSearching.value = false
  posts.value = [...allPosts.value]
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取经验贴列表
const fetchPosts = async () => {
  loading.value = true
  try {
    const response = await getPosts('', 0, 100) // 获取所有经验贴
    allPosts.value = response
    posts.value = [...allPosts.value]
  } catch (error) {
    ElMessage.error('获取经验贴列表失败')
    console.error('获取经验贴列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 发布经验贴
const handleCreate = () => {
  router.push('/posts/create')
}

// 查看经验贴详情
const handleView = (post: Post) => {
  router.push(`/posts/${post.id}`)
}

// 编辑经验贴
const handleEdit = (post: Post) => {
  router.push(`/posts/edit/${post.id}`)
}

// 删除经验贴
const handleDelete = async (id: number) => {
  try {
    await deletePost(id)
    ElMessage.success('经验贴删除成功')
    fetchPosts()
  } catch (error) {
    ElMessage.error('经验贴删除失败')
    console.error('删除经验贴失败:', error)
  }
}

// 初始化加载数据
onMounted(() => {
  fetchPosts()
})
</script>

<style scoped lang="scss">
.posts-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  
  .posts-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    
    h2 {
      margin: 0;
      color: #333;
      font-size: 24px;
    }
    
    .posts-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      
      .search-box {
        min-width: 300px;
      }
    }
  }
  
  .categories-container {
    display: flex;
    flex-direction: column;
    gap: 40px;
  }
  
  .category-section {
    
    .category-header {
      margin-bottom: 20px;
      
      h3 {
        margin: 0;
        color: #333;
        font-size: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #eaeaea;
      }
    }
    
    .post-cards {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
    }
  }
  
  .post-card {
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }
    
    &.pinned-post {
      border-left: 4px solid #409eff;
    }
    
    .post-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .post-title {
        color: #333;
        text-decoration: none;
        font-size: 18px;
        font-weight: 600;
        margin-right: 10px;
        
        &:hover {
          color: #409eff;
        }
        
        .pinned-badge {
          display: inline-block;
          background-color: #409eff;
          color: white;
          font-size: 12px;
          padding: 2px 6px;
          border-radius: 10px;
          margin-left: 8px;
        }
      }
    }
    
    .post-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 15px;
      margin: 15px 0;
      font-size: 14px;
      color: #666;
    }
    
    .post-actions {
      display: flex;
      gap: 10px;
      margin-top: 15px;
    }
  }
  
  .empty-state {
    text-align: center;
    padding: 60px 0;
  }
  
  .search-results {
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
        
        .result-category {
          color: #409eff;
          font-weight: 500;
        }
      }
    }
  }
}
</style>
