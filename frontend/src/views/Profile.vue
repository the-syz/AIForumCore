<template>
  <div class="profile-container">
    <h2>个人中心</h2>
    <el-tabs v-model="activeTab" type="border-card">
      <el-tab-pane label="个人信息" name="info">
        <el-card>
          <el-form :model="userInfo" :rules="rules" ref="formRef" label-width="120px">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="userInfo.name" :disabled="!isEditing" />
            </el-form-item>
            <el-form-item label="学号/工号" prop="student_id">
              <el-input v-model="userInfo.student_id" disabled />
            </el-form-item>
            <el-form-item label="身份" prop="role">
              <el-input v-model="userInfo.role_display" disabled />
            </el-form-item>
            <el-form-item label="年级" prop="grade">
              <el-input v-model="userInfo.grade" :disabled="!isEditing" />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="userInfo.email" :disabled="!isEditing" />
            </el-form-item>
            <el-form-item label="电话" prop="phone">
              <el-input v-model="userInfo.phone" :disabled="!isEditing" />
            </el-form-item>
            <el-form-item label="研究方向" prop="research_direction">
              <el-input v-model="userInfo.research_direction" :disabled="!isEditing" />
            </el-form-item>
            <el-form-item label="微信" prop="wechat">
              <el-input v-model="userInfo.wechat" :disabled="!isEditing" />
            </el-form-item>
            <el-form-item>
              <template v-if="!isEditing">
                <el-button type="primary" @click="startEdit">编辑信息</el-button>
                <el-button @click="showPasswordDialog = true">修改密码</el-button>
              </template>
              <template v-else>
                <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
                <el-button @click="cancelEdit">取消</el-button>
              </template>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="我的发布" name="my-posts">
        <el-tabs v-model="postsTab" type="card">
          <el-tab-pane label="论文" name="papers">
            <div class="my-papers-section">
              <el-table :data="myPapers" style="width: 100%" v-loading="loadingPapers">
                <el-table-column prop="title" label="标题" />
                <el-table-column prop="authors" label="作者" width="150" />
                <el-table-column prop="upload_time" label="上传时间" width="180">
                  <template #default="{ row }">
                    {{ formatDate(row.upload_time) }}
                  </template>
                </el-table-column>
                <el-table-column prop="download_count" label="下载次数" width="100" />
                <el-table-column label="操作" width="200">
                  <template #default="{ row }">
                    <el-button size="small" @click="viewPaper(row.id)">查看</el-button>
                    <el-button size="small" @click="editPaper(row.id)">编辑</el-button>
                  </template>
                </el-table-column>
              </el-table>
              <el-empty v-if="myPapers.length === 0 && !loadingPapers" description="暂无上传的论文" />
            </div>
          </el-tab-pane>
          <el-tab-pane label="经验贴" name="posts">
            <div class="my-posts-section">
              <el-table :data="myPosts" style="width: 100%" v-loading="loadingPosts">
                <el-table-column prop="title" label="标题" />
                <el-table-column prop="category" label="分类" width="100" />
                <el-table-column prop="created_at" label="发布时间" width="180">
                  <template #default="{ row }">
                    {{ formatDate(row.created_at) }}
                  </template>
                </el-table-column>
                <el-table-column prop="view_count" label="浏览量" width="80" />
                <el-table-column label="操作" width="200">
                  <template #default="{ row }">
                    <el-button size="small" @click="viewPost(row.id)">查看</el-button>
                    <el-button size="small" @click="editPost(row.id)">编辑</el-button>
                  </template>
                </el-table-column>
              </el-table>
              <el-empty v-if="myPosts.length === 0 && !loadingPosts" description="暂无发布的经验贴" />
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-tab-pane>

      <el-tab-pane label="我的收藏" name="favorites">
        <el-tabs v-model="favoritesTab" type="card">
          <el-tab-pane label="论文" name="favorite-papers">
            <div class="favorite-papers-section">
              <el-table :data="favoritePapers" style="width: 100%" v-loading="loadingFavorites">
                <el-table-column prop="title" label="标题" />
                <el-table-column prop="authors" label="作者" width="150" />
                <el-table-column prop="upload_time" label="上传时间" width="180">
                  <template #default="{ row }">
                    {{ formatDate(row.upload_time) }}
                  </template>
                </el-table-column>
                <el-table-column prop="favorited_at" label="收藏时间" width="180">
                  <template #default="{ row }">
                    {{ formatDate(row.favorited_at) }}
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="120">
                  <template #default="{ row }">
                    <el-button size="small" @click="viewPaper(row.id)">查看</el-button>
                  </template>
                </el-table-column>
              </el-table>
              <el-empty v-if="favoritePapers.length === 0 && !loadingFavorites" description="暂无收藏的论文" />
            </div>
          </el-tab-pane>
          <el-tab-pane label="经验贴" name="favorite-posts">
            <div class="favorite-posts-section">
              <el-table :data="favoritePosts" style="width: 100%" v-loading="loadingFavorites">
                <el-table-column prop="title" label="标题" />
                <el-table-column prop="category" label="分类" width="100" />
                <el-table-column prop="created_at" label="发布时间" width="180">
                  <template #default="{ row }">
                    {{ formatDate(row.created_at) }}
                  </template>
                </el-table-column>
                <el-table-column prop="favorited_at" label="收藏时间" width="180">
                  <template #default="{ row }">
                    {{ formatDate(row.favorited_at) }}
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="120">
                  <template #default="{ row }">
                    <el-button size="small" @click="viewPost(row.id)">查看</el-button>
                  </template>
                </el-table-column>
              </el-table>
              <el-empty v-if="favoritePosts.length === 0 && !loadingFavorites" description="暂无收藏的经验贴" />
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="showPasswordDialog" title="修改密码" width="400px">
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="80px">
        <el-form-item label="旧密码" prop="old_password">
          <el-input v-model="passwordForm.old_password" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="passwordForm.new_password" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input v-model="passwordForm.confirm_password" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPasswordDialog = false">取消</el-button>
        <el-button type="primary" @click="handleChangePassword" :loading="changingPassword">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import { getCurrentUser, updateCurrentUser, changePassword, getUserPapers, getUserPosts } from '@/api/users'
