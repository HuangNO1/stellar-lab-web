<template>
  <div class="member-management-table">
    <n-data-table
      :columns="columns"
      :data="members"
      :pagination="false"
    />
  </div>
</template>

<script setup lang="ts">
import { h } from 'vue'
import { NButton, NSpace, NTag } from 'naive-ui'
import { useI18n } from 'vue-i18n'
import type { Member } from '@/types'

defineProps<{
  members: Member[]
}>()

const emit = defineEmits<{
  edit: [member: Member]
  delete: [member: Member]
}>()

const { t } = useI18n()

const columns = [
  {
    title: '姓名',
    key: 'mem_name_zh'
  },
  {
    title: '類型',
    key: 'mem_type',
    render: (row: Member) => {
      const types = ['教師', '學生', '校友']
      return h(NTag, {}, { default: () => types[row.mem_type] || '未知' })
    }
  },
  {
    title: '操作',
    key: 'actions',
    render: (row: Member) => {
      return h(NSpace, {}, {
        default: () => [
          h(NButton, {
            size: 'small',
            onClick: () => emit('edit', row)
          }, { default: () => t('common.edit') }),
          h(NButton, {
            size: 'small',
            type: 'error',
            onClick: () => emit('delete', row)
          }, { default: () => t('common.delete') })
        ]
      })
    }
  }
]
</script>