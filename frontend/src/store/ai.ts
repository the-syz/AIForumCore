import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface SelectedContent {
  type: string
  id: number
  title: string
}

export const useAIStore = defineStore('ai', () => {
  const isOpen = ref(false)
  const pendingSelectedContent = ref<SelectedContent | null>(null)
  
  const toggle = () => {
    isOpen.value = !isOpen.value
  }
  
  const open = () => {
    isOpen.value = true
  }
  
  const close = () => {
    isOpen.value = false
  }
  
  // 添加选中的内容到AI对话
  const addSelectedContent = (content: SelectedContent) => {
    pendingSelectedContent.value = content
    open()
  }
  
  // 获取并清除待添加的内容
  const getAndClearPendingContent = (): SelectedContent | null => {
    const content = pendingSelectedContent.value
    pendingSelectedContent.value = null
    return content
  }
  
  return {
    isOpen,
    pendingSelectedContent,
    toggle,
    open,
    close,
    addSelectedContent,
    getAndClearPendingContent
  }
})
