<template>
  <n-card>
    <n-space justify="space-between" align="center">
      <h2>管理控制台</h2>
      <n-button @click="refreshData">
        <template #icon>
          <n-icon :component="RefreshOutlined" />
        </template>
        刷新
      </n-button>
    </n-space>
    
    <n-grid :cols="4" :x-gap="24" :y-gap="24" style="margin-top: 24px;">
      <n-grid-item>
        <n-card>
          <n-statistic label="成員總數" :value="stats.memberCount" />
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card>
          <n-statistic label="論文總數" :value="stats.paperCount" />
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card>
          <n-statistic label="項目總數" :value="stats.projectCount" />
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card>
          <n-statistic label="新聞總數" :value="stats.newsCount" />
        </n-card>
      </n-grid-item>
    </n-grid>

    <n-card style="margin-top: 24px;">
      <template #header>
        快捷操作
      </template>
      <n-space>
        <n-button 
          type="primary" 
          @click="$router.push('/admin/members')"
        >
          成員管理
        </n-button>
        <n-button @click="$router.push('/admin/papers')">
          論文管理
        </n-button>
        <n-button @click="$router.push('/admin/news')">
          新聞管理
        </n-button>
        <n-button @click="$router.push('/admin/projects')">
          項目管理
        </n-button>
      </n-space>
    </n-card>
  </n-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RefreshOutlined } from '@vicons/material'
import { memberAPI, paperAPI, projectAPI, newsAPI } from '@/utils/api'

const stats = ref({
  memberCount: 0,
  paperCount: 0,
  projectCount: 0,
  newsCount: 0
})

const loadStats = async () => {
  try {
    const [memberRes, paperRes, projectRes, newsRes] = await Promise.all([
      memberAPI.getMembers({ page: 1, limit: 1 }),
      paperAPI.getPapers({ page: 1, limit: 1 }),
      projectAPI.getProjects({ page: 1, limit: 1 }),
      newsAPI.getNews({ page: 1, limit: 1 })
    ])
    
    stats.value = {
      memberCount: memberRes.total,
      paperCount: paperRes.total,
      projectCount: projectRes.total,
      newsCount: newsRes.total
    }
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

const refreshData = () => {
  loadStats()
}

onMounted(() => {
  loadStats()
})
</script>