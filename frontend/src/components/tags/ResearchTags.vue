<template>
  <div 
    class="research-tags-container"
    :style="containerStyle"
  >
    <n-space>
      <n-tag
        v-for="(area, index) in processedAreas"
        :key="area.text"
        :type="area.color ? undefined : getTagType(index)"
        :style="area.color ? { backgroundColor: area.color, color: getTextColor(area.color), border: `1px solid ${area.color}` } : {}"
        round
        strong
        size="medium"
      >
        {{ area.text }}
      </n-tag>
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// Props
interface Props {
  areas: string[];
  backgroundColor?: string; // 容器背景色
}

const props = withDefaults(defineProps<Props>(), {
  backgroundColor: undefined
});

// 容器样式计算
const containerStyle = computed(() => {
  if (!props.backgroundColor) {
    return {};
  }
  
  return {
    backgroundColor: props.backgroundColor,
    padding: '0.75rem',
    borderRadius: '8px',
    border: `1px solid ${props.backgroundColor}`
  };
});

// 处理研究领域，支持颜色语法
const processedAreas = computed(() => {
  return props.areas.map(area => {
    // 检查是否包含颜色语法：文本#颜色
    const colorMatch = area.match(/^(.+?)#([0-9a-fA-F]{6})$/);
    if (colorMatch) {
      return {
        text: colorMatch[1].trim(),
        color: `#${colorMatch[2]}`
      };
    }
    return {
      text: area.trim(),
      color: null
    };
  });
});

// 循環使用不同的標籤類型來創建豐富的顏色效果
// 按照要求的顺序：蓝色、资讯蓝、绿色、橙色、红色  
const getTagType = (index: number) => {
  const types = ['info', 'primary', 'success', 'warning', 'error']; // info是蓝色，primary是资讯蓝
  return types[index % types.length];
};

// 根据背景颜色计算合适的文字颜色
const getTextColor = (hexColor: string): string => {
  // 移除#号
  const hex = hexColor.replace('#', '');
  
  // 转换为RGB
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);
  
  // 计算亮度 (使用相对亮度公式)
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  
  // 如果背景较亮使用深色文字，否则使用浅色文字
  return brightness > 128 ? '#000000' : '#ffffff';
};
</script>

<style scoped>
.research-tags-container {
  margin: 0.5rem 0;
  transition: all 0.3s ease;
}

/* 当有自定义背景色时的额外样式 */
.research-tags-container[style*="backgroundColor"] {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 自定义颜色标签的额外样式 */
:deep(.n-tag[style*="backgroundColor"]) {
  font-weight: 600;
  border-width: 1px !important;
  border-style: solid !important;
}

/* 确保自定义颜色标签在暗色模式下也显示正确 */
[data-theme="dark"] :deep(.n-tag[style*="backgroundColor"]),
.dark :deep(.n-tag[style*="backgroundColor"]) {
  border-width: 1px !important;
  border-style: solid !important;
}

/* 暗色模式下的容器样式 */
[data-theme="dark"] .research-tags-container[style*="backgroundColor"],
.dark .research-tags-container[style*="backgroundColor"] {
  box-shadow: 0 2px 8px rgba(255, 255, 255, 0.1);
}
</style>