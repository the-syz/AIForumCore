<template>
  <div class="admin-container">
    <h2>管理员中心</h2>
    <el-tabs>
      <el-tab-pane label="用户管理">
        <div class="search-section">
          <el-button type="primary" @click="showAddUserDialog = true">添加用户</el-button>
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
        <el-table :data="filteredUsers" style="width: 100%" v-loading="usersLoading">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="student_id" label="学号/工号" />
          <el-table-column label="身份" width="120">
            <template #default="{ row }">
              {{ getRoleDisplay(row.role) }}
            </template>
          </el-table-column>
          <el-table-column label="是否管理员" width="120">
            <template #default="{ row }">
              <el-tag :type="row.is_admin ? 'danger' : 'info'">
                {{ row.is_admin ? '是' : '否' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="280">
            <template #default="scope">
              <el-button size="small" @click="handleEditUser(scope.row)">编辑</el-button>
              <el-button 
                size="small" 
                @click="handleSetRole(scope.row)"
                :disabled="
                  // 教师用户无法修改自己的身份和管理员权限
                  (scope.row.role === 'teacher' && scope.row.id === currentUser?.value?.id) ||
                  // 学生管理员无法修改其他教师的权限
                  (currentUser?.value?.role !== 'teacher' && scope.row.role === 'teacher')
                "
              >权限</el-button>
              <el-button 
                size="small" 
                type="danger" 
                @click="handleDeleteUser(scope.row)"
                :disabled="
                  // 无法删除自己
                  scope.row.id === currentUser?.value?.id ||
                  // 学生管理员无法删除教师
                  (currentUser?.value?.role !== 'teacher' && scope.row.role === 'teacher')
                "
              >删除</el-button>
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
          <el-table-column prop="upload_time" label="上传时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.upload_time) }}
            </template>
          </el-table-column>
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
          <el-table-column prop="created_at" label="创建时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
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
          <el-table-column prop="upload_time" label="上传时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.upload_time) }}
            </template>
          </el-table-column>
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

    <el-dialog v-model="showAddUserDialog" title="添加用户" width="500px">
      <el-form :model="addUserForm" :rules="addUserRules" ref="addUserFormRef" label-width="100px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="addUserForm.name" />
        </el-form-item>
        <el-form-item label="学号" prop="student_id">
          <el-input v-model="addUserForm.student_id" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="addUserForm.password" type="password" show-password />
        </el-form-item>
        <el-form-item label="年级" prop="grade">
          <el-input v-model="addUserForm.grade" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="addUserForm.email" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="addUserForm.phone" />
        </el-form-item>
        <el-form-item label="研究方向" prop="research_direction">
          <el-input v-model="addUserForm.research_direction" />
        </el-form-item>
        <el-form-item label="微信" prop="wechat">
          <el-input v-model="addUserForm.wechat" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddUserDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAddUser" :loading="addingUser">添加</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showEditUserDialog" title="编辑用户" width="500px">
      <el-form :model="editUserForm" :rules="editUserRules" ref="editUserFormRef" label-width="100px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="editUserForm.name" />
        </el-form-item>
        <el-form-item label="学号" prop="student_id">
          <el-input v-model="editUserForm.student_id" />
        </el-form-item>
        <el-form-item label="年级" prop="grade">
          <el-input v-model="editUserForm.grade" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editUserForm.email" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="editUserForm.phone" />
        </el-form-item>
        <el-form-item label="研究方向" prop="research_direction">
          <el-input v-model="editUserForm.research_direction" />
        </el-form-item>
        <el-form-item label="微信" prop="wechat">
          <el-input v-model="editUserForm.wechat" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditUserDialog = false">取消</el-button>
        <el-button type="primary" @click="handleUpdateUser" :loading="updatingUser">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showSetRoleDialog" title="设置权限" width="400px">
      <el-form :model="setRoleForm" label-width="100px">
        <el-form-item label="身份">
          <el-select 
            v-model="setRoleForm.role"
            :disabled="
              // 教师用户无法修改自己的身份
              (currentUser?.value?.role === 'teacher' && setRoleForm.id === currentUser.value.id) ||
              // 学生管理员无法设置教师身份
              (currentUser?.value?.role !== 'teacher' && setRoleForm.role === 'teacher')
            "
          >
            <el-option label="硕士研究生" value="master" />
            <el-option label="博士研究生" value="phd" />
            <el-option label="毕业生" value="graduate" />
            <el-option 
              label="教师" 
              value="teacher"
              :disabled="currentUser?.value?.role !== 'teacher'"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="管理员">
          <el-switch 
            v-model="setRoleForm.is_admin" 
            :disabled="
              setRoleForm.role === 'graduate' ||
              // 教师用户无法剥夺自己的管理员权限
              (currentUser?.value?.role === 'teacher' && setRoleForm.id === currentUser.value.id && currentUser.value.is_admin)
            " 
          />
          <span v-if="setRoleForm.role === 'graduate'" class="tip-text">（毕业生无法设置为管理员）</span>
          <span v-else-if="currentUser?.value?.role === 'teacher' && setRoleForm.id === currentUser.value.id && currentUser.value.is_admin" class="tip-text">（无法剥夺自己的管理员权限）</span>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSetRoleDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          @click="handleUpdateRole" 
          :loading="updatingRole"
          :disabled="
            // 教师用户无法修改自己的身份和管理员权限
            (currentUser?.value?.role === 'teacher' && setRoleForm.id === currentUser.value.id)
          "
        >保存</el-button>
      </template>
    </el-dialog>
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
import { getUsers, createUser, deleteUser, updateUserRole, updateUser } from '@/api/users'
import { useUserStore } from '@/store/user'
import { getCurrentUser } from '@/api/users'

const router = useRouter()
const userStore = useUserStore()

// 当前用户信息
const currentUser = ref<any>(null)

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

interface User {
  id: number
  name: string
  student_id: string
  role: string
  is_admin: boolean
  grade?: string
  email?: string
  phone?: string
  research_direction?: string
  wechat?: string
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
const usersLoading = ref(false)
const addingUser = ref(false)
const updatingUser = ref(false)
const updatingRole = ref(false)

const userSearchKeyword = ref('')
const paperSearchKeyword = ref('')
const postSearchKeyword = ref('')
const postCategoryFilter = ref('')
const downloadSearchKeyword = ref('')
const downloadCategoryFilter = ref('')

const showAddUserDialog = ref(false)
const showEditUserDialog = ref(false)
const showSetRoleDialog = ref(false)

const addUserFormRef = ref()
const editUserFormRef = ref()

const addUserForm = ref({
  name: '',
  student_id: '',
  password: '',
  grade: '',
  email: '',
  phone: '',
  research_direction: '',
  wechat: ''
})

const editUserForm = ref({
  id: 0,
  name: '',
  student_id: '',
  grade: '',
  email: '',
  phone: '',
  research_direction: '',
  wechat: ''
})

const setRoleForm = ref({
  id: 0,
  role: 'student',
  is_admin: false
})

const addUserRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  student_id: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ]
}

const editUserRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }]
}

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

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

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

