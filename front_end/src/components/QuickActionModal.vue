<template>
  <n-modal v-model:show="show" @update:show="handleModalClose" class="quick-action-modal">
    <n-card
      :style="{ width: isMobile ? '95vw' : '800px', maxWidth: isMobile ? '95vw' : '800px' }"
      :title="modalTitle"
      :bordered="false"
      :size="isMobile ? 'medium' : 'huge'"
      role="dialog"
      aria-modal="true"
      class="modal-card"
    >
      <template #header-extra>
        <n-button
          quaternary
          circle
          @click="show = false"
        >
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
              </svg>
            </n-icon>
          </template>
        </n-button>
      </template>

      <n-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        :label-placement="isMobile ? 'top' : 'left'"
        :label-width="isMobile ? 'auto' : '120'"
        require-mark-placement="right-hanging"
        class="modal-form"
      >
        <!-- 成員表單 -->
        <template v-if="moduleType === 'members'">
          <n-form-item :label="t('admin.members.form.nameZh')" path="mem_name_zh">
            <n-input
              v-model:value="formData.mem_name_zh"
              :placeholder="t('admin.members.form.placeholders.nameZh')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.nameEn')" path="mem_name_en">
            <n-input
              v-model:value="formData.mem_name_en"
              :placeholder="t('admin.members.form.placeholders.nameEn')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.email')" path="mem_email">
            <n-input
              v-model:value="formData.mem_email"
              :placeholder="t('admin.members.form.placeholders.email')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.type')" path="mem_type">
            <n-select
              v-model:value="formData.mem_type"
              :options="memberTypeOptions"
              :placeholder="t('admin.members.form.placeholders.type')"
              style="width: 100%"
            />
          </n-form-item>
          
          <!-- 教師職務類型 -->
          <n-form-item 
            v-if="formData.mem_type === 0" 
            :label="t('admin.members.form.jobType')" 
            path="job_type"
          >
            <n-select
              v-model:value="formData.job_type"
              :options="jobTypeOptions"
              :placeholder="t('admin.members.form.placeholders.jobType')"
              style="width: 100%"
            />
          </n-form-item>
          
          <!-- 學生類型和年級 -->
          <template v-if="formData.mem_type === 1">
            <n-form-item :label="t('admin.members.form.studentType')" path="student_type">
              <n-select
                v-model:value="formData.student_type"
                :options="studentTypeOptions"
                :placeholder="t('admin.members.form.placeholders.studentType')"
                style="width: 100%"
              />
            </n-form-item>
            <n-form-item :label="t('admin.members.form.studentGrade')" path="student_grade">
              <n-input-number
                v-model:value="formData.student_grade"
                :placeholder="t('admin.members.form.placeholders.studentGrade')"
                :min="1"
                :max="10"
                style="width: 100%"
              />
            </n-form-item>
          </template>
          
          <!-- 校友去向 -->
          <template v-if="formData.mem_type === 2">
            <n-form-item :label="t('admin.members.form.destinationZh')" path="destination_zh">
              <n-input
                v-model:value="formData.destination_zh"
                :placeholder="t('admin.members.form.placeholders.destinationZh')"
                style="width: 100%"
              />
            </n-form-item>
            <n-form-item :label="t('admin.members.form.destinationEn')" path="destination_en">
              <n-input
                v-model:value="formData.destination_en"
                :placeholder="t('admin.members.form.placeholders.destinationEn')"
                style="width: 100%"
              />
            </n-form-item>
          </template>
          
          <n-form-item :label="t('admin.members.form.group')" path="research_group_id">
            <n-select
              v-model:value="formData.research_group_id"
              :options="researchGroupOptions"
              :placeholder="t('admin.members.form.placeholders.group')"
              :loading="loadingGroups"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.description')" path="mem_desc_zh">
            <I18nMdEditor
              v-model="formData.mem_desc_zh"
              :placeholder="t('admin.members.form.placeholders.description')"
              style="height: 200px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.avatar')" path="mem_avatar">
            <n-upload
              :default-file-list="getDefaultFileList('mem_avatar')"
              :max="1"
              accept="image/*"
              @change="handleFileChange('mem_avatar', $event)"
              @remove="handleFileRemove('mem_avatar')"
            >
              <n-button>{{ t('admin.common.fileUpload.selectImage') }}</n-button>
            </n-upload>
          </n-form-item>
        </template>

        <!-- 論文表單 -->
        <template v-if="moduleType === 'papers'">
          <n-form-item :label="t('admin.papers.form.titleZh')" path="paper_title_zh">
            <n-input
              v-model:value="formData.paper_title_zh"
              :placeholder="t('admin.papers.form.placeholders.titleZh')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.titleEn')" path="paper_title_en">
            <n-input
              v-model:value="formData.paper_title_en"
              :placeholder="t('admin.papers.form.placeholders.titleEn')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.description')" path="paper_desc_zh">
            <I18nMdEditor
              v-model="formData.paper_desc_zh"
              :placeholder="t('admin.papers.form.placeholders.description')"
              style="height: 200px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.authors')" path="authors">
            <n-select
              v-model:value="formData.authors"
              multiple
              filterable
              :options="memberOptions"
              :placeholder="t('admin.papers.form.placeholders.authors')"
              :loading="loadingMembers"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.venue')" path="paper_venue">
            <n-input
              v-model:value="formData.paper_venue"
              :placeholder="t('admin.papers.form.placeholders.venue')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.type')" path="paper_type">
            <n-select
              v-model:value="formData.paper_type"
              :options="paperTypeOptions"
              :placeholder="t('admin.papers.form.placeholders.type')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.date')" path="paper_date">
            <n-date-picker
              v-model:value="formData.paper_date"
              type="date"
              :placeholder="t('admin.papers.form.placeholders.date')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.status')" path="paper_accept">
            <n-select
              v-model:value="formData.paper_accept"
              :options="paperAcceptOptions"
              :placeholder="t('admin.papers.form.placeholders.status')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.file')" path="paper_file">
            <n-upload
              :default-file-list="getDefaultFileList('paper_file')"
              :max="1"
              accept=".pdf"
              @change="handleFileChange('paper_file', $event)"
              @remove="handleFileRemove('paper_file')"
            >
              <n-button>{{ t('admin.common.fileUpload.selectPdf') }}</n-button>
            </n-upload>
          </n-form-item>
        </template>

        <!-- 項目表單 -->
        <template v-if="moduleType === 'projects'">
          <n-form-item :label="t('admin.projects.form.nameZh')" path="project_name_zh">
            <n-input
              v-model:value="formData.project_name_zh"
              :placeholder="t('admin.projects.form.placeholders.nameZh')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.nameEn')" path="project_name_en">
            <n-input
              v-model:value="formData.project_name_en"
              :placeholder="t('admin.projects.form.placeholders.nameEn')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.description')" path="project_desc_zh">
            <I18nMdEditor
              v-model="formData.project_desc_zh"
              :placeholder="t('admin.projects.form.placeholders.description')"
              style="height: 200px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.url')" path="project_url">
            <n-input
              v-model:value="formData.project_url"
              :placeholder="t('admin.projects.form.placeholders.url')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.startDate')" path="project_date_start">
            <n-date-picker
              v-model:value="formData.project_date_start"
              type="date"
              :placeholder="t('admin.projects.form.placeholders.startDate')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.status')" path="is_end">
            <n-select
              v-model:value="formData.is_end"
              :options="projectStatusOptions"
              :placeholder="t('admin.projects.form.placeholders.status')"
              style="width: 100%"
            />
          </n-form-item>
        </template>

        <!-- 新聞表單 -->
        <template v-if="moduleType === 'news'">
          <n-form-item :label="t('admin.news.form.type')" path="news_type">
            <n-select
              v-model:value="formData.news_type"
              :options="newsTypeOptions"
              :placeholder="t('admin.news.form.placeholders.type')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.news.form.contentZh')" path="news_content_zh">
            <I18nMdEditor
              v-model="formData.news_content_zh"
              :placeholder="t('admin.news.form.placeholders.contentZh')"
              style="height: 200px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.news.form.contentEn')" path="news_content_en">
            <I18nMdEditor
              v-model="formData.news_content_en"
              :placeholder="t('admin.news.form.placeholders.contentEn')"
              style="height: 200px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.news.form.date')" path="news_date">
            <n-date-picker
              v-model:value="formData.news_date"
              type="date"
              :placeholder="t('admin.news.form.placeholders.date')"
              style="width: 100%"
            />
          </n-form-item>
        </template>

        <!-- 課題組表單 -->
        <template v-if="moduleType === 'research-groups'">
          <n-form-item :label="t('admin.groups.form.nameZh')" path="research_group_name_zh">
            <n-input
              v-model:value="formData.research_group_name_zh"
              :placeholder="t('admin.groups.form.placeholders.nameZh')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.groups.form.nameEn')" path="research_group_name_en">
            <n-input
              v-model:value="formData.research_group_name_en"
              :placeholder="t('admin.groups.form.placeholders.nameEn')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.groups.form.descriptionZh')" path="research_group_desc_zh">
            <I18nMdEditor
              v-model="formData.research_group_desc_zh"
              :placeholder="t('admin.groups.form.placeholders.descriptionZh')"
              style="height: 200px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.groups.form.descriptionEn')" path="research_group_desc_en">
            <I18nMdEditor
              v-model="formData.research_group_desc_en"
              :placeholder="t('admin.groups.form.placeholders.descriptionEn')"
              style="height: 200px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.groups.form.leader')" path="mem_id">
            <n-select
              v-model:value="formData.mem_id"
              :options="memberOptions"
              :placeholder="t('admin.groups.form.placeholders.leader')"
              :loading="loadingMembers"
              style="width: 100%"
            />
          </n-form-item>
        </template>

        <!-- 管理員表單 -->
        <template v-if="moduleType === 'admins'">
          <n-form-item :label="t('admin.admins.form.adminName')" path="admin_name">
            <n-input
              v-model:value="formData.admin_name"
              :placeholder="t('admin.admins.form.placeholders.adminName')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item v-if="actionType === 'create'" :label="t('admin.admins.form.adminPass')" path="admin_pass">
            <n-input
              v-model:value="formData.admin_pass"
              type="password"
              :placeholder="t('admin.admins.form.placeholders.adminPass')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.admins.form.isSuper')" path="is_super">
            <n-select
              v-model:value="formData.is_super"
              :options="adminTypeOptions"
              :placeholder="t('admin.admins.form.placeholders.isSuper')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item v-if="actionType === 'edit'" :label="t('admin.admins.form.enable')" path="enable">
            <n-select
              v-model:value="formData.enable"
              :options="enableOptions"
              :placeholder="t('admin.admins.form.placeholders.enable')"
              style="width: 100%"
            />
          </n-form-item>
        </template>
      </n-form>

      <template #footer>
        <div class="modal-footer">
          <n-button @click="show = false">
            {{ t('admin.common.cancel') }}
          </n-button>
          <n-button
            type="primary"
            :loading="submitting"
            @click="handleSubmit"
          >
            {{ actionType === 'create' ? t('admin.common.create') : t('admin.common.update') }}
          </n-button>
        </div>
      </template>
    </n-card>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, nextTick, onMounted, onUnmounted } from 'vue';
