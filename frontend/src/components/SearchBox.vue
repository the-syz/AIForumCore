<template>
  <div class="search-box">
    <el-input
      v-model="searchKeyword"
      placeholder="搜索论文、经验贴..."
      suffix-icon="el-icon-search"
      @keyup.enter="handleSearch"
      size="large"
    >
      <template #append>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
      </template>
    </el-input>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  defaultKeyword?: string
}>()

const emit = defineEmits<{
  (e: 'search', keyword: string): void
}>()

const searchKeyword = ref(props.defaultKeyword || '')

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    emit('search', searchKeyword.value.trim())
  }
}
</script>

<style scoped scss>
.search-box {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}
</style>