import { getFavorites } from '@/api/forum'
import { getPaperById } from '@/api/papers'
import { getPostById } from '@/api/posts'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref()
const passwordFormRef = ref()

const activeTab = ref('info')
const postsTab = ref('papers')
const favoritesTab = ref('favorite-papers')
const isEditing = ref(false)
const saving = ref(false)
const changingPassword = ref(false)
const showPasswordDialog = ref(false)
const loadingPapers = ref(false)
const loadingPosts = ref(false)
const loadingFavorites = ref(false)

// 角色映射
const roleMap: Record<string, string> = {
  'master': '硕士研究生',
  'phd': '博士研究生',
  'graduate': '毕业生',
  'teacher': '教师'
}

const originalUserInfo = ref<any>({})
const userInfo = reactive({
  name: '',
  student_id: '',
  role: '',
  role_display: '',
  grade: '',
  email: '',
  phone: '',
  research_direction: '',
  wechat: ''
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  email: [{ type: 'email', message: '请输入正确的邮箱', trigger: 'blur' }]
}

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const validateConfirmPassword = (rule: any, value: any, callback: any) => {
  if (value !== passwordForm.new_password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  old_password: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const myPapers = ref<any[]>([])
const myPosts = ref<any[]>([])
const favoritePapers = ref<any[]>([])
const favoritePosts = ref<any[]>([])

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const loadUserInfo = async () => {
  try {
    const data = await getCurrentUser()
    Object.assign(userInfo, {
      name: data.name,
      student_id: data.student_id,
      role: data.role || '',
      role_display: roleMap[data.role] || data.role || '未知',
      grade: data.grade || '',
      email: data.email || '',
      phone: data.phone || '',
      research_direction: data.research_direction || '',
      wechat: data.wechat || ''
    })
    Object.assign(originalUserInfo.value, userInfo)
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

const loadMyPapers = async () => {
  if (!userStore.userInfo) return
  loadingPapers.value = true
  try {
    const papers = await getUserPapers(userStore.userInfo.id)
    myPapers.value = papers
  } catch (error) {
    console.error('获取我的论文失败:', error)
  } finally {
    loadingPapers.value = false
  }
}

const loadMyPosts = async () => {
  if (!userStore.userInfo) return
  loadingPosts.value = true
  try {
    const posts = await getUserPosts(userStore.userInfo.id)
    myPosts.value = posts
  } catch (error) {
    console.error('获取我的经验贴失败:', error)
  } finally {
    loadingPosts.value = false
  }
}

const loadFavorites = async () => {
  if (!userStore.userInfo) return
  loadingFavorites.value = true
  try {
    const favorites = await getFavorites()
    
    // 清空之前的数据
    favoritePapers.value = []
    favoritePosts.value = []
    
    // 按类型分类处理
    for (const fav of favorites) {
      if (fav.target_type === 'paper') {
        try {
          const paper = await getPaperById(fav.target_id)
          favoritePapers.value.push({ ...paper, favorite_id: fav.id, favorited_at: fav.created_at })
        } catch (error) {
          console.error(`获取收藏的论文 ${fav.target_id} 失败:`, error)
        }
      } else if (fav.target_type === 'post') {
        try {
          const post = await getPostById(fav.target_id)
          favoritePosts.value.push({ ...post, favorite_id: fav.id, favorited_at: fav.created_at })
        } catch (error) {
          console.error(`获取收藏的经验贴 ${fav.target_id} 失败:`, error)
        }
      }
    }
  } catch (error) {
    console.error('获取收藏列表失败:', error)
  } finally {
    loadingFavorites.value = false
  }
}

const startEdit = () => {
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
  Object.assign(userInfo, originalUserInfo.value)
}

const handleSave = async () => {
  await formRef.value.validate()
  saving.value = true
  try {
    await updateCurrentUser(userInfo)
    ElMessage.success('信息更新成功')
    isEditing.value = false
    Object.assign(originalUserInfo.value, userInfo)
    await loadUserInfo()
  } catch (error: any) {
    ElMessage.error(error.message || '更新失败')
  } finally {
    saving.value = false
  }
}

const handleChangePassword = async () => {
  await passwordFormRef.value.validate()
  changingPassword.value = true
  try {
    await changePassword({
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password
    })
    ElMessage.success('密码修改成功')
    showPasswordDialog.value = false
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  } catch (error: any) {
    ElMessage.error(error.message || '密码修改失败')
  } finally {
    changingPassword.value = false
  }
}

const viewPaper = (id: number) => {
  router.push(`/papers/${id}`)
}

const editPaper = (id: number) => {
  router.push(`/papers/edit/${id}`)
}

const viewPost = (id: number) => {
  router.push(`/posts/${id}`)
}

const editPost = (id: number) => {
  router.push(`/posts/edit/${id}`)
}

onMounted(() => {
  loadUserInfo()
  loadMyPapers()
  loadMyPosts()
  loadFavorites()
})
</script>

<style scoped lang="scss">
.profile-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  
  h2 {
    margin-bottom: 20px;
    color: #333;
  }
  
  .my-papers-section,
  .my-posts-section,
  .favorite-papers-section,
  .favorite-posts-section {
    margin-top: 20px;
  }
}
</style>
