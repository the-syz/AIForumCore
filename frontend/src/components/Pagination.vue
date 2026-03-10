<template>
  <div class="pagination-wrapper">
    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :page-sizes="pageSizes"
      :layout="layout"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue: number
  pageSize: number
  total: number
  pageSizes?: number[]
  layout?: string
}

interface Emits {
  (e: 'update:modelValue', value: number): void
  (e: 'update:pageSize', value: number): void
  (e: 'size-change', size: number): void
  (e: 'current-change', page: number): void
}

const props = withDefaults(defineProps<Props>(), {
  pageSizes: () => [10, 20, 50, 100],
  layout: 'total, sizes, prev, pager, next, jumper'
})

const emit = defineEmits<Emits>()

const currentPage = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const pageSize = computed({
  get: () => props.pageSize,
  set: (value) => emit('update:pageSize', value)
})

const handleSizeChange = (size: number) => {
  emit('size-change', size)
}

const handleCurrentChange = (page: number) => {
  emit('current-change', page)
}
</script>

<style scoped lang="scss">
.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
