<template>
  <div class="user-profile-container">
    <el-card v-loading="loading" class="user-info-card">
      <template #header>
        <div class="card-header">
          <h2>{{ userInfo?.name }}的个人主页</h2>
        </div>
      </template>
      
      <div class="user-info-section" v-if="userInfo">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="姓名">{{ userInfo.name }}</el-descriptions-item>
          <el-descriptions-item label="学号/工号">{{ userInfo.student_id }}</el-descriptions-item>
          <el-descriptions-item label="年级">{{ userInfo.grade || '未填写' }}</el-descriptions-item>
          <el-descriptions-item label="身份">
            <el-tag :type="userInfo.role === 'teacher' ? 'success' : 'primary'">
              {{ getRoleDisplay(userInfo.role) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ userInfo.email || '未填写' }}</el-descriptions-item>
          <el-descriptions-item label="电话">{{ userInfo.phone || '未填写' }}</el-descriptions-item>
          <el-descriptions-item label="研究方向" :span="2">{{ userInfo.research_direction || '未填写' }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>

    <el-card class="user-posts-card">
      <template #header>
        <div class="card-header">
          <h3>发布的内容</h3>
        </div>
      </template>
      
      <el-tabs v-model="activeTab" type="card">
        <el-tab-pane label="论文" name="papers">
          <div class="papers-list">
            <el-table :data="userPapers" style="width: 100%" v-loading="loadingPapers">
              <el-table-column prop="title" label="标题" />
              <el-table-column prop="authors" label="作者" width="150" />
              <el-table-column prop="upload_time" label="上传时间" width="180">
                <template #default="{ row }">
                  {{ formatDate(row.upload_time) }}
                </template>
              </el-table-column>
              <el-table-column prop="download_count" label="下载次数" width="100" />
              <el-table-column label="操作" width="100">
                <template #default="{ row }">
                  <el-button size="small" @click="viewPaper(row.id)">查看</el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-empty v-if="userPapers.length === 0 && !loadingPapers" description="暂无上传的论文" />
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="经验贴" name="posts">
          <div class="posts-list">
            <el-table :data="userPosts" style="width: 100%" v-loading="loadingPosts">
              <el-table-column prop="title" label="标题" />
              <el-table-column prop="category" label="分类" width="100" />
              <el-table-column prop="created_at" label="发布时间" width="180">
                <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column prop="view_count" label="浏览量" width="80" />
              <el-table-column label="操作" width="100">
                <template #default="{ row }">
                  <el-button size="small" @click="viewPost(row.id)">查看</el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-empty v-if="userPosts.length === 0 && !loadingPosts" description="暂无发布的经验贴" />
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getUserPublic, getUserPapers, getUserPosts } from '@/api/users'

const route = useRoute()
const router = useRouter()

// 角色显示映射
const roleDisplayMap: Record<string, string> = {
  'master': '硕士研究生',
  'phd': '博士研究生',
  'graduate': '毕业生',
  'teacher': '教师',
  'student': '学生'  // 兼容旧数据
}

// 获取角色显示名称
const getRoleDisplay = (role: string): string => {
  return roleDisplayMap[role] || role || '未知'
}

const loading = ref(false)
const loadingPapers = ref(false)
const loadingPosts = ref(false)
const activeTab = ref('papers')
const userInfo = ref<any>(null)
const userPapers = ref<any[]>([])
const userPosts = ref<any[]>([])

const userId = computed(() => Number(route.params.id))

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const loadUserInfo = async () => {
  loading.value = true
  try {
    userInfo.value = await getUserPublic(userId.value)
  } catch (error) {
    ElMessage.error('获取用户信息失败')
    console.error('获取用户信息失败:', error)
  } finally {
    loading.value = false
  }
}

const loadUserPapers = async () => {
  loadingPapers.value = true
  try {
    userPapers.value = await getUserPapers(userId.value)
  } catch (error) {
    console.error('获取用户论文失败:', error)
  } finally {
    loadingPapers.value = false
  }
}

const loadUserPosts = async () => {
  loadingPosts.value = true
  try {
    userPosts.value = await getUserPosts(userId.value)
  } catch (error) {
    console.error('获取用户经验贴失败:', error)
  } finally {
    loadingPosts.value = false
  }
}

const viewPaper = (id: number) => {
  router.push(`/papers/${id}`)
}

const viewPost = (id: number) => {
  router.push(`/posts/${id}`)
}

onMounted(() => {
  loadUserInfo()
  loadUserPapers()
  loadUserPosts()
})
</script>

<style scoped lang="scss">
.user-profile-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  
  .user-info-card,
  .user-posts-card {
    margin-bottom: 20px;
    
    .card-header {
      h2, h3 {
        margin: 0;
        color: #333;
      }
    }
    
    .user-info-section {
      margin-top: 10px;
    }
  }
  
  .papers-list,
  .posts-list {
    margin-top: 20px;
  }
}
</style>
