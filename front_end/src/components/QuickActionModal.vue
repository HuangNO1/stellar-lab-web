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
          <n-form-item label="中文姓名" path="mem_name_zh">
            <n-input
              v-model:value="formData.mem_name_zh"
              placeholder="請輸入中文姓名"
            />
          </n-form-item>
          <n-form-item label="英文姓名" path="mem_name_en">
            <n-input
              v-model:value="formData.mem_name_en"
              placeholder="請輸入英文姓名"
            />
          </n-form-item>
          <n-form-item label="電子信箱" path="mem_email">
            <n-input
              v-model:value="formData.mem_email"
              placeholder="請輸入電子信箱"
            />
          </n-form-item>
          <n-form-item label="成員類型" path="mem_type">
            <n-select
              v-model:value="formData.mem_type"
              :options="memberTypeOptions"
              placeholder="請選擇成員類型"
            />
          </n-form-item>
          <n-form-item label="課題組" path="research_group_id">
            <n-select
              v-model:value="formData.research_group_id"
              :options="researchGroupOptions"
              placeholder="請選擇課題組"
              :loading="loadingGroups"
            />
          </n-form-item>
          <n-form-item label="成員描述" path="mem_desc_zh">
            <MarkdownEditor
              v-model="formData.mem_desc_zh"
              placeholder="請輸入成員中文描述（支持 Markdown 語法）"
              :rows="3"
            />
          </n-form-item>
        </template>

        <!-- 論文表單 -->
        <template v-if="moduleType === 'papers'">
          <n-form-item label="中文標題" path="paper_title_zh">
            <n-input
              v-model:value="formData.paper_title_zh"
              placeholder="請輸入論文中文標題"
            />
          </n-form-item>
          <n-form-item label="英文標題" path="paper_title_en">
            <n-input
              v-model:value="formData.paper_title_en"
              placeholder="請輸入論文英文標題"
            />
          </n-form-item>
          <n-form-item label="論文描述" path="paper_desc_zh">
            <MarkdownEditor
              v-model="formData.paper_desc_zh"
              placeholder="請輸入論文中文描述（支持 Markdown 語法）"
              :rows="3"
            />
          </n-form-item>
          <n-form-item label="期刊/會議" path="paper_venue">
            <n-input
              v-model:value="formData.paper_venue"
              placeholder="請輸入發表期刊或會議"
            />
          </n-form-item>
          <n-form-item label="論文類型" path="paper_type">
            <n-select
              v-model:value="formData.paper_type"
              :options="paperTypeOptions"
              placeholder="請選擇論文類型"
            />
          </n-form-item>
          <n-form-item label="發表日期" path="paper_date">
            <n-date-picker
              v-model:value="formData.paper_date"
              type="date"
              placeholder="請選擇發表日期"
            />
          </n-form-item>
          <n-form-item label="接收狀態" path="paper_accept">
            <n-select
              v-model:value="formData.paper_accept"
              :options="paperAcceptOptions"
              placeholder="請選擇接收狀態"
            />
          </n-form-item>
        </template>

        <!-- 項目表單 -->
        <template v-if="moduleType === 'projects'">
          <n-form-item label="中文名稱" path="project_name_zh">
            <n-input
              v-model:value="formData.project_name_zh"
              placeholder="請輸入項目中文名稱"
            />
          </n-form-item>
          <n-form-item label="英文名稱" path="project_name_en">
            <n-input
              v-model:value="formData.project_name_en"
              placeholder="請輸入項目英文名稱"
            />
          </n-form-item>
          <n-form-item label="項目描述" path="project_desc_zh">
            <MarkdownEditor
              v-model="formData.project_desc_zh"
              placeholder="請輸入項目描述（支持 Markdown 語法）"
              :rows="3"
            />
          </n-form-item>
          <n-form-item label="項目URL" path="project_url">
            <n-input
              v-model:value="formData.project_url"
              placeholder="請輸入項目URL"
            />
          </n-form-item>
          <n-form-item label="開始日期" path="project_date_start">
            <n-date-picker
              v-model:value="formData.project_date_start"
              type="date"
              placeholder="請選擇開始日期"
            />
          </n-form-item>
          <n-form-item label="項目狀態" path="is_end">
            <n-select
              v-model:value="formData.is_end"
              :options="projectStatusOptions"
              placeholder="請選擇項目狀態"
            />
          </n-form-item>
        </template>

        <!-- 新聞表單 -->
        <template v-if="moduleType === 'news'">
          <n-form-item label="新聞類型" path="news_type">
            <n-select
              v-model:value="formData.news_type"
              :options="newsTypeOptions"
              placeholder="請選擇新聞類型"
            />
          </n-form-item>
          <n-form-item label="中文內容" path="news_content_zh">
            <MarkdownEditor
              v-model="formData.news_content_zh"
              placeholder="請輸入新聞中文內容（支持 Markdown 語法）"
              :rows="4"
            />
          </n-form-item>
          <n-form-item label="英文內容" path="news_content_en">
            <MarkdownEditor
              v-model="formData.news_content_en"
              placeholder="請輸入新聞英文內容（支持 Markdown 語法）"
              :rows="4"
            />
          </n-form-item>
          <n-form-item label="新聞日期" path="news_date">
            <n-date-picker
              v-model:value="formData.news_date"
              type="date"
              placeholder="請選擇新聞日期"
            />
          </n-form-item>
        </template>

        <!-- 課題組表單 -->
        <template v-if="moduleType === 'research-groups'">
          <n-form-item label="中文名稱" path="research_group_name_zh">
            <n-input
              v-model:value="formData.research_group_name_zh"
              placeholder="請輸入課題組中文名稱"
            />
          </n-form-item>
          <n-form-item label="英文名稱" path="research_group_name_en">
            <n-input
              v-model:value="formData.research_group_name_en"
              placeholder="請輸入課題組英文名稱"
            />
          </n-form-item>
          <n-form-item label="中文描述" path="research_group_desc_zh">
            <MarkdownEditor
              v-model="formData.research_group_desc_zh"
              placeholder="請輸入課題組中文描述（支持 Markdown 語法）"
              :rows="3"
            />
          </n-form-item>
          <n-form-item label="英文描述" path="research_group_desc_en">
            <MarkdownEditor
              v-model="formData.research_group_desc_en"
              placeholder="請輸入課題組英文描述（支持 Markdown 語法）"
              :rows="3"
            />
          </n-form-item>
          <n-form-item label="組長" path="mem_id">
            <n-select
              v-model:value="formData.mem_id"
              :options="memberOptions"
              placeholder="請選擇組長"
              :loading="loadingMembers"
            />
          </n-form-item>
        </template>
      </n-form>

      <template #footer>
        <div class="modal-footer">
          <n-button @click="show = false">
            取消
          </n-button>
          <n-button
            type="primary"
            :loading="submitting"
            @click="handleSubmit"
          >
            {{ actionType === 'create' ? '創建' : '更新' }}
          </n-button>
        </div>
      </template>
    </n-card>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, nextTick } from 'vue';
