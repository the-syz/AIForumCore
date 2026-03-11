<template>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-brand">
        <h1>AIForum</h1>
      </div>
      <div class="navbar-menu">
        <el-menu
          :default-active="activeIndex"
          class="nav-bar"
          router
          mode="horizontal"
        >
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/papers">
            <el-icon><Document /></el-icon>
            <span>论文</span>
          </el-menu-item>
          <el-menu-item index="/posts">
            <el-icon><ChatDotRound /></el-icon>
            <span>经验贴</span>
          </el-menu-item>
          <el-menu-item index="/downloads">
            <el-icon><Download /></el-icon>
            <span>下载中心</span>
          </el-menu-item>
          <el-menu-item index="/profile">
            <el-icon><User /></el-icon>
            <span>个人中心</span>
          </el-menu-item>
          <el-menu-item v-if="isAdmin" index="/admin">
            <el-icon><Setting /></el-icon>
            <span>管理员</span>
          </el-menu-item>
        </el-menu>
      </div>
      <div class="navbar-user">
        <template v-if="userInfo">
          <span class="user-name">{{ userInfo.name }}</span>
          <el-dropdown>
            <el-button type="text">
              <el-icon><CaretBottom /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button @click="$router.push('/login')">登录</el-button>
        </template>
        <el-button 
          :type="aiStore.isOpen ? 'primary' : 'default'" 
          @click="aiStore.toggle"
          class="ai-btn"
        >
          <el-icon><ChatLineRound /></el-icon>
          <span class="ai-text">AI助手</span>
        </el-button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useAIStore } from '@/store/ai'
import { HomeFilled, Document, ChatDotRound, Download, User, Setting, CaretBottom, ChatLineRound } from '@element-plus/icons-vue'
import { logout } from '@/api/auth'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const aiStore = useAIStore()

const activeIndex = computed(() => route.path)
const isAdmin = computed(() => userStore.isAdmin)
const userInfo = computed(() => userStore.userInfo)

const handleLogout = async () => {
  await logout()
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped lang="scss">
.navbar {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 10px 0;
  position: sticky;
  top: 0;
  z-index: 100;
  
  .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  .navbar-brand {
    h1 {
      font-size: 20px;
      font-weight: 600;
      color: #409eff;
      margin: 0;
    }
  }
  
  .navbar-menu {
    flex: 1;
    margin: 0 20px;
  }
  
  .nav-bar {
    border-bottom: none;
  }
  
  .navbar-user {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .ai-btn {
      display: flex;
      align-items: center;
      gap: 4px;
      
      .ai-text {
        @media (max-width: 768px) {
          display: none;
        }
      }
    }
    
    .user-name {
      margin-right: 4px;
      color: #333;
      font-size: 14px;
    }
  }
}
</style>
