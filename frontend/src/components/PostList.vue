<template>
  <div class="post-list">
    <el-empty v-if="posts.length === 0" description="暂无推荐经验贴" />
    <el-card v-else v-for="post in posts" :key="post.id" class="post-card" @click="handlePostClick(post.id)">
      <template #header>
        <div class="post-header">
          <h4 class="post-title">{{ post.title }}</h4>
        </div>
      </template>
      <div class="post-content">
        <div class="post-footer">
          <span class="post-author">
            <i class="el-icon-user"></i> {{ post.author_name || '未知用户' }}
          </span>
          <span class="post-category">{{ post.category }}</span>
          <span class="post-meta">
            <i class="el-icon-time"></i> {{ formatDate(post.created_at) }}
            <i class="el-icon-view"></i> {{ post.view_count || 0 }}
          </span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

interface Post {
  id: number
  title: string
  content: string
  category?: string
  view_count?: number
  comment_count?: number
  like_count?: number
  author_name?: string
  created_at?: string
}

const props = defineProps<{
  posts: Post[]
}>()

const router = useRouter()

const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const handlePostClick = (postId: number) => {
  router.push(`/posts/${postId}`)
}
</script>

<style scoped scss>
.post-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 12px;
}

.post-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: all 0.3s ease;
  
  :deep(.el-card__header) {
    padding: 12px;
    border-bottom: none;
  }

  :deep(.el-card__body) {
    padding: 12px;
  }
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-title {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  line-height: 1.3;
}

.post-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding-top: 6px;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  font-size: 10px;
  color: #999;
  padding-top: 6px;
}

.post-author {
  display: flex;
  align-items: center;
  gap: 4px;
}

.post-category {
  background-color: #f0f9eb;
  color: #67c23a;
  padding: 2px 8px;
  border-radius: 10px;
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 15px;
}

.post-meta i {
  margin-right: 4px;
}
</style>