import { useMessage } from 'naive-ui';
import { useI18n } from 'vue-i18n';
import { useAuthStore } from '@/stores/auth';
import { memberApi, paperApi, projectApi, newsApi, researchGroupApi, adminApi } from '@/services/api';
import I18nMdEditor from '@/components/I18nMdEditor.vue';

const { t, locale } = useI18n();
const authStore = useAuthStore();

// Props
interface Props {
  modelValue: boolean;
  moduleType: 'members' | 'papers' | 'projects' | 'news' | 'research-groups' | 'admins';
  actionType: 'create' | 'edit';
  editData?: Record<string, any>;
}

const props = withDefaults(defineProps<Props>(), {
  editData: () => ({})
});

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: boolean];
  'success': [data: any];
}>();

// Reactive data
const show = ref(props.modelValue);
const formRef = ref();
const submitting = ref(false);
const message = useMessage();
const isMobile = ref(window.innerWidth <= 768);

// Loading states
const loadingGroups = ref(false);
const loadingMembers = ref(false);

// Form data
const formData = reactive<Record<string, any>>({});
const uploadedFiles = reactive<Record<string, File>>({});

// Options
const memberTypeOptions = computed(() => [
  { label: t('admin.common.memberTypes.teacher'), value: 0 },
  { label: t('admin.common.memberTypes.student'), value: 1 },
  { label: t('admin.common.memberTypes.alumni'), value: 2 }
]);

