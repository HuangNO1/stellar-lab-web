<template>
  <div class="lab-manage">
    <div class="page-header">
      <h2>{{ t('admin.menu.lab') }}</h2>
      <n-space>
        <n-button 
          type="primary" 
          :loading="saving"
          @click="handleSave"
        >
          <template #icon>
            <n-icon>
              <svg viewBox="0 0 24 24">
                <path fill="currentColor" d="M17,3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V7L17,3M19,19H5V5H16.17L19,7.83V19M12,12C10.34,12 9,13.34 9,15C9,16.66 10.34,18 12,18C13.66,18 15,16.66 15,15C15,13.34 13.66,12 12,12M6,6H15V10H6V6Z"/>
              </svg>
            </n-icon>
          </template>
          {{ t('admin.common.submit') }}
        </n-button>
      </n-space>
    </div>

    <n-spin :show="loading">
      <n-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-placement="left"
        label-width="120"
        require-mark-placement="right-hanging"
        size="medium"
      >
        <!-- 基本信息卡片 -->
        <n-card :title="t('admin.lab.basicInfo')" class="form-card">
          <n-grid :cols="2" :x-gap="24">
            <n-gi>
              <n-form-item :label="t('admin.lab.nameZh')" path="lab_zh">
                <n-input
                  v-model:value="formData.lab_zh"
                  :placeholder="t('admin.lab.placeholders.nameZh')"
                />
              </n-form-item>
            </n-gi>
            <n-gi>
              <n-form-item :label="t('admin.lab.nameEn')" path="lab_en">
                <n-input
                  v-model:value="formData.lab_en"
                  :placeholder="t('admin.lab.placeholders.nameEn')"
                />
              </n-form-item>
            </n-gi>
          </n-grid>

          <n-form-item :label="t('admin.lab.descZh')" path="lab_desc_zh">
            <n-input
              v-model:value="formData.lab_desc_zh"
              type="textarea"
              :rows="3"
              :placeholder="t('admin.lab.placeholders.descZh')"
            />
          </n-form-item>

          <n-form-item :label="t('admin.lab.descEn')" path="lab_desc_en">
            <n-input
              v-model:value="formData.lab_desc_en"
              type="textarea"
              :rows="3"
              :placeholder="t('admin.lab.placeholders.descEn')"
            />
          </n-form-item>
        </n-card>

        <!-- 聯繫信息卡片 -->
        <n-card :title="t('admin.lab.contactInfo')" class="form-card">
          <n-grid :cols="2" :x-gap="24">
            <n-gi>
              <n-form-item :label="t('admin.lab.addressZh')" path="lab_address_zh">
                <n-input
                  v-model:value="formData.lab_address_zh"
                  :placeholder="t('admin.lab.placeholders.addressZh')"
                />
              </n-form-item>
            </n-gi>
            <n-gi>
              <n-form-item :label="t('admin.lab.addressEn')" path="lab_address_en">
                <n-input
                  v-model:value="formData.lab_address_en"
                  :placeholder="t('admin.lab.placeholders.addressEn')"
                />
              </n-form-item>
            </n-gi>
            <n-gi>
              <n-form-item :label="t('admin.lab.email')" path="lab_email">
                <n-input
                  v-model:value="formData.lab_email"
                  :placeholder="t('admin.lab.placeholders.email')"
                />
              </n-form-item>
            </n-gi>
            <n-gi>
              <n-form-item :label="t('admin.lab.phone')" path="lab_phone">
                <n-input
                  v-model:value="formData.lab_phone"
                  :placeholder="t('admin.lab.placeholders.phone')"
                />
              </n-form-item>
            </n-gi>
          </n-grid>
        </n-card>

        <!-- 圖片管理卡片 -->
        <n-card :title="t('admin.lab.imageManagement')" class="form-card">
          <!-- Logo 上傳 -->
          <n-form-item :label="t('admin.lab.logo')" path="lab_logo">
            <div class="upload-section">
              <div v-if="hasLogoToShow" class="image-preview">
                <img :src="getLogoPreview()" :alt="t('admin.lab.logoPreview')" class="logo-preview" />
                <div class="image-actions">
                  <n-button size="small" @click="openLogoCropper">
                    {{ t('admin.imageCropper.cropLogo') }}
                  </n-button>
                  <n-button size="small" type="error" @click="handleLogoRemove">
                    {{ t('admin.common.delete') }}
                  </n-button>
                </div>
              </div>
              <n-button v-else @click="openLogoCropper">
                {{ t('admin.common.fileUpload.selectImage') }}
              </n-button>
            </div>
          </n-form-item>

          <!-- 輪播圖片上傳 -->
          <n-form-item :label="t('admin.lab.carouselImages')">
            <div class="carousel-uploads">
              <div 
                v-for="(carousel, index) in carouselImages" 
                :key="index"
                class="carousel-item"
              >
                <div class="carousel-header">
                  <span>{{ t('admin.lab.carouselImage', { number: index + 1 }) }}</span>
                </div>
                <div class="upload-section">
                  <div v-if="hasCarouselToShow(index)" class="image-preview">
                    <img :src="getCarouselPreview(index)" :alt="t('admin.lab.carouselPreview', { number: index + 1 })" class="carousel-preview" />
                    <div class="image-actions">
                      <n-button size="small" @click="openCarouselCropper(index)">
                        {{ t('admin.imageCropper.cropCarousel') }}
                      </n-button>
                      <n-button size="small" type="error" @click="handleCarouselRemove(index)">
                        {{ t('admin.common.delete') }}
                      </n-button>
                    </div>
                  </div>
                  <n-button v-else size="small" @click="openCarouselCropper(index)">
                    {{ t('admin.common.fileUpload.selectImage') }}
                  </n-button>
                </div>
              </div>
            </div>
          </n-form-item>
        </n-card>
      </n-form>
    </n-spin>
    
    <!-- 圖片裁切 Modal -->
    <ImageCropperModal
      v-model="showCropper"
      :crop-type="cropType"
      @cropped="handleCroppedImage"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useMessage } from 'naive-ui';
