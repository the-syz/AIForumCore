<template>
  <div class="profile-container">
    <h2>个人中心</h2>
    <el-card>
      <h3>个人信息</h3>
      <el-form :model="userInfo" label-width="120px">
        <el-form-item label="姓名">
          <el-input v-model="userInfo.name" disabled />
        </el-form-item>
        <el-form-item label="学号/工号">
          <el-input v-model="userInfo.student_id" disabled />
        </el-form-item>
        <el-form-item label="年级">
          <el-input v-model="userInfo.grade" disabled />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="userInfo.email" disabled />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="userInfo.phone" disabled />
        </el-form-item>
        <el-form-item label="研究方向">
          <el-input v-model="userInfo.research_direction" disabled />
        </el-form-item>
        <el-form-item label="微信">
          <el-input v-model="userInfo.wechat" disabled />
        </el-form-item>
        <el-form-item>
          <el-button type="primary">编辑信息</el-button>
          <el-button>修改密码</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const userInfo = ref({
  name: '张三',
  student_id: '2023001',
  grade: '2023级',
  email: 'zhangsan@example.com',
  phone: '13800138000',
  research_direction: '深度学习',
  wechat: 'zhangsan123'
})

onMounted(async () => {
  // 获取用户信息
  console.log('获取用户信息')
})
</script>

<style scoped lang="scss">
.profile-container {
  h2 {
    margin-bottom: 20px;
    color: #333;
  }
  
  el-card {
    margin-bottom: 20px;
  }
}
</style>
