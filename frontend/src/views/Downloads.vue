<template>
  <div class="downloads-container">
    <h2>下载中心</h2>
    <el-table :data="downloads" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="category" label="分类" />
      <el-table-column prop="upload_time" label="上传时间" />
      <el-table-column prop="download_count" label="下载次数" />
      <el-table-column label="操作" width="100">
        <template #default="scope">
          <el-button size="small" @click="handleDownload(scope.row)">下载</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Download {
  id: number
  title: string
  category: string
  upload_time: string
  download_count: number
}

const downloads = ref<Download[]>([])

const handleDownload = (download: Download) => {
  // 下载资源
  console.log('下载资源:', download)
}

onMounted(async () => {
  // 模拟数据
  downloads.value = [
    {
      id: 1,
      title: '深度学习入门教程',
      category: '学习资料',
      upload_time: '2026-03-01',
      download_count: 20
    }
  ]
})
</script>

<style scoped lang="scss">
.downloads-container {
  h2 {
    margin-bottom: 20px;
    color: #333;
  }
}
</style>
