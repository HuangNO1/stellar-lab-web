<template>
  <n-modal v-model:show="show" @update:show="handleModalClose" class="image-cropper-modal">
    <n-card
      :style="{ width: isMobile ? '95vw' : '800px', maxWidth: isMobile ? '95vw' : '800px' }"
      :title="modalTitle"
      :bordered="false"
      :size="isMobile ? 'medium' : 'huge'"
      role="dialog"
      aria-modal="true"
      class="modal-card"
    >
      <template #header-extra>
        <n-button
          quaternary
          circle
          @click="show = false"
        >
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
              </svg>
            </n-icon>
          </template>
        </n-button>
      </template>

      <div class="cropper-container">
        <!-- 文件選擇區域 -->
        <div v-if="!selectedFile" class="file-selector">
          <n-upload
            :show-file-list="false"
            accept="image/*"
            :on-change="handleFileSelect"
          >
            <n-upload-dragger>
              <div style="margin-bottom: 12px">
                <n-icon size="48" :depth="3">
                  <svg viewBox="0 0 24 24">
                    <path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                  </svg>
                </n-icon>
              </div>
              <n-text style="font-size: 16px">
                {{ $t('admin.imageCropper.selectImage') }}
              </n-text>
              <n-p :depth="3" style="margin: 8px 0 0 0">
                {{ $t('admin.imageCropper.supportedFormats') }}
              </n-p>
              <n-p :depth="3" style="margin: 4px 0 0 0; font-size: 13px; font-style: italic;">
                {{ getAspectRatioHint() }}
              </n-p>
            </n-upload-dragger>
          </n-upload>
        </div>

        <!-- 裁切區域 -->
        <div v-if="selectedFile" class="cropper-area">
          <VuePictureCropper
            ref="cropperRef"
            :boxStyle="{
              width: '100%',
              height: '400px',
              backgroundColor: '#f6f6f6',
              margin: 'auto',
            }"
            :img="previewSrc"
            :options="{
              viewMode: 1,
              dragMode: 'crop',
              aspectRatio: aspectRatio,
              autoCropArea: 0.8,
              restore: false,
              guides: true,
              center: true,
              highlight: false,
              cropBoxMovable: true,
              cropBoxResizable: true,
              toggleDragModeOnDblclick: false,
            }"
            @ready="onCropperReady"
          />
        </div>

        <!-- 預設比例選擇 -->
        <div v-if="cropType === 'carousel'" class="aspect-ratio-selector">
          <div class="selector-title">{{ $t('admin.imageCropper.aspectRatio') }}</div>
          <n-radio-group v-model:value="selectedAspectRatio" @update:value="handleAspectRatioChange">
            <n-radio-button 
              v-for="ratio in aspectRatioOptions" 
              :key="ratio.value" 
              :value="ratio.value"
              :label="ratio.label"
            >
              {{ ratio.label }}
            </n-radio-button>
          </n-radio-group>
        </div>
      </div>

      <template #footer>
        <div class="modal-footer">
          <n-button @click="show = false">
            {{ $t('admin.common.cancel') }}
          </n-button>
          <n-button 
            v-if="selectedFile" 
            @click="resetCropper"
          >
            {{ $t('admin.imageCropper.reselect') }}
          </n-button>
          <n-button
            v-if="selectedFile"
            type="primary"
            :loading="processing"
            @click="handleCrop"
          >
            {{ $t('admin.imageCropper.cropAndSave') }}
          </n-button>
        </div>
      </template>
    </n-card>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useMessage } from 'naive-ui';
import { useI18n } from 'vue-i18n';
import VuePictureCropper, { cropper } from 'vue-picture-cropper';

// Props
interface Props {
  modelValue: boolean;
  cropType: 'avatar' | 'logo' | 'carousel';
}

const props = defineProps<Props>();

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: boolean];
  'cropped': [file: File];
}>();

const { t } = useI18n();
const message = useMessage();

// Reactive data
const show = ref(props.modelValue);
const selectedFile = ref<File | null>(null);
const previewSrc = ref<string>('');
const processing = ref(false);
const isMobile = ref(window.innerWidth <= 768);
const cropperRef = ref();
const selectedAspectRatio = ref<number>(16/9);
const cropperReady = ref(false);

// 裁切類型對應的比例
const aspectRatio = computed(() => {
  switch (props.cropType) {
    case 'avatar':
      return 1; // 正方形
    case 'logo':
      return NaN; // 不限比例
    case 'carousel':
      return selectedAspectRatio.value;
    default:
      return NaN;
  }
});

// Cropper ready handler
const onCropperReady = () => {
  console.log('Cropper ready');
  cropperReady.value = true;
};

// 輪播圖片比例選項
const aspectRatioOptions = [
  { label: '16:9', value: 16/9 },
  { label: '16:10', value: 16/10 },
  { label: '4:3', value: 4/3 },
  { label: '3:2', value: 3/2 },
  { label: '21:9', value: 21/9 }
];

// Modal 標題
const modalTitle = computed(() => {
  const typeMap = {
    avatar: t('admin.imageCropper.cropAvatar'),
    logo: t('admin.imageCropper.cropLogo'),
    carousel: t('admin.imageCropper.cropCarousel')
  };
  return typeMap[props.cropType];
});

// 獲取比例提示文字
const getAspectRatioHint = () => {
  const hintMap = {
    avatar: t('admin.imageCropper.avatarHint'),
    logo: t('admin.imageCropper.logoHint'),
    carousel: t('admin.imageCropper.carouselHint')
  };
  return hintMap[props.cropType];
};

