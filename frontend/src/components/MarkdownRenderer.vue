<template>
  <div class="markdown-renderer">
    <!-- 渲染处理后的markdown内容 -->
    <template v-for="(item, index) in parsedContent" :key="index">
      <!-- HTML 内容 -->
      <div 
        v-if="item.type === 'div'" 
        v-bind="item.props"
      />
      <!-- 研究领域标签 -->
      <ResearchTags 
        v-if="item.type === 'ResearchTags'" 
        v-bind="item.props"
      />
      <!-- 主页链接 -->
      <HomepageLink 
        v-else-if="item.type === 'HomepageLink'" 
        v-bind="item.props"
      />
      <!-- 论文列表 -->
      <PapersList 
        v-else-if="item.type === 'PapersList'" 
        v-bind="item.props"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import MarkdownIt from 'markdown-it';
import { processMarkdownImageUrls } from '@/utils/media';
import { createMarkdownPlugins } from '@/utils/markdown';
import ResearchTags from './tags/ResearchTags.vue';
import HomepageLink from './tags/HomepageLink.vue';
import PapersList from './tags/PapersList.vue';

// Props
interface Props {
  source?: string;
  processImages?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  processImages: true
});

// 创建 markdown-it 实例，使用通用插件
const md = new MarkdownIt({
  html: true,
  breaks: true,
  linkify: true,
});

// 应用所有插件
const plugins = createMarkdownPlugins();
plugins.forEach(({ plugin }) => {
  plugin(md);
});

// 解析内容接口
interface ContentItem {
  type: string;
  props: Record<string, unknown>;
}

// 解析markdown并替换自定义TAG为Vue组件
const parsedContent = computed<ContentItem[]>(() => {
  if (!props.source) return [];
  
  let content = props.source;
  
  // 处理图片URL（如果需要）
  if (props.processImages) {
    content = processMarkdownImageUrls(content);
  }
  
  // 按顺序处理所有TAG，将它们替换为占位符
  const tagReplacements: Array<{ type: string; props: Record<string, unknown> }> = [];
  
  // 1. 处理研究领域TAG - 重新添加以确保功能正常
  content = content.replace(/\{\{research:\s*([^}]+)\}\}/g, (_, tagsStr) => {
    // 检查是否包含背景色语法: tags[bg:#ffffff]
    let backgroundColor = null;
    let areas = [];
    
    // 检查背景色语法 [bg:#ffffff]
    const backgroundMatch = tagsStr.match(/^(.*?)\[bg:#([0-9a-fA-F]{6})\]$/);
    if (backgroundMatch) {
      backgroundColor = `#${backgroundMatch[2]}`;
      areas = backgroundMatch[1].split(',').map((area: string) => area.trim()).filter((area: string) => area);
    } else {
      // 普通语法
      areas = tagsStr.split(',').map((area: string) => area.trim()).filter((area: string) => area);
    }
    
    const index = tagReplacements.length;
    tagReplacements.push({
      type: 'ResearchTags',
      props: { 
        areas,
        backgroundColor
      }
    });
    return `\n\n<!-- COMPONENT_${index} -->\n\n`;
  });
  
  // 2. 处理具体平台的主页TAG
  const platforms = ['github', 'scholar', 'linkedin', 'researchgate', 'website'];
  platforms.forEach(platform => {
    const regex = new RegExp(`\\{\\{${platform}:\\s*([^}]+)\\}\\}`, 'g');
    content = content.replace(regex, (_, url) => {
      const index = tagReplacements.length;
      tagReplacements.push({
        type: 'HomepageLink',
        props: { 
          url: url.trim(),
          platform: platform
        }
      });
      return `\n\n<!-- COMPONENT_${index} -->\n\n`;
    });
  });
  
  // 处理通用TAG（在特定平台TAG处理之后，避免冲突）
  content = content.replace(/\{\{([^:}]+):\s*([^}]+)\}\}/g, (match, key, value) => {
    // 跳过已经处理的特定TAG
    if (['research', 'papers', 'homepage', 'github', 'scholar', 'linkedin', 'researchgate', 'website'].includes(key.trim())) {
      return match; // 保持原样，让其他处理器处理
    }
    
    const index = tagReplacements.length;
    tagReplacements.push({
      type: 'HomepageLink',
      props: { 
        url: value.trim(),
        platform: 'generic', // 使用 'generic' 作为通用标签
        label: key.trim() // 传递自定义标签名
      }
    });
    return `\n\n<!-- COMPONENT_${index} -->\n\n`;
  });
  
  // 3. 处理论文列表TAG
  content = content.replace(/\{\{papers:\s*([^}]+)\}\}/g, (_, idsStr) => {
    const paperIds = idsStr.split(',').map((id: string) => parseInt(id.trim())).filter((id: number) => !isNaN(id));
    const index = tagReplacements.length;
    tagReplacements.push({
      type: 'PapersList',
      props: { paperIds }
    });
    return `\n\n<!-- COMPONENT_${index} -->\n\n`;
  });
  
  // 4. 处理旧的 homepage 标签格式（向后兼容）
  content = content.replace(/\{\{homepage:\s*([^}]+)\}\}/g, (_, url) => {
    const index = tagReplacements.length;
    tagReplacements.push({
      type: 'HomepageLink',
      props: { 
        url: url.trim(),
        platform: 'auto' // 自动检测平台
      }
    });
    return `\n\n<!-- COMPONENT_${index} -->\n\n`;
  });
  
  // 5. 处理旧的 homepagelink 标签格式（向后兼容）
  content = content.replace(/<homepagelink\s+[^>]*url\s*=\s*"([^"]+)"[^>]*><\/homepagelink>/g, (_, url) => {
    const index = tagReplacements.length;
    tagReplacements.push({
      type: 'HomepageLink',
      props: { 
        url: url.trim(),
        platform: 'auto'
      }
    });
    return `\n\n<!-- COMPONENT_${index} -->\n\n`;
  });
  
  // 6. 处理自闭合的 homepagelink 标签
  content = content.replace(/<homepagelink\s+[^>]*url\s*=\s*"([^"]+)"[^>]*\/>/g, (_, url) => {
    const index = tagReplacements.length;
    tagReplacements.push({
      type: 'HomepageLink',
      props: { 
        url: url.trim(),
        platform: 'auto'
      }
    });
    return `\n\n<!-- COMPONENT_${index} -->\n\n`;
  });
  
  // 7. 清理任何残留的无效 homepagelink 标签
  content = content.replace(/<\/?homepagelink[^>]*>/g, '');
  
  // 渲染markdown
  const renderedHtml = md.render(content);
  
  // 将HTML按组件占位符分割
  const parts = renderedHtml.split(/<!-- COMPONENT_(\d+) -->/);
  const result: ContentItem[] = [];
  
  for (let i = 0; i < parts.length; i++) {
    if (i % 2 === 0) {
      // HTML部分
      const htmlContent = parts[i].trim();
      if (htmlContent) {
        result.push({
          type: 'div',
          props: {
            innerHTML: htmlContent,
            class: 'markdown-content'
          }
        });
      }
    } else {
      // 组件部分
      const componentIndex = parseInt(parts[i]);
      if (tagReplacements[componentIndex]) {
        result.push(tagReplacements[componentIndex]);
      }
    }
  }
  
  return result;
});
</script>

