<template>
  <div class="register-container">
    <el-card class="register-card">
      <h2>AIForum 注册</h2>
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item label="姓名" prop="name" required>
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="学号/工号" prop="student_id" required>
          <el-input v-model="form.student_id" placeholder="请输入学号/工号" />
        </el-form-item>
        <el-form-item label="密码" prop="password" required>
          <el-input v-model="form.password" type="password" placeholder="请输入密码（至少8位，包含数字和英文）" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword" required>
          <el-input v-model="form.confirmPassword" type="password" placeholder="请确认密码" show-password />
        </el-form-item>
        <el-form-item label="身份" prop="role" required>
          <el-select v-model="form.role" placeholder="请选择身份">
            <el-option label="硕士研究生" value="master" />
            <el-option label="博士研究生" value="phd" />
            <el-option label="毕业生" value="graduate" />
          </el-select>
        </el-form-item>
        <el-form-item label="年级" prop="grade" required>
          <el-select v-model="form.grade" placeholder="请选择年级">
            <el-option
              v-for="option in gradeOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入电话" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister" :loading="loading">注册</el-button>
          <el-button @click="$router.push('/login')">返回登录</el-button>
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

// 年级选项
const gradeOptions = [
  { label: '2020级', value: '2020级' },
  { label: '2021级', value: '2021级' },
  { label: '2022级', value: '2022级' },
  { label: '2023级', value: '2023级' },
  { label: '2024级', value: '2024级' },
  { label: '2025级', value: '2025级' },
  { label: '2026级', value: '2026级' }
]

const form = reactive({
  name: '',
  student_id: '',
  password: '',
  confirmPassword: '',
  role: 'master',
  grade: '',
  email: '',
  phone: '',
  research_direction: '',
  wechat: ''
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  student_id: [{ required: true, message: '请输入学号/工号', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码长度至少8位', trigger: 'blur' },
    { pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/, message: '密码必须包含数字和英文', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== form.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  role: [{ required: true, message: '请选择身份', trigger: 'blur' }],
  grade: [{ required: true, message: '请输入年级', trigger: 'blur' }],
  email: [{ message: '请输入邮箱', trigger: 'blur' }],
  phone: [{ message: '请输入电话', trigger: 'blur' }]
}

const handleRegister = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    // 移除 confirmPassword 字段，因为后端模型中没有这个字段
    const { confirmPassword, ...registerData } = form
    
    // 将空字符串转换为 null，以便后端正确处理可选字段
    Object.keys(registerData).forEach(key => {
      if (registerData[key] === '') {
        registerData[key] = null
      }
    })
    
    await register(registerData)
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
