<template>
  <n-modal v-model:show="visible" preset="dialog" title="編輯成員">
    <template #default>
      <n-form :model="formData" ref="formRef" :rules="rules">
        <n-form-item label="中文姓名" path="mem_name_zh">
          <n-input v-model:value="formData.mem_name_zh" />
        </n-form-item>
        <n-form-item label="英文姓名" path="mem_name_en">
          <n-input v-model:value="formData.mem_name_en" />
        </n-form-item>
        <n-form-item label="成員類型" path="mem_type">
          <n-select v-model:value="formData.mem_type" :options="typeOptions" />
        </n-form-item>
      </n-form>
    </template>
    <template #action>
      <n-space>
        <n-button @click="visible = false">取消</n-button>
        <n-button type="primary" @click="handleSave">保存</n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import type { FormInst, FormRules } from 'naive-ui'
import type { Member } from '@/types'

const props = defineProps<{
  show: boolean
  member: Member | null
}>()

const emit = defineEmits<{
  'update:show': [show: boolean]
  save: [data: Partial<Member>]
}>()

const formRef = ref<FormInst>()
const formData = ref<Partial<Member>>({})

const visible = computed({
  get: () => props.show,
  set: (val) => emit('update:show', val)
})

const typeOptions = [
  { label: '教師', value: 0 },
  { label: '學生', value: 1 },
  { label: '校友', value: 2 }
]

const rules: FormRules = {
  mem_name_zh: {
    required: true,
    message: '請輸入中文姓名',
    trigger: 'blur'
  }
}

const handleSave = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    emit('save', formData.value)
  } catch (error) {
    // 驗證失敗
  }
}

watch(() => props.member, (member) => {
  if (member) {
    formData.value = { ...member }
  } else {
    formData.value = {}
  }
}, { immediate: true })
</script>