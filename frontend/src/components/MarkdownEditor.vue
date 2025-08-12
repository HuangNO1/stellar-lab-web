<template>
  <div class="markdown-editor">
    <div class="editor-header" v-if="showHeader">
      <span class="editor-title">{{ label }}</span>
      <div class="editor-tools">
        <n-button size="tiny" quaternary @click="insertMarkdown('**', '**')">
          <template #icon>
            <n-icon><strong>B</strong></n-icon>
          </template>
        </n-button>
        <n-button size="tiny" quaternary @click="insertMarkdown('*', '*')">
          <template #icon>
            <n-icon><em>I</em></n-icon>
          </template>
        </n-button>
        <n-button size="tiny" quaternary @click="insertMarkdown('### ', '')">
          <template #icon>
            <n-icon>H</n-icon>
          </template>
        </n-button>
        <n-button size="tiny" quaternary @click="insertMarkdown('- ', '')">
          <template #icon>
            <n-icon>•</n-icon>
          </template>
        </n-button>
        <n-button size="tiny" quaternary @click="insertMarkdown('[', '](url)')">
          <template #icon>
            <n-icon>🔗</n-icon>
          </template>
        </n-button>
      </div>
    </div>
    
    <n-input
      ref="textareaRef"
      v-model:value="inputValue"
      type="textarea"
      :rows="rows"
      :placeholder="placeholder || t('admin.markdownEditor.placeholder')"
      :disabled="disabled"
      @input="handleInput"
      @blur="handleBlur"
      @focus="handleFocus"
    />
    
    <div class="editor-footer" v-if="showPreview">
      <n-button size="tiny" quaternary @click="togglePreview">
        {{ isPreviewMode ? t('admin.markdownEditor.edit') : t('admin.markdownEditor.preview') }}
      </n-button>
    </div>
    
    <div v-if="isPreviewMode" class="markdown-preview">
      <markdown-it :source="inputValue" :plugins="markdownPlugins"></markdown-it>
    </div>
    
    <div class="editor-tip" v-if="showTip">
      <n-text depth="3" style="font-size: 12px">
        {{ t('admin.markdownEditor.tip') }}
      </n-text>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';
import { NInput, NButton, NIcon, NText } from 'naive-ui';
import MarkdownIt from 'vue3-markdown-it';

const { t } = useI18n();

interface Props {
  modelValue: string;
  label?: string;
  placeholder?: string;
  rows?: number;
  disabled?: boolean;
  showHeader?: boolean;
  showPreview?: boolean;
  showTip?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  label: '',
  placeholder: '',
  rows: 4,
  disabled: false,
  showHeader: true,
  showPreview: false,
  showTip: true
});

const emit = defineEmits<{
  'update:modelValue': [value: string];
  'input': [value: string];
  'blur': [event: FocusEvent];
  'focus': [event: FocusEvent];
}>();

const textareaRef = ref<InstanceType<typeof NInput>>();
const inputValue = ref(props.modelValue);
const isPreviewMode = ref(false);

// Markdown插件配置
const markdownPlugins = [
  {
    plugin: (md: any) => {
      // 修改链接渲染规则
      const defaultRender = md.renderer.rules.link_open || function(tokens: any, idx: any, options: any, env: any, renderer: any) {
        return renderer.renderToken(tokens, idx, options);
      };

      md.renderer.rules.link_open = function (tokens: any, idx: any, options: any, env: any, renderer: any) {
        const token = tokens[idx];
        const href = token.attrGet('href');
        
        // 检查是否为外部链接
        if (href && (href.startsWith('http://') || href.startsWith('https://') || href.startsWith('//') || href.includes('://'))) {
          token.attrSet('target', '_blank');
          token.attrSet('rel', 'noopener noreferrer');
        }
        
        return defaultRender(tokens, idx, options, env, renderer);
      };
    }
  }
];

watch(
  () => props.modelValue,
  (newValue) => {
    inputValue.value = newValue;
  }
);

watch(inputValue, (newValue) => {
  emit('update:modelValue', newValue);
});

const handleInput = (value: string) => {
  inputValue.value = value;
  emit('input', value);
};

const handleBlur = (event: FocusEvent) => {
  emit('blur', event);
};

const handleFocus = (event: FocusEvent) => {
  emit('focus', event);
};

const togglePreview = () => {
  isPreviewMode.value = !isPreviewMode.value;
};

const insertMarkdown = (before: string, after = '') => {
  nextTick(() => {
    const textarea = textareaRef.value?.inputElRef;
    if (!textarea) return;
    
    const start = textarea.selectionStart ?? 0;
    const end = textarea.selectionEnd ?? 0;
    const selectedText = inputValue.value.substring(start, end);
    
    const newText = inputValue.value.substring(0, start) + 
                   before + selectedText + after + 
                   inputValue.value.substring(end);
    
    inputValue.value = newText;
    
    // 設置新的光標位置
    nextTick(() => {
      textarea.focus();
      textarea.setSelectionRange(
        start + before.length, 
        start + before.length + selectedText.length
      );
    });
  });
};
</script>

<style scoped>
.markdown-editor {
  width: 100%;
}

.editor-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  padding: 8px 12px;
  background-color: #f8f9fa;
  border-radius: 6px 6px 0 0;
  border: 1px solid #e0e0e6;
  border-bottom: none;
}

.editor-title {
  font-weight: 500;
  color: #333;
}

.editor-tools {
  display: flex;
  gap: 4px;
}

.editor-footer {
  display: flex;
  justify-content: flex-end;
  padding: 8px;
  background-color: #f8f9fa;
  border: 1px solid #e0e0e6;
  border-top: none;
  border-radius: 0 0 6px 6px;
}

.markdown-preview {
  margin-top: 12px;
  padding: 12px;
  border: 1px solid #e0e0e6;
  border-radius: 6px;
  background-color: #fff;
  min-height: 100px;
}

.markdown-preview :deep(h1) {
  font-size: 1.5em;
  font-weight: bold;
  margin: 0.5em 0;
}

.markdown-preview :deep(h2) {
  font-size: 1.3em;
  font-weight: bold;
  margin: 0.5em 0;
}

.markdown-preview :deep(h3) {
  font-size: 1.1em;
  font-weight: bold;
  margin: 0.5em 0;
}

.markdown-preview :deep(ul) {
  margin: 0.5em 0;
  padding-left: 20px;
}

.markdown-preview :deep(li) {
  list-style-type: disc;
}

.markdown-preview :deep(a) {
  color: #1890ff;
  text-decoration: none;
}

.markdown-preview :deep(a:hover) {
  text-decoration: underline;
}

.editor-tip {
  margin-top: 8px;
  padding: 4px 8px;
}

/* 暗色主題支持 */
[data-theme="dark"] .editor-header,
[data-theme="dark"] .editor-footer {
  background-color: #2c2c32;
  border-color: #3c3c41;
}

[data-theme="dark"] .editor-title {
  color: #ffffffd1;
}

[data-theme="dark"] .markdown-preview {
  background-color: #1f1f23;
  border-color: #3c3c41;
  color: #ffffffd1;
}
</style>