// 教師職務類型選項
const jobTypeOptions = computed(() => [
  { label: t('admin.common.jobTypes.professor'), value: 0 },
  { label: t('admin.common.jobTypes.associateProfessor'), value: 1 },
  { label: t('admin.common.jobTypes.lecturer'), value: 2 },
  { label: t('admin.common.jobTypes.assistantResearcher'), value: 3 },
  { label: t('admin.common.jobTypes.postdoc'), value: 4 }
]);

// 學生類型選項
const studentTypeOptions = computed(() => [
  { label: t('admin.common.studentTypes.phd'), value: 0 },
  { label: t('admin.common.studentTypes.master'), value: 1 },
  { label: t('admin.common.studentTypes.undergraduate'), value: 2 }
]);

const paperTypeOptions = computed(() => [
  { label: t('admin.common.paperTypes.conference'), value: 0 },
  { label: t('admin.common.paperTypes.journal'), value: 1 },
  { label: t('admin.common.paperTypes.patent'), value: 2 },
  { label: t('admin.common.paperTypes.book'), value: 3 },
  { label: t('admin.common.paperTypes.other'), value: 4 }
]);

const paperAcceptOptions = computed(() => [
  { label: t('admin.common.paperStatus.submitting'), value: 0 },
  { label: t('admin.common.paperStatus.accepted'), value: 1 }
]);

