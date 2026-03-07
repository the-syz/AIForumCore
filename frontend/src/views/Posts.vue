<template>
  <div class="posts-container">
    <h2>经验贴管理</h2>
    <el-button type="primary" @click="handleCreate">发布经验贴</el-button>
    <el-table :data="posts" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="author_id" label="作者" />
      <el-table-column prop="created_at" label="创建时间" />
      <el-table-column prop="view_count" label="浏览次数" />
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button size="small" @click="handleView(scope.row)">查看</el-button>
          <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Post {
  id: number
  title: string
  author_id: string
  created_at: string
  view_count: number
}

const posts = ref<Post[]>([])

const handleCreate = () => {
  // 发布经验贴逻辑
  console.log('发布经验贴')
}

const handleView = (post: Post) => {
  // 查看经验贴详情
  console.log('查看经验贴:', post)
}

const handleEdit = (post: Post) => {
  // 编辑经验贴
  console.log('编辑经验贴:', post)
}

onMounted(async () => {
  // 模拟数据
  posts.value = [
    {
      id: 1,
      title: '研究生学习经验分享',
      author_id: '张三',
      created_at: '2026-03-01',
      view_count: 50
    }
  ]
})
</script>

<style scoped lang="scss">
.posts-container {
  h2 {
    margin-bottom: 20px;
    color: #333;
  }
  
  .el-button {
    margin-bottom: 20px;
  }
}
</style>
