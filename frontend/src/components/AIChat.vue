<template>
  <div class="ai-chat-panel" :class="{ open: aiStore.isOpen }">
    <div class="chat-header">
      <h3>AI助手</h3>
      <el-button @click="aiStore.close" circle size="small">
        <el-icon><Close /></el-icon>
      </el-button>
    </div>
    
    <div class="chat-content">
      <div class="history-section" v-if="conversations.length > 0">
        <div class="history-header" @click="toggleHistory">
          <span>对话历史</span>
          <div class="history-actions">
            <el-button link type="primary" size="small" @click.stop="loadConversations">
              <el-icon><Refresh /></el-icon>
            </el-button>
            <el-button link size="small" @click.stop="toggleHistory">
              <el-icon>
                <ArrowUp v-if="isHistoryExpanded" />
                <ArrowDown v-else />
              </el-icon>
            </el-button>
          </div>
        </div>
        <div class="conversation-list" v-show="isHistoryExpanded">
          <div 
            v-for="conv in conversations" 
            :key="conv.id"
            :class="['conversation-item', { active: currentConversationId === conv.id }]"
            @click="selectConversation(conv)"
          >
            <span class="conv-title">{{ conv.topic }}</span>
            <el-button 
              v-if="currentConversationId !== conv.id" 
              link 
              type="danger" 
              size="small"
              @click.stop="handleDeleteConversation(conv.id)"
            >
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
        </div>
      </div>
      
      <div class="selected-contents-section" v-if="selectedContents.length > 0">
        <div class="selected-header" @click="toggleSelectedContents">
          <span>已选文章 ({{ selectedContents.length }})</span>
          <div class="selected-actions">
            <el-button link type="danger" size="small" @click.stop="clearSelectedContents">
              <el-icon><Delete /></el-icon>
            </el-button>
            <el-button link size="small" @click.stop="toggleSelectedContents">
              <el-icon>
                <ArrowUp v-if="isSelectedContentsExpanded" />
                <ArrowDown v-else />
              </el-icon>
            </el-button>
          </div>
        </div>
        <div class="selected-list" v-show="isSelectedContentsExpanded">
          <div 
            v-for="content in selectedContents" 
            :key="`${content.type}-${content.id}`"
            class="selected-item"
          >
            <el-icon class="content-icon">
              <Document v-if="content.type === 'paper'" />
              <DocumentCopy v-else-if="content.type === 'post'" />
              <Download v-else />
            </el-icon>
            <span class="content-title" :title="content.title">{{ content.title }}</span>
            <el-button link type="danger" size="small" @click="removeSelectedContent(content)">
              <el-icon><Close /></el-icon>
            </el-button>
          </div>
        </div>
      </div>
      
      <div class="new-conv-btn">
        <el-button type="primary" size="small" @click="startNewConversation" style="width: 100%">
          <el-icon><Plus /></el-icon> 新对话
        </el-button>
      </div>
      
      <div class="message-list" ref="messageList">
        <div v-for="(msg, index) in messages" 
             :key="index" 
             :class="['message', msg.role]">
          <div class="message-avatar">
            <el-icon v-if="msg.role === 'user'"><User /></el-icon>
            <el-icon v-else><ChatDotRound /></el-icon>
          </div>
          <div class="message-content">
            <div class="message-text" v-html="renderMarkdown(msg.content)"></div>
            
            <div v-if="msg.references && msg.references.length > 0" class="references">
              <p class="ref-title">参考资料：</p>
              <ul>
                <li v-for="ref in msg.references" :key="ref.id">
                  <router-link :to="getReferenceLink(ref)" @click="aiStore.close">
                    {{ ref.title }}
                  </router-link>
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="message assistant">
          <div class="message-avatar">
            <el-icon><ChatDotRound /></el-icon>
          </div>
          <div class="message-content">
            <div class="message-text loading-text">
              <span class="dot"></span>
              <span class="dot"></span>
              <span class="dot"></span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="input-area">
        <div class="selected-hint" v-if="selectedContents.length > 0">
          <el-tag type="success" size="small">
            <el-icon><Filter /></el-icon>
            已选择 {{ selectedContents.length }} 篇文章进行限定搜索
          </el-tag>
        </div>
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="3"
          :placeholder="selectedContents.length > 0 ? '基于选中的文章提问... (Ctrl+Enter发送)' : '请输入问题... (Ctrl+Enter发送)'"
          @keydown.ctrl.enter="sendMessage"
          resize="none"
        />
        <div class="input-actions">
          <el-button type="primary" @click="sendMessage" :loading="loading" style="width: 100%">
            <el-icon><Promotion /></el-icon> 发送
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAIStore } from '@/store/ai'
import { 
  sendChatMessage, 
  createNewConversation, 
  getChatHistory, 
  deleteConversation as deleteConvApi,
  type SelectedContent
} from '@/api/ai'
import { 
  User, 
  ChatDotRound, 
  Plus, 
  Refresh, 
  Delete, 
  Close,
  Promotion,
  ArrowUp,
  ArrowDown,
  Document,
  DocumentCopy,
  Download,
  Filter
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import MarkdownIt from 'markdown-it'

const router = useRouter()
const aiStore = useAIStore()
const messages = ref([
  { role: 'assistant', content: '你好，我是AI助手，可以与我进行对话。' }
])
const inputMessage = ref('')
const loading = ref(false)
const currentConversationId = ref<number | null>(null)
const conversations = ref<any[]>([])
const messageList = ref<HTMLElement | null>(null)
const isHistoryExpanded = ref(false)
const isSelectedContentsExpanded = ref(true)
const selectedContents = ref<SelectedContent[]>([])

// 初始化 Markdown 解析器
const md = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: true,
  breaks: true
})