const projectStatusOptions = computed(() => [
  { label: t('admin.common.projectStatus.ongoing'), value: 0 },
  { label: t('admin.common.projectStatus.completed'), value: 1 }
]);

const newsTypeOptions = computed(() => [
  { label: t('admin.common.newsTypes.publication'), value: 0 },
  { label: t('admin.common.newsTypes.award'), value: 1 },
  { label: t('admin.common.newsTypes.activity'), value: 2 }
]);

const adminTypeOptions = computed(() => [
  { label: t('admin.admins.normalAdmin'), value: 0 },
  { label: t('admin.admins.superAdmin'), value: 1 }
]);

const enableOptions = computed(() => [
  { label: t('admin.common.disabled'), value: 0 },
  { label: t('admin.common.enabled'), value: 1 }
]);

const researchGroupOptions = ref<Array<{ label: string; value: number }>>([]);
const memberOptions = ref<Array<{ label: string; value: number }>>([]);

// Computed
const modalTitle = computed(() => {
  // Map module types to correct title keys
  const moduleKeyMap: Record<string, string> = {
    'members': 'Member',
    'papers': 'Paper', 
    'projects': 'Project',
    'news': 'News',
    'research-groups': 'Group',
    'admins': 'Admin'
  };
  
  const actionKey = props.actionType === 'create' ? 'create' : 'edit';
  const moduleKey = moduleKeyMap[props.moduleType] || 'Member';
  
  return t(`admin.quickAction.modalTitle.${actionKey}${moduleKey}`);
});

// Form rules
const formRules = computed(() => {
  const rules: Record<string, any> = {};
  
  if (props.moduleType === 'members') {
    rules.mem_name_zh = { required: true, message: t('admin.members.form.validation.nameZhRequired'), trigger: 'blur' };
    rules.mem_name_en = { required: true, message: t('admin.members.form.validation.nameEnRequired'), trigger: 'blur' };
    rules.mem_email = { required: true, message: t('admin.members.form.validation.emailRequired'), trigger: 'blur' };
    rules.mem_type = { required: true, message: t('admin.members.form.validation.typeRequired'), trigger: 'change' };
    rules.research_group_id = { required: true, message: t('admin.members.form.validation.groupRequired'), trigger: 'change' };
  } else if (props.moduleType === 'papers') {
    rules.paper_title_zh = { required: true, message: t('admin.papers.form.validation.titleZhRequired'), trigger: 'blur' };
    rules.paper_type = { required: true, message: t('admin.papers.form.validation.typeRequired'), trigger: 'change' };
    rules.paper_accept = { required: true, message: t('admin.papers.form.validation.statusRequired'), trigger: 'change' };
    rules.paper_date = { required: true, message: t('admin.papers.form.validation.dateRequired'), trigger: 'change' };
  } else if (props.moduleType === 'projects') {
    rules.project_name_zh = { required: true, message: t('admin.projects.form.validation.nameZhRequired'), trigger: 'blur' };
  } else if (props.moduleType === 'news') {
    rules.news_type = { required: true, message: t('admin.news.form.validation.typeRequired'), trigger: 'change' };
    rules.news_content_zh = { required: true, message: t('admin.news.form.validation.contentZhRequired'), trigger: 'blur' };
    rules.news_date = { required: true, message: t('admin.news.form.validation.dateRequired'), trigger: 'change' };
  } else if (props.moduleType === 'research-groups') {
    rules.research_group_name_zh = { required: true, message: t('admin.groups.form.validation.nameZhRequired'), trigger: 'blur' };
  } else if (props.moduleType === 'admins') {
    rules.admin_name = { required: true, message: t('admin.admins.form.validation.adminNameRequired'), trigger: 'blur' };
    if (props.actionType === 'create') {
      rules.admin_pass = { required: true, message: t('admin.admins.form.validation.adminPassRequired'), trigger: 'blur' };
    }
  }
  
  return rules;
});