import { labApi } from '@/services/api';
import { getMediaUrl } from '@/utils/media';
import ImageCropperModal from '@/components/ImageCropperModal.vue';
import type { Lab } from '@/types/api';
import type { FormInst, FormRules, UploadFileInfo } from 'naive-ui';

const { t } = useI18n();
const message = useMessage();

// Refs
const formRef = ref<FormInst>();
const loading = ref(false);
const saving = ref(false);

// Form data
const formData = reactive<Partial<Lab>>({
  lab_zh: '',
  lab_en: '',
  lab_desc_zh: '',
  lab_desc_en: '',
  lab_address_zh: '',
  lab_address_en: '',
  lab_email: '',
  lab_phone: ''
});

// 原始實驗室數據（用於比較是否有現有圖片）
const originalLabData = ref<Partial<Lab>>({});

// Image upload states
const logoFileList = ref<UploadFileInfo[]>([]);
const logoPreview = ref<string>('');
const logoFile = ref<File | null>(null);
const logoShouldDelete = ref<boolean>(false);

interface CarouselImage {
  fileList: UploadFileInfo[];
  preview: string;
  file: File | null;
  shouldClear: boolean;
}

const carouselImages = ref<CarouselImage[]>([
  { fileList: [], preview: '', file: null, shouldClear: false },
  { fileList: [], preview: '', file: null, shouldClear: false },
  { fileList: [], preview: '', file: null, shouldClear: false },
  { fileList: [], preview: '', file: null, shouldClear: false }
]);

// Image cropper states
const showCropper = ref(false);
const cropType = ref<'avatar' | 'logo' | 'carousel'>('logo');
const currentImageType = ref<'logo' | 'carousel'>('logo');
const currentCarouselIndex = ref<number>(-1);

// 計算是否有 Logo 需要顯示
const hasLogoToShow = computed(() => {
  // 如果有新上傳的文件
  if (logoFile.value) {
    return true;
  }
  
  // 如果有現有的 Logo 且沒有被標記為刪除
  if (originalLabData.value.lab_logo_path && !logoShouldDelete.value) {
    return true;
  }
  
  return false;
});

// 獲取 Logo 預覽 URL
const getLogoPreview = () => {
  // 優先顯示新上傳的文件
  if (logoFile.value) {
    return URL.createObjectURL(logoFile.value);
  }
  
  // 顯示現有的 Logo
  if (originalLabData.value.lab_logo_path && !logoShouldDelete.value) {
    return getMediaUrl(originalLabData.value.lab_logo_path);
  }
  
  return '';
};

