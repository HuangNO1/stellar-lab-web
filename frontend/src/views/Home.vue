<template>
  <div class="home">
    <n-card class="hero-section">
      <div class="hero-content">
        <h1>{{ t('nav.home') }}</h1>
        <p class="hero-description">
          {{ labInfo?.lab_desc_zh || labInfo?.lab_desc_en || '歡迎來到我們的實驗室' }}
        </p>
        <n-space>
          <n-button
            type="primary" 
            size="large"
            @click="router.push('/members')"
          >
            {{ t('nav.members') }}
          </n-button>
          <n-button
            type="default"
            size="large"
            @click="router.push('/papers')"
          >
            {{ t('nav.papers') }}
          </n-button>
        </n-space>
      </div>
    </n-card>

    <n-grid :cols="3" :x-gap="24" :y-gap="24" style="margin-top: 24px;">
      <n-grid-item>
        <n-card hoverable>
          <template #header>
            <n-space align="center">
              <n-icon size="20" :color="themeVars.primaryColor">
                <People />
              </n-icon>
              {{ t('nav.members') }}
            </n-space>
          </template>
          <n-statistic :value="stats.memberCount" />
          <template #footer>
            <n-button text @click="router.push('/members')">
              查看更多 →
            </n-button>
          </template>
        </n-card>
      </n-grid-item>

      <n-grid-item>
        <n-card hoverable>
          <template #header>
            <n-space align="center">
              <n-icon size="20" :color="themeVars.primaryColor">
                <Document />
              </n-icon>
              {{ t('nav.papers') }}
            </n-space>
          </template>
          <n-statistic :value="stats.paperCount" />
          <template #footer>
            <n-button text @click="router.push('/papers')">
              查看更多 →
            </n-button>
          </template>
        </n-card>
      </n-grid-item>

      <n-grid-item>
        <n-card hoverable>
          <template #header>
            <n-space align="center">
              <n-icon size="20" :color="themeVars.primaryColor">
                <Briefcase />
              </n-icon>
              {{ t('nav.projects') }}
            </n-space>
          </template>
          <n-statistic :value="stats.projectCount" />
          <template #footer>
            <n-button text @click="router.push('/projects')">
              查看更多 →
            </n-button>
          </template>
        </n-card>
      </n-grid-item>
    </n-grid>

    <n-card class="news-section" style="margin-top: 24px;">
      <template #header>
        <n-space justify="space-between" align="center">
          <span>{{ t('nav.news') }}</span>
          <n-button text @click="router.push('/news')">
            查看全部 →
          </n-button>
        </n-space>
      </template>
      <n-list v-if="recentNews.length">
        <n-list-item v-for="news in recentNews" :key="news.news_id">
          <n-thing :title="news.news_content_zh || news.news_content_en || '無標題'">
            <template #description>
              <n-space>
                <n-tag size="small" :type="getNewsTypeColor(news.news_type)">
                  {{ getNewsTypeText(news.news_type) }}
                </n-tag>
                <span>{{ formatDate(news.news_date || news.created_at || '') }}</span>
              </n-space>
            </template>
            {{ (news.news_content_zh || news.news_content_en || '').substring(0, 100) }}...
          </n-thing>
        </n-list-item>
      </n-list>
      <n-empty v-else description="暫無新聞" />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from '@vue/reactivity'
import { onMounted } from '@vue/runtime-core'
import { useThemeVars } from 'naive-ui'
import { useRouter } from 'vue-router'
import { People, Document, Briefcase } from '@vicons/ionicons5'
import { useI18n } from 'vue-i18n'
import type { Lab, News } from '@/types'
import { labAPI, newsAPI, memberAPI, paperAPI, projectAPI } from '@/utils/api'

const router = useRouter()
const themeVars = useThemeVars()
const { t } = useI18n()
const labInfo = ref<Lab | null>(null)
const recentNews = ref<News[]>([])
const stats = ref({
  memberCount: 0,
  paperCount: 0,
  projectCount: 0
})

const getNewsTypeColor = (type: number) => {
  const colors: Record<number, string> = {
    0: 'info',    // 論文
    1: 'success', // 獎項
    2: 'warning', // 報告
    3: 'default'  // 其它
  }
  return colors[type] || 'default'
}

const getNewsTypeText = (type: number) => {
  const types: Record<number, string> = {
    0: t('news.paper'),
    1: t('news.award'),
    2: t('news.report'),
    3: t('news.other')
  }
  return types[type] || t('news.other')
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const loadData = async () => {
  try {
    // Load lab info
    const labResponse = await labAPI.getLab()
    labInfo.value = labResponse.data

    // Load recent news
    const newsResponse = await newsAPI.getNews({ page: 1, limit: 5 })
    recentNews.value = newsResponse.data.data

    // Load statistics
    const [memberResponse, paperResponse, projectResponse] = await Promise.all([
      memberAPI.getMembers({ page: 1, limit: 1 }),
      paperAPI.getPapers({ page: 1, limit: 1 }),
      projectAPI.getProjects({ page: 1, limit: 1 })
    ])

    stats.value = {
      memberCount: memberResponse.data.total,
      paperCount: paperResponse.data.total,
      projectCount: projectResponse.data.total
    }
  } catch (error) {
    console.error('Failed to load home data:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.hero-section {
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.hero-section :deep(.n-card__content) {
  padding: 60px 40px;
}

.hero-content h1 {
  font-size: 48px;
  margin-bottom: 20px;
  font-weight: 700;
}

.hero-description {
  font-size: 18px;
  margin-bottom: 40px;
  opacity: 0.9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}
</style>