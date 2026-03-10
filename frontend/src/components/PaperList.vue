<template>
  <div class="paper-list">
    <el-empty v-if="papers.length === 0" description="暂无推荐论文" />
    <el-card v-else v-for="paper in papers" :key="paper.id" class="paper-card" @click="handlePaperClick(paper.id)">
      <template #header>
        <div class="paper-header">
          <h4 class="paper-title">{{ paper.title }}</h4>
        </div>
      </template>
      <div class="paper-content">
        <p class="paper-authors">{{ paper.authors }}</p>
        <p class="paper-abstract">{{ paper.abstract }}</p>
        <div class="paper-footer">
          <span class="paper-category">{{ paper.category }}</span>
          <span class="paper-time">
            <i class="el-icon-time"></i> {{ formatDate(paper.upload_time) }}
          </span>
          <span class="paper-downloads">
            <i class="el-icon-download"></i> {{ paper.download_count || 0 }} 次
          </span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

interface Paper {
  id: number
  title: string
  authors: string
  abstract: string
  category?: string
  download_count?: number
  upload_time?: string
}

const props = defineProps<{
  papers: Paper[]
}>()

const router = useRouter()

const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const handlePaperClick = (paperId: number) => {
  router.push(`/papers/${paperId}`)
}
</script>

<style scoped scss>
.paper-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.paper-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  }
}

.paper-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.paper-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  line-height: 1.4;
}

.paper-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.paper-authors {
  font-size: 12px;
  color: #999;
  margin: 10px 0;
}

.paper-abstract {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin: 0 0 15px 0;
  flex: 1;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.paper-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 12px;
  color: #999;
  margin-top: auto;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.paper-category {
  background-color: #ecf5ff;
  color: #409eff;
  padding: 2px 8px;
  border-radius: 10px;
}

.paper-time,
.paper-downloads {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>