const handleAddUser = async () => {
  await addUserFormRef.value.validate()
  addingUser.value = true
  try {
    await createUser(addUserForm.value)
    ElMessage.success('用户添加成功')
    showAddUserDialog.value = false
    loadUsers()
    addUserForm.value = {
      name: '',
      student_id: '',
      password: '',
      grade: '',
      email: '',
      phone: '',
      research_direction: '',
      wechat: ''
    }
  } catch (error: any) {
    ElMessage.error(error.message || '添加用户失败')
  } finally {
    addingUser.value = false
  }
}

const handleEditUser = (user: User) => {
  Object.assign(editUserForm.value, user)
  showEditUserDialog.value = true
}

const handleUpdateUser = async () => {
  await editUserFormRef.value.validate()
  updatingUser.value = true
  try {
    await updateUser(editUserForm.value.id, editUserForm.value)
    ElMessage.success('用户更新成功')
    showEditUserDialog.value = false
    loadUsers()
  } catch (error: any) {
    ElMessage.error(error.message || '更新用户失败')
  } finally {
    updatingUser.value = false
  }
}

const handleSetRole = (user: User) => {
  setRoleForm.value.id = user.id
  setRoleForm.value.role = user.role
  setRoleForm.value.is_admin = user.is_admin
  showSetRoleDialog.value = true
}

const handleUpdateRole = async () => {
  updatingRole.value = true
  try {
    // 如果角色是毕业生，自动取消管理员权限
    const isAdmin = setRoleForm.value.role === 'graduate' ? false : setRoleForm.value.is_admin
    
    await updateUserRole(setRoleForm.value.id, {
      role: setRoleForm.value.role,
      is_admin: isAdmin
    })
    ElMessage.success('权限更新成功')
    showSetRoleDialog.value = false
    loadUsers()
  } catch (error: any) {
    ElMessage.error(error.message || '更新权限失败')
  } finally {
    updatingRole.value = false
  }
}

const handleDeleteUser = (user: User) => {
  // 防呆检查
  if (user.id === currentUser?.value?.id) {
    ElMessage.warning('无法删除自己的账号')
    return
  }
  
  if (user.role === 'teacher' && currentUser?.value?.role !== 'teacher') {
    ElMessage.warning('学生管理员无法删除教师账号')
    return
  }

  ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteUser(user.id)
      ElMessage.success('删除成功')
      loadUsers()
    } catch (error) {
      ElMessage.error('删除失败')
      console.error('删除用户失败:', error)
    }
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

const loadUsers = async () => {
  usersLoading.value = true
  try {
    users.value = await getUsers()
  } catch (error) {
    console.error('获取用户列表失败:', error)
  } finally {
    usersLoading.value = false
  }
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

// 加载当前用户信息
const loadCurrentUser = async () => {
  try {
    currentUser.value = await getCurrentUser()
  } catch (error) {
    console.error('获取当前用户信息失败:', error)
  }
}

onMounted(async () => {
  await loadCurrentUser()
  loadUsers()
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
  
  .tip-text {
    color: #909399;
    font-size: 12px;
    margin-left: 8px;
  }
}
</style>