// 渲染 Markdown
const renderMarkdown = (content: string): string => {
  if (!content) return ''
  return md.render(content)
}

// 切换对话历史展开/收起
const toggleHistory = () => {
  isHistoryExpanded.value = !isHistoryExpanded.value
}

// 切换选中内容展开/收起
const toggleSelectedContents = () => {
  isSelectedContentsExpanded.value = !isSelectedContentsExpanded.value
}

// 添加选中的内容
const addSelectedContent = (content: SelectedContent) => {
  const exists = selectedContents.value.find(
    c => c.type === content.type && c.id === content.id
  )
  if (!exists) {
    selectedContents.value.push(content)
    ElMessage.success(`已添加: ${content.title}`)
  } else {
    ElMessage.warning('该文章已在选择列表中')
  }
}

// 移除选中的内容
const removeSelectedContent = (content: SelectedContent) => {
  const index = selectedContents.value.findIndex(
    c => c.type === content.type && c.id === content.id
  )
  if (index > -1) {
    selectedContents.value.splice(index, 1)
  }
}

// 清空选中的内容
const clearSelectedContents = () => {
  selectedContents.value = []
}

// 暴露方法供外部调用
defineExpose({
  addSelectedContent
})

const scrollToBottom = async () => {
  await nextTick()
  if (messageList.value) {
    messageList.value.scrollTop = messageList.value.scrollHeight
  }
}

const startNewConversation = async () => {
  try {
    const res = await createNewConversation()
    currentConversationId.value = res.id
    messages.value = [
      { role: 'assistant', content: '你好，我是AI助手，可以与我进行对话。' }
    ]
    inputMessage.value = ''
    selectedContents.value = [] // 清空选中的内容
    await loadConversations()
  } catch (error) {
    ElMessage.error('创建新对话失败')
  }
}

const selectConversation = async (conv: any) => {
  try {
    currentConversationId.value = conv.id
    const res = await getChatHistory(conv.id)
    if (res.messages) {
      messages.value = res.messages.map((msg: any) => ({
        role: msg.role,
        content: msg.content
      }))
    }
    await scrollToBottom()
  } catch (error) {
    ElMessage.error('加载对话失败')
  }
}

const loadConversations = async () => {
  try {
    const res = await getChatHistory()
    if (res.conversations) {
      conversations.value = res.conversations
    }
  } catch (error) {
    console.error('加载对话历史失败', error)
  }
}

