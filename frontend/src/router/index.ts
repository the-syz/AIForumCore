import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { public: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'Home', component: () => import('@/views/Home.vue') },
      { path: 'papers', name: 'Papers', component: () => import('@/views/Papers.vue') },
      { path: 'papers/:id', name: 'PaperDetail', component: () => import('@/views/PaperDetail.vue') },
      { path: 'papers/upload', name: 'PaperUpload', component: () => import('@/views/PaperUpload.vue') },
      { path: 'papers/edit/:id', name: 'PaperEdit', component: () => import('@/views/PaperEdit.vue') },
      { path: 'posts', name: 'Posts', component: () => import('@/views/Posts.vue') },
      { path: 'downloads', name: 'Downloads', component: () => import('@/views/Downloads.vue') },
      { path: 'profile', name: 'Profile', component: () => import('@/views/Profile.vue') },
      { path: 'admin', name: 'Admin', component: () => import('@/views/Admin.vue'), meta: { admin: true } }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  const userStore = useUserStore()
  
  if (!to.meta.public && !userStore.token) {
    next('/login')
  } else if (to.meta.admin && !userStore.isAdmin) {
    next('/')
  } else {
    next()
  }
})

export default router