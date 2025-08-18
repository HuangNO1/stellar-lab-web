<template>
  <MdEditor 
    :modelValue="modelValue || ''" 
    :language="currentLanguage"
    :placeholder="placeholder"
    :preview="preview"
    :toolbars="toolbars || defaultToolbars"
    :style="style"
    :theme="currentTheme"
    :onUploadImg="handleUploadImg"
    @update:modelValue="$emit('update:modelValue', $event)"
  />
</template>

<script setup lang="ts">
import { computed, inject } from 'vue';
import { useI18n } from 'vue-i18n';
import { MdEditor } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import { getTheme } from '@/locales';
import { useMessage } from 'naive-ui';
import { imageApi } from '@/services/api';
import type { ApiError } from '@/types/api';

// Props
const props = defineProps<{
  modelValue?: string;
  placeholder?: string;
  preview?: boolean;
  toolbars?: string[];
  style?: string | Record<string, unknown>;
  entityType?: string;
  entityId?: number;
  fieldName?: string;
}>();

// Emits
defineEmits<{
  'update:modelValue': [value: string];
}>();

const { locale, t } = useI18n();
const message = useMessage();

// 默認工具欄配置，包含KaTeX數學公式按鈕
const defaultToolbars = [
  'bold', 'underline', 'italic', 'strikeThrough', '-',
  'title', 'sub', 'sup', 'quote', 'unorderedList', 'orderedList', 'task', '-',
  'codeRow', 'code', 'link', 'image', 'table', 'mermaid', 'katex', '-',
  'revoke', 'next', 'save', '=', 'pageFullscreen', 'fullscreen', 'preview', 'htmlPreview', 'catalog'
];

// Try to inject theme from parent, fallback to getTheme()
const isDarkMode = inject<{ value: boolean } | null>('isDarkMode', null);

// 當前語言
const currentLanguage = computed(() => {
  return locale.value === 'zh' ? 'zh-CN' : 'en-US';
});

// 當前主題
const currentTheme = computed(() => {
  if (isDarkMode && typeof isDarkMode === 'object' && 'value' in isDarkMode) {
    return isDarkMode.value ? 'dark' : 'light';
  }
  return getTheme() === 'dark' ? 'dark' : 'light';
});

// 處理圖片上傳
const handleUploadImg = async (files: File[], callback: (urls: string[]) => void) => {
  const uploadResults: string[] = [];
  
  for (const file of files) {
    try {
      // 檢查文件類型
      if (!file.type.startsWith('image/')) {
        message.error(t('admin.markdownEditor.imageUpload.invalidFileType'));
        continue;
      }
      
      // 檢查文件大小 (5MB)
      if (file.size > 5 * 1024 * 1024) {
        message.error(t('admin.markdownEditor.imageUpload.fileSizeExceeded'));
        continue;
      }
      
      // 使用封裝的 API 上傳圖片
      const response = await imageApi.uploadImage(
        file,
        props.entityType,
        props.entityId,
        props.fieldName
      );
      
      if (response.code === 0 && response.data) {
        uploadResults.push(response.data.file_url);
      } else {
        message.error(response.message || t('admin.markdownEditor.imageUpload.uploadFailed'));
      }
    } catch (error) {
      console.error('圖片上傳錯誤:', error);
      const apiError = error as ApiError;
      message.error(apiError?.message || t('admin.markdownEditor.imageUpload.uploadFailed'));
    }
  }
  
  // 回調返回上傳成功的圖片URL
  callback(uploadResults);
  
  if (uploadResults.length > 0) {
    message.success(t('admin.markdownEditor.imageUpload.uploadSuccess', { count: uploadResults.length }));
  }
};

</script>

<style scoped>
/* 自定義樣式 */
:deep(.md-editor) {
  --md-color: #000;
  --md-hover-color: #1976d2;
  --md-bk-color: #fff;
  --md-bk-color-outstand: #f8f9fa;
  --md-bk-hover-color: #f5f5f5;
  --md-border-color: #e0e0e0;
  --md-border-hover-color: #bdbdbd;
  --md-border-active-color: #1976d2;
  --md-modal-mask: rgba(0, 0, 0, 0.5);
  --md-scrollbar-bg-color: #f5f5f5;
  --md-scrollbar-thumb-color: #bdbdbd;
  --md-scrollbar-thumb-hover-color: #9e9e9e;
  --md-scrollbar-thumb-active-color: #757575;
}

