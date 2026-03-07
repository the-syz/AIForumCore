<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2>AIForum 登录</h2>
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item prop="account">
          <el-input v-model="form.account" placeholder="学号/姓名" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" />
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="form.remember">记住密码</el-checkbox>
          <el-checkbox v-model="form.autoLogin">7天免登录</el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading">登录</el-button>
          <el-button @click="$router.push('/register')">注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { login, getCurrentUserInfo } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  account: '',
  password: '',
  remember: false,
  autoLogin: false
})

const rules = {
  account: [{ required: true, message: '请输入学号或姓名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    const res = await login(form)
    userStore.setToken(res.access_token, form.autoLogin)
    // 登录成功后获取用户信息
    const userInfo = await getCurrentUserInfo()
    userStore.setUserInfo(userInfo)
    router.push('/')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
  
  .login-card {
    width: 400px;
    padding: 20px;
    
    h2 {
      text-align: center;
      margin-bottom: 20px;
      color: #409eff;
    }
  }
}
</style>
