<template>
  <div class="papers-container">
    <div class="papers-header">
      <h2>论文管理</h2>
      <div class="papers-actions">
        <div class="search-box">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索论文标题、作者..."
            suffix-icon="el-icon-search"
            @keyup.enter="handleSearch"
          >
            <template #append>
              <el-button type="primary" @click="handleSearch">搜索</el-button>
            </template>
          </el-input>
        </div>
        <el-button v-if="isSearching" type="info" @click="handleReset">重置</el-button>
        <el-button type="primary" @click="handleUpload">上传论文</el-button>
      </div>
    </div>
    
    <el-table v-if="!loading" :data="papers" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="authors" label="作者" />
      <el-table-column prop="category" label="研究领域" width="120" />
      <el-table-column prop="upload_time" label="上传时间" width="180" />
      <el-table-column prop="download_count" label="下载次数" width="100" />
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button size="small" @click="handleView(scope.row)">查看</el-button>
          <el-button size="small" @click="handleDownload(scope.row)">下载</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <el-skeleton v-else :rows="10" animated style="width: 100%" />
    
    <div v-if="error" class="error-message">
      <el-alert
        title="获取论文列表失败"
        type="error"
        :closable="false"
        show-icon
      />
      <el-button type="primary" @click="fetchPapers" style="margin-top: 10px">重新加载</el-button>
    </div>
    
    <div v-if="!loading && papers.length === 0" class="empty-message">
      <el-empty description="暂无论文数据" />
    </div>
    
    <div v-if="!loading && papers.length > 0" class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getPapers, downloadPaper } from '@/api/papers'
import { searchPapers } from '@/api/search'
import { ElMessage } from 'element-plus'

interface Paper {
  id: number
  title: string
  authors: string
  category?: string
  upload_time: string
  download_count: number
}

const router = useRouter()
const papers = ref<Paper[]>([])
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)
const error = ref(false)
const isSearching = ref(false)

const handleUpload = () => {
  // 跳转到论文上传页面
  router.push('/papers/upload')
}

const handleView = (paper: Paper) => {
  // 跳转到论文详情页面
  router.push(`/papers/${paper.id}`)
}

const handleDownload = async (paper: Paper) => {
  // 下载论文
  try {
    await downloadPaper(paper.id)
    ElMessage.success('下载成功')
  } catch (error) {
    ElMessage.error('下载失败')
  }
}

const handleSearch = () => {
  if (!searchKeyword.value.trim()) {
    handleReset()
    return
  }
  isSearching.value = true
  currentPage.value = 1
  fetchPapers()
}

const handleReset = () => {
  searchKeyword.value = ''
  isSearching.value = false
  currentPage.value = 1
  fetchPapers()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  fetchPapers()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  fetchPapers()
}

const fetchPapers = async () => {
  loading.value = true
  error.value = false
  
  try {
    console.log('开始获取论文列表...')
    if (searchKeyword.value.trim()) {
      const response = await searchPapers(searchKeyword.value.trim())
      papers.value = response.items || []
      total.value = response.total || 0
    } else {
      const response = await getPapers({
        page: currentPage.value,
        page_size: pageSize.value
      })
      console.log('获取论文列表成功:', response)
      papers.value = response.items || []
      total.value = response.total || 0
    }
    console.log('论文列表数据:', papers.value)
    console.log('论文总数:', total.value)
  } catch (error) {
    console.error('获取论文列表失败:', error)
    error.value = true
    papers.value = []
    total.value = 0
    ElMessage.error('获取论文列表失败，请稍后重试')
  } finally {
    console.log('获取论文列表完成，设置loading为false')
    loading.value = false
  }
}

onMounted(() => {
  fetchPapers()
})
</script>

<style scoped scss>
.papers-container {
  .papers-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      color: #333;
      margin: 0;
    }
    
    .papers-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      
      .search-box {
        min-width: 300px;
      }
    }
  }
  
  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
