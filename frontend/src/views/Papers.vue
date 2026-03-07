<template>
  <div class="papers-container">
    <h2>论文管理</h2>
    <el-button type="primary" @click="handleUpload">上传论文</el-button>
    <el-table :data="papers" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="authors" label="作者" />
      <el-table-column prop="upload_time" label="上传时间" />
      <el-table-column prop="download_count" label="下载次数" />
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button size="small" @click="handleView(scope.row)">查看</el-button>
          <el-button size="small" @click="handleDownload(scope.row)">下载</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Paper {
  id: number
  title: string
  authors: string
  upload_time: string
  download_count: number
}

const papers = ref<Paper[]>([])

const handleUpload = () => {
  // 上传论文逻辑
  console.log('上传论文')
}

const handleView = (paper: Paper) => {
  // 查看论文详情
  console.log('查看论文:', paper)
}

const handleDownload = (paper: Paper) => {
  // 下载论文
  console.log('下载论文:', paper)
}

onMounted(async () => {
  // 模拟数据
  papers.value = [
    {
      id: 1,
      title: '深度学习在计算机视觉中的应用',
      authors: '张三, 李四',
      upload_time: '2026-03-01',
      download_count: 10
    }
  ]
})
</script>

<style scoped lang="scss">
.papers-container {
  h2 {
    margin-bottom: 20px;
    color: #333;
  }
  
  .el-button {
    margin-bottom: 20px;
  }
}
</style>