// 檢查輪播圖是否需要顯示
const hasCarouselToShow = (index: number) => {
  const carousel = carouselImages.value[index];
  
  // 如果有新上傳的文件
  if (carousel.file) {
    return true;
  }
  
  // 如果有現有的輪播圖且沒有被標記為清除
  const carouselField = `carousel_img_${index + 1}` as keyof Lab;
  if (originalLabData.value[carouselField] && !carousel.shouldClear) {
    return true;
  }
  
  return false;
};

// 獲取輪播圖預覽 URL
const getCarouselPreview = (index: number) => {
  const carousel = carouselImages.value[index];
  
  // 優先顯示新上傳的文件
  if (carousel.file) {
    return URL.createObjectURL(carousel.file);
  }
  
  // 顯示現有的輪播圖
  const carouselField = `carousel_img_${index + 1}` as keyof Lab;
  if (originalLabData.value[carouselField] && !carousel.shouldClear) {
    return getMediaUrl(originalLabData.value[carouselField] as string);
  }
  
  return '';
};

// Form validation rules
const formRules: FormRules = {
  lab_zh: {
    required: true,
    message: t('admin.lab.validation.nameZhRequired'),
    trigger: ['blur', 'input']
  },
  lab_en: {
    required: true,
    message: t('admin.lab.validation.nameEnRequired'),
    trigger: ['blur', 'input']
  },
  lab_email: {
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    message: t('admin.common.validationMessages.invalidEmail'),
    trigger: ['blur', 'input']
  }
};

// Methods
const fetchLabData = async () => {
  try {
    loading.value = true;
    const response = await labApi.getLab();
    if (response.code === 0 && response.data) {
      // 保存原始數據
      originalLabData.value = { ...response.data };
      
      // 更新表單數據
      Object.assign(formData, response.data);
      
      // 重置刪除標記
      logoShouldDelete.value = false;
      
      // 重置輪播圖狀態
      carouselImages.value.forEach(carousel => {
        carousel.shouldClear = false;
      });
      
      // 清除之前的預覽（因為現在會通過 computed 屬性自動處理）
      logoPreview.value = '';
      carouselImages.value.forEach(carousel => {
        carousel.preview = '';
      });
    }
  } catch (error) {
    console.error('Failed to fetch lab data:', error);
    message.error(t('admin.lab.messages.fetchFailed'));
  } finally {
    loading.value = false;
  }
};

const handleLogoChange = ({ fileList }: { fileList: UploadFileInfo[] }) => {
  logoFileList.value = fileList;
  if (fileList.length > 0 && fileList[0].file) {
    logoFile.value = fileList[0].file;
    const reader = new FileReader();
    reader.onload = (e) => {
      logoPreview.value = e.target?.result as string;
    };
    reader.readAsDataURL(fileList[0].file);
  }
};

const handleLogoRemove = () => {
  logoFileList.value = [];
  logoFile.value = null;
  logoPreview.value = '';
  
  // 如果有現有的 Logo，標記為刪除
  if (originalLabData.value.lab_logo_path) {
    logoShouldDelete.value = true;
  }
};

const handleCarouselChange = (index: number, { fileList }: { fileList: UploadFileInfo[] }) => {
  carouselImages.value[index].fileList = fileList;
  if (fileList.length > 0 && fileList[0].file) {
    carouselImages.value[index].file = fileList[0].file;
    const reader = new FileReader();
    reader.onload = (e) => {
      carouselImages.value[index].preview = e.target?.result as string;
    };
    reader.readAsDataURL(fileList[0].file);
  }
  carouselImages.value[index].shouldClear = false;
};

const handleCarouselRemove = (index: number) => {
  carouselImages.value[index].fileList = [];
  carouselImages.value[index].file = null;
  carouselImages.value[index].preview = '';
  
  // 如果有現有的輪播圖，標記為清除
  const carouselField = `carousel_img_${index + 1}` as keyof Lab;
  if (originalLabData.value[carouselField]) {
    carouselImages.value[index].shouldClear = true;
  }
};

// Image cropper methods
const openLogoCropper = () => {
  currentImageType.value = 'logo';
  cropType.value = 'logo';
  showCropper.value = true;
};

const openCarouselCropper = (index: number) => {
  currentImageType.value = 'carousel';
  currentCarouselIndex.value = index;
  cropType.value = 'carousel';
  showCropper.value = true;
};