// Watchers
watch(
  () => props.modelValue,
  (newValue) => {
    show.value = newValue;
    if (newValue) {
      resetForm();
      loadOptionsData();
      if (props.actionType === 'edit' && props.editData) {
        nextTick(() => {
          const editDataCopy = { ...props.editData };
          
          // 轉換日期字段為時間戳
          if (editDataCopy.paper_date) {
            editDataCopy.paper_date = parseDateForForm(editDataCopy.paper_date);
          }
          if (editDataCopy.news_date) {
            editDataCopy.news_date = parseDateForForm(editDataCopy.news_date);
          }
          if (editDataCopy.project_date_start) {
            editDataCopy.project_date_start = parseDateForForm(editDataCopy.project_date_start);
          }
          
          // 處理論文作者數據：將authors對象數組轉換為mem_id數組
          if (props.moduleType === 'papers' && editDataCopy.authors && Array.isArray(editDataCopy.authors)) {
            editDataCopy.authors = editDataCopy.authors.map((author: any) => author.mem_id);
            console.log('轉換後的作者ID數組:', editDataCopy.authors);
          }
          
          Object.assign(formData, editDataCopy);
        });
      }
    }
  }
);

watch(show, (newValue) => {
  emit('update:modelValue', newValue);
});

// Watch locale changes to reload options with correct language
watch(locale, () => {
  if (show.value) {
    loadOptionsData();
  }
});

// 檢查屏幕尺寸
const checkScreenSize = () => {
  isMobile.value = window.innerWidth <= 768;
};

// 監聽窗口大小變化
onMounted(() => {
  window.addEventListener('resize', checkScreenSize);
  checkScreenSize();
});

onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize);
});

// Methods
const resetForm = () => {
  Object.keys(formData).forEach(key => {
    delete formData[key];
  });
  Object.keys(uploadedFiles).forEach(key => {
    delete uploadedFiles[key];
  });
  formRef.value?.restoreValidation();
};

const handleModalClose = (value: boolean) => {
  if (!value) {
    resetForm();
  }
};

const loadOptionsData = async () => {
  if (props.moduleType === 'members' || props.moduleType === 'research-groups') {
    await loadResearchGroups();
  }
  if (props.moduleType === 'papers' || props.moduleType === 'research-groups') {
    await loadMembers();
  }
};

const loadResearchGroups = async () => {
  try {
    loadingGroups.value = true;
    const response = await researchGroupApi.getResearchGroups({ all: 'true' });
    if (response.code === 0) {
      researchGroupOptions.value = response.data.items.map((group: any) => ({
        label: locale.value === 'zh' 
          ? (group.research_group_name_zh || group.research_group_name_en)
          : (group.research_group_name_en || group.research_group_name_zh),
        value: group.research_group_id
      }));
    }
  } catch (error) {
    console.error(t('admin.quickAction.messages.loadGroupsFailed'), error);
  } finally {
    loadingGroups.value = false;
  }
};

