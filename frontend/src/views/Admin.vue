<template>
  <div class="admin-container">
    <h2>管理员中心</h2>
    <el-tabs>
      <el-tab-pane label="用户管理">
        <div class="search-section">
          <el-button type="primary">添加用户</el-button>
          <el-input
            v-model="userSearchKeyword"
            placeholder="搜索用户姓名"
            style="width: 250px; margin-left: 10px; margin-right: 10px"
            @keyup.enter="handleUserSearch"
          >
            <template #append>
              <el-button @click="handleUserSearch"><el-icon><Search /></el-icon></el-button>
            </template>
          </el-input>
          <el-button type="info" @click="resetUserSearch">重置</el-button>
        </div>
        <el-table :data="filteredUsers" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="student_id" label="学号/工号" />
          <el-table-column prop="role" label="角色" />
          <el-table-column prop="is_admin" label="是否管理员" />
          <el-table-column label="操作" width="150">
            <template #default="scope">
              <el-button size="small" @click="handleEditUser(scope.row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDeleteUser(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="论文管理">
        <div class="search-section">
          <el-input
            v-model="paperSearchKeyword"
            placeholder="搜索论文标题、作者"
            style="width: 300px; margin-right: 10px"
            @keyup.enter="handlePaperSearch"
          >
            <template #append>
              <el-button @click="handlePaperSearch"><el-icon><Search /></el-icon></el-button>
            </template>
          </el-input>
          <el-button type="info" @click="resetPaperSearch">重置</el-button>
        </div>
        <el-table v-loading="papersLoading" :data="filteredPapers" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="标题" />
          <el-table-column prop="authors" label="作者" />
          <el-table-column prop="paper_type" label="类型" width="100" />
          <el-table-column prop="upload_time" label="上传时间" width="180" />
          <el-table-column prop="download_count" label="下载次数" width="100" />
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <el-button size="small" @click="handleEditPaper(scope.row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDeletePaper(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="经验贴管理">
        <div class="search-section">
          <el-input
            v-model="postSearchKeyword"
            placeholder="搜索经验贴标题"
            style="width: 300px; margin-right: 10px"
            @keyup.enter="handlePostSearch"
          >
            <template #append>
              <el-button @click="handlePostSearch"><el-icon><Search /></el-icon></el-button>
            </template>
          </el-input>
          <el-select
            v-model="postCategoryFilter"
            placeholder="筛选分类"
            style="width: 150px; margin-right: 10px"
            @change="handlePostSearch"
          >
            <el-option label="全部" value="" />
            <el-option label="学习经验" value="学习经验" />
            <el-option label="科研经验" value="科研经验" />
            <el-option label="生活经验" value="生活经验" />
            <el-option label="其他" value="其他" />
          </el-select>
          <el-button type="info" @click="resetPostSearch">重置</el-button>
        </div>
        <el-table v-loading="postsLoading" :data="filteredPosts" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="标题" />
          <el-table-column prop="category" label="分类" width="100" />
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column prop="view_count" label="浏览量" width="80" />
          <el-table-column label="状态" width="100">
            <template #default="scope">
              <el-tag v-if="scope.row.is_pinned" type="danger">置顶</el-tag>
              <el-tag v-else-if="scope.row.is_draft" type="info">草稿</el-tag>
              <el-tag v-else>正常</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="250">
            <template #default="scope">
              <el-button 
                size="small" 
                :type="scope.row.is_pinned ? 'warning' : 'success'"
                @click="handlePinPost(scope.row)"
              >
                {{ scope.row.is_pinned ? '取消置顶' : '置顶' }}
              </el-button>
              <el-button size="small" @click="handleEditPost(scope.row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDeletePost(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="下载中心管理">
        <div class="search-section">
          <el-button type="primary" @click="router.push('/downloads/upload')">上传资源</el-button>
          <el-input
            v-model="downloadSearchKeyword"
            placeholder="搜索资源标题"
            style="width: 300px; margin-left: 10px; margin-right: 10px"
            @keyup.enter="handleDownloadSearch"
          >
            <template #append>
              <el-button @click="handleDownloadSearch"><el-icon><Search /></el-icon></el-button>
            </template>
          </el-input>
          <el-select
            v-model="downloadCategoryFilter"
            placeholder="筛选分类"
            style="width: 150px; margin-right: 10px"
            @change="handleDownloadSearch"
          >
            <el-option label="全部" value="" />
            <el-option label="科研资源" value="科研资源" />
            <el-option label="常用文件" value="常用文件" />
            <el-option label="其他" value="其他" />
          </el-select>
          <el-button type="info" @click="resetDownloadSearch">重置</el-button>
        </div>
        <el-table v-loading="downloadsLoading" :data="filteredDownloads" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="标题" />
          <el-table-column prop="category" label="分类" width="100" />
          <el-table-column prop="upload_time" label="上传时间" width="180" />
          <el-table-column prop="download_count" label="下载次数" width="100" />
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <el-button size="small" @click="handleEditDownload(scope.row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDeleteDownload(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getPapers, deletePaper } from '@/api/papers'
import { getPosts, deletePost, pinPost } from '@/api/posts'
import { getDownloads, deleteDownload } from '@/api/downloads'

const router = useRouter()

interface User {
  id: number
  name: string
  student_id: string
  role: string
  is_admin: boolean
}

interface Paper {
  id: number
  title: string
  authors: string
  paper_type: string
  upload_time: string
  download_count: number
}

interface Post {
  id: number
  title: string
  category: string
  created_at: string
  view_count: number
  is_pinned: boolean
  is_draft: boolean
}

interface Download {
  id: number
  title: string
  category: string
  upload_time: string
  download_count: number
}

