<template>
  <n-button
    :href="validUrl"
    tag="a"
    target="_blank"
    rel="noopener noreferrer"
    :type="buttonType"
    strong
    secondary
    round
    size="medium"
    style="margin: 0.25rem;"
  >
    <template #icon>
      <n-icon size="16">
        <component :is="linkIcon" />
      </n-icon>
    </template>
    {{ linkText }}
  </n-button>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { 
  LogoGithub as GithubIcon,
  School as ScholarIcon,
  Globe as WebIcon,
  LogoLinkedin as LinkedInIcon,
  Newspaper as ResearchGateIcon
} from '@vicons/ionicons5';

// Props
interface Props {
  url: string;
  platform?: 'github' | 'scholar' | 'linkedin' | 'researchgate' | 'website' | 'auto' | 'generic';
  label?: string; // 自定义标签文本（用于通用TAG）
}

const props = withDefaults(defineProps<Props>(), {
  platform: 'auto'
});

// 验证并格式化URL
const validUrl = computed(() => {
  let url = props.url.trim();
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = `https://${url}`;
  }
  return url;
});

// 检测平台类型（如果是 auto 模式）
const detectedPlatform = computed(() => {
  if (props.platform !== 'auto') {
    return props.platform;
  }
  
  const url = props.url.toLowerCase();
  if (url.includes('github.com')) {
    return 'github';
  } else if (url.includes('scholar.google')) {
    return 'scholar';
  } else if (url.includes('linkedin.com')) {
    return 'linkedin';
  } else if (url.includes('researchgate.net')) {
    return 'researchgate';
  } else {
    return 'website';
  }
});

// 根据平台确定按钮类型
const buttonType = computed(() => {
  const platform = detectedPlatform.value;
  
  switch (platform) {
    case 'github':
      return 'default';
    case 'scholar':
      return 'info';
    case 'linkedin':
      return 'primary';
    case 'researchgate':
      return 'success';
    case 'website':
      return 'warning';
    case 'generic':
      return 'tertiary'; // 通用TAG使用不同的样式
    default:
      return 'default';
  }
});

// 根据平台选择图标
const linkIcon = computed(() => {
  const platform = detectedPlatform.value;
  
  switch (platform) {
    case 'github':
      return GithubIcon;
    case 'scholar':
      return ScholarIcon;
    case 'linkedin':
      return LinkedInIcon;
    case 'researchgate':
      return ResearchGateIcon;
    case 'website':
    case 'generic': // 通用TAG也使用Web图标
    default:
      return WebIcon;
  }
});

// 根据平台生成链接文本
const linkText = computed(() => {
  // 如果有自定义标签文本，优先使用
  if (props.label) {
    return props.label;
  }
  
  const platform = detectedPlatform.value;
  
  switch (platform) {
    case 'github':
      return 'GitHub';
    case 'scholar':
      return 'Google Scholar';
    case 'linkedin':
      return 'LinkedIn';
    case 'researchgate':
      return 'ResearchGate';
    case 'website':
      return '個人網站';
    case 'generic':
      return '訪問鏈接';
    default:
      return '訪問鏈接';
  }
});
</script>