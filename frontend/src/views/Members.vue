<template>
  <div class="members-page">
    <n-card>
      <template #header>
        <n-space justify="space-between" align="center">
          <h2>{{ $t('nav.members') }}</h2>
          <n-input
            v-model:value="searchQuery"
            type="text"
            :placeholder="$t('common.search')"
            clearable
            style="width: 300px"
          >
            <template #prefix>
              <n-icon :component="Search" />
            </template>
          </n-input>
        </n-space>
      </template>
      
      <n-tabs v-model:value="activeTab" type="line" animated>
        <n-tab-pane name="all" :tab="$t('common.all')">
          <MemberGrid :members="filteredMembers" />
        </n-tab-pane>
        <n-tab-pane name="teacher" :tab="$t('member.teacher')">
          <MemberGrid :members="teacherMembers" />
        </n-tab-pane>
        <n-tab-pane name="student" :tab="$t('member.student')">
          <MemberGrid :members="studentMembers" />
        </n-tab-pane>
        <n-tab-pane name="alumni" :tab="$t('member.alumni')">
          <MemberGrid :members="alumniMembers" />
        </n-tab-pane>
      </n-tabs>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Search } from '@vicons/ionicons5'
import type { Member } from '@/types'
import { memberAPI } from '@/utils/api'
import MemberGrid from '@/components/MemberGrid.vue'

const members = ref<Member[]>([])
const searchQuery = ref('')
const activeTab = ref('all')

const filteredMembers = computed(() => {
  let filtered = members.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(member => 
      member.name.toLowerCase().includes(query) ||
      member.job_title?.toLowerCase().includes(query) ||
      member.bio?.toLowerCase().includes(query)
    )
  }
  
  return filtered
})

const teacherMembers = computed(() => 
  filteredMembers.value.filter(m => m.member_type === 'teacher')
)

const studentMembers = computed(() => 
  filteredMembers.value.filter(m => m.member_type === 'student')
)

const alumniMembers = computed(() => 
  filteredMembers.value.filter(m => m.member_type === 'alumni')
)

const loadMembers = async () => {
  try {
    const response = await memberAPI.getMembers({ page: 1, limit: 100 })
    members.value = response.data.data
  } catch (error) {
    console.error('Failed to load members:', error)
  }
}

onMounted(() => {
  loadMembers()
})
</script>