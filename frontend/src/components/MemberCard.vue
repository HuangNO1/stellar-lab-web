<template>
  <div class="member-card" @click="onCardClick">
    <n-avatar
      :round="true"
      :size="avatarSize"
      :src="getMemberAvatar(member) || '/default-avatar.svg'"
      :fallback-src="'/default-avatar.svg'"
      class="member-avatar"
    />
    <div class="member-info">
      <n-tooltip trigger="hover" :disabled="!isNameTruncated">
        <template #trigger>
          <div class="member-name">
            {{ displayName }}
          </div>
        </template>
        {{ displayName }}
      </n-tooltip>
      <n-tooltip trigger="hover" :disabled="!isPositionTruncated">
        <template #trigger>
          <div class="member-position">
            {{ displayPosition }}
          </div>
        </template>
        {{ fullPosition }}
      </n-tooltip>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useMembers } from '@/composables/useMembers';
import type { Member } from '@/types/api';

interface Props {
  member: Member;
  avatarSize?: number;
  showGraduationInfo?: boolean;
}

interface Emits {
  (e: 'click', memberId: number): void;
}

const props = withDefaults(defineProps<Props>(), {
  avatarSize: 60,
  showGraduationInfo: false
});

const emit = defineEmits<Emits>();

const { locale } = useI18n();
const { getMemberAvatar, getMemberPosition } = useMembers();

// 獲取當前語言
const getCurrentLocale = () => {
  return locale.value as 'zh' | 'en';
};

// 顯示的名稱
const displayName = computed(() => {
  return getCurrentLocale() === 'zh' ? props.member.mem_name_zh : props.member.mem_name_en;
});

// 顯示的職位信息（校友只顯示去向）
const displayPosition = computed(() => {
  if (props.member.mem_type === 2 || (props.member.mem_type === 1 && (props.member.destination_zh || props.member.destination_en))) {
    // 校友类型，只显示去向
    const destination = getCurrentLocale() === 'zh' ? props.member.destination_zh : props.member.destination_en;
    return destination || getMemberPosition(props.member);
  }
  return getMemberPosition(props.member);
});

// 完整的職位信息（用於tooltip）
const fullPosition = computed(() => {
  return getMemberPosition(props.member);
});

// 判斷名字是否被截斷
const isNameTruncated = computed(() => {
  const name = displayName.value;
  return getCurrentLocale() === 'zh' ? (name?.length || 0) > 7 : (name?.length || 0) > 15;
});

// 判斷職位是否需要顯示tooltip
const isPositionTruncated = computed(() => {
  // 對於校友，如果完整信息比顯示信息更詳細，就需要顯示 tooltip
  if (props.member.mem_type === 2 || (props.member.mem_type === 1 && (props.member.destination_zh || props.member.destination_en))) {
    // 校友總是顯示 tooltip，因為完整信息包含身份、年份等詳細信息
    return fullPosition.value !== displayPosition.value;
  }
  
  // 對於其他成員，按原邏輯判斷文字是否被截斷
  const position = displayPosition.value;
  return getCurrentLocale() === 'zh' ? (position?.length || 0) > 8 : (position?.length || 0) > 18;
});

// 卡片點擊事件
const onCardClick = () => {
  emit('click', props.member.mem_id);
};
</script>

<style scoped>
.member-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border-radius: 0.75rem;
  background: #fff;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 0.125rem solid transparent;
  /* 固定尺寸 */
  width: 10rem;
  min-width: 10rem;
  max-width: 10rem;
  height: 9rem;
  min-height: 9rem;
  max-height: 9rem;
  flex-shrink: 0;
}

/* 小屏幕調整 */
@media (max-width: 30rem) {
  .member-card {
    width: 8rem;
    min-width: 8rem;
    max-width: 8rem;
    height: 8rem;
    min-height: 8rem;
    max-height: 8rem;
  }
}

.member-card:hover {
  transform: translateY(-0.25rem);
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.15);
  border-color: #1890ff;
}

.member-info {
  text-align: center;
  margin-top: 0.75rem;
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: visible;
  padding: 0 4px;
}

