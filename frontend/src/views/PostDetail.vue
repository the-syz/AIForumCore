<template>
  <div class="post-detail-container">
    <el-card v-loading="loading">
      <template #header>
        <div class="post-header">
          <h2>{{ post.title }}</h2>
          <div class="post-meta">
            <span class="author">作者: {{ post.author_name }}</span>
            <span class="category">分类: {{ post.category }}</span>
            <span class="created-at">发布时间: {{ formatDate(post.created_at) }}</span>
            <span class="view-count">浏览: {{ post.view_count }}</span>
            <span class="comment-count">评论: {{ post.comment_count }}</span>
          </div>
        </div>
      </template>
      
      <!-- 经验贴内容 -->
      <div class="post-content" v-html="post.content"></div>
      
      <!-- 附件列表 -->
      <div class="attachments-section" v-if="post.attachments && post.attachments.length > 0">
        <h3>附件</h3>
        <el-list>
          <el-list-item v-for="(attachment, index) in post.attachments" :key="index">
            <div class="attachment-item">
              <el-icon><Document /></el-icon>
              <span class="attachment-name">{{ getAttachmentName(attachment) }}</span>
              <el-button type="primary" size="small" @click="downloadAttachment(attachment)">
                <el-icon><Download /></el-icon>
                下载
              </el-button>
            </div>
          </el-list-item>
        </el-list>
      </div>
      
      <!-- 操作按钮 -->
      <div class="post-actions">
        <el-button v-if="canManagePost()" type="primary" @click="handleEdit">编辑</el-button>
        <el-button v-if="canManagePost()" type="danger" @click="handleDelete">删除</el-button>
        <el-button @click="router.push('/posts')">返回列表</el-button>
      </div>
    </el-card>
    
    <!-- 评论区域 -->
    <div class="comments-section">
      <h3>评论 ({{ comments.length }})</h3>
      
      <!-- 评论表单 -->
      <el-card class="comment-form">
        <h4>发表评论</h4>
        <el-form :model="commentForm" :rules="commentRules" ref="commentFormRef">
          <el-form-item prop="content">
            <el-input
              v-model="commentForm.content"
              type="textarea"
              rows="3"
              placeholder="请输入评论内容"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSubmitComment" :loading="submittingComment">提交评论</el-button>
          </el-form-item>
        </el-form>
      </el-card>
      
      <!-- 评论列表 -->
      <el-card v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-header">
          <span class="comment-author">{{ comment.author_name }}</span>
          <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
        </div>
        <div class="comment-content">{{ comment.content }}</div>
        <div class="comment-actions">
          <el-button size="small" @click="handleReply(comment)">回复</el-button>
        </div>
      </el-card>
      
      <!-- 回复表单 -->
      <el-card v-if="replyingComment" class="reply-form">
        <h4>回复 {{ replyingComment.author_name }}</h4>
        <el-form :model="replyForm" :rules="replyRules" ref="replyFormRef">
          <el-form-item prop="content">
            <el-input
              v-model="replyForm.content"
              type="textarea"
              rows="2"
              placeholder="请输入回复内容"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSubmitReply" :loading="submittingReply">提交回复</el-button>
            <el-button @click="replyingComment = null">取消</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getPostById, deletePost } from '@/api/posts'
import { getComments, createComment as apiCreateComment } from '@/api/forum'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import { Download, Document } from '@element-plus/icons-vue'

interface Post {
  id: number
  title: string
  content: string
  category: string
  author_id: number
  author_name: string
  created_at: string
  updated_at: string
  is_pinned: boolean
  is_draft: boolean
  view_count: number
  like_count: number
  comment_count: number
  attachments: string[]
}

interface Comment {
  id: number
  content: string
  author_id: number
  author_name: string
  created_at: string
  parent_id?: number
}

const router = useRouter()
const route = useRoute()
const postId = Number(route.params.id)
const userStore = useUserStore()

const post = ref<Post>({
  id: 0,
  title: '',
  content: '',
  category: '',
  author_id: 0,
  author_name: '',
  created_at: '',
  updated_at: '',
  is_pinned: false,
  is_draft: false,
  view_count: 0,
  like_count: 0,
  comment_count: 0,
  attachments: []
})

const comments = ref<Comment[]>([])
const loading = ref(false)
const submittingComment = ref(false)
const submittingReply = ref(false)
const replyingComment = ref<Comment | null>(null)

// 检查是否有权限删除或编辑经验贴
const canManagePost = () => {
  if (!userStore.userInfo) return false
  return userStore.userInfo.id === post.value.author_id || userStore.isAdmin
}

const commentForm = ref({
  content: ''
})

const replyForm = ref({
  content: ''
})

const commentRules = {
  content: [{ required: true, message: '请输入评论内容', trigger: 'blur' }]
}

const replyRules = {
  content: [{ required: true, message: '请输入回复内容', trigger: 'blur' }]
}

const commentFormRef = ref()
const replyFormRef = ref()

