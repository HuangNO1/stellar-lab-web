<template>
  <n-grid :cols="4" :x-gap="24" :y-gap="24" responsive="screen">
    <n-grid-item v-for="member in members" :key="member.id">
      <n-card hoverable class="member-card">
        <div class="member-avatar">
          <n-avatar
            :size="80"
            :src="member.avatar_url"
            :fallback-src="'/default-avatar.png'"
            round
          >
            {{ member.name.charAt(0) }}
          </n-avatar>
        </div>
        
        <div class="member-info">
          <h3>{{ member.name }}</h3>
          <n-space vertical size="small">
            <n-tag
              v-if="member.job_title"
              size="small"
              type="primary"
            >
              {{ member.job_title }}
            </n-tag>
            
            <n-tag
              v-if="member.student_type && member.grade"
              size="small"
              type="info"
            >
              {{ $t(`member.${member.student_type}`) }} {{ member.grade }}
            </n-tag>
            
            <span v-if="member.bio" class="member-bio">
              {{ member.bio.substring(0, 100) }}...
            </span>
          </n-space>
        </div>
        
        <template #action>
          <n-space>
            <n-button
              v-if="member.email"
              text
              @click="window.open(`mailto:${member.email}`)"
            >
              <template #icon>
                <n-icon :component="EmailOutlined" />
              </template>
            </n-button>
            
            <n-button
              v-if="member.personal_page"
              text
              @click="window.open(member.personal_page, '_blank')"
            >
              <template #icon>
                <n-icon :component="LinkOutlined" />
              </template>
            </n-button>
          </n-space>
        </template>
      </n-card>
    </n-grid-item>
  </n-grid>
  
  <n-empty v-if="!members.length" :description="$t('common.noData')" />
</template>

<script setup lang="ts">
import { EmailOutlined, LinkOutlined } from '@vicons/material'
import type { Member } from '@/types'

interface Props {
  members: Member[]
}

defineProps<Props>()
</script>

<style scoped>
.member-card {
  text-align: center;
  height: 280px;
}

.member-avatar {
  margin-bottom: 16px;
}

.member-info h3 {
  margin: 8px 0;
  font-size: 16px;
  font-weight: 600;
}

.member-bio {
  font-size: 12px;
  color: #666;
  line-height: 1.4;
  display: block;
}
</style>