// 檢查屏幕尺寸
const checkScreenSize = () => {
  isMobile.value = window.innerWidth <= 768;
};

// 監聽 Props 變化
watch(() => props.modelValue, (newValue) => {
  show.value = newValue;
  if (newValue) {
    resetCropper();
  }
});

watch(show, (newValue) => {
  emit('update:modelValue', newValue);
});

// 處理文件選擇
const handleFileSelect = (event: { file: { file: File } }) => {
  const file = event.file.file;
  if (file && file.type.startsWith('image/')) {
    selectedFile.value = file;
    
    // 創建預覽 URL
    const reader = new FileReader();
    reader.onload = (e) => {
      previewSrc.value = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  } else {
    message.error(t('admin.imageCropper.invalidFormat'));
  }
};

// 處理比例變化
const handleAspectRatioChange = (ratio: number) => {
  // Use the global cropper instance to change aspect ratio
  if (cropper) {
    cropper.setAspectRatio(ratio);
  }
};

// 重置裁切器
const resetCropper = () => {
  selectedFile.value = null;
  previewSrc.value = '';
  selectedAspectRatio.value = 16/9;
};

// 處理裁切
const handleCrop = async () => {
  if (!selectedFile.value || !previewSrc.value) {
    message.error('No image selected for cropping');
    return;
  }
  
  try {
    processing.value = true;
    
    console.log('Starting crop operation...');
    console.log('Cropper ready state:', cropperReady.value);
    console.log('Preview src:', previewSrc.value);
    console.log('Global cropper instance:', cropper);
    
    // Wait a bit to ensure cropper is fully initialized
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // Check if global cropper instance is available
    if (!cropper) {
      throw new Error('Cropper instance not available');
    }
    
    console.log('Attempting to get blob...');
    
    // Try different approaches to get the blob
    let blob;
    
    // Method 1: Basic getBlob
    try {
      blob = await cropper.getBlob();
      console.log('Method 1 - Basic getBlob result:', blob);
    } catch (error) {
      console.log('Method 1 failed:', error);
    }
    
    // Method 2: getBlob with options
    if (!blob) {
      try {
        blob = await cropper.getBlob({
          type: 'image/png'
        });
        console.log('Method 2 - getBlob with PNG result:', blob);
      } catch (error) {
        console.log('Method 2 failed:', error);
      }
    }
    
    // Method 3: Try getDataURL and convert to blob
    if (!blob) {
      try {
        const dataURL = cropper.getDataURL();
        console.log('Method 3 - getDataURL result length:', dataURL?.length);
        if (dataURL) {
          // Convert dataURL to blob
          const response = await fetch(dataURL);
          blob = await response.blob();
          console.log('Method 3 - Converted blob:', blob);
        }
      } catch (error) {
        console.log('Method 3 failed:', error);
      }
    }
    
    if (!blob) {
      throw new Error('All methods failed to get cropped image blob');
    }
    
    // 創建新的 File 對象
    const timestamp = Date.now();
    const extension = selectedFile.value.name.split('.').pop() || 'jpg';
    const croppedFile = new File([blob], `cropped_${timestamp}.${extension}`, {
      type: blob.type || 'image/jpeg'
    });
    
    emit('cropped', croppedFile);
    show.value = false;
    message.success(t('admin.imageCropper.cropSuccess'));
    
  } catch (error) {
    console.error('Crop error:', error);
    message.error(t('admin.imageCropper.cropFailed'));
  } finally {
    processing.value = false;
  }
};

// 處理 Modal 關閉
const handleModalClose = (value: boolean) => {
  if (!value) {
    resetCropper();
  }
};

// 生命週期
onMounted(() => {
  window.addEventListener('resize', checkScreenSize);
  checkScreenSize();
});

onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize);
  // 清理 URL
  if (previewSrc.value) {
    URL.revokeObjectURL(previewSrc.value);
  }
});
</script>

<style scoped>
.image-cropper-modal :deep(.n-modal) {
  padding: 1rem;
}

.modal-card {
  margin: 0 auto;
}

.cropper-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.file-selector {
  width: 100%;
}

.cropper-area {
  width: 100%;
}

.aspect-ratio-selector {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  align-items: center;
}

.selector-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 1rem;
}

/* 移動端調整 */
@media (max-width: 768px) {
  .image-cropper-modal :deep(.n-modal) {
    padding: 0.5rem;
  }
  
  .modal-card :deep(.n-card__header) {
    padding: 1rem 1rem 0.75rem 1rem;
    font-size: 1.125rem;
  }
  
  .modal-card :deep(.n-card__content) {
    padding: 0.75rem 1rem;
  }
  
  .modal-card :deep(.n-card__footer) {
    padding: 0.75rem 1rem 1rem 1rem;
  }
  
  .cropper-area :deep(.vue-picture-cropper) {
    height: 300px !important;
  }
  
  .aspect-ratio-selector {
    flex-direction: column;
    gap: 1rem;
  }
  
  .aspect-ratio-selector :deep(.n-radio-group) {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .modal-footer {
    flex-direction: column-reverse;
    gap: 0.75rem;
  }
  
  .modal-footer .n-button {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .image-cropper-modal :deep(.n-modal) {
    padding: 0.25rem;
  }
  
  .cropper-area :deep(.vue-picture-cropper) {
    height: 250px !important;
  }
}

/* 暗色主題 */
[data-theme="dark"] .selector-title,
.dark .selector-title {
  color: #f9fafb;
}

[data-theme="dark"] .cropper-area :deep(.vue-picture-cropper),
.dark .cropper-area :deep(.vue-picture-cropper) {
  background-color: #1f2937 !important;
}
</style>