<template>
  <div class="empty-state-wrapper">
    <el-empty :description="description" :image="image">
      <template #image>
        <component v-if="iconComponent" :is="iconComponent" class="empty-icon" />
      </template>
      <template v-if="$slots.default">
        <slot></slot>
      </template>
      <template v-else-if="actionText">
        <el-button type="primary" @click="handleAction">{{ actionText }}</el-button>
      </template>
    </el-empty>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import {
  Document,
  ChatDotRound,
  Download,
  Search,
  Warning,
  Connection
} from '@element-plus/icons-vue'

type PresetType = 'no-data' | 'no-result' | 'no-network' | 'no-paper' | 'no-post' | 'no-download'

interface Props {
  description?: string
  type?: PresetType
  icon?: any
  actionText?: string
}

interface Emits {
  (e: 'action'): void
}

const props = withDefaults(defineProps<Props>(), {
  type: 'no-data',
  description: ''
})

const emit = defineEmits<Emits>()

const presetConfigs: Record<PresetType, { icon: any; description: string }> = {
  'no-data': {
    icon: Document,
    description: '暂无数据'
  },
  'no-result': {
    icon: Search,
    description: '未找到相关结果'
  },
  'no-network': {
    icon: Connection,
    description: '网络连接异常'
  },
  'no-paper': {
    icon: Document,
    description: '暂无论文'
  },
  'no-post': {
    icon: ChatDotRound,
    description: '暂无经验贴'
  },
  'no-download': {
    icon: Download,
    description: '暂无下载资源'
  }
}

const iconComponent = computed(() => {
  if (props.icon) return props.icon
  return presetConfigs[props.type].icon
})

const description = computed(() => {
  if (props.description) return props.description
  return presetConfigs[props.type].description
})

const image = computed(() => {
  return props.icon || iconComponent.value ? '' : undefined
})

const handleAction = () => {
  emit('action')
}
</script>

<style scoped lang="scss">
.empty-state-wrapper {
  padding: 60px 0;
  
  .empty-icon {
    width: 80px;
    height: 80px;
    color: #c0c4cc;
  }
}
</style>
