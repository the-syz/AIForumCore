<template>
  <div class="home-container">
    <!-- 欢迎信息 -->
    <div class="welcome-section">
      <h2>{{ welcomeMessage }}</h2>
      <p>{{ currentDate }}</p>
    </div>
    
    <!-- 搜索框 -->
    <div class="search-section">
      <SearchBox @search="handleSearch" />
    </div>
    
    <!-- 论文推荐 -->
    <div class="section">
      <h3>论文推荐</h3>
      <PaperList :papers="recommendedPapers" />
    </div>
    
    <!-- 经验贴推荐 -->
    <div class="section">
      <h3>经验贴推荐</h3>
      <PostList :posts="recommendedPosts" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/store/user'
import { getPapers } from '@/api/papers'
import { getPosts } from '@/api/posts'
import { searchAll } from '@/api/search'
import SearchBox from '@/components/SearchBox.vue'
import PaperList from '@/components/PaperList.vue'
import PostList from '@/components/PostList.vue'

interface Paper {
  id: number
  title: string
  authors: string
  abstract: string
  category?: string
  download_count?: number
}

interface Post {
  id: number
  title: string
  content: string
  category?: string
  view_count?: number
  comment_count?: number
  like_count?: number
}

const userStore = useUserStore()
const recommendedPapers = ref<Paper[]>([])
const recommendedPosts = ref<Post[]>([])

const welcomeMessage = computed(() => {
  const user = userStore.userInfo
  if (user?.role === 'teacher') {
    return `你好，${user.name}教授，欢迎！`
  }
  return `你好，${user?.name}同学，欢迎！`
})

const currentDate = computed(() => {
  const date = new Date()
  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 ${weekdays[date.getDay()]}`
})

const handleSearch = async (keyword: string) => {
  if (!keyword) return
  
  try {
    const results = await searchAll(keyword)
    console.log('搜索结果:', results)
    // 跳转到搜索结果页，这里可以添加路由跳转逻辑
  } catch (error) {
    console.error('搜索失败:', error)
  }
}

onMounted(async () => {
  try {
    // 使用API获取数据
    const papers = await getPapers()
    recommendedPapers.value = papers
    
    const posts = await getPosts()
    recommendedPosts.value = posts
  } catch (error) {
    console.error('获取推荐数据失败:', error)
  }
})
</script>

<style scoped scss>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  
  .welcome-section {
    margin-bottom: 30px;
    text-align: center;
    
    h2 {
      color: #409eff;
      margin-bottom: 10px;
      font-size: 24px;
    }
    
    p {
      color: #666;
      font-size: 16px;
    }
  }
  
  .search-section {
    margin-bottom: 40px;
  }
  
  .section {
    margin-bottom: 50px;
    
    h3 {
      margin-bottom: 20px;
      color: #333;
      border-bottom: 1px solid #eaeaea;
      padding-bottom: 10px;
      font-size: 18px;
      font-weight: 600;
    }
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-container {
    padding: 15px;
    
    .welcome-section h2 {
      font-size: 20px;
    }
    
    .welcome-section p {
      font-size: 14px;
    }
    
    .section h3 {
      font-size: 16px;
    }
  }
  
  .paper-list,
  .post-list {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .paper-list,
  .post-list {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1025px) {
  .paper-list,
  .post-list {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
