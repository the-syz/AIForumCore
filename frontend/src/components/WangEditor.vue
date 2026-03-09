<template>
  <div class="wangeditor-container">
    <div ref="editorRef" style="width: 100%; height: 100%"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'

interface Props {
  modelValue?: string
  height?: number | string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  height: 500
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'ready', editor: any): void
  (e: 'change', content: string): void
}>()

const editorRef = ref<HTMLElement>()
let editor: any = null

// 动态加载wangEditor
const loadWangEditor = async (): Promise<boolean> => {
  if (window.wangEditor) {
    return true
  }

  try {
    // 加载wangEditor脚本
    await new Promise((resolve, reject) => {
      const script = document.createElement('script')
      script.src = 'https://cdn.jsdelivr.net/npm/wang-editor@1.5.0/dist/wangEditor.min.js'
      script.onload = resolve
      script.onerror = reject
      document.head.appendChild(script)
    })
    
    return true
  } catch (error) {
    console.error('加载wangEditor失败:', error)
    return false
  }
}

const initEditor = async () => {
  console.log('开始初始化wangEditor')
  
  // 加载wangEditor
  const loaded = await loadWangEditor()
  if (!loaded) {
    console.error('wangEditor加载失败，无法初始化')
    return
  }
  
  console.log('wangEditor加载成功')
  console.log('window.wangEditor:', window.wangEditor)
  
  if (!window.wangEditor || !editorRef.value) {
    console.error('wangEditor is not loaded or editorRef is null')
    return
  }

  try {
    // 创建编辑器实例
    editor = new window.wangEditor(editorRef.value)
    console.log('编辑器实例:', editor)

    // 配置编辑器
    editor.config.uploadImgServer = '/api/editor/upload'
    editor.config.uploadImgMaxSize = 5 * 1024 * 1024
    editor.config.uploadImgAccept = ['jpg', 'jpeg', 'png', 'gif']
    editor.config.uploadImgFieldName = 'file'

    // 设置初始内容
    if (props.modelValue) {
      editor.txt.html(props.modelValue)
    }

    // 监听内容变化
    editor.on('change', () => {
      const content = editor.txt.html()
      emit('update:modelValue', content)
      emit('change', content)
    })

    // 初始化编辑器
    editor.create()
    console.log('wangEditor初始化完成')
    emit('ready', editor)
  } catch (error) {
    console.error('初始化wangEditor失败:', error)
  }
}

const destroyEditor = () => {
  if (editor) {
    editor.destroy()
    editor = null
  }
}

const setContent = (content: string) => {
  if (editor) {
    editor.txt.html(content)
  }
}

const getContent = () => {
  if (editor) {
    return editor.txt.html()
  }
  return ''
}

const getContentTxt = () => {
  if (editor) {
    return editor.txt.text()
  }
  return ''
}

const clearContent = () => {
  if (editor) {
    editor.txt.clear()
  }
}

watch(() => props.modelValue, (newVal) => {
  if (editor && editor.txt.html() !== newVal) {
    editor.txt.html(newVal || '')
  }
})

onMounted(() => {
  console.log('WangEditor组件挂载')
  nextTick(() => {
    console.log('执行nextTick回调')
    initEditor()
  })
})

onBeforeUnmount(() => {
  destroyEditor()
})

defineExpose({
  setContent,
  getContent,
  getContentTxt,
  clearContent,
  getEditor: () => editor
})
</script>

<style scoped>
.wangeditor-container {
  width: 100%;
  height: 100%;
  min-height: 400px;
}
</style>