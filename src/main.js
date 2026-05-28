import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import './styles/global.css'

import Landing from './pages/Landing.vue'
import Home from './pages/Home.vue'
import Search from './pages/Search.vue'
import BookDetail from './pages/BookDetail.vue'
import Upload from './pages/Upload.vue'
import Profile from './pages/Profile.vue'
import Admin from './pages/Admin.vue'
import Recommend from './pages/Recommend.vue'

const routes = [
  { path: '/', name: 'landing', component: Landing },
  { path: '/home', name: 'home', component: Home },
  { path: '/search', name: 'search', component: Search },
  { path: '/book/:id', name: 'bookDetail', component: BookDetail },
  { path: '/upload', name: 'upload', component: Upload },
  { path: '/profile', name: 'profile', component: Profile },
  { path: '/admin', name: 'admin', component: Admin },
  { path: '/recommend', name: 'recommend', component: Recommend },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
app.use(router)
app.mount('#app')
