<template>
  <div class="register-container">
    <el-card class="register-card">
      <h2>AIForum 注册</h2>
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item prop="name">
          <el-input v-model="form.name" placeholder="姓名" />
        </el-form-item>
        <el-form-item prop="student_id">
          <el-input v-model="form.student_id" placeholder="学号/工号" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" />
        </el-form-item>
        <el-form-item prop="grade">
          <el-input v-model="form.grade" placeholder="年级" />
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="form.email" placeholder="邮箱" />
        </el-form-item>
        <el-form-item prop="phone">
          <el-input v-model="form.phone" placeholder="电话" />
        </el-form-item>
        <el-form-item prop="research_direction">
          <el-input v-model="form.research_direction" placeholder="研究方向" />
        </el-form-item>
        <el-form-item prop="wechat">
          <el-input v-model="form.wechat" placeholder="微信" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister" :loading="loading">注册</el-button>
          <el-button @click="$router.push('/login')">登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/auth'

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  name: '',
  student_id: '',
  password: '',
  grade: '',
  email: '',
  phone: '',
  research_direction: '',
  wechat: ''
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  student_id: [{ required: true, message: '请输入学号/工号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  grade: [{ required: true, message: '请输入年级', trigger: 'blur' }],
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入电话', trigger: 'blur' }],
  research_direction: [{ required: true, message: '请输入研究方向', trigger: 'blur' }],
  wechat: [{ required: true, message: '请输入微信', trigger: 'blur' }]
}

const handleRegister = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    await register(form)
    router.push('/login')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
  
  .register-card {
    width: 500px;
    padding: 20px;
    
    h2 {
      text-align: center;
      margin-bottom: 20px;
      color: #409eff;
    }
  }
}
</style>
