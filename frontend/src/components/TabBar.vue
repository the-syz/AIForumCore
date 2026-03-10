<template>
  <div class="tab-bar-container">
    <div class="tab-bar">
      <div
        v-for="tab in tabs"
        :key="tab.name"
        class="tab-item"
        :class="{ active: activeTab === tab.name }"
        @click="handleTabClick(tab)"
      >
        <span class="tab-title">{{ tab.title }}</span>
        <el-icon
          v-if="tab.closable"
          class="tab-close"
          @click.stop="handleTabClose(tab)"
        >
          <Close />
        </el-icon>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTabsStore } from '@/store/tabs'
import { Close } from '@element-plus/icons-vue'

const router = useRouter()
const tabsStore = useTabsStore()

const tabs = computed(() => tabsStore.tabs)
const activeTab = computed(() => tabsStore.activeTab)

const handleTabClick = (tab: any) => {
  tabsStore.setActiveTab(tab.name)
  router.push(tab.path)
}

const handleTabClose = (tab: any) => {
  tabsStore.removeTab(tab.name)
  const newActiveTab = tabsStore.tabs.find((t: any) => t.name === tabsStore.activeTab)
  if (newActiveTab) {
    router.push(newActiveTab.path)
  }
}
</script>

<style scoped lang="scss">
.tab-bar-container {
  background-color: #f5f7fa;
  border-bottom: 1px solid #e4e7ed;
  height: 36px;
}

.tab-bar {
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  overflow-x: auto;
  height: 100%;
  align-items: flex-start;
  
  &::-webkit-scrollbar {
    height: 3px;
  }
  
  &::-webkit-scrollbar-thumb {
    background-color: #c0c4cc;
    border-radius: 2px;
  }
}

.tab-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background-color: #fff;
  border: 1px solid #e4e7ed;
  border-bottom: none;
  border-radius: 4px 4px 0 0;
  margin-right: 4px;
  margin-top: 4px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
  font-size: 12px;
  max-width: 180px;
  
  &:hover {
    background-color: #ecf5ff;
    
    .tab-close {
      opacity: 1;
    }
  }
  
  &.active {
    background-color: #409eff;
    color: #fff;
    border-color: #409eff;
    
    .tab-close {
      color: #fff;
      opacity: 1;
    }
  }
  
  .tab-title {
    font-size: 12px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .tab-close {
    font-size: 10px;
    opacity: 0;
    transition: opacity 0.2s;
    padding: 2px;
    border-radius: 2px;
    
    &:hover {
      background-color: rgba(0, 0, 0, 0.1);
    }
  }
}
</style>
