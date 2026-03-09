<template>
  <div class="downloads-container">
    <div class="page-header">
      <h2>下载中心</h2>
      <el-button v-if="isAdmin" type="primary" @click="router.push('/downloads/upload')">上传资源</el-button>
    </div>
    
    <!-- 搜索和筛选 -->
    <div class="search-filter">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索资源标题"
        style="width: 300px; margin-right: 10px"
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button @click="handleSearch"><el-icon><Search /></el-icon></el-button>
        </template>
      </el-input>
      <el-select
          v-model="selectedCategory"
          placeholder="筛选分类"
          style="width: 150px; margin-right: 10px"
          @change="handleSearch"
        >
          <el-option label="全部" value="" />
          <el-option label="科研资源" value="科研资源" />
          <el-option label="常用文件" value="常用文件" />
          <el-option label="其他" value="其他" />
        </el-select>
      <el-button type="info" @click="resetFilter">重置</el-button>
    </div>
    
    <!-- 资源列表 -->
    <el-table 
      v-loading="loading" 
      :data="filteredDownloads" 
      style="width: 100%"
      @row-click="handleRowClick"
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="category" label="分类" width="120" />
      <el-table-column prop="upload_time" label="上传时间" width="180" />
      <el-table-column prop="download_count" label="下载次数" width="100" />
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" @click.stop="handleDownload(scope.row)">下载</el-button>
          <el-button v-if="isAdmin" size="small" type="primary" @click.stop="handleEdit(scope.row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { getDownloads, downloadResource } from '@/api/downloads'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

interface Download {
  id: number
  title: string
  category: string
  upload_time: string
  download_count: number
}

const router = useRouter()
const userStore = useUserStore()

const downloads = ref<Download[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchKeyword = ref('')
const selectedCategory = ref('')

const isAdmin = computed(() => userStore.isAdmin)

const filteredDownloads = computed(() => {
  let result = downloads.value
  
  // 搜索筛选
  if (searchKeyword.value) {
    result = result.filter(item => 
      item.title.toLowerCase().includes(searchKeyword.value.toLowerCase())
    )
  }
  
  // 分类筛选
  if (selectedCategory.value) {
    result = result.filter(item => item.category === selectedCategory.value)
  }
  
  return result
})

const handleSearch = () => {
  currentPage.value = 1
  loadDownloads()
}

const resetFilter = () => {
  searchKeyword.value = ''
  selectedCategory.value = ''
  currentPage.value = 1
  loadDownloads()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  loadDownloads()
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
  loadDownloads()
}

const handleDownload = async (download: Download) => {
  try {
    await downloadResource(download.id)
    ElMessage.success('下载开始')
    // 刷新列表以更新下载次数
    loadDownloads()
  } catch (error) {
    ElMessage.error('下载失败，请重试')
    console.error('下载资源失败:', error)
  }
}

const handleEdit = (download: Download) => {
  router.push(`/downloads/edit/${download.id}`)
}

const handleRowClick = (row: Download) => {
  router.push(`/downloads/${row.id}`)
}

const loadDownloads = async () => {
  loading.value = true
  try {
    const data = await getDownloads()
    downloads.value = data
    total.value = data.length
  } catch (error) {
    ElMessage.error('获取资源列表失败')
    console.error('获取资源列表失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDownloads()
})
</script>

<style scoped lang="scss">
.downloads-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      margin: 0;
      color: #333;
      font-size: 22px;
      font-weight: 600;
    }
  }
  
  .search-filter {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
  
  :deep(.el-table__row) {
    cursor: pointer;
    
    &:hover {
      background-color: #f5f7fa;
    }
  }
}
</style>
