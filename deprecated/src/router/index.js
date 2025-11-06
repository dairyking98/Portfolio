import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProjectsView from '../views/ProjectsView.vue'
import ContactView from '../views/ContactView.vue'
import Project3DPrintingView from '../views/Project3DPrintingView.vue'
import ProjectPhotographyView from '../views/ProjectPhotographyView.vue'
import ProjectMotorcyclesView from '../views/ProjectMotorcyclesView.vue'

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
      component: ProjectsView
    },
    {
      path: '/contact',
      name: 'contact',
      component: ContactView
    },
    {
      path: '/projects/3dprinting',
      name: '3dprinting',
      component: Project3DPrintingView
    },
    {
      path: '/projects/photography',
      name: 'photography',
      component: ProjectPhotographyView
    },
    {
      path: '/projects/motorcycles',
      name: 'motorcycles',
      component: ProjectMotorcyclesView
    }
  ]
})

export default router
