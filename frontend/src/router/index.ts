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
                path: 'resources',
                name: 'resources',
                component: () => import('@/views/ResourceView.vue')
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
                path: 'resources',
                name: 'admin-resources',
                component: () => import('@/views/admin/ResourceManageView.vue')
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
            },
            // 管理員 404 頁面
            {
                path: ':pathMatch(.*)*',
                name: 'admin-not-found',
                component: () => import('@/views/admin/AdminNotFoundView.vue')
            }
        ]
    },
    
    // 用戶端 404 頁面（必須放在最後）
    {
        path: '/:pathMatch(.*)*',
        name: 'not-found',
        component: () => import('@/views/NotFoundView.vue')
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
        
        // 對於所有路由切換，都滾動到頂部，但給詳情頁面更多時間來渲染
        const isDetailPage = to.name && [
            'paper-detail', 
            'project-detail', 
            'news-detail', 
            'member', 
            'group'
        ].includes(to.name as string);
        
        if (isDetailPage) {
            // 詳情頁面使用延遲滾動，確保內容已經渲染完成
            return new Promise((resolve) => {
                setTimeout(() => {
                    resolve({ top: 0, behavior: 'smooth' });
                }, 100); // 100ms 延遲確保 DOM 已更新
            });
        }
        
        // 對於其他頁面切換，立即滾動到頂部
        return { top: 0 }
    }
})

export default router
