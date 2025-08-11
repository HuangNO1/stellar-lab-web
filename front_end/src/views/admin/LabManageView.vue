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
              <div class="upload-area">
                <n-upload
                  :file-list="logoFileList"
                  :max="1"
                  accept="image/*"
                  @change="handleLogoChange"
                  @remove="handleLogoRemove"
                  :show-file-list="false"
                >
                  <n-button>{{ t('admin.common.fileUpload.selectImage') }}</n-button>
                </n-upload>
              </div>
              <div class="image-preview" v-if="logoPreview">
                <img :src="logoPreview" alt="Logo Preview" class="preview-image" />
                <div class="image-actions">
                  <n-button size="small" @click="handleLogoRemove">
                    {{ t('admin.common.delete') }}
                  </n-button>
                </div>
              </div>
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
                  <div class="upload-area">
                    <n-upload
                      :file-list="carousel.fileList"
                      :max="1"
                      accept="image/*"
                      @change="(data: { fileList: UploadFileInfo[] }) => handleCarouselChange(index, data)"
                      @remove="() => handleCarouselRemove(index)"
                      :show-file-list="false"
                    >
                      <n-button size="small">{{ t('admin.common.fileUpload.selectImage') }}</n-button>
                    </n-upload>
                  </div>
                  <div class="image-preview" v-if="carousel.preview">
                    <img :src="carousel.preview" :alt="`Carousel ${index + 1}`" class="preview-image" />
                    <div class="image-actions">
                      <n-button size="small" @click="handleCarouselRemove(index)">
                        {{ t('admin.common.delete') }}
                      </n-button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </n-form-item>
        </n-card>
      </n-form>
    </n-spin>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useMessage } from 'naive-ui';
import { labApi } from '@/services/api';
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

// Image upload states
const logoFileList = ref<UploadFileInfo[]>([]);
const logoPreview = ref<string>('');
const logoFile = ref<File | null>(null);

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
      Object.assign(formData, response.data);
      
      // 設置 logo 預覽
      if (response.data.lab_logo_path) {
        logoPreview.value = getImageUrl(response.data.lab_logo_path);
      }
      
      // 設置輪播圖預覽
      const carouselFields = ['carousel_img_1', 'carousel_img_2', 'carousel_img_3', 'carousel_img_4'];
      carouselFields.forEach((field, index) => {
        if (response.data[field as keyof Lab]) {
          carouselImages.value[index].preview = getImageUrl(response.data[field as keyof Lab] as string);
        }
      });
    }
  } catch (error) {
    console.error('Failed to fetch lab data:', error);
    message.error(t('admin.lab.messages.fetchFailed'));
  } finally {
    loading.value = false;
  }
};

const getImageUrl = (path: string) => {
  const baseUrl = process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.1:8000';
  return `${baseUrl}/api/media/serve/${path.replace('/media/', '')}`;
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
  carouselImages.value[index].shouldClear = true;
};

const handleSave = async () => {
  try {
    await formRef.value?.validate();
    saving.value = true;

    const formDataToSend = new FormData();

    // 添加基本信息
    Object.keys(formData).forEach(key => {
      const value = formData[key as keyof typeof formData];
      if (value !== null && value !== undefined && value !== '') {
        formDataToSend.append(key, String(value));
      }
    });

    // 添加 logo 文件
    if (logoFile.value) {
      formDataToSend.append('lab_logo', logoFile.value);
    }

    // 添加輪播圖文件
    carouselImages.value.forEach((carousel, index) => {
      if (carousel.file) {
        formDataToSend.append(`carousel_img_${index + 1}`, carousel.file);
      } else if (carousel.shouldClear) {
        formDataToSend.append(`clear_carousel_img_${index + 1}`, 'true');
      }
    });

    const response = await labApi.updateLab(formDataToSend);
    if (response.code === 0) {
      message.success(t('admin.lab.messages.saveSuccess'));
      // 重新獲取數據以更新預覽
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
  border: 1px solid #d1d5db;
  border-radius: 8px;
  overflow: hidden;
  background: #f9fafb;
}

.preview-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  display: block;
}

.image-actions {
  position: absolute;
  top: 4px;
  right: 4px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
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