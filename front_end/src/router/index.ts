import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/members',
        name: 'members',
        component: () => import('@/views/MemberView.vue'),
    },
    {
        path: '/group/:id',
        name: 'group',
        component: () => import('@/views/GroupView.vue'),
        props: true
    },
    {
        path: '/member/:id',
        name: 'member',
        component: () => import('@/views/MemberDetailView.vue'),
        props: true
    },
    {
        path: '/news',
        name: 'news',
        component: () => import('@/views/NewsView.vue')
    },
    {
        path: '/papers',
        name: 'papers',
        component: () => import('@/views/PaperView.vue')
    },
    {
        path: '/projects',
        name: 'projects',
        component: () => import('@/views/ProjectView.vue')
    },
    {
        path: '/about',
        name: 'about',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