const users = ref<User[]>([])
const papers = ref<Paper[]>([])
const posts = ref<Post[]>([])
const downloads = ref<Download[]>([])

const papersLoading = ref(false)
const postsLoading = ref(false)
const downloadsLoading = ref(false)

const userSearchKeyword = ref('')
const paperSearchKeyword = ref('')
const postSearchKeyword = ref('')
const postCategoryFilter = ref('')
const downloadSearchKeyword = ref('')
const downloadCategoryFilter = ref('')

const filteredUsers = computed(() => {
  if (!userSearchKeyword.value) return users.value
  const keyword = userSearchKeyword.value.toLowerCase()
  return users.value.filter(user => 
    user.name.toLowerCase().includes(keyword)
  )
})

const filteredPapers = computed(() => {
  if (!paperSearchKeyword.value) return papers.value
  const keyword = paperSearchKeyword.value.toLowerCase()
  return papers.value.filter(paper => 
    paper.title.toLowerCase().includes(keyword) || 
    paper.authors.toLowerCase().includes(keyword)
  )
})

const filteredPosts = computed(() => {
  let result = posts.value
  if (postSearchKeyword.value) {
    const keyword = postSearchKeyword.value.toLowerCase()
    result = result.filter(post => post.title.toLowerCase().includes(keyword))
  }
  if (postCategoryFilter.value) {
    result = result.filter(post => post.category === postCategoryFilter.value)
  }
  return result
})

const filteredDownloads = computed(() => {
  let result = downloads.value
  if (downloadSearchKeyword.value) {
    const keyword = downloadSearchKeyword.value.toLowerCase()
    result = result.filter(download => download.title.toLowerCase().includes(keyword))
  }
  if (downloadCategoryFilter.value) {
    result = result.filter(download => download.category === downloadCategoryFilter.value)
  }
  return result
})

const handleUserSearch = () => {}
const resetUserSearch = () => { userSearchKeyword.value = '' }
const handlePaperSearch = () => {}
const resetPaperSearch = () => { paperSearchKeyword.value = '' }
const handlePostSearch = () => {}
const resetPostSearch = () => { 
  postSearchKeyword.value = ''
  postCategoryFilter.value = ''
}
const handleDownloadSearch = () => {}
const resetDownloadSearch = () => { 
  downloadSearchKeyword.value = ''
  downloadCategoryFilter.value = ''
}

const handleEditUser = (user: User) => {
  console.log('编辑用户:', user)
}

const handleDeleteUser = (user: User) => {
  ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('删除成功')
  }).catch(() => {})
}

const handleEditPaper = (paper: Paper) => {
  router.push(`/papers/edit/${paper.id}`)
}

const handleDeletePaper = (paper: Paper) => {
  ElMessageBox.confirm('确定要删除该论文吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deletePaper(paper.id)
      ElMessage.success('论文删除成功')
      loadPapers()
    } catch (error) {
      ElMessage.error('删除失败')
      console.error('删除论文失败:', error)
    }
  }).catch(() => {})
}

const handlePinPost = (post: Post) => {
  const newPinStatus = !post.is_pinned
  const action = newPinStatus ? '置顶' : '取消置顶'
  
  ElMessageBox.confirm(`确定要${action}该经验贴吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await pinPost(post.id, newPinStatus)
      ElMessage.success(`${action}成功`)
      loadPosts()
    } catch (error) {
      ElMessage.error(`${action}失败`)
      console.error(`${action}失败:`, error)
    }
  }).catch(() => {})
}

const handleEditPost = (post: Post) => {
  router.push(`/posts/edit/${post.id}`)
}

const handleDeletePost = (post: Post) => {
  ElMessageBox.confirm('确定要删除该经验贴吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deletePost(post.id)
      ElMessage.success('经验贴删除成功')
      loadPosts()
    } catch (error) {
      ElMessage.error('删除失败')
      console.error('删除经验贴失败:', error)
    }
  }).catch(() => {})
}

const handleEditDownload = (download: Download) => {
  router.push(`/downloads/edit/${download.id}`)
}

const handleDeleteDownload = (download: Download) => {
  ElMessageBox.confirm('确定要删除该资源吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteDownload(download.id)
      ElMessage.success('资源删除成功')
      loadDownloads()
    } catch (error) {
      ElMessage.error('删除失败')
      console.error('删除资源失败:', error)
    }
  }).catch(() => {})
}

const loadPapers = async () => {
  papersLoading.value = true
  try {
    const response = await getPapers()
    papers.value = response.items || []
  } catch (error) {
    console.error('获取论文列表失败:', error)
  } finally {
    papersLoading.value = false
  }
}

const loadPosts = async () => {
  postsLoading.value = true
  try {
    const data = await getPosts()
    posts.value = data
  } catch (error) {
    console.error('获取经验贴列表失败:', error)
  } finally {
    postsLoading.value = false
  }
}

const loadDownloads = async () => {
  downloadsLoading.value = true
  try {
    const data = await getDownloads()
    downloads.value = data
  } catch (error) {
    console.error('获取下载资源列表失败:', error)
  } finally {
    downloadsLoading.value = false
  }
}

onMounted(async () => {
  users.value = [
    {
      id: 1,
      name: '张三',
      student_id: '2023001',
      role: 'student',
      is_admin: false
    }
  ]
  
  loadPapers()
  loadPosts()
  loadDownloads()
})
</script>

<style scoped lang="scss">
.admin-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  
  h2 {
    margin-bottom: 20px;
    color: #333;
    font-size: 22px;
    font-weight: 600;
  }
  
  .search-section {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 10px;
  }
}
</style>