const loadMembers = async () => {
  try {
    loadingMembers.value = true;
    
    // 獲取所有類型的成員，包括教師、學生、校友
    const response = await memberApi.getMembers({ all: 'true' });
    
    if (response.code === 0) {
      memberOptions.value = response.data.items.map((member: any) => {
        const name = locale.value === 'zh'
          ? (member.mem_name_zh || member.mem_name_en)
          : (member.mem_name_en || member.mem_name_zh);
        
        // 獲取成員類型標籤
        const memberTypeLabels = {
          0: t('admin.common.memberTypes.teacher'),
          1: t('admin.common.memberTypes.student'),
          2: t('admin.common.memberTypes.alumni')
        };
        const typeLabel = memberTypeLabels[member.mem_type as keyof typeof memberTypeLabels] || '';
        
        return {
          label: `${name} (${member.mem_email}) - ${typeLabel}`,
          value: member.mem_id
        };
      });
      console.log(`成功加載 ${memberOptions.value.length} 個成員選項`);
    } else {
      console.error('API 響應錯誤:', response.message);
    }
  } catch (error) {
    console.error('加載成員失敗:', error);
  } finally {
    loadingMembers.value = false;
  }
};

const formatDateForApi = (date: any) => {
  if (!date) return '';
  const d = new Date(date);
  return d.toISOString().split('T')[0];
};

// 將字符串日期轉換為時間戳（用於日期選擇器）
const parseDateForForm = (dateString: string): number | null => {
  if (!dateString) return null;
  const date = new Date(dateString);
  return isNaN(date.getTime()) ? null : date.getTime();
};

// 文件處理方法
const getDefaultFileList = (fieldName: string) => {
  if (props.actionType === 'edit' && props.editData) {
    const filePath = props.editData[`${fieldName}_path`];
    if (filePath) {
      return [{
        id: fieldName,
        name: filePath.split('/').pop() || 'file',
        status: 'finished',
        url: `${process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.1:8000'}/api/media/serve/${filePath.replace('/media/', '')}`
      }];
    }
  }
  return [];
};

const handleFileChange = (fieldName: string, { fileList }: { fileList: any[] }) => {
  if (fileList.length > 0) {
    const file = fileList[0].file;
    if (file) {
      uploadedFiles[fieldName] = file;
    }
  } else {
    delete uploadedFiles[fieldName];
  }
};

const handleFileRemove = (fieldName: string) => {
  delete uploadedFiles[fieldName];
};

