<template>
  <n-modal v-model:show="show" @update:show="handleModalClose">
    <n-card
      style="width: 800px"
      :title="modalTitle"
      :bordered="false"
      size="huge"
      role="dialog"
      aria-modal="true"
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
        label-placement="left"
        label-width="120"
        require-mark-placement="right-hanging"
      >
        <!-- 成員表單 -->
        <template v-if="moduleType === 'members'">
          <n-form-item :label="t('admin.members.form.nameZh')" path="mem_name_zh">
            <n-input
              v-model:value="formData.mem_name_zh"
              :placeholder="t('admin.members.form.placeholders.nameZh')"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.nameEn')" path="mem_name_en">
            <n-input
              v-model:value="formData.mem_name_en"
              :placeholder="t('admin.members.form.placeholders.nameEn')"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.email')" path="mem_email">
            <n-input
              v-model:value="formData.mem_email"
              :placeholder="t('admin.members.form.placeholders.email')"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.type')" path="mem_type">
            <n-select
              v-model:value="formData.mem_type"
              :options="memberTypeOptions"
              :placeholder="t('admin.members.form.placeholders.type')"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.group')" path="research_group_id">
            <n-select
              v-model:value="formData.research_group_id"
              :options="researchGroupOptions"
              :placeholder="t('admin.members.form.placeholders.group')"
              :loading="loadingGroups"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.description')" path="mem_desc_zh">
            <MarkdownEditor
              v-model="formData.mem_desc_zh"
              :placeholder="t('admin.members.form.placeholders.description')"
              :rows="3"
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
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.titleEn')" path="paper_title_en">
            <n-input
              v-model:value="formData.paper_title_en"
              :placeholder="t('admin.papers.form.placeholders.titleEn')"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.description')" path="paper_desc_zh">
            <MarkdownEditor
              v-model="formData.paper_desc_zh"
              :placeholder="t('admin.papers.form.placeholders.description')"
              :rows="3"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.venue')" path="paper_venue">
            <n-input
              v-model:value="formData.paper_venue"
              :placeholder="t('admin.papers.form.placeholders.venue')"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.type')" path="paper_type">
            <n-select
              v-model:value="formData.paper_type"
              :options="paperTypeOptions"
              :placeholder="t('admin.papers.form.placeholders.type')"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.date')" path="paper_date">
            <n-date-picker
              v-model:value="formData.paper_date"
              type="date"
              :placeholder="t('admin.papers.form.placeholders.date')"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.status')" path="paper_accept">
            <n-select
              v-model:value="formData.paper_accept"
              :options="paperAcceptOptions"
              :placeholder="t('admin.papers.form.placeholders.status')"
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
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.nameEn')" path="project_name_en">
            <n-input
              v-model:value="formData.project_name_en"
              :placeholder="t('admin.projects.form.placeholders.nameEn')"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.description')" path="project_desc_zh">
            <MarkdownEditor
              v-model="formData.project_desc_zh"
              :placeholder="t('admin.projects.form.placeholders.description')"
              :rows="3"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.url')" path="project_url">
            <n-input
              v-model:value="formData.project_url"
              :placeholder="t('admin.projects.form.placeholders.url')"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.startDate')" path="project_date_start">
            <n-date-picker
              v-model:value="formData.project_date_start"
              type="date"
              :placeholder="t('admin.projects.form.placeholders.startDate')"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.status')" path="is_end">
            <n-select
              v-model:value="formData.is_end"
              :options="projectStatusOptions"
              :placeholder="t('admin.projects.form.placeholders.status')"
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
            />
          </n-form-item>
          <n-form-item :label="t('admin.news.form.contentZh')" path="news_content_zh">
            <MarkdownEditor
              v-model="formData.news_content_zh"
              :placeholder="t('admin.news.form.placeholders.contentZh')"
              :rows="4"
            />
          </n-form-item>
          <n-form-item :label="t('admin.news.form.contentEn')" path="news_content_en">
            <MarkdownEditor
              v-model="formData.news_content_en"
              :placeholder="t('admin.news.form.placeholders.contentEn')"
              :rows="4"
            />
          </n-form-item>
          <n-form-item :label="t('admin.news.form.date')" path="news_date">
            <n-date-picker
              v-model:value="formData.news_date"
              type="date"
              :placeholder="t('admin.news.form.placeholders.date')"
            />
          </n-form-item>
        </template>

        <!-- 課題組表單 -->
        <template v-if="moduleType === 'research-groups'">
          <n-form-item :label="t('admin.groups.form.nameZh')" path="research_group_name_zh">
            <n-input
              v-model:value="formData.research_group_name_zh"
              :placeholder="t('admin.groups.form.placeholders.nameZh')"
            />
          </n-form-item>
          <n-form-item :label="t('admin.groups.form.nameEn')" path="research_group_name_en">
            <n-input
              v-model:value="formData.research_group_name_en"
              :placeholder="t('admin.groups.form.placeholders.nameEn')"
            />
          </n-form-item>
          <n-form-item :label="t('admin.groups.form.descriptionZh')" path="research_group_desc_zh">
            <MarkdownEditor
              v-model="formData.research_group_desc_zh"
              :placeholder="t('admin.groups.form.placeholders.descriptionZh')"
              :rows="3"
            />
          </n-form-item>
          <n-form-item :label="t('admin.groups.form.descriptionEn')" path="research_group_desc_en">
            <MarkdownEditor
              v-model="formData.research_group_desc_en"
              :placeholder="t('admin.groups.form.placeholders.descriptionEn')"
              :rows="3"
            />
          </n-form-item>
          <n-form-item :label="t('admin.groups.form.leader')" path="mem_id">
            <n-select
              v-model:value="formData.mem_id"
              :options="memberOptions"
              :placeholder="t('admin.groups.form.placeholders.leader')"
              :loading="loadingMembers"
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
import { ref, reactive, computed, watch, nextTick } from 'vue';
import { useMessage } from 'naive-ui';
import { useI18n } from 'vue-i18n';
import { memberApi, paperApi, projectApi, newsApi, researchGroupApi } from '@/services/api';
import MarkdownEditor from './MarkdownEditor.vue';