.member-name {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #333;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
  min-height: 1.26rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.member-position {
  font-size: 0.8rem;
  color: #666;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
  min-height: 1.12rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 暗色主題支持 */
[data-theme="dark"] .member-card,
.dark .member-card,
.dark-mode .member-card {
  background: rgba(255, 255, 255, 0.08) !important;
  border-color: transparent !important;
}

[data-theme="dark"] .member-card:hover,
.dark .member-card:hover,
.dark-mode .member-card:hover {
  background: rgba(255, 255, 255, 0.12) !important;
  border-color: #70a1ff !important;
}

[data-theme="dark"] .member-name,
.dark .member-name,
.dark-mode .member-name {
  color: #fff !important;
}

[data-theme="dark"] .member-position,
.dark .member-position,
.dark-mode .member-position {
  color: #ccc !important;
}

/* 成員頭像固定樣式 */
.member-avatar {
  flex-shrink: 0;
  width: 60px !important;
  height: 60px !important;
  border-radius: 50% !important;
  object-fit: cover;
}

/* 不同屏幕尺寸下的頭像調整 */
@media (max-width: 1024px) {
  .member-card .member-avatar {
    width: 50px !important;
    height: 50px !important;
  }
}

@media (max-width: 640px) {
  .member-card .member-avatar {
    width: 45px !important;
    height: 45px !important;
  }
}

@media (max-width: 30rem) {
  .member-card .member-avatar {
    width: 40px !important;
    height: 40px !important;
  }
}

/* 響應式設計 - 改善版 */
@media (max-width: 1024px) {
  .member-card {
    width: 9rem;
    min-width: 9rem;
    max-width: 9rem;
    height: 8.5rem;
    min-height: 8.5rem;
    max-height: 8.5rem;
  }
  
  .member-name {
    font-size: 0.875rem;
  }
  
  .member-position {
    font-size: 0.75rem;
  }
}

@media (max-width: 768px) {
  .member-card {
    width: 8.5rem;
    min-width: 8.5rem;
    max-width: 8.5rem;
    height: 8.5rem;
    min-height: 8.5rem;
    max-height: 8.5rem;
  }
  
  .member-info {
    margin-top: 0.5rem;
    padding: 0 3px;
  }
  
  .member-name {
    font-size: 0.85rem;
    line-height: 1.4;
    min-height: 1.19rem;
    margin-bottom: 0.2rem;
  }
  
  .member-position {
    font-size: 0.7rem;
    line-height: 1.4;
    min-height: 0.98rem;
  }
}

@media (max-width: 640px) {
  .member-card {
    width: 8rem;
    min-width: 8rem;
    max-width: 8rem;
    height: 8rem;
    min-height: 8rem;
    max-height: 8rem;
    padding: 0.75rem;
  }
  
  .member-info {
    margin-top: 0.4rem;
    padding: 0 2px;
  }
  
  .member-name {
    font-size: 0.8rem;
    margin-bottom: 0.15rem;
    min-height: 1.12rem;
  }
  
  .member-position {
    font-size: 0.65rem;
    min-height: 0.91rem;
  }
}

@media (max-width: 48rem) {
  .member-name {
    font-size: 0.85rem;
    line-height: 1.4;
    min-height: 1.19rem;
  }
  
  .member-position {
    font-size: 0.75rem;
    line-height: 1.4;
    min-height: 1.05rem;
  }
}

/* 小屏幕調整 - 優化版 */
@media (max-width: 30rem) {
  .member-card {
    width: 7.5rem;
    min-width: 7.5rem;
    max-width: 7.5rem;
    height: 7.5rem;
    min-height: 7.5rem;
    max-height: 7.5rem;
    padding: 0.6rem 0.4rem;
  }
  
  .member-info {
    margin-top: 0.3rem;
    padding: 0 2px;
  }
  
  .member-name {
    font-size: 0.75rem;
    min-height: 1.05rem;
    margin-bottom: 0.1rem;
  }
  
  .member-position {
    font-size: 0.6rem;
    min-height: 0.84rem;
  }
}
</style>