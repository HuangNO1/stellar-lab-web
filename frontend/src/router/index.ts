import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/store/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/papers',
    name: 'papers',
    component: () => import('@/views/Papers.vue')
  },
  {
    path: '/members',
    name: 'members',
    component: () => import('@/views/Members.vue')
  },
  {
    path: '/projects',
    name: 'projects',
    component: () => import('@/views/Projects.vue')
  },
  {
    path: '/news',
    name: 'news',
    component: () => import('@/views/News.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('@/views/admin/Dashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'admin-dashboard',
        component: () => import('@/views/admin/Dashboard.vue')
      },
      {
        path: 'lab',
        name: 'admin-lab',
        component: () => import('@/views/admin/LabSettings.vue')
      },
      {
        path: 'groups',
        name: 'admin-groups',
        component: () => import('@/views/admin/ResearchGroups.vue')
      },
      {
        path: 'members',
        name: 'admin-members',
        component: () => import('@/views/admin/MemberManagement.vue')
      },
      {
        path: 'papers',
        name: 'admin-papers',
        component: () => import('@/views/admin/PaperManagement.vue')
      },
      {
        path: 'news',
        name: 'admin-news',
        component: () => import('@/views/admin/NewsManagement.vue')
      },
      {
        path: 'projects',
        name: 'admin-projects',
        component: () => import('@/views/admin/ProjectManagement.vue')
      },
      {
        path: 'admins',
        name: 'admin-admins',
        component: () => import('@/views/admin/AdminManagement.vue')
      },
      {
        path: 'records',
        name: 'admin-records',
        component: () => import('@/views/admin/EditRecords.vue')
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, _from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
    return
  }
  
  if (to.meta.requiresAdmin && !userStore.isAdmin) {
    next('/')
    return
  }
  
  next()
})

export default router