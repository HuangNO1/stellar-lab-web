<template>
  <n-modal
    v-model:show="visible"
    preset="dialog"
    :title="title"
    class="json-detail-modal"
    @update:show="handleUpdateShow"
  >
    <template #header>
      <div class="modal-header">
        <n-icon size="20" color="#1890ff">
          <svg viewBox="0 0 24 24">
            <path fill="currentColor" d="M5,3H7V5H5V10A2,2 0 0,1 3,8V6A2,2 0 0,1 5,4V3M19,3V4A2,2 0 0,1 21,6V8A2,2 0 0,1 19,10V5H17V3H19M5,21V20A2,2 0 0,0 3,18V16A2,2 0 0,0 5,14V19H7V21H5M19,21H17V19H19V14A2,2 0 0,0 21,16V18A2,2 0 0,0 19,20V21M12,5A2,2 0 0,1 14,7V9A2,2 0 0,1 12,11A2,2 0 0,1 10,9V7A2,2 0 0,1 12,5M12,15A2,2 0 0,1 14,17V19A2,2 0 0,1 12,21A2,2 0 0,1 10,19V17A2,2 0 0,1 12,15Z"/>
          </svg>
        </n-icon>
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
          <n-space>
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
            
            <n-button
              size="small"
              @click="toggleExpanded"
            >
              <template #icon>
                <n-icon>
                  <svg v-if="expanded" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24">
                    <path fill="currentColor" d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"/>
                  </svg>
                </n-icon>
              </template>
              {{ expanded ? $t('admin.operationLogs.collapse') : $t('admin.operationLogs.expand') }}
            </n-button>
          </n-space>
        </div>
        
        <div class="json-display" :class="{ expanded }">
          <pre class="json-pre"><code class="json-code">{{ formattedJson }}</code></pre>
        </div>
      </div>
    </div>
    
    <template #action>
      <n-button @click="handleClose">{{ $t('common.confirm') }}</n-button>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useMessage } from 'naive-ui';

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
const expanded = ref(false);
const copying = ref(false);

// 監聽 show prop 的變化
watch(
  () => props.show,
  (newShow) => {
    visible.value = newShow;
    if (newShow) {
      expanded.value = false; // 重置展開狀態
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

// 切換展開狀態
const toggleExpanded = () => {
  expanded.value = !expanded.value;
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

.json-display {
  max-height: 400px;
  overflow: auto;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background-color: #fafbfc;
  transition: max-height 0.3s ease;
}

.json-display.expanded {
  max-height: 600px;
}

[data-theme="dark"] .json-display,
.dark .json-display {
  background-color: #1f2937;
  border-color: #374151;
}

.json-pre {
  margin: 0;
  padding: 1rem;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
  color: #374151;
}

[data-theme="dark"] .json-pre,
.dark .json-pre {
  color: #f3f4f6;
}

.json-code {
  font-family: inherit;
  background: transparent;
}

/* 語法高亮樣式 */
.json-pre {
  position: relative;
}

.json-pre::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

/* 滾動條樣式 */
.json-display::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.json-display::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.json-display::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.json-display::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

[data-theme="dark"] .json-display::-webkit-scrollbar-track,
.dark .json-display::-webkit-scrollbar-track {
  background: #374151;
}

[data-theme="dark"] .json-display::-webkit-scrollbar-thumb,
.dark .json-display::-webkit-scrollbar-thumb {
  background: #6b7280;
}

[data-theme="dark"] .json-display::-webkit-scrollbar-thumb:hover,
.dark .json-display::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .json-detail-modal :deep(.n-dialog) {
    width: 95vw;
    max-width: none;
  }
  
  .json-display {
    max-height: 300px;
  }
  
  .json-display.expanded {
    max-height: 500px;
  }
  
  .json-pre {
    font-size: 12px;
    padding: 0.75rem;
  }
}

@media (max-width: 480px) {
  .json-toolbar {
    padding: 0.25rem;
  }
  
  .json-toolbar :deep(.n-space) {
    flex-direction: column;
    align-items: stretch;
  }
  
  .json-toolbar :deep(.n-button) {
    width: 100%;
  }
  
  .json-display {
    max-height: 250px;
  }
  
  .json-display.expanded {
    max-height: 400px;
  }
}
</style>