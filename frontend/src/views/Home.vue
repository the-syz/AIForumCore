<template>
  <div class="home-container">
    <!-- 欢迎信息 -->
    <div class="welcome-section">
      <h2>{{ welcomeMessage }}</h2>
      <p>{{ currentDate }}</p>
    </div>
    
    <!-- 搜索框 -->
    <div class="search-section">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索论文、经验贴..."
        suffix-icon="el-icon-search"
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </template>
      </el-input>
    </div>
    
    <!-- 论文推荐 -->
    <div class="section">
      <h3>论文推荐</h3>
      <el-empty v-if="recommendedPapers.length === 0" description="暂无推荐论文" />
      <el-list v-else>
        <el-list-item v-for="paper in recommendedPapers" :key="paper.id">
          <div class="paper-item">
            <h4>{{ paper.title }}</h4>
            <p class="paper-authors">{{ paper.authors }}</p>
            <p class="paper-abstract">{{ paper.abstract }}</p>
          </div>
        </el-list-item>
      </el-list>
    </div>
    
    <!-- 经验贴推荐 -->
    <div class="section">
      <h3>经验贴推荐</h3>
      <el-empty v-if="recommendedPosts.length === 0" description="暂无推荐经验贴" />
      <el-list v-else>
        <el-list-item v-for="post in recommendedPosts" :key="post.id">
          <div class="post-item">
            <h4>{{ post.title }}</h4>
            <p class="post-content">{{ post.content }}</p>
          </div>
        </el-list-item>
      </el-list>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/store/user'

interface Paper {
  id: number
  title: string
  authors: string
  abstract: string
}

interface Post {
  id: number
  title: string
  content: string
}

const userStore = useUserStore()
const recommendedPapers = ref<Paper[]>([])
const recommendedPosts = ref<Post[]>([])
const searchKeyword = ref('')

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

const handleSearch = (keyword: string) => {
  // 跳转到搜索结果页
  console.log('搜索关键词:', keyword || searchKeyword.value)
}

onMounted(async () => {
  // 模拟数据
  recommendedPapers.value = [
    {
      id: 1,
      title: '深度学习在计算机视觉中的应用',
      authors: '张三, 李四',
      abstract: '本文探讨了深度学习在计算机视觉领域的最新应用...'
    }
  ]
  recommendedPosts.value = [
    {
      id: 1,
      title: '研究生学习经验分享',
      content: '作为一名研究生，我想分享一下我的学习经验...'
    }
  ]
})
</script>

<style scoped lang="scss">
.home-container {
  .welcome-section {
    margin-bottom: 30px;
    
    h2 {
      color: #409eff;
      margin-bottom: 10px;
    }
    
    p {
      color: #666;
    }
  }
  
  .search-section {
    margin-bottom: 30px;
  }
  
  .section {
    margin-bottom: 40px;
    
    h3 {
      margin-bottom: 20px;
      color: #333;
      border-bottom: 1px solid #eaeaea;
      padding-bottom: 10px;
    }
  }
  
  .paper-item,
  .post-item {
    h4 {
      margin-bottom: 10px;
      color: #333;
    }
    
    p {
      margin-bottom: 10px;
      color: #666;
    }
  }
  
  .paper-authors {
    font-size: 12px;
    color: #999;
  }
  
  .paper-abstract,
  .post-content {
    font-size: 14px;
    line-height: 1.5;
  }
}
</style>
