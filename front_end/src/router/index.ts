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
                path: 'about',
                name: 'about',
                component: () => import('@/views/AboutView.vue')
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
                path: 'members/create',
                name: 'admin-member-create',
                component: () => import('@/views/admin/MemberEditView.vue')
            },
            {
                path: 'members/:id/edit',
                name: 'admin-member-edit',
                component: () => import('@/views/admin/MemberEditView.vue'),
                props: true
            },
            {
                path: 'groups',
                name: 'admin-groups',
                component: () => import('@/views/admin/GroupManageView.vue')
            },
            {
                path: 'groups/create',
                name: 'admin-group-create',
                component: () => import('@/views/admin/GroupEditView.vue')
            },
            {
                path: 'groups/:id/edit',
                name: 'admin-group-edit',
                component: () => import('@/views/admin/GroupEditView.vue'),
                props: true
            },
            {
                path: 'papers',
                name: 'admin-papers',
                component: () => import('@/views/admin/PaperManageView.vue')
            },
            {
                path: 'papers/create',
                name: 'admin-paper-create',
                component: () => import('@/views/admin/PaperEditView.vue')
            },
            {
                path: 'papers/:id/edit',
                name: 'admin-paper-edit',
                component: () => import('@/views/admin/PaperEditView.vue'),
                props: true
            },
            {
                path: 'projects',
                name: 'admin-projects',
                component: () => import('@/views/admin/ProjectManageView.vue')
            },
            {
                path: 'projects/create',
                name: 'admin-project-create',
                component: () => import('@/views/admin/ProjectEditView.vue')
            },
            {
                path: 'projects/:id/edit',
                name: 'admin-project-edit',
                component: () => import('@/views/admin/ProjectEditView.vue'),
                props: true
            },
            {
                path: 'news',
                name: 'admin-news',
                component: () => import('@/views/admin/NewsManageView.vue')
            },
            {
                path: 'news/create',
                name: 'admin-news-create',
                component: () => import('@/views/admin/NewsEditView.vue')
            },
            {
                path: 'news/:id/edit',
                name: 'admin-news-edit',
                component: () => import('@/views/admin/NewsEditView.vue'),
                props: true
            },
            {
                path: 'lab',
                name: 'admin-lab',
                component: () => import('@/views/admin/LabManageView.vue')
            },
            {
                path: 'system',
                name: 'admin-system',
                component: () => import('@/views/admin/SystemManageView.vue')
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
    routes
})

export default router