<style scoped>
.markdown-renderer {
  line-height: 1.6;
  color: inherit;
}

/* 基本样式 */
:deep(.markdown-content h1),
:deep(.markdown-content h2),
:deep(.markdown-content h3),
:deep(.markdown-content h4),
:deep(.markdown-content h5),
:deep(.markdown-content h6) {
  margin-top: 1.5em;
  margin-bottom: 0.75em;
  font-weight: 600;
  line-height: 1.25;
}

:deep(.markdown-content h1) { font-size: 2em; }
:deep(.markdown-content h2) { font-size: 1.75em; }
:deep(.markdown-content h3) { font-size: 1.5em; }
:deep(.markdown-content h4) { font-size: 1.25em; }
:deep(.markdown-content h5) { font-size: 1.125em; }
:deep(.markdown-content h6) { font-size: 1em; }

:deep(.markdown-content p) {
  margin-bottom: 1em;
}

:deep(.markdown-content a) {
  color: #1890ff;
  text-decoration: none;
}

:deep(.markdown-content a:hover) {
  text-decoration: underline;
}

:deep(.markdown-content ul),
:deep(.markdown-content ol) {
  margin: 1em 0;
  padding-left: 2em;
}

:deep(.markdown-content li) {
  margin: 0.25em 0;
}

:deep(.markdown-content blockquote) {
  margin: 1em 0;
  padding: 0.75em 1em;
  border-left: 4px solid #1890ff;
  background: #f8f9fa;
  color: #666;
  font-style: italic;
}

:deep(.markdown-content code) {
  background: #f5f5f5;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.9em;
}

:deep(.markdown-content pre) {
  background: #f5f5f5;
  padding: 1em;
  border-radius: 5px;
  overflow-x: auto;
  margin: 1em 0;
}

:deep(.markdown-content pre code) {
  background: none;
  padding: 0;
}

:deep(.markdown-content table) {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

:deep(.markdown-content th),
:deep(.markdown-content td) {
  border: 1px solid #ddd;
  padding: 0.5em;
  text-align: left;
}

:deep(.markdown-content th) {
  background: #f5f5f5;
  font-weight: 600;
}

:deep(.markdown-content img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

/* 暗色主题支持 */
[data-theme="dark"] :deep(.markdown-content blockquote),
.dark :deep(.markdown-content blockquote) {
  background: #2a2a2e;
  color: #ccc;
  border-left-color: #70a1ff;
}

[data-theme="dark"] :deep(.markdown-content code),
.dark :deep(.markdown-content code) {
  background: #2a2a2e;
  color: #f8f9fa;
}

[data-theme="dark"] :deep(.markdown-content pre),
.dark :deep(.markdown-content pre) {
  background: #2a2a2e;
  color: #f8f9fa;
}

[data-theme="dark"] :deep(.markdown-content th),
.dark :deep(.markdown-content th) {
  background: #2a2a2e;
  color: #f8f9fa;
}

[data-theme="dark"] :deep(.markdown-content td),
.dark :deep(.markdown-content td) {
  border-color: #424242;
  color: #f8f9fa;
}

[data-theme="dark"] :deep(.markdown-content a),
.dark :deep(.markdown-content a) {
  color: #70a1ff;
}
</style>