<template>
  <div class="main-layout" :class="{ 'ai-open': aiStore.isOpen }">
    <!-- 导航栏 -->
    <NavBar />

    <!-- 标签栏 -->
    <TabBar />

    <!-- 主内容 -->
    <main class="main-content">
      <div class="container">
        <router-view></router-view>
      </div>
    </main>

    <!-- 页脚 -->
    <Footer />
    
    <!-- AI聊天面板 -->
    <AIChat />
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import TabBar from '@/components/TabBar.vue'
import Footer from '@/components/Footer.vue'
import AIChat from '@/components/AIChat.vue'
import { useTabsStore } from '@/store/tabs'
import { useAIStore } from '@/store/ai'

const route = useRoute()
const tabsStore = useTabsStore()
const aiStore = useAIStore()

const getTabInfo = (path: string) => {
  // 主页标签处理
  if (path === '/' || 
      path === '/papers' || 
      path === '/posts' || 
      path === '/downloads' || 
      path === '/profile' || 
      path === '/admin') {
    let title = '首页'
    if (path === '/papers') title = '论文'
    if (path === '/posts') title = '经验贴'
    if (path === '/downloads') title = '下载中心'
    if (path === '/profile') title = '个人中心'
    if (path === '/admin') title = '管理员'
    return { name: 'home', title, path, closable: false }
  }
  // 详情页和编辑页生成新标签
  if (path.match(/^\/papers\/\d+$/)) {
    return { name: `paper-${path.split('/')[2]}`, title: '论文详情', path, closable: true }
  }
  if (path.match(/^\/papers\/edit\/\d+$/)) {
    return { name: `paper-edit-${path.split('/')[3]}`, title: '编辑论文', path, closable: true }
  }
  if (path === '/papers/upload') {
    return { name: 'paper-upload', title: '上传论文', path, closable: true }
  }
  if (path.match(/^\/posts\/\d+$/)) {
    return { name: `post-${path.split('/')[2]}`, title: '经验贴详情', path, closable: true }
  }
  if (path.match(/^\/posts\/edit\/\d+$/)) {
    return { name: `post-edit-${path.split('/')[3]}`, title: '编辑经验贴', path, closable: true }
  }
  if (path === '/posts/create') {
    return { name: 'post-create', title: '发布经验贴', path, closable: true }
  }
  if (path.match(/^\/downloads\/\d+$/)) {
    return { name: `download-${path.split('/')[2]}`, title: '资源详情', path, closable: true }
  }
  if (path.match(/^\/downloads\/edit\/\d+$/)) {
    return { name: `download-edit-${path.split('/')[3]}`, title: '编辑资源', path, closable: true }
  }
  if (path === '/downloads/upload') {
    return { name: 'download-upload', title: '上传资源', path, closable: true }
  }
  return { name: `tab-${Date.now()}`, title: '页面', path, closable: true }
}

const handleRouteChange = (path: string) => {
  const tabInfo = getTabInfo(path)
  // 对于主页标签，更新现有标签
  if (tabInfo.name === 'home') {
    const homeTab = tabsStore.tabs.find(t => t.name === 'home')
    if (homeTab) {
      homeTab.title = tabInfo.title
      homeTab.path = tabInfo.path
      tabsStore.setActiveTab('home')
    } else {
      tabsStore.addTab(tabInfo)
    }
  } else {
    tabsStore.addTab(tabInfo)
  }
}

onMounted(() => {
  tabsStore.initTabs()
  handleRouteChange(route.path)
})

watch(
  () => route.path,
  (newPath) => {
    handleRouteChange(newPath)
  }
)
</script>

<style scoped lang="scss">
.main-layout {
  transition: padding-right 0.3s ease;
  
  .main-content {
    min-height: 600px;
    padding: 20px 0;
    transition: margin-right 0.3s ease;
    
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 20px;
      transition: max-width 0.3s ease;
    }
  }
  
  &.ai-open {
    .main-content {
      margin-right: 400px;
      
      .container {
        max-width: calc(1200px - 400px);
      }
    }
  }
}

@media (max-width: 1200px) {
  .main-layout.ai-open {
    .main-content {
      margin-right: 350px;
      
      .container {
        max-width: calc(100% - 350px);
      }
    }
  }
}

@media (max-width: 768px) {
  .main-layout.ai-open {
    .main-content {
      margin-right: 0;
      opacity: 0.3;
      pointer-events: none;
    }
  }
}
</style>
