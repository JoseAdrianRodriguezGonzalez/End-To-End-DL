import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Metricas from '../views/Metricas.vue'

const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/metricas',
      name: 'metricas',
      component: Metricas,
    },
  ],
})

export default router
