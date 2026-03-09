import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './style/global.scss'
import App from './App.vue'
import router from './router'
import VueUeditorWrap from 'vue-ueditor-wrap'

const app = createApp(App)

app.use(createPinia())
app.use(ElementPlus)
app.use(router)
app.use(VueUeditorWrap)

app.mount('#app')