const handleCroppedImage = (croppedFile: File) => {
  if (currentImageType.value === 'logo') {
    logoFile.value = croppedFile;
    logoPreview.value = URL.createObjectURL(croppedFile);
    logoShouldDelete.value = false; // 上傳新文件時清除刪除標記
  } else if (currentImageType.value === 'carousel' && currentCarouselIndex.value >= 0) {
    const index = currentCarouselIndex.value;
    carouselImages.value[index].file = croppedFile;
    carouselImages.value[index].preview = URL.createObjectURL(croppedFile);
    carouselImages.value[index].shouldClear = false;
  }
};

const handleSave = async () => {
  try {
    await formRef.value?.validate();
    saving.value = true;

    const formDataToSend = new FormData();

    // 清理並添加基本信息，確保不包含函數或無效值
    Object.keys(formData).forEach(key => {
      const value = formData[key as keyof typeof formData];
      
      // 檢查是否為有效值
      const isValidValue = value !== null && 
                          value !== undefined && 
                          value !== '' &&
                          typeof value !== 'function';
      
      // 對於對象類型，只允許基本數據類型
      const isValidObject = typeof value !== 'object' || 
                           Array.isArray(value) || 
                           (value != null && typeof value === 'object' && (value as object) instanceof Date);
      
      if (isValidValue && isValidObject) {
        formDataToSend.append(key, String(value));
      }
    });

    // 添加 logo 文件或刪除標記
    if (logoFile.value !== null && logoFile.value instanceof File) {
      formDataToSend.append('lab_logo', logoFile.value);
    } else if (logoShouldDelete.value) {
      formDataToSend.append('lab_logo_delete', 'true');
    }

    // 添加輪播圖文件
    carouselImages.value.forEach((carousel, index) => {
      if (carousel.file !== null && carousel.file instanceof File) {
        formDataToSend.append(`carousel_img_${index + 1}`, carousel.file);
      } else if (carousel.shouldClear) {
        formDataToSend.append(`clear_carousel_img_${index + 1}`, 'true');
      }
    });

    const response = await labApi.updateLab(formDataToSend);
    if (response.code === 0) {
      message.success(t('admin.lab.messages.saveSuccess'));
      // 重新獲取數據以更新預覽和原始數據
      await fetchLabData();
    } else {
      message.error(response.message || t('admin.lab.messages.saveFailed'));
    }
  } catch (error) {
    console.error('Save lab data failed:', error);
    if (error && typeof error === 'object' && 'message' in error) {
      message.error((error as { message: string }).message);
    } else {
      message.error(t('admin.lab.messages.saveFailed'));
    }
  } finally {
    saving.value = false;
  }
};

// Lifecycle
onMounted(() => {
  fetchLabData();
});
</script>

<style scoped>
.lab-manage {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.5rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.page-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

.form-card {
  margin-bottom: 1.5rem;
}

.upload-section {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.upload-area {
  flex-shrink: 0;
}

.image-preview {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border: 2px dashed #e0e0e0;
  border-radius: 8px;
  background-color: #fafafa;
}

.logo-preview {
  max-width: 200px;
  max-height: 100px;
  object-fit: contain;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
  display: block;
}

.carousel-preview {
  width: 200px;
  height: auto;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
  display: block;
}

.image-actions {
  display: flex;
  gap: 0.5rem;
}

.carousel-uploads {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.carousel-item {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  background: #f9fafb;
}

.carousel-header {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

/* 暗色主題 */
[data-theme="dark"] .page-header h2,
.dark .page-header h2,
.dark-mode .page-header h2 {
  color: #f9fafb;
}

[data-theme="dark"] .carousel-item,
.dark .carousel-item,
.dark-mode .carousel-item {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

[data-theme="dark"] .carousel-header,
.dark .carousel-header,
.dark-mode .carousel-header {
  color: #e5e7eb;
}

[data-theme="dark"] .image-preview,
.dark .image-preview,
.dark-mode .image-preview {
  border-color: rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .logo-preview,
.dark .logo-preview,
.dark-mode .logo-preview,
[data-theme="dark"] .carousel-preview,
.dark .carousel-preview,
.dark-mode .carousel-preview {
  border-color: rgba(255, 255, 255, 0.1);
}

/* 響應式設計 */
@media (max-width: 768px) {
  .lab-manage {
    padding: 1rem;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .upload-section {
    flex-direction: column;
  }
  
  .carousel-uploads {
    grid-template-columns: 1fr;
  }
}
</style>