const handleSubmit = async () => {
  try {
    // 對於管理員操作，檢查權限
    if (props.moduleType === 'admins') {
      // 編輯管理員時，檢查是否為超級管理員且不是編輯其他超級管理員
      if (props.actionType === 'edit') {
        if (!authStore.isSuperAdmin) {
          message.error(t('admin.admins.noEditPermission'));
          return;
        }
        
        // 不能編輯自己
        if (formData.admin_id === authStore.admin?.admin_id) {
          message.error(t('admin.admins.cannotEditSelf'));
          return;
        }
        
        // 不能編輯其他超級管理員
        if (props.editData?.is_super === 1) {
          message.error(t('admin.admins.cannotEditSuperAdmin'));
          return;
        }
      }
      
      // 創建管理員時，檢查是否為超級管理員
      if (props.actionType === 'create' && !authStore.isSuperAdmin) {
        message.error(t('admin.admins.noCreatePermission'));
        return;
      }
    }

    await formRef.value?.validate();
    submitting.value = true;

    // 準備提交數據
    let submitData: any;
    const hasFiles = Object.keys(uploadedFiles).length > 0;
    
    if (hasFiles) {
      // 使用 FormData 處理文件上傳
      submitData = new FormData();
      
      // 添加表單字段
      Object.keys(formData).forEach(key => {
        let value = formData[key];
        
        // 格式化日期字段
        if (key.includes('date') && value) {
          value = formatDateForApi(value);
        }
        
        if (value !== null && value !== undefined && value !== '') {
          submitData.append(key, value);
        }
      });
      
      // 添加文件
      Object.keys(uploadedFiles).forEach(key => {
        submitData.append(key, uploadedFiles[key]);
      });
      
    } else {
      // 普通 JSON 提交
      submitData = { ...formData };
      
      // 格式化日期欄位
      if (submitData.paper_date) {
        submitData.paper_date = formatDateForApi(submitData.paper_date);
      }
      if (submitData.news_date) {
        submitData.news_date = formatDateForApi(submitData.news_date);
      }
      if (submitData.project_date_start) {
        submitData.project_date_start = formatDateForApi(submitData.project_date_start);
      }
    }

    let response;
    const apis = {
      members: memberApi,
      papers: paperApi,
      projects: projectApi,
      news: newsApi,
      'research-groups': researchGroupApi,
      admins: adminApi
    };

    const api = apis[props.moduleType];
    
    if (props.actionType === 'create') {
      const createMethods = {
        members: 'createMember',
        papers: 'createPaper',
        projects: 'createProject',
        news: 'createNews',
        'research-groups': 'createResearchGroup',
        admins: 'createAdmin'
      };
      response = await (api as any)[createMethods[props.moduleType]](submitData);
    } else {
      const updateMethods = {
        members: 'updateMember',
        papers: 'updatePaper',
        projects: 'updateProject',
        news: 'updateNews',
        'research-groups': 'updateResearchGroup',
        admins: 'updateAdmin'
      };
      const idField = {
        members: 'mem_id',
        papers: 'paper_id',
        projects: 'project_id',
        news: 'news_id',
        'research-groups': 'research_group_id',
        admins: 'admin_id'
      };
      const id = props.editData[idField[props.moduleType]];
      response = await (api as any)[updateMethods[props.moduleType]](id, submitData);
    }

    if (response.code === 0) {
      const successMessage = props.actionType === 'create' 
        ? t('admin.quickAction.messages.createSuccess')
        : t('admin.quickAction.messages.updateSuccess');
      message.success(successMessage);
      emit('success', response.data);
      show.value = false;
    } else {
      message.error(response.message || t('admin.quickAction.messages.operationFailed'));
    }
  } catch (error: any) {
    if (error?.message) {
      message.error(error.message);
    } else {
      message.error(t('admin.quickAction.messages.checkInput'));
    }
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.quick-action-modal :deep(.n-modal) {
  padding: 1rem;
}

.modal-card {
  margin: 0 auto;
}

.modal-form {
  max-height: 70vh;
  overflow-y: auto;
  padding-right: 8px;
  margin-right: -8px;
}

/* 自定義滾動條樣式 */
.modal-form::-webkit-scrollbar {
  width: 6px;
}

.modal-form::-webkit-scrollbar-track {
  background: transparent;
}

.modal-form::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.modal-form::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 1rem;
}

/* 移動端樣式調整 */
@media (max-width: 768px) {
  .quick-action-modal :deep(.n-modal) {
    padding: 0.5rem;
  }
  
  .modal-card :deep(.n-card__header) {
    padding: 1rem 1rem 0.75rem 1rem;
    font-size: 1.125rem;
  }
  
  .modal-card :deep(.n-card__content) {
    padding: 0.75rem 1rem;
  }
  
  .modal-card :deep(.n-card__footer) {
    padding: 0.75rem 1rem 1rem 1rem;
  }
  
  .modal-form {
    max-height: 60vh;
    padding-right: 6px;
    margin-right: -6px;
  }
  
  .modal-form :deep(.n-form-item) {
    margin-bottom: 1rem;
  }
  
  .modal-form :deep(.n-form-item-label) {
    margin-bottom: 0.5rem;
    font-weight: 500;
  }
  
  .modal-footer {
    flex-direction: column-reverse;
    gap: 0.75rem;
  }
  
  .modal-footer .n-button {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .quick-action-modal :deep(.n-modal) {
    padding: 0.25rem;
  }
  
  .modal-card :deep(.n-card__header) {
    padding: 0.75rem 0.75rem 0.5rem 0.75rem;
  }
  
  .modal-card :deep(.n-card__content) {
    padding: 0.5rem 0.75rem;
  }
  
  .modal-card :deep(.n-card__footer) {
    padding: 0.5rem 0.75rem 0.75rem 0.75rem;
  }
  
  .modal-form {
    max-height: 55vh;
    padding-right: 4px;
    margin-right: -4px;
  }
  
  .modal-form :deep(.n-form-item) {
    margin-bottom: 0.75rem;
  }
}

/* MarkdownEditor 在移動端的調整 */
@media (max-width: 768px) {
  .modal-form :deep(.markdown-editor) {
    min-height: 100px;
  }
  
  .modal-form :deep(.n-input__textarea-el) {
    min-height: 100px !important;
  }
}

/* 上傳組件在移動端的調整 */
@media (max-width: 768px) {
  .modal-form :deep(.n-upload) {
    width: 100%;
  }
  
  .modal-form :deep(.n-upload .n-button) {
    width: 100%;
  }
}
</style>