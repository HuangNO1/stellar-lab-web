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
import { computed, onMounted, inject, watch, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { MdEditor, config } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import { getTheme } from '@/locales';
import { useMessage } from 'naive-ui';
import { imageApi } from '@/services/api';
import { createMarkdownPlugins } from '@/utils/markdown';
import type { ApiError } from '@/types/api';

// 定義 MarkdownIt 類型
interface MarkdownIt {
  use(plugin: (...args: any[]) => void): MarkdownIt;
}

// Props
const props = defineProps<{
  modelValue?: string;
  placeholder?: string;
  preview?: boolean;
  toolbars?: any[];
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

// 配置國際化和主題
onMounted(() => {
  config({
    editorConfig: {
      markdownItConfig: (md: MarkdownIt) => {
        const customPlugins = createMarkdownPlugins();
        customPlugins.forEach(pluginConfig => {
          md.use(pluginConfig.plugin);
        });
        return md;
      },
      languageUserDefined: {
        'zh-CN': {
          toolbarTips: {
            bold: '粗體',
            underline: '底線',
            italic: '斜體',
            strikeThrough: '刪除線',
            title: '標題',
            sub: '下標',
            sup: '上標',
            quote: '引用',
            unorderedList: '無序列表',
            orderedList: '有序列表',
            task: '任務列表',
            codeRow: '行內代碼',
            code: '代碼塊',
            link: '連結',
            image: '圖片',
            table: '表格',
            mermaid: 'Mermaid圖表',
            katex: 'KaTeX公式',
            revoke: '撤銷',
            next: '重做',
            save: '保存',
            prettier: '格式化',
            pageFullscreen: '頁面全屏',
            fullscreen: '全屏',
            preview: '預覽',
            htmlPreview: 'HTML預覽',
            catalog: '目錄',
            github: '源代碼',
          },
          titleItem: {
            h1: '一級標題',
            h2: '二級標題',
            h3: '三級標題',
            h4: '四級標題',
            h5: '五級標題',
            h6: '六級標題',
          },
          imgTitleItem: {
            link: '添加連結',
            upload: '上傳圖片',
            clip2upload: '裁剪上傳',
          },
          linkModalTips: {
            linkTitle: '添加連結',
            imageTitle: '添加圖片',
            descLabel: '連結描述：',
            descLabelPlaceHolder: '請輸入描述...',
            urlLabel: '連結地址：',
            urlLabelPlaceHolder: '請輸入連結...',
            buttonOK: '確定',
          },
          clipModalTips: {
            title: '裁剪圖片上傳',
            buttonUpload: '上傳',
          },
          copyCode: {
            text: '複製代碼',
            successTips: '已複製！',
            failTips: '複製失敗！',
          },
          mermaid: {
            flow: '流程圖',
            sequence: '時序圖',
            gantt: '甘特圖',
            class: '類圖',
            state: '狀態圖',
            pie: '餅圖',
            relationship: '關係圖',
            journey: '旅程圖',
          },
          katex: {
            inline: '行內公式',
            block: '塊級公式',
          },
          footer: {
            markdownTotal: '字數',
            scrollAuto: '同步滾動',
          },
        },
        'en-US': {
          toolbarTips: {
            bold: 'Bold',
            underline: 'Underline',
            italic: 'Italic',
            strikeThrough: 'Strike Through',
            title: 'Title',
            sub: 'Subscript',
            sup: 'Superscript',
            quote: 'Quote',
            unorderedList: 'Unordered List',
            orderedList: 'Ordered List',
            task: 'Task List',
            codeRow: 'Inline Code',
            code: 'Code Block',
            link: 'Link',
            image: 'Image',
            table: 'Table',
            mermaid: 'Mermaid Chart',
            katex: 'KaTeX Formula',
            revoke: 'Undo',
            next: 'Redo',
            save: 'Save',
            prettier: 'Format',
            pageFullscreen: 'Page Fullscreen',
            fullscreen: 'Fullscreen',
            preview: 'Preview',
            htmlPreview: 'HTML Preview',
            catalog: 'Catalog',
            github: 'Source Code',
          },
          titleItem: {
            h1: 'Heading 1',
            h2: 'Heading 2',
            h3: 'Heading 3',
            h4: 'Heading 4',
            h5: 'Heading 5',
            h6: 'Heading 6',
          },
          imgTitleItem: {
            link: 'Add Link',
            upload: 'Upload Image',
            clip2upload: 'Clip & Upload',
          },
          linkModalTips: {
            linkTitle: 'Add Link',
            imageTitle: 'Add Image',
            descLabel: 'Description:',
            descLabelPlaceHolder: 'Enter description...',
            urlLabel: 'URL:',
            urlLabelPlaceHolder: 'Enter URL...',
            buttonOK: 'OK',
          },
          clipModalTips: {
            title: 'Clip Image Upload',
            buttonUpload: 'Upload',
          },
          copyCode: {
            text: 'Copy Code',
            successTips: 'Copied!',
            failTips: 'Copy failed!',
          },
          mermaid: {
            flow: 'Flowchart',
            sequence: 'Sequence Diagram',
            gantt: 'Gantt Chart',
            class: 'Class Diagram',
            state: 'State Diagram',
            pie: 'Pie Chart',
            relationship: 'Relationship Diagram',
            journey: 'Journey Diagram',
          },
          katex: {
            inline: 'Inline Formula',
            block: 'Block Formula',
          },
          footer: {
            markdownTotal: 'Word Count',
            scrollAuto: 'Sync Scroll',
          },
        },
      },
    },
    editorExtensions: {
      highlight: {
        css: {
          atom: {
            light: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-light.min.css',
            dark: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-dark.min.css',
          },
          github: {
            light: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github.min.css',
            dark: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github-dark.min.css',
          },
          vscode: {
            light: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/vs.min.css',
            dark: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/vs2015.min.css',
          },
        },
      },
    },
  });
});
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