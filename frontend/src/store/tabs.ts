import { defineStore } from 'pinia'

interface TabItem {
  name: string
  title: string
  path: string
  closable: boolean
}

export const useTabsStore = defineStore('tabs', {
  state: () => ({
    tabs: [] as TabItem[],
    activeTab: '',
  }),
  getters: {
    tabList: (state) => state.tabs,
  },
  actions: {
    initTabs() {
      this.tabs = [
        {
          name: 'home',
          title: '首页',
          path: '/',
          closable: false,
        },
      ]
      this.activeTab = 'home'
    },

    addTab(tab: TabItem) {
      if (tab.name === 'home') {
        // 更新主页标签
        const homeTab = this.tabs.find((t) => t.name === 'home')
        if (homeTab) {
          homeTab.title = tab.title
          homeTab.path = tab.path
        } else {
          this.tabs.push(tab)
        }
      } else {
        const existTab = this.tabs.find((t) => t.path === tab.path)
        if (existTab) {
          // 更新现有标签的标题
          existTab.title = tab.title
        } else {
          this.tabs.push(tab)
        }
      }
      this.activeTab = tab.name
    },

    removeTab(name: string) {
      const index = this.tabs.findIndex((t) => t.name === name)
      if (index > -1 && this.tabs[index].closable) {
        this.tabs.splice(index, 1)
        if (this.activeTab === name) {
          const lastTab = this.tabs[this.tabs.length - 1]
          this.activeTab = lastTab ? lastTab.name : 'home'
        }
      }
    },

    setActiveTab(name: string) {
      this.activeTab = name
    },

    getTabByPath(path: string) {
      return this.tabs.find((t) => t.path === path)
    },

    updateTabTitle(path: string, title: string) {
      const tab = this.tabs.find((t) => t.path === path)
      if (tab) {
        tab.title = title
      }
    },
  },
})
