<template>
  <div v-if="loading" class="loading-wrapper" :class="{ 'fullscreen': fullscreen }">
    <div class="loading-content">
      <div class="loading-spinner">
        <div class="spinner-dot" v-for="i in 8" :key="i" :style="{ '--i': i }"></div>
      </div>
      <p v-if="text" class="loading-text">{{ text }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  loading: boolean
  fullscreen?: boolean
  text?: string
}

withDefaults(defineProps<Props>(), {
  fullscreen: false,
  text: '加载中...'
})
</script>

<style scoped lang="scss">
.loading-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  
  &.fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(255, 255, 255, 0.9);
    z-index: 9999;
    padding: 0;
  }
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.loading-spinner {
  position: relative;
  width: 60px;
  height: 60px;
  
  .spinner-dot {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #409eff;
    transform: translate(-50%, -50%) rotate(calc(var(--i) * 45deg)) translateY(20px);
    animation: spinner-bounce 1.2s ease-in-out infinite;
    animation-delay: calc(var(--i) * 0.15s);
    opacity: 0.7;
  }
}

@keyframes spinner-bounce {
  0%, 80%, 100% {
    transform: translate(-50%, -50%) rotate(calc(var(--i) * 45deg)) translateY(20px) scale(0.6);
    opacity: 0.4;
  }
  40% {
    transform: translate(-50%, -50%) rotate(calc(var(--i) * 45deg)) translateY(20px) scale(1);
    opacity: 1;
  }
}

.loading-text {
  margin: 0;
  color: #606266;
  font-size: 14px;
}
</style>