/* 暗色主題 */
[data-theme="dark"] :deep(.md-editor),
.dark :deep(.md-editor) {
  --md-color: #fff;
  --md-hover-color: #64b5f6;
  --md-bk-color: #1a1a1a;
  --md-bk-color-outstand: #2d2d2d;
  --md-bk-hover-color: #333;
  --md-border-color: #424242;
  --md-border-hover-color: #616161;
  --md-border-active-color: #64b5f6;
  --md-modal-mask: rgba(0, 0, 0, 0.7);
  --md-scrollbar-bg-color: #2d2d2d;
  --md-scrollbar-thumb-color: #616161;
  --md-scrollbar-thumb-hover-color: #757575;
  --md-scrollbar-thumb-active-color: #9e9e9e;
}

/* 自定義 TAG 樣式 */
:deep(.md-editor .research-tags-container) {
  margin: 0.75rem 0;
  padding: 0.75rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #1976d2;
}

:deep(.md-editor .research-tags-label) {
  font-weight: 600;
  color: #1976d2;
  margin-right: 0.5rem;
  font-size: 0.9rem;
}

:deep(.md-editor .research-tags) {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
  margin-top: 0.5rem;
}

:deep(.md-editor .research-tag) {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, #1976d2, #42a5f5);
  color: white;
  border-radius: 16px;
  font-size: 0.75rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

:deep(.md-editor .research-tag:hover) {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.3);
}

:deep(.md-editor .homepage-container) {
  margin: 0.75rem 0;
  padding: 0.75rem;
  background-color: #f0f8ff;
  border-radius: 8px;
  border-left: 4px solid #52c41a;
}

:deep(.md-editor .homepage-label) {
  font-weight: 600;
  color: #52c41a;
  margin-right: 0.5rem;
  font-size: 0.9rem;
}

:deep(.md-editor .homepage-link) {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  background: linear-gradient(135deg, #52c41a, #73d13d);
  color: white;
  border-radius: 20px;
  text-decoration: none;
  font-size: 0.75rem;
  font-weight: 500;
  transition: all 0.2s ease;
  margin-right: 0.375rem;
  margin-top: 0.25rem;
}

:deep(.md-editor .homepage-link:hover) {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(82, 196, 26, 0.3);
}

:deep(.md-editor .homepage-icon),
:deep(.md-editor .homepage-external-icon) {
  width: 12px;
  height: 12px;
  opacity: 0.9;
}

:deep(.md-editor .papers-list-container) {
  margin: 0.75rem 0;
  padding: 0.75rem;
  background-color: #fff7e6;
  border-radius: 8px;
  border-left: 4px solid #fa8c16;
}

:deep(.md-editor .papers-list-label) {
  font-weight: 600;
  color: #fa8c16;
  margin-right: 0.5rem;
  font-size: 0.9rem;
}

:deep(.md-editor .papers-list-loading) {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  color: #666;
  font-size: 0.8rem;
}

:deep(.md-editor .loading-spinner) {
  width: 16px;
  height: 16px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #fa8c16;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 暗色主題下的 TAG 樣式 */
[data-theme="dark"] :deep(.md-editor .research-tags-container),
.dark :deep(.md-editor .research-tags-container) {
  background-color: rgba(25, 118, 210, 0.1);
  border-left-color: #64b5f6;
}

[data-theme="dark"] :deep(.md-editor .research-tags-label),
.dark :deep(.md-editor .research-tags-label) {
  color: #64b5f6;
}

[data-theme="dark"] :deep(.md-editor .research-tag),
.dark :deep(.md-editor .research-tag) {
  background: linear-gradient(135deg, #64b5f6, #90caf9);
  color: #1a1a1a;
}

[data-theme="dark"] :deep(.md-editor .homepage-container),
.dark :deep(.md-editor .homepage-container) {
  background-color: rgba(82, 196, 26, 0.1);
  border-left-color: #73d13d;
}

[data-theme="dark"] :deep(.md-editor .homepage-label),
.dark :deep(.md-editor .homepage-label) {
  color: #73d13d;
}

[data-theme="dark"] :deep(.md-editor .homepage-link),
.dark :deep(.md-editor .homepage-link) {
  background: linear-gradient(135deg, #73d13d, #95de64);
  color: #1a1a1a;
}

[data-theme="dark"] :deep(.md-editor .papers-list-container),
.dark :deep(.md-editor .papers-list-container) {
  background-color: rgba(250, 140, 22, 0.1);
  border-left-color: #ffa940;
}

[data-theme="dark"] :deep(.md-editor .papers-list-label),
.dark :deep(.md-editor .papers-list-label) {
  color: #ffa940;
}

[data-theme="dark"] :deep(.md-editor .papers-list-loading),
.dark :deep(.md-editor .papers-list-loading) {
  color: #bbb;
}

[data-theme="dark"] :deep(.md-editor .loading-spinner),
.dark :deep(.md-editor .loading-spinner) {
  border-color: #424242;
  border-top-color: #ffa940;
}
</style>