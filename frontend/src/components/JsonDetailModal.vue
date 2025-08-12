<template>
  <n-modal
    v-model:show="visible"
    preset="dialog"
    class="json-detail-modal"
    @update:show="handleUpdateShow"
  >
    <template #header>
      <div class="modal-header">
        <span>{{ title || $t('common.viewDetails') }}</span>
      </div>
    </template>
    
    <div class="json-content">
      <!-- 空狀態 -->
      <div v-if="!hasContent" class="empty-state">
        <n-empty :description="$t('admin.operationLogs.emptyContent')" />
      </div>
      
      <!-- JSON 內容 -->
      <div v-else class="json-container">
        <div class="json-toolbar">
          <n-button
            size="small"
            @click="copyToClipboard"
            :loading="copying"
          >
            <template #icon>
              <n-icon>
                <svg viewBox="0 0 24 24">
                  <path fill="currentColor" d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"/>
                </svg>
              </n-icon>
            </template>
            {{ copying ? $t('admin.operationLogs.copying') : $t('admin.operationLogs.copyJson') }}
          </n-button>
        </div>
        
        <div class="json-display">
          <pre ref="codeRef" class="json-pre"><code class="language-json">{{ formattedJson }}</code></pre>
        </div>
      </div>
    </div>
    
    <template #action>
      <n-button @click="handleClose">{{ $t('common.confirm') }}</n-button>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';
import { useMessage } from 'naive-ui';
import hljs from 'highlight.js/lib/core';
import json from 'highlight.js/lib/languages/json';
import 'highlight.js/styles/github.css';

// 註冊 JSON 語言
hljs.registerLanguage('json', json);

interface Props {
  show: boolean;
  title?: string;
  content?: Record<string, any> | null;
}

interface Emits {
  (e: 'update:show', value: boolean): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const { t } = useI18n();
const message = useMessage();

const visible = ref(false);
const copying = ref(false);
const codeRef = ref<HTMLElement>();

// 監聽 show prop 的變化
watch(
  () => props.show,
  (newShow) => {
    visible.value = newShow;
    if (newShow) {
      // 等待 DOM 更新後應用高亮
      nextTick(() => {
        highlightCode();
      });
    }
  },
  { immediate: true }
);


// 處理 modal 顯示狀態更新
const handleUpdateShow = (show: boolean) => {
  visible.value = show;
  emit('update:show', show);
};

// 處理關閉
const handleClose = () => {
  handleUpdateShow(false);
};

// 檢查是否有內容
const hasContent = computed(() => {
  return props.content && typeof props.content === 'object' && Object.keys(props.content).length > 0;
});

// 格式化 JSON
const formattedJson = computed(() => {
  if (!hasContent.value) return '';
  return JSON.stringify(props.content, null, 2);
});

// 應用語法高亮
const highlightCode = () => {
  if (codeRef.value && hasContent.value) {
    const codeElement = codeRef.value.querySelector('code');
    if (codeElement) {
      // 清除之前的高亮
      codeElement.removeAttribute('data-highlighted');
      // 應用新的高亮
      hljs.highlightElement(codeElement);
    }
  }
};


// 複製到剪貼板
const copyToClipboard = async () => {
  if (!hasContent.value) return;
  
  try {
    copying.value = true;
    await navigator.clipboard.writeText(formattedJson.value);
    message.success(t('admin.operationLogs.copySuccess'));
  } catch (error) {
    console.error('Copy failed:', error);
    
    // 降級方案：創建臨時 textarea
    const textarea = document.createElement('textarea');
    textarea.value = formattedJson.value;
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
      document.execCommand('copy');
      message.success(t('admin.operationLogs.copySuccess'));
    } catch (fallbackError) {
      console.error('Fallback copy failed:', fallbackError);
      message.error(t('admin.operationLogs.copyFailed'));
    } finally {
      document.body.removeChild(textarea);
    }
  } finally {
    copying.value = false;
  }
};
</script>

<style scoped>
/* Modal 樣式 */
.json-detail-modal :deep(.n-dialog) {
  max-width: 800px;
  width: 90vw;
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 16px;
  font-weight: 600;
}

.json-content {
  max-height: 70vh;
  overflow: hidden;
}

.empty-state {
  padding: 2rem 0;
  text-align: center;
}

.json-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.json-toolbar {
  padding: 0.5rem;
  background-color: #f5f5f5;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

[data-theme="dark"] .json-toolbar,
.dark .json-toolbar {
  background-color: #374151;
  border-color: #4b5563;
}

/* JSON 顯示區域 */
.json-display {
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background-color: #fafbfc;
  overflow: hidden;
  max-height: 60vh; /* 使用視窗高度的 60% 作為最大高度 */
  min-height: 200px; /* 最小高度確保內容可見 */
}

[data-theme="dark"] .json-display,
.dark .json-display {
  background-color: #1f2937;
  border-color: #374151;
}

.json-pre {
  margin: 0;
  padding: 1rem;
  height: auto; /* 自適應內容高度 */
  max-height: calc(60vh - 2rem); /* 扣除 padding */
  overflow: auto; /* 當內容超出時顯示滾動條 */
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.5;
  background: transparent;
}

.json-pre code {
  font-family: inherit;
  background: transparent;
  color: inherit;
}

/* 覆蓋 highlight.js 的暗色主題 */
[data-theme="dark"] .json-pre,
.dark .json-pre {
  filter: invert(1) hue-rotate(180deg);
}

[data-theme="dark"] .json-pre code,
.dark .json-pre code {
  background: transparent !important;
}

/* 滾動條樣式 */
.json-pre::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.json-pre::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.json-pre::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.json-pre::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

[data-theme="dark"] .json-pre::-webkit-scrollbar-track,
.dark .json-pre::-webkit-scrollbar-track {
  background: #374151;
}

[data-theme="dark"] .json-pre::-webkit-scrollbar-thumb,
.dark .json-pre::-webkit-scrollbar-thumb {
  background: #6b7280;
}

[data-theme="dark"] .json-pre::-webkit-scrollbar-thumb:hover,
.dark .json-pre::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .json-detail-modal :deep(.n-dialog) {
    width: 95vw;
    max-width: none;
  }
  
  .json-display {
    max-height: 50vh; /* 移動端減少最大高度 */
    min-height: 150px;
  }
  
  .json-pre {
    max-height: calc(50vh - 2rem);
    font-size: 12px;
    padding: 0.75rem;
  }
}

@media (max-width: 480px) {
  .json-toolbar {
    padding: 0.25rem;
  }
  
  .json-toolbar :deep(.n-button) {
    width: 100%;
  }
  
  .json-display {
    max-height: 40vh; /* 小屏幕進一步減少高度 */
    min-height: 120px;
  }
  
  .json-pre {
    max-height: calc(40vh - 2rem);
    font-size: 11px;
    padding: 0.5rem;
  }
}
</style>