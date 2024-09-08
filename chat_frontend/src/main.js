import { createApp } from 'vue'
import './index.css'
import App from './App.vue'
import router from './router'
import Toast from "vue-toastification";
import "./vue-toastification/dist/index.css"

const app = createApp(App)

app.config.globalProperties.$apiBaseUrl = 'http://127.0.0.1:8000';//local
//app.config.globalProperties.$apiBaseUrl = 'http://172.16.120.14:8081';//server

app.use(router).use(Toast).mount('#app')