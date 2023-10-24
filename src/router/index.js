import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/projects',
      name: 'projects',
      component: () => import('../views/ProjectsView.vue')
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('../views/ContactView.vue')
    },
    {
      path: '/projects/3dprinting',
      name: '3dprinting',
      component: () => import('../views/Project3DPrintingView.vue')
    },
    {
      path: '/projects/photography',
      name: 'photography',
      component: () => import('../views/ProjectPhotographyView.vue')
    },
    {
      path: '/projects/motorcycles',
      name: 'motorcycles',
      component: () => import('../views/ProjectMotorcyclesView.vue')
    }
  ]
})

export default router