import { useMessage } from 'naive-ui';
import { memberApi, paperApi, projectApi, newsApi, researchGroupApi } from '@/services/api';
import MarkdownEditor from './MarkdownEditor.vue';

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

// Options
const memberTypeOptions = [
  { label: '教師', value: 0 },
  { label: '學生', value: 1 },
  { label: '校友', value: 2 }
];

const paperTypeOptions = [
  { label: '會議', value: 0 },
  { label: '期刊', value: 1 },
  { label: '專利', value: 2 },
  { label: '書籍', value: 3 },
  { label: '其他', value: 4 }
];

const paperAcceptOptions = [
  { label: '投稿中', value: 0 },
  { label: '已接收', value: 1 }
];

const projectStatusOptions = [
  { label: '進行中', value: 0 },
  { label: '已完成', value: 1 }
];

const newsTypeOptions = [
  { label: '論文發表', value: 0 },
  { label: '獲獎消息', value: 1 },
  { label: '學術活動', value: 2 }
];

const researchGroupOptions = ref<Array<{ label: string; value: number }>>([]);
const memberOptions = ref<Array<{ label: string; value: number }>>([]);

// Computed
const modalTitle = computed(() => {
  const moduleNames = {
    members: '成員',
    papers: '論文',
    projects: '項目',
    news: '新聞',
    'research-groups': '課題組'
  };
  const actionNames = {
    create: '新增',
    edit: '編輯'
  };
  return `${actionNames[props.actionType]}${moduleNames[props.moduleType]}`;
});

// Form rules
const formRules = computed(() => {
  const rules: Record<string, any> = {};
  
  if (props.moduleType === 'members') {
    rules.mem_name_zh = { required: true, message: '請輸入中文姓名', trigger: 'blur' };
    rules.mem_name_en = { required: true, message: '請輸入英文姓名', trigger: 'blur' };
    rules.mem_email = { required: true, message: '請輸入電子信箱', trigger: 'blur' };
    rules.mem_type = { required: true, message: '請選擇成員類型', trigger: 'change' };
    rules.research_group_id = { required: true, message: '請選擇課題組', trigger: 'change' };
  } else if (props.moduleType === 'papers') {
    rules.paper_title_zh = { required: true, message: '請輸入中文標題', trigger: 'blur' };
    rules.paper_type = { required: true, message: '請選擇論文類型', trigger: 'change' };
    rules.paper_accept = { required: true, message: '請選擇接收狀態', trigger: 'change' };
    rules.paper_date = { required: true, message: '請選擇發表日期', trigger: 'change' };
  } else if (props.moduleType === 'projects') {
    rules.project_name_zh = { required: true, message: '請輸入項目中文名稱', trigger: 'blur' };
  } else if (props.moduleType === 'news') {
    rules.news_type = { required: true, message: '請選擇新聞類型', trigger: 'change' };
    rules.news_content_zh = { required: true, message: '請輸入新聞中文內容', trigger: 'blur' };
    rules.news_date = { required: true, message: '請選擇新聞日期', trigger: 'change' };
  } else if (props.moduleType === 'research-groups') {
    rules.research_group_name_zh = { required: true, message: '請輸入課題組中文名稱', trigger: 'blur' };
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
    console.error('載入課題組失敗:', error);
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
    console.error('載入成員失敗:', error);
  } finally {
    loadingMembers.value = false;
  }
};

const formatDateForApi = (date: any) => {
  if (!date) return '';
  const d = new Date(date);
  return d.toISOString().split('T')[0];
};

const handleSubmit = async () => {
  try {
    await formRef.value?.validate();
    submitting.value = true;

    // 格式化日期欄位
    const submitData = { ...formData };
    if (submitData.paper_date) {
      submitData.paper_date = formatDateForApi(submitData.paper_date);
    }
    if (submitData.news_date) {
      submitData.news_date = formatDateForApi(submitData.news_date);
    }
    if (submitData.project_date_start) {
      submitData.project_date_start = formatDateForApi(submitData.project_date_start);
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
      message.success(`${props.actionType === 'create' ? '創建' : '更新'}成功`);
      emit('success', response.data);
      show.value = false;
    } else {
      message.error(response.message || '操作失敗');
    }
  } catch (error: any) {
    if (error?.message) {
      message.error(error.message);
    } else {
      message.error('操作失敗，請檢查輸入');
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