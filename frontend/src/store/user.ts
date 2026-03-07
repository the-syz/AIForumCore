import { defineStore } from 'pinia'

interface UserInfo {
  id: number
  name: string
  student_id: string
  grade: string
  email: string
  phone: string
  research_direction: string
  wechat: string
  role: string
  is_admin: boolean
}

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: null as UserInfo | null,
  }),
  getters: {
    isAdmin: (state) => state.userInfo?.is_admin || false,
  },
  actions: {
    setToken(token: string, autoLogin: boolean = false) {
      this.token = token
      if (autoLogin) {
        localStorage.setItem('token', token)
      }
    },
    setUserInfo(userInfo: UserInfo) {
      this.userInfo = userInfo
    },
    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
    },
  },
})