// 获取经验贴详情
const fetchPostDetail = async () => {
  loading.value = true
  try {
    const response = await getPostById(postId)
    post.value = response
    // 从后端获取真实评论数据
    const commentsData = await getComments(postId)
    // 处理评论数据格式
    comments.value = commentsData.map((comment: any) => ({
      id: comment.id,
      content: comment.content,
      author_id: comment.user_id,
      author_name: comment.user_name,
      created_at: comment.created_at,
      parent_id: comment.parent_id
    }))
  } catch (error) {
    ElMessage.error('获取经验贴详情失败')
    console.error('获取经验贴详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 编辑经验贴
const handleEdit = () => {
  router.push(`/posts/edit/${postId}`)
}

// 删除经验贴
const handleDelete = async () => {
  try {
    await deletePost(postId)
    ElMessage.success('经验贴删除成功')
    router.push('/posts')
  } catch (error) {
    ElMessage.error('经验贴删除失败')
    console.error('删除经验贴失败:', error)
  }
}

// 提交评论
const handleSubmitComment = async () => {
  await commentFormRef.value.validate()
  submittingComment.value = true
  try {
    // 调用后端API提交评论
    const response = await apiCreateComment(commentForm.value.content, postId)
    // 处理返回的评论数据
    const newComment: Comment = {
      id: response.id,
      content: response.content,
      author_id: response.user_id,
      author_name: response.user_name || '当前用户',
      created_at: response.created_at,
      parent_id: response.parent_id
    }
    comments.value.push(newComment)
    commentForm.value.content = ''
    ElMessage.success('评论提交成功')
  } catch (error) {
    ElMessage.error('评论提交失败')
    console.error('提交评论失败:', error)
  } finally {
    submittingComment.value = false
  }
}

// 回复评论
const handleReply = (comment: Comment) => {
  replyingComment.value = comment
}

// 提交回复
const handleSubmitReply = async () => {
  await replyFormRef.value.validate()
  submittingReply.value = true
  try {
    // 调用后端API提交回复
    const response = await apiCreateComment(replyForm.value.content, postId, replyingComment.value?.id)
    // 处理返回的回复数据
    const newReply: Comment = {
      id: response.id,
      content: response.content,
      author_id: response.user_id,
      author_name: response.user_name || '当前用户',
      created_at: response.created_at,
      parent_id: response.parent_id
    }
    comments.value.push(newReply)
    replyForm.value.content = ''
    replyingComment.value = null
    ElMessage.success('回复提交成功')
  } catch (error) {
    ElMessage.error('回复提交失败')
    console.error('提交回复失败:', error)
  } finally {
    submittingReply.value = false
  }
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 从文件路径中提取文件名
const getAttachmentName = (attachment: any) => {
  if (typeof attachment === 'object' && attachment.name) {
    return attachment.name
  }
  if (typeof attachment === 'string') {
    const parts = attachment.split('/')
    return parts[parts.length - 1]
  }
  return '未知文件'
}

// 获取附件路径
const getAttachmentPath = (attachment: any) => {
  if (typeof attachment === 'object' && attachment.path) {
    return attachment.path
  }
  return attachment
}

// 下载附件
const downloadAttachment = async (attachment: any) => {
  try {
    const filePath = getAttachmentPath(attachment)
    const fileName = getAttachmentName(attachment)
    const response = await fetch(`/api/files/upload/download?file_path=${encodeURIComponent(filePath)}&file_name=${encodeURIComponent(fileName)}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    if (!response.ok) {
      throw new Error('下载失败')
    }
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = fileName
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
    ElMessage.success('下载开始')
  } catch (error) {
    ElMessage.error('下载失败，请重试')
    console.error('下载附件失败:', error)
  }
}

// 初始化加载数据
onMounted(() => {
  fetchPostDetail()
})
</script>

<style scoped lang="scss">
.post-detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  
  .post-header {
    margin-bottom: 20px;
    
    h2 {
      margin-bottom: 10px;
      color: #333;
    }
    
    .post-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 15px;
      font-size: 14px;
      color: #666;
      
      span {
        display: flex;
        align-items: center;
      }
    }
  }
  
  .post-content {
    margin: 20px 0;
    line-height: 1.6;
    color: #333;
    
    h1, h2, h3, h4, h5, h6 {
      margin: 20px 0 10px;
      color: #333;
    }
    
    p {
      margin-bottom: 15px;
    }
    
    img {
      max-width: 100%;
      height: auto;
      margin: 10px 0;
    }
    
    code {
      background-color: #f5f5f5;
      padding: 2px 4px;
      border-radius: 3px;
    }
    
    pre {
      background-color: #f5f5f5;
      padding: 10px;
      border-radius: 5px;
      overflow-x: auto;
      margin: 10px 0;
    }
  }
  
  .post-actions {
    margin-top: 30px;
    display: flex;
    gap: 10px;
  }
  
  .attachments-section {
    margin: 30px 0;
    
    h3 {
      margin-bottom: 15px;
      color: #333;
      font-size: 16px;
      font-weight: 500;
    }
    
    .attachment-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 0;
      border-bottom: 1px solid #f0f0f0;
      
      .attachment-name {
        flex: 1;
        color: #333;
      }
    }
  }
  
  .comments-section {
    margin-top: 40px;
    
    h3 {
      margin-bottom: 20px;
      color: #333;
    }
    
    .comment-form {
      margin-bottom: 30px;
    }
    
    .comment-item {
      margin-bottom: 20px;
      
      .comment-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        font-size: 14px;
        
        .comment-author {
          font-weight: bold;
          color: #333;
        }
        
        .comment-time {
          color: #999;
        }
      }
      
      .comment-content {
        margin-bottom: 10px;
        color: #333;
      }
      
      .comment-actions {
        display: flex;
        justify-content: flex-end;
      }
    }
    
    .reply-form {
      margin: 20px 0;
      padding: 15px;
      background-color: #f9f9f9;
      border-radius: 5px;
    }
  }
}
</style>