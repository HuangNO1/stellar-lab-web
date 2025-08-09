<template>
  <div class="member-management">
    <n-card>
      <template #header>
        <n-space justify="space-between" align="center">
          <h2>{{ $t('admin.memberManagement') }}</h2>
          <n-button type="primary" @click="showAddModal = true">
            {{ $t('common.add') }}{{ $t('nav.members') }}
          </n-button>
        </n-space>
      </template>

      <n-space vertical size="large">
        <!-- 搜索和筛选 -->
        <n-space>
          <n-input
            v-model:value="searchQuery"
            :placeholder="$t('common.search')"
            clearable
            style="width: 300px"
          >
            <template #prefix>
              <n-icon :component="SearchOutlined" />
            </template>
          </n-input>
          
          <n-select
            v-model:value="filterType"
            :options="memberTypeOptions"
            :placeholder="$t('member.memberType')"
            clearable
            style="width: 150px"
          />
        </n-space>

        <!-- 拖拽成员管理 -->
        <div class="drag-container">
          <h3>{{ $t('member.dragToChange') }}</h3>
          <p style="color: #666; margin-bottom: 16px;">
            拖拽學生卡片到不同年級分組來修改他們的年級
          </p>
          
          <n-grid :cols="5" :x-gap="16" :y-gap="16">
            <n-grid-item v-for="grade in grades" :key="grade.key">
              <n-card 
                class="grade-column"
                :class="{ 'drag-over': dragOverGrade === grade.key }"
                @drop="handleDrop($event, grade.key)"
                @dragover.prevent="dragOverGrade = grade.key"
                @dragleave="dragOverGrade = null"
              >
                <template #header>
                  <n-space align="center">
                    <n-tag :type="grade.color">
                      {{ grade.label }}
                    </n-tag>
                    <n-badge :value="getStudentsByGrade(grade.key).length" />
                  </n-space>
                </template>
                
                <VueDraggable
                  v-model="gradedStudents[grade.key]"
                  :animation="300"
                  group="students"
                  @start="onDragStart"
                  @end="onDragEnd"
                  class="draggable-area"
                >
                  <div
                    v-for="student in getStudentsByGrade(grade.key)"
                    :key="student.id"
                    class="student-card"
                    :draggable="true"
                  >
                    <n-card size="small" hoverable class="student-card-inner">
                      <n-space size="small" align="center">
                        <n-avatar :size="32" :src="student.avatar_url" round>
                          {{ student.name.charAt(0) }}
                        </n-avatar>
                        <div>
                          <div class="student-name">{{ student.name }}</div>
                          <div class="student-type">
                            {{ $t(`member.${student.student_type}`) }}
                          </div>
                        </div>
                      </n-space>
                      
                      <template #action>
                        <n-space>
                          <n-button size="tiny" @click="editStudent(student)">
                            <template #icon>
                              <n-icon :component="EditOutlined" />
                            </template>
                          </n-button>
                          <n-button 
                            size="tiny" 
                            type="error" 
                            @click="deleteStudent(student)"
                          >
                            <template #icon>
                              <n-icon :component="DeleteOutlined" />
                            </template>
                          </n-button>
                        </n-space>
                      </template>
                    </n-card>
                  </div>
                </VueDraggable>
              </n-card>
            </n-grid-item>
          </n-grid>
        </div>

        <!-- 教師和校友 -->
        <n-card title="教師">
          <MemberManagementTable 
            :members="teacherMembers"
            @edit="editMember"
            @delete="deleteMember"
          />
        </n-card>

        <n-card title="校友">
          <MemberManagementTable 
            :members="alumniMembers"
            @edit="editMember"
            @delete="deleteMember"
          />
        </n-card>
      </n-space>
    </n-card>

    <!-- Add/Edit Modal -->
    <MemberEditModal
      v-model:show="showAddModal"
      :member="editingMember"
      @save="saveMember"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
import { VueDraggable } from 'vue-draggable-plus'
import { SearchOutlined, EditOutlined, DeleteOutlined } from '@vicons/material'
import type { Member } from '@/types'
import { memberAPI } from '@/utils/api'
import MemberManagementTable from '@/components/admin/MemberManagementTable.vue'
import MemberEditModal from '@/components/admin/MemberEditModal.vue'

const message = useMessage()
const members = ref<Member[]>([])
const searchQuery = ref('')
const filterType = ref<string | null>(null)
const showAddModal = ref(false)
const editingMember = ref<Member | null>(null)
const dragOverGrade = ref<string | null>(null)

const grades = [
  { key: 'year1', label: '一年級', color: 'success' },
  { key: 'year2', label: '二年級', color: 'info' },
  { key: 'year3', label: '三年級', color: 'warning' },
  { key: 'year4', label: '四年級', color: 'error' },
  { key: 'year5', label: '五年級', color: 'default' }
]

const memberTypeOptions = [
  { label: '教師', value: 'teacher' },
  { label: '學生', value: 'student' },
  { label: '校友', value: 'alumni' }
]

const filteredMembers = computed(() => {
  let filtered = members.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(member => 
      member.name.toLowerCase().includes(query) ||
      member.job_title?.toLowerCase().includes(query)
    )
  }
  
  if (filterType.value) {
    filtered = filtered.filter(m => m.member_type === filterType.value)
  }
  
  return filtered
})

const studentMembers = computed(() => 
  filteredMembers.value.filter(m => m.member_type === 'student')
)

const teacherMembers = computed(() => 
  filteredMembers.value.filter(m => m.member_type === 'teacher')
)

const alumniMembers = computed(() => 
  filteredMembers.value.filter(m => m.member_type === 'alumni')
)

const gradedStudents = computed(() => {
  const grouped = {
    year1: [],
    year2: [],
    year3: [],
    year4: [],
    year5: []
  }
  
  studentMembers.value.forEach(student => {
    const grade = student.grade || 'year1'
    if (grouped[grade]) {
      grouped[grade].push(student)
    }
  })
  
  return grouped
})

const getStudentsByGrade = (grade: string) => {
  return studentMembers.value.filter(s => s.grade === grade)
}

const handleDrop = async (event: DragEvent, targetGrade: string) => {
  event.preventDefault()
  dragOverGrade.value = null
  
  const studentId = event.dataTransfer?.getData('text/plain')
  if (!studentId) return
  
  const student = members.value.find(m => m.id === parseInt(studentId))
  if (!student) return
  
  try {
    await memberAPI.updateMember(student.id, { grade: targetGrade })
    student.grade = targetGrade
    message.success(`已將 ${student.name} 移至 ${grades.find(g => g.key === targetGrade)?.label}`)
  } catch (error) {
    message.error('更新失敗')
  }
}

const onDragStart = (event: any) => {
  event.dataTransfer.setData('text/plain', event.item.id)
}

const onDragEnd = () => {
  dragOverGrade.value = null
}

const editStudent = (student: Member) => {
  editingMember.value = student
  showAddModal.value = true
}

const editMember = (member: Member) => {
  editingMember.value = member
  showAddModal.value = true
}

const deleteStudent = async (student: Member) => {
  try {
    await memberAPI.deleteMember(student.id)
    members.value = members.value.filter(m => m.id !== student.id)
    message.success('刪除成功')
  } catch (error) {
    message.error('刪除失敗')
  }
}

const deleteMember = deleteStudent

const saveMember = async (memberData: Partial<Member>) => {
  try {
    let savedMember: Member
    if (editingMember.value) {
      savedMember = await memberAPI.updateMember(editingMember.value.id, memberData)
      const index = members.value.findIndex(m => m.id === editingMember.value!.id)
      if (index !== -1) {
        members.value[index] = savedMember
      }
    } else {
      savedMember = await memberAPI.createMember(memberData)
      members.value.push(savedMember)
    }
    
    showAddModal.value = false
    editingMember.value = null
    message.success('保存成功')
  } catch (error) {
    message.error('保存失敗')
  }
}

const loadMembers = async () => {
  try {
    const response = await memberAPI.getMembers({ page: 1, limit: 1000 })
    members.value = response.data
  } catch (error) {
    message.error('加載成員失敗')
  }
}

onMounted(() => {
  loadMembers()
})
</script>

<style scoped>
.grade-column {
  min-height: 300px;
  transition: all 0.3s ease;
}

.grade-column.drag-over {
  border: 2px dashed #18a058;
  background-color: #f0f9ff;
}

.draggable-area {
  min-height: 200px;
  padding: 8px;
}

.student-card {
  margin-bottom: 8px;
  cursor: grab;
}

.student-card:active {
  cursor: grabbing;
}

.student-card-inner {
  transition: all 0.2s ease;
}

.student-card-inner:hover {
  transform: translateY(-2px);
}

.student-name {
  font-weight: 500;
  font-size: 12px;
}

.student-type {
  font-size: 10px;
  color: #666;
}

.drag-container {
  background: #fafafa;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}
</style>