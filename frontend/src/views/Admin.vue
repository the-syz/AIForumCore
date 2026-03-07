<template>
  <div class="admin-container">
    <h2>管理员中心</h2>
    <el-tabs>
      <el-tab-pane label="用户管理">
        <el-button type="primary">添加用户</el-button>
        <el-table :data="users" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="student_id" label="学号/工号" />
          <el-table-column prop="role" label="角色" />
          <el-table-column prop="is_admin" label="是否管理员" />
          <el-table-column label="操作" width="150">
            <template #default="scope">
              <el-button size="small" @click="handleEditUser(scope.row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDeleteUser(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="论文管理">
        <!-- 论文管理内容 -->
      </el-tab-pane>
      <el-tab-pane label="经验贴管理">
        <!-- 经验贴管理内容 -->
      </el-tab-pane>
      <el-tab-pane label="下载中心管理">
        <!-- 下载中心管理内容 -->
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface User {
  id: number
  name: string
  student_id: string
  role: string
  is_admin: boolean
}

const users = ref<User[]>([])

const handleEditUser = (user: User) => {
  // 编辑用户
  console.log('编辑用户:', user)
}

const handleDeleteUser = (user: User) => {
  // 删除用户
  console.log('删除用户:', user)
}

onMounted(async () => {
  // 模拟数据
  users.value = [
    {
      id: 1,
      name: '张三',
      student_id: '2023001',
      role: 'student',
      is_admin: false
    }
  ]
})
</script>

<style scoped lang="scss">
.admin-container {
  h2 {
    margin-bottom: 20px;
    color: #333;
  }
  
  .el-button {
    margin-bottom: 20px;
  }
}
</style>
