<template>
  <div class="ueditor-container">
    <div
      :id="id"
      style="width: 100%; height: 100%"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'

interface Props {
  modelValue?: string
  config?: Record<string, any>
  height?: number | string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  config: () => ({}),
  height: 400
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'ready', editor: any): void
  (e: 'change', content: string): void
}>()

const id = ref(`editor_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`)
let editor: any = null
let isLoaded = false

const defaultConfig = {
  UEDITOR_HOME_URL: 'https://cdn.jsdelivr.net/npm/ueditor@1.4.3.3/',
  serverUrl: '/api/editor/upload',
  initialFrameWidth: '100%',
  initialFrameHeight: props.height,
  autoHeightEnabled: false,
  autoFloatEnabled: true,
  wordCount: true,
  maximumWords: 10000,
  toolbars: [[
    'fullscreen', 'source', '|', 'undo', 'redo', '|',
    'bold', 'italic', 'underline', 'fontborder', 'strikethrough', '|',
    'forecolor', 'backcolor', '|',
    'justifyleft', 'justifycenter', 'justifyright', '|',
    'insertorderedlist', 'insertunorderedlist', '|',
    'paragraph', 'fontfamily', 'fontsize', '|',
    'link', 'unlink', '|',
    'simpleupload', 'insertimage', 'emotion', '|',
    'inserttable', 'horizontal', '|',
    'preview', 'help'
  ]]
}

// 动态加载脚本
const loadScript = (src: string): Promise<void> => {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = src
    script.onload = () => resolve()
    script.onerror = () => reject(new Error(`Failed to load script: ${src}`))
    document.head.appendChild(script)
  })
}

// 加载UEditor
const loadUEditor = async (): Promise<boolean> => {
  if (isLoaded || window.UE) {
    isLoaded = true
    return true
  }

  try {
    // 设置UEditor根路径
    window.UEDITOR_HOME_URL = 'https://cdn.jsdelivr.net/npm/ueditor@1.4.3.3/'
    
    // 加载UEditor脚本
    await loadScript('https://cdn.jsdelivr.net/npm/ueditor@1.4.3.3/ueditor.config.js')
    await loadScript('https://cdn.jsdelivr.net/npm/ueditor@1.4.3.3/ueditor.all.min.js')
    await loadScript('https://cdn.jsdelivr.net/npm/ueditor@1.4.3.3/lang/zh-cn/zh-cn.js')
    
    isLoaded = true
    return true
  } catch (error) {
    console.error('加载UEditor失败:', error)
    return false
  }
}

const initEditor = async () => {
  console.log('开始初始化UEditor')
  
  // 加载UEditor
  const loaded = await loadUEditor()
  if (!loaded) {
    console.error('UEditor加载失败，无法初始化')
    return
  }
  
  console.log('UEditor加载成功')
  console.log('window.UE:', window.UE)
  console.log('id.value:', id.value)
  
  if (!window.UE) {
    console.error('UEditor is not loaded')
    return
  }

  const config = { ...defaultConfig, ...props.config }
  console.log('UEditor配置:', config)
  
  try {
    editor = window.UE.getEditor(id.value, config)
    console.log('编辑器实例:', editor)

    editor.ready(() => {
      console.log('UEditor准备就绪')
      if (props.modelValue) {
        editor.setContent(props.modelValue)
        console.log('已设置初始内容')
      }
      emit('ready', editor)
      console.log('已触发ready事件')

      editor.addListener('contentChange', () => {
        const content = editor.getContent()
        emit('update:modelValue', content)
        emit('change', content)
      })
      console.log('已添加contentChange监听器')
    })
  } catch (error) {
    console.error('初始化UEditor失败:', error)
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
    editor.setContent(content)
  }
}

const getContent = () => {
  if (editor) {
    return editor.getContent()
  }
  return ''
}

const getContentTxt = () => {
  if (editor) {
    return editor.getContentTxt()
  }
  return ''
}

const clearContent = () => {
  if (editor) {
    editor.setContent('')
  }
}

watch(() => props.modelValue, (newVal) => {
  if (editor && editor.getContent() !== newVal) {
    editor.setContent(newVal || '')
  }
})

onMounted(() => {
  console.log('UEditor组件挂载')
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
.ueditor-container {
  width: 100%;
  height: 100%;
  min-height: 400px;
}
</style>