const handleDeleteConversation = async (convId: number) => {
  try {
    await ElMessageBox.confirm('确定删除此对话？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteConvApi(convId)
    
    if (currentConversationId.value === convId) {
      await startNewConversation()
    }
    
    await loadConversations()
    ElMessage.success('删除成功')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return
  
  const userMessage = inputMessage.value
  messages.value.push({ role: 'user', content: userMessage })
  inputMessage.value = ''
  loading.value = true
  
  await scrollToBottom()
  
  try {
    const res = await sendChatMessage({
      message: userMessage,
      conversation_id: currentConversationId.value || undefined,
      selected_contents: selectedContents.value.length > 0 ? selectedContents.value : undefined
    })
    
    if (!currentConversationId.value) {
      await loadConversations()
    }
    
    messages.value.push({
      role: 'assistant',
      content: res.answer,
      references: res.references
    })
    
  } catch (error) {
    messages.value.push({
      role: 'assistant',
      content: '抱歉，发生了错误，请稍后重试。'
    })
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

const getReferenceLink = (ref: any) => {
  switch (ref.type) {
    case 'paper':
      return `/papers/${ref.id}`
    case 'post':
      return `/posts/${ref.id}`
    case 'download':
      return `/downloads/${ref.id}`
    default:
      return '#'
  }
}

watch(() => aiStore.isOpen, (isOpen) => {
  if (isOpen) {
    loadConversations()
    // 检查是否有待添加的内容
    const pendingContent = aiStore.getAndClearPendingContent()
    if (pendingContent) {
      addSelectedContent(pendingContent)
    }
  }
})

onMounted(async () => {
  await loadConversations()
})
</script>

<style scoped lang="scss">
.ai-chat-panel {
  position: fixed;
  right: -400px;
  top: 100px;
  bottom: 0;
  width: 400px;
  background: #fff;
  border-left: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  transition: right 0.3s ease;
  z-index: 999;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  
  &.open {
    right: 0;
  }
}

.chat-header {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  position: sticky;
  top: 0;
  z-index: 10;
  
  h3 {
    margin: 0;
    font-size: 16px;
    color: #333;
  }
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.history-section,
.selected-contents-section {
  padding: 12px;
  border-bottom: 1px solid #e0e0e0;
  
  .history-header,
  .selected-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
    color: #666;
    cursor: pointer;
    user-select: none;
    padding: 4px 0;
    
    &:hover {
      color: #409eff;
    }
    
    .history-actions,
    .selected-actions {
      display: flex;
      gap: 4px;
      align-items: center;
    }
  }
  
  .conversation-list,
  .selected-list {
    max-height: 150px;
    overflow-y: auto;
    margin-top: 8px;
  }
  
  .conversation-item {
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: background 0.2s;
    
    &:hover {
      background: #f5f5f5;
    }
    
    &.active {
      background: #e3f2fd;
    }
    
    .conv-title {
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-size: 13px;
    }
  }
  
  .selected-item {
    padding: 6px 10px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
    background: #f0f9ff;
    margin-bottom: 4px;
    
    .content-icon {
      color: #409eff;
      font-size: 14px;
    }
    
    .content-title {
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-size: 12px;
      color: #333;
    }
  }
}

.new-conv-btn {
  padding: 12px;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  
  .message {
    margin-bottom: 16px;
    display: flex;
    gap: 12px;
    
    .message-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      
      .el-icon {
        font-size: 20px;
        color: #fff;
      }
    }
    
    &.user {
      .message-avatar {
        background: #409eff;
      }
      
      .message-content {
        background: #e3f2fd;
        border-radius: 12px 12px 12px 4px;
      }
    }
    
    &.assistant {
      .message-avatar {
        background: #67c23a;
      }
      
      .message-content {
        background: #f5f5f5;
        border-radius: 12px 12px 4px 12px;
      }
    }
    
    .message-content {
      flex: 1;
      padding: 12px 16px;
      max-width: 85%;
      overflow-wrap: break-word;
      
      .message-text {
        line-height: 1.6;
        word-break: break-word;
        
        // Markdown 样式
        :deep(h1), :deep(h2), :deep(h3), :deep(h4), :deep(h5), :deep(h6) {
          margin: 12px 0 8px 0;
          font-weight: 600;
          line-height: 1.4;
        }
        
        :deep(h1) { font-size: 1.4em; }
        :deep(h2) { font-size: 1.3em; }
        :deep(h3) { font-size: 1.2em; }
        :deep(h4), :deep(h5), :deep(h6) { font-size: 1.1em; }
        
        :deep(p) {
          margin: 8px 0;
        }
        
        :deep(ul), :deep(ol) {
          margin: 8px 0;
          padding-left: 20px;
        }
        
        :deep(li) {
          margin: 4px 0;
        }
        
        :deep(code) {
          background: rgba(0, 0, 0, 0.05);
          padding: 2px 6px;
          border-radius: 3px;
          font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
          font-size: 0.9em;
        }
        
        :deep(pre) {
          background: #f4f4f4;
          padding: 12px;
          border-radius: 6px;
          overflow-x: auto;
          margin: 8px 0;
          
          code {
            background: none;
            padding: 0;
          }
        }
        
        :deep(blockquote) {
          border-left: 4px solid #ddd;
          padding-left: 12px;
          margin: 8px 0;
          color: #666;
        }
        
        :deep(a) {
          color: #409eff;
          text-decoration: none;
          
          &:hover {
            text-decoration: underline;
          }
        }
        
        :deep(table) {
          border-collapse: collapse;
          margin: 8px 0;
          width: 100%;
        }
        
        :deep(th), :deep(td) {
          border: 1px solid #ddd;
          padding: 8px;
          text-align: left;
        }
        
        :deep(th) {
          background: #f5f5f5;
          font-weight: 600;
        }
        
        :deep(hr) {
          border: none;
          border-top: 1px solid #ddd;
          margin: 12px 0;
        }
      }
      
      .loading-text {
        display: flex;
        gap: 4px;
        
        .dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #67c23a;
          animation: bounce 1.4s infinite ease-in-out both;
          
          &:nth-child(1) { animation-delay: -0.32s; }
          &:nth-child(2) { animation-delay: -0.16s; }
        }
      }
      
      .references {
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid #ddd;
        font-size: 12px;
        
        .ref-title {
          margin: 0 0 8px 0;
          color: #666;
        }
        
        ul {
          margin: 0;
          padding-left: 16px;
          
          li {
            margin-bottom: 4px;
            
            a {
              color: #409eff;
              text-decoration: none;
              
              &:hover {
                text-decoration: underline;
              }
            }
          }
        }
      }
    }
  }
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.input-area {
  padding: 16px;
  border-top: 1px solid #e0e0e0;
  background: #fff;
  
  .selected-hint {
    margin-bottom: 8px;
  }
  
  .input-actions {
    margin-top: 12px;
  }
}

@media (max-width: 768px) {
  .ai-chat-panel {
    width: 100%;
    right: -100%;
  }
}
</style>
