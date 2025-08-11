<template>
  <MdEditor 
    :modelValue="modelValue" 
    :language="currentLanguage"
    :placeholder="placeholder"
    :preview="preview"
    :toolbars="toolbars"
    :style="style"
    :theme="currentTheme"
    @update:modelValue="$emit('update:modelValue', $event)"
  />
</template>

<script setup lang="ts">
import { computed, onMounted, inject } from 'vue';
import { useI18n } from 'vue-i18n';
import { MdEditor, config } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import { getTheme } from '@/locales';

// Props
interface Props {
  modelValue: string;
  placeholder?: string;
  preview?: boolean;
  toolbars?: string[];
  style?: string | Record<string, any>;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '',
  preview: false,
  toolbars: () => ['bold', 'underline', 'italic', '-', 'title', 'strikeThrough', 'sub', 'sup', 'quote', 'unorderedList', 'orderedList', '-', 'codeRow', 'code', 'link', 'image', '-', 'revoke', 'next', 'save', '=', 'pageFullscreen', 'fullscreen', 'preview', 'previewOnly'],
  style: 'height: 200px; width: 100%'
});

// Emits
defineEmits<{
  'update:modelValue': [value: string];
}>();

const { locale } = useI18n();

// Try to inject theme from parent, fallback to getTheme()
const isDarkMode = inject('isDarkMode', null);

// 當前語言
const currentLanguage = computed(() => {
  return locale.value === 'zh' ? 'zh-CN' : 'en-US';
});

// 當前主題
const currentTheme = computed(() => {
  // Try to get theme from injected value or fallback to stored theme
  if (isDarkMode && typeof isDarkMode === 'object' && 'value' in isDarkMode) {
    return isDarkMode.value ? 'dark' : 'light';
  }
  return getTheme() === 'dark' ? 'dark' : 'light';
});

// 配置國際化和主題
onMounted(() => {
  config({
    editorConfig: {
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
</style>