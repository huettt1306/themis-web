import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import ProblemsListView from '@/views/ProblemsListView.vue'
import ProblemDetailView from '@/views/ProblemDetailView.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginView },
  { path: '/problems', component: ProblemsListView, meta: { requiresAuth: true } },
  { path: '/problems/:filename', component: ProblemDetailView, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// --- Middleware chặn truy cập nếu chưa đăng nhập ---
router.beforeEach((to, from, next) => {
  const user = localStorage.getItem('user')
  if (to.meta.requiresAuth && !user) {
    next('/login')
  } else if (to.path === '/login' && user) {
    next('/problems')
  } else {
    next()
  }
})

export default router
