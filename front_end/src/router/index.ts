import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import { adminAuthGuard, loginGuard } from '@/guards/auth'

const routes: Array<RouteRecordRaw> = [
    // 用戶展示端路由 - 使用UserLayout包裝
    {
        path: '/',
        component: () => import('@/layouts/UserLayout.vue'),
        children: [
            {
                path: '',
                name: 'home',
                component: () => import('@/views/HomeView.vue')
            },
            {
                path: 'members',
                name: 'members',
                component: () => import('@/views/MemberView.vue'),
            },
            {
                path: 'group/:id',
                name: 'group',
                component: () => import('@/views/GroupView.vue'),
                props: true
            },
            {
                path: 'member/:id',
                name: 'member',
                component: () => import('@/views/MemberDetailView.vue'),
                props: true
            },
            {
                path: 'news',
                name: 'news',
                component: () => import('@/views/NewsView.vue')
            },
            {
                path: 'papers',
                name: 'papers',
                component: () => import('@/views/PaperView.vue')
            },
            {
                path: 'projects',
                name: 'projects',
                component: () => import('@/views/ProjectView.vue')
            },
            {
                path: 'project/:id',
                name: 'project-detail',
                component: () => import('@/views/ProjectDetailView.vue'),
                props: true
            },
            {
                path: 'paper/:id',
                name: 'paper-detail',
                component: () => import('@/views/PaperDetailView.vue'),
                props: true
            },
            {
                path: 'news/:id',
                name: 'news-detail',
                component: () => import('@/views/NewsDetailView.vue'),
                props: true
            }
        ]
    },

    // 管理員登錄頁面（無需認證，但已登錄會重定向）
    {
        path: '/admin/login',
        name: 'admin-login',
        component: () => import('@/views/admin/LoginView.vue'),
        beforeEnter: loginGuard
    },

    // 管理員後台路由（需要認證）
    {
        path: '/admin',
        redirect: '/admin/dashboard',
        component: () => import('@/layouts/AdminLayout.vue'),
        beforeEnter: adminAuthGuard,
        children: [
            {
                path: 'dashboard',
                name: 'admin-dashboard',
                component: () => import('@/views/admin/DashboardView.vue')
            },
            {
                path: 'members',
                name: 'admin-members',
                component: () => import('@/views/admin/MemberManageView.vue')
            },
            {
                path: 'groups',
                name: 'admin-groups',
                component: () => import('@/views/admin/GroupManageView.vue')
            },
            {
                path: 'papers',
                name: 'admin-papers',
                component: () => import('@/views/admin/PaperManageView.vue')
            },
            {
                path: 'projects',
                name: 'admin-projects',
                component: () => import('@/views/admin/ProjectManageView.vue')
            },
            {
                path: 'news',
                name: 'admin-news',
                component: () => import('@/views/admin/NewsManageView.vue')
            },
            {
                path: 'lab',
                name: 'admin-lab',
                component: () => import('@/views/admin/LabManageView.vue')
            },
            {
                path: 'admins',
                name: 'admin-admins',
                component: () => import('@/views/admin/AdminManageView.vue')
            },
            {
                path: 'system',
                name: 'admin-system',
                component: () => import('@/views/admin/SystemManageView.vue')
            },
            {
                path: 'operation-logs',
                name: 'admin-operation-logs',
                component: () => import('@/views/admin/OperationLogsView.vue')
            },
            {
                path: 'profile',
                name: 'admin-profile',
                component: () => import('@/views/admin/ProfileView.vue')
            },
            {
                path: 'change-password',
                name: 'admin-change-password',
                component: () => import('@/views/admin/ChangePasswordView.vue')
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
    scrollBehavior(to, from, savedPosition) {
        // 如果有保存的位置（例如使用瀏覽器的前進/後退按鈕）
        if (savedPosition) {
            return savedPosition
        }
        // 對於詳情頁面（包含 id 參數的路由），保持平滑滾動到頂部
        if (to.name && ['paper-detail', 'project-detail', 'news-detail', 'member', 'group'].includes(to.name as string)) {
            return { top: 0, behavior: 'smooth' }
        }
        // 對於其他頁面切換，立即滾動到頂部
        return { top: 0 }
    }
})

export default router