const { t } = useI18n();

// Props
interface Props {
  modelValue: boolean;
  moduleType: 'members' | 'papers' | 'projects' | 'news' | 'research-groups';
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
    'research-groups': 'Group'
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
          Object.assign(formData, { ...props.editData });
        });
      }
    }
  }
);

watch(show, (newValue) => {
  emit('update:modelValue', newValue);
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
  if (props.moduleType === 'research-groups') {
    await loadMembers();
  }
};

const loadResearchGroups = async () => {
  try {
    loadingGroups.value = true;
    const response = await researchGroupApi.getResearchGroups({ all: 'true' });
    if (response.code === 0) {
      researchGroupOptions.value = response.data.items.map((group: any) => ({
        label: group.research_group_name_zh || group.research_group_name_en,
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
    const response = await memberApi.getMembers({ all: 'true', type: 0 }); // 只載入教師
    if (response.code === 0) {
      memberOptions.value = response.data.items.map((member: any) => ({
        label: member.mem_name_zh || member.mem_name_en,
        value: member.mem_id
      }));
    }
  } catch (error) {
    console.error(t('admin.quickAction.messages.loadMembersFailed'), error);
  } finally {
    loadingMembers.value = false;
  }
};

const formatDateForApi = (date: any) => {
  if (!date) return '';
  const d = new Date(date);
  return d.toISOString().split('T')[0];
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
      'research-groups': researchGroupApi
    };

    const api = apis[props.moduleType];
    
    if (props.actionType === 'create') {
      const createMethods = {
        members: 'createMember',
        papers: 'createPaper',
        projects: 'createProject',
        news: 'createNews',
        'research-groups': 'createResearchGroup'
      };
      response = await (api as any)[createMethods[props.moduleType]](submitData);
    } else {
      const updateMethods = {
        members: 'updateMember',
        papers: 'updatePaper',
        projects: 'updateProject',
        news: 'updateNews',
        'research-groups': 'updateResearchGroup'
      };
      const idField = {
        members: 'mem_id',
        papers: 'paper_id',
        projects: 'project_id',
        news: 'news_id',
        'research-groups': 'research_group_id'
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
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>