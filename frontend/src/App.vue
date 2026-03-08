<template>
  <router-view></router-view>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/store/user'
import { getCurrentUserInfo } from '@/api/auth'

const userStore = useUserStore()

onMounted(async () => {
  // 检查是否存在token
  if (userStore.token) {
    try {
      // 如果存在token，获取用户信息
      const userInfo = await getCurrentUserInfo()
      userStore.setUserInfo(userInfo)
    } catch (error) {
      // 获取用户信息失败，清除token
      userStore.logout()
    }
  }
})
</script>

