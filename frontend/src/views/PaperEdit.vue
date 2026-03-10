<template>
  <div class="paper-edit-container">
    <div class="edit-header">
      <el-button @click="goBack">返回</el-button>
      <h2>{{ isNew ? '新建论文' : '编辑论文' }}</h2>
    </div>
    
    <el-card class="edit-card" v-if="paper">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="论文标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入论文标题" />
        </el-form-item>
        
        <el-form-item label="作者" prop="authors">
          <el-input v-model="form.authors" placeholder="请输入作者，多个作者用逗号分隔" />
        </el-form-item>
        
        <el-form-item label="摘要" prop="abstract">
          <el-input v-model="form.abstract" type="textarea" :rows="4" placeholder="请输入论文摘要" />
        </el-form-item>
        
        <el-form-item label="关键词" prop="keywords">
          <el-input v-model="form.keywords" placeholder="请输入关键词，多个关键词用逗号分隔" />
        </el-form-item>
        
        <el-form-item label="DOI" prop="doi">
          <el-input v-model="form.doi" placeholder="请输入DOI" />
        </el-form-item>
        
        <el-form-item label="论文类型" prop="paper_type">
          <el-select v-model="form.paper_type" placeholder="请选择论文类型">
            <el-option label="期刊论文" value="journal" />
            <el-option label="会议论文" value="conference" />
            <el-option label="学位论文" value="thesis" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="研究领域" prop="category">
          <el-input v-model="form.category" placeholder="请输入研究领域" />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">保存</el-button>
          <el-button @click="goBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-skeleton v-else :rows="10" animated />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPaperById, updatePaper, createPaper } from '@/api/papers'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const formRef = ref<any>(null)
const submitting = ref(false)
const paper = ref<any>(null)

const paperId = route.params.id
const isNew = computed(() => paperId === 'new')

const form = reactive({
  title: '',
  authors: '',
  abstract: '',
  keywords: '',
  doi: '',
  paper_type: '',
  category: ''
})

const rules = {
  title: [{ required: true, message: '请输入论文标题', trigger: 'blur' }],
  authors: [{ required: true, message: '请输入作者', trigger: 'blur' }],
  abstract: [{ required: true, message: '请输入摘要', trigger: 'blur' }],
  keywords: [{ required: true, message: '请输入关键词', trigger: 'blur' }],
  paper_type: [{ required: true, message: '请选择论文类型', trigger: 'blur' }],
  category: [{ required: true, message: '请输入研究领域', trigger: 'blur' }]
}

const goBack = () => {
  router.push('/papers')
}

const handleSubmit = async () => {
  await formRef.value.validate()
  
  submitting.value = true
  
  try {
    if (isNew.value) {
      await createPaper(form)
      ElMessage.success('论文创建成功')
    } else {
      await updatePaper(Number(paperId), form)
      ElMessage.success('论文信息更新成功')
    }
    router.push('/papers')
  } catch (error) {
    ElMessage.error(isNew.value ? '论文创建失败' : '论文信息更新失败')
  } finally {
    submitting.value = false
  }
}

const fetchPaperDetail = async () => {
  if (!isNew.value) {
    try {
      const data = await getPaperById(Number(paperId))
      paper.value = data
      // 填充表单
      form.title = data.title
      form.authors = data.authors
      form.abstract = data.abstract
      form.keywords = data.keywords
      form.doi = data.doi
      form.paper_type = data.paper_type
      form.category = data.category
    } catch (error) {
      ElMessage.error('获取论文详情失败')
    }
  } else {
    // 新建论文，初始化表单
    paper.value = {}
  }
}

onMounted(() => {
  fetchPaperDetail()
})
</script>

<style scoped scss>
.paper-edit-container {
  .edit-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      margin: 0 0 0 20px;
      color: #333;
    }
  }
  
  .edit-card {
    width: 100%;
  }
}
</style>