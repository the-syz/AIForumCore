<template>
  <div class="post-list">
    <el-empty v-if="posts.length === 0" description="暂无推荐经验贴" />
    <el-card v-else v-for="post in posts" :key="post.id" class="post-card">
      <template #header>
        <div class="post-header">
          <h4 class="post-title">{{ post.title }}</h4>
        </div>
      </template>
      <div class="post-content">
        <p class="post-excerpt">{{ post.content }}</p>
        <div class="post-footer">
          <span class="post-category">{{ post.category }}</span>
          <span class="post-meta">
            <i class="el-icon-view"></i> {{ post.view_count || 0 }}
            <i class="el-icon-chat-dot-round"></i> {{ post.comment_count || 0 }}
            <i class="el-icon-star-off"></i> {{ post.like_count || 0 }}
          </span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
interface Post {
  id: number
  title: string
  content: string
  category?: string
  view_count?: number
  comment_count?: number
  like_count?: number
}

const props = defineProps<{
  posts: Post[]
}>()
</script>

<style scoped scss>
.post-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.post-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  line-height: 1.4;
}

.post-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.post-excerpt {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin: 10px 0;
  flex: 1;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #999;
  margin-top: auto;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
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