<template>
  <n-modal v-model:show="show" @update:show="handleModalClose" class="quick-action-modal">
    <n-card
      :style="{ width: isMobile ? '95vw' : '60rem', maxWidth: isMobile ? '95vw' : '60rem' }"
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

      <div class="modal-content">
        <n-form
          ref="formRef"
          :model="formData"
          :rules="formRules"
          :label-placement="isMobile ? 'top' : 'left'"
          :label-width="isMobile ? 'auto' : '160'"
          require-mark-placement="right-hanging"
          class="modal-form"
        >
          <!-- 成員表單 -->
        <template v-if="moduleType === 'members'">
          <n-form-item :label="t('admin.members.form.nameZh')" path="mem_name_zh" required>
            <n-input
              v-model:value="formData.mem_name_zh"
              :placeholder="t('admin.members.form.placeholders.nameZh')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.nameEn')" path="mem_name_en" required>
            <n-input
              v-model:value="formData.mem_name_en"
              :placeholder="t('admin.members.form.placeholders.nameEn')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.email')" path="mem_email" required>
            <n-input
              v-model:value="formData.mem_email"
              :placeholder="t('admin.members.form.placeholders.email')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.type')" path="mem_type">
            <n-select
              v-model:value="formData.mem_type"
              :options="memberTypeOptions"
              :placeholder="t('admin.members.form.placeholders.type')"
              style="width: 100%"
            />
          </n-form-item>
          
          <!-- 教師職務類型 -->
          <n-form-item 
            v-if="formData.mem_type === 0" 
            :label="t('admin.members.form.jobType')" 
            path="job_type"
          >
            <n-select
              v-model:value="formData.job_type"
              :options="jobTypeOptions"
              :placeholder="t('admin.members.form.placeholders.jobType')"
              style="width: 100%"
            />
          </n-form-item>
          
          <!-- 學生類型和年級 -->
          <template v-if="formData.mem_type === 1">
            <n-form-item :label="t('admin.members.form.studentType')" path="student_type">
              <n-select
                v-model:value="formData.student_type"
                :options="studentTypeOptions"
                :placeholder="t('admin.members.form.placeholders.studentType')"
                style="width: 100%"
              />
            </n-form-item>
            <n-form-item :label="t('admin.members.form.studentGrade')" path="student_grade">
              <n-input-number
                v-model:value="formData.student_grade"
                :placeholder="t('admin.members.form.placeholders.studentGrade')"
                :min="1"
                :max="10"
                style="width: 100%"
              />
            </n-form-item>
          </template>
          
          <!-- 校友去向 -->
          <template v-if="formData.mem_type === 2">
            <n-form-item :label="t('admin.members.form.graduationYear')" path="graduation_year">
              <n-input-number
                v-model:value="formData.graduation_year"
                :placeholder="t('admin.members.form.placeholders.graduationYear')"
                :min="1900"
                :max="new Date().getFullYear()"
                style="width: 100%"
              />
            </n-form-item>
            <n-form-item :label="t('admin.members.form.alumniIdentity')" path="alumni_identity">
              <n-select
                v-model:value="formData.alumni_identity"
                :options="alumniIdentityOptions"
                :placeholder="t('admin.members.form.placeholders.alumniIdentity')"
                style="width: 100%"
              />
            </n-form-item>
            <n-form-item :label="t('admin.members.form.destinationZh')" path="destination_zh">
              <n-input
                v-model:value="formData.destination_zh"
                :placeholder="t('admin.members.form.placeholders.destinationZh')"
                style="width: 100%"
              />
            </n-form-item>
            <n-form-item :label="t('admin.members.form.destinationEn')" path="destination_en">
              <n-input
                v-model:value="formData.destination_en"
                :placeholder="t('admin.members.form.placeholders.destinationEn')"
                style="width: 100%"
              />
            </n-form-item>
          </template>
          
          <!-- 課題組選擇，所有類型都可以選擇「無」 -->
          <n-form-item :label="t('admin.members.form.group.label')" path="research_group_id">
            <n-select
              v-model:value="formData.research_group_id"
              :options="researchGroupOptionsWithNone"
              :placeholder="t('admin.members.form.placeholders.group')"
              :loading="loadingGroups"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.description')" path="mem_desc_zh">
            <I18nMdEditor
              v-model="formData.mem_desc_zh"
              :placeholder="t('admin.members.form.placeholders.description')"
              :entity-type="entityType"
              :entity-id="entityId"
              field-name="mem_desc_zh"
              style="height: 300px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.descriptionEn')" path="mem_desc_en">
            <I18nMdEditor
              v-model="formData.mem_desc_en"
              :placeholder="t('admin.members.form.placeholders.descriptionEn')"
              :entity-type="entityType"
              :entity-id="entityId"
              field-name="mem_desc_en"
              style="height: 300px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.members.form.avatar')" path="mem_avatar">
            <div class="image-upload-container">
              <!-- 已選擇的圖片預覽 -->
              <div v-if="hasAvatarToShow" class="image-preview">
                <img 
                  :src="getImagePreview('mem_avatar')" 
                  :alt="t('admin.common.avatarPreview')" 
                  class="avatar-preview"
                />
                <div class="image-actions">
                  <n-button size="small" @click="openCropper('mem_avatar', 'avatar')">
                    {{ props.editData && props.editData['mem_avatar_path'] ? t('admin.imageCropper.cropAvatar') : t('admin.common.fileUpload.selectImage') }}
                  </n-button>
                  <n-button size="small" type="error" @click="removeImage('mem_avatar')">
                    {{ t('admin.common.delete') }}
                  </n-button>
                </div>
              </div>
              <!-- 上傳按鈕 -->
              <n-button v-else @click="openCropper('mem_avatar', 'avatar')">
                {{ t('admin.common.fileUpload.selectImage') }}
              </n-button>
            </div>
          </n-form-item>
        </template>

        <!-- 論文表單 -->
        <template v-if="moduleType === 'papers'">
          <n-form-item :label="t('admin.papers.form.titleZh')" path="paper_title_zh" required>
            <n-input
              v-model:value="formData.paper_title_zh"
              :placeholder="t('admin.papers.form.placeholders.titleZh')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.titleEn')" path="paper_title_en">
            <n-input
              v-model:value="formData.paper_title_en"
              :placeholder="t('admin.papers.form.placeholders.titleEn')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.description')" path="paper_desc_zh">
            <I18nMdEditor
              v-model="formData.paper_desc_zh"
              :placeholder="t('admin.papers.form.placeholders.description')"
              :entity-type="entityType"
              :entity-id="entityId"
              field-name="paper_desc_zh"
              style="height: 300px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.descriptionEn')" path="paper_desc_en">
            <I18nMdEditor
              v-model="formData.paper_desc_en"
              :placeholder="t('admin.papers.form.placeholders.descriptionEn')"
              :entity-type="entityType"
              :entity-id="entityId"
              field-name="paper_desc_en"
              style="height: 300px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.labAuthors')" path="authors">
            <n-select
              v-model:value="formData.authors"
              multiple
              filterable
              tag
              :options="memberOptions"
              :placeholder="t('admin.papers.form.placeholders.authors')"
              :loading="loadingMembers"
              :filter="filterMemberOption"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.allAuthorsZh')" path="all_authors_zh">
            <n-input
              v-model:value="formData.all_authors_zh"
              :placeholder="t('admin.papers.form.placeholders.allAuthorsZh')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.allAuthorsEn')" path="all_authors_en">
            <n-input
              v-model:value="formData.all_authors_en"
              :placeholder="t('admin.papers.form.placeholders.allAuthorsEn')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.venue')" path="paper_venue">
            <n-input
              v-model:value="formData.paper_venue"
              :placeholder="t('admin.papers.form.placeholders.venue')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.type')" path="paper_type">
            <n-select
              v-model:value="formData.paper_type"
              :options="paperTypeOptions"
              :placeholder="t('admin.papers.form.placeholders.type')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.date')" path="paper_date">
            <n-date-picker
              v-model:value="formData.paper_date"
              type="date"
              :placeholder="t('admin.papers.form.placeholders.date')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.status')" path="paper_accept">
            <n-select
              v-model:value="formData.paper_accept"
              :options="paperAcceptOptions"
              :placeholder="t('admin.papers.form.placeholders.status')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.url')" path="paper_url">
            <n-input
              v-model:value="formData.paper_url"
              :placeholder="t('admin.papers.form.placeholders.url')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.previewImg')" path="preview_img">
            <div class="image-upload-container">
              <!-- 已選擇的圖片預覽 -->
              <div v-if="hasPreviewImageToShow" class="image-preview">
                <img 
                  :src="getPreviewImageUrl('preview_img')" 
                  :alt="t('admin.papers.form.previewImgAlt')" 
                  class="preview-image"
                />
                <div class="image-actions">
                  <n-button size="small" @click="openCropper('preview_img', 'carousel')">
                    {{ props.editData && props.editData['preview_img'] ? t('admin.imageCropper.cropImage') : t('admin.common.fileUpload.selectImage') }}
                  </n-button>
                  <n-button size="small" type="error" @click="removePreviewImage('preview_img')">
                    {{ t('admin.common.delete') }}
                  </n-button>
                </div>
              </div>
              <!-- 上傳按鈕 -->
              <n-button v-else @click="openCropper('preview_img', 'carousel')">
                {{ t('admin.common.fileUpload.selectImage') }}
              </n-button>
            </div>
          </n-form-item>
          <n-form-item :label="t('admin.papers.form.file')" path="paper_file">
            <n-upload
              :default-file-list="getDefaultFileList('paper_file')"
              :max="1"
              accept=".pdf"
              @change="handleFileChange('paper_file', $event)"
              @remove="handleFileRemove('paper_file')"
            >
              <n-button>{{ t('admin.common.fileUpload.selectPdf') }}</n-button>
            </n-upload>
          </n-form-item>
        </template>

        <!-- 項目表單 -->
        <template v-if="moduleType === 'projects'">
          <n-form-item :label="t('admin.projects.form.nameZh')" path="project_name_zh" required>
            <n-input
              v-model:value="formData.project_name_zh"
              :placeholder="t('admin.projects.form.placeholders.nameZh')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.nameEn')" path="project_name_en">
            <n-input
              v-model:value="formData.project_name_en"
              :placeholder="t('admin.projects.form.placeholders.nameEn')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.description')" path="project_desc_zh">
            <I18nMdEditor
              v-model="formData.project_desc_zh"
              :placeholder="t('admin.projects.form.placeholders.description')"
              :entity-type="entityType"
              :entity-id="entityId"
              field-name="project_desc_zh"
              style="height: 300px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.descriptionEn')" path="project_desc_en">
            <I18nMdEditor
              v-model="formData.project_desc_en"
              :placeholder="t('admin.projects.form.placeholders.descriptionEn')"
              :entity-type="entityType"
              :entity-id="entityId"
              field-name="project_desc_en"
              style="height: 300px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.url')" path="project_url">
            <n-input
              v-model:value="formData.project_url"
              :placeholder="t('admin.projects.form.placeholders.url')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.startDate')" path="project_date_start">
            <n-date-picker
              v-model:value="formData.project_date_start"
              type="date"
              :placeholder="t('admin.projects.form.placeholders.startDate')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.projects.form.status')" path="is_end">
            <n-select
              v-model:value="formData.is_end"
              :options="projectStatusOptions"
              :placeholder="t('admin.projects.form.placeholders.status')"
              style="width: 100%"
            />
          </n-form-item>
        </template>

        <!-- 新聞表單 -->
        <template v-if="moduleType === 'news'">
          <n-form-item :label="t('admin.news.form.type')" path="news_type" required>
            <n-select
              v-model:value="formData.news_type"
              :options="newsTypeOptions"
              :placeholder="t('admin.news.form.placeholders.type')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.news.form.titleZh')" path="news_title_zh" required>
            <n-input
              v-model:value="formData.news_title_zh"
              :placeholder="t('admin.news.form.placeholders.titleZh')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.news.form.titleEn')" path="news_title_en" required>
            <n-input
              v-model:value="formData.news_title_en"
              :placeholder="t('admin.news.form.placeholders.titleEn')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.news.form.contentZh')" path="news_content_zh">
            <I18nMdEditor
              v-model="formData.news_content_zh"
              :placeholder="t('admin.news.form.placeholders.contentZh')"
              :entity-type="entityType"
              :entity-id="entityId"
              field-name="news_content_zh"
              style="height: 300px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.news.form.contentEn')" path="news_content_en">
            <I18nMdEditor
              v-model="formData.news_content_en"
              :placeholder="t('admin.news.form.placeholders.contentEn')"
              :entity-type="entityType"
              :entity-id="entityId"
              field-name="news_content_en"
              style="height: 300px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.news.form.date')" path="news_date" required>
            <n-date-picker
              v-model:value="formData.news_date"
              type="date"
              :placeholder="t('admin.news.form.placeholders.date')"
              style="width: 100%"
            />
          </n-form-item>
        </template>

        <!-- 課題組表單 -->
        <template v-if="moduleType === 'research-groups'">
          <n-form-item :label="t('admin.groups.form.nameZh')" path="research_group_name_zh" required>
            <n-input
              v-model:value="formData.research_group_name_zh"
              :placeholder="t('admin.groups.form.placeholders.nameZh')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.groups.form.nameEn')" path="research_group_name_en">
            <n-input
              v-model:value="formData.research_group_name_en"
              :placeholder="t('admin.groups.form.placeholders.nameEn')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.groups.form.descriptionZh')" path="research_group_desc_zh">
            <I18nMdEditor
              v-model="formData.research_group_desc_zh"
              :placeholder="t('admin.groups.form.placeholders.descriptionZh')"
              :entity-type="entityType"
              :entity-id="entityId"
              field-name="research_group_desc_zh"
              style="height: 300px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.groups.form.descriptionEn')" path="research_group_desc_en">
            <I18nMdEditor
              v-model="formData.research_group_desc_en"
              :placeholder="t('admin.groups.form.placeholders.descriptionEn')"
              :entity-type="entityType"
              :entity-id="entityId"
              field-name="research_group_desc_en"
              style="height: 300px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.groups.form.leader')" path="mem_id">
            <n-select
              v-model:value="formData.mem_id"
              filterable
              :options="memberOptions"
              :placeholder="t('admin.groups.form.placeholders.leader')"
              :loading="loadingMembers"
              :filter="filterMemberOption"
              style="width: 100%"
            />
          </n-form-item>
        </template>

        <!-- 資源表單 -->
        <template v-if="moduleType === 'resources'">
          <n-form-item :label="t('admin.resources.form.nameZh')" path="resource_name_zh" required>
            <n-input
              v-model:value="formData.resource_name_zh"
              :placeholder="t('admin.resources.form.placeholders.nameZh')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.resources.form.nameEn')" path="resource_name_en">
            <n-input
              v-model:value="formData.resource_name_en"
              :placeholder="t('admin.resources.form.placeholders.nameEn')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.resources.form.type')" path="resource_type">
            <n-select
              v-model:value="formData.resource_type"
              :options="resourceTypeOptions"
              :placeholder="t('admin.resources.form.placeholders.type')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.resources.form.availabilityStatus')" path="availability_status">
            <n-select
              v-model:value="formData.availability_status"
              :options="resourceStatusOptions"
              :placeholder="t('admin.resources.form.placeholders.availabilityStatus')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.resources.form.descriptionZh')" path="resource_description_zh">
            <I18nMdEditor
              v-model="formData.resource_description_zh"
              :placeholder="t('admin.resources.form.placeholders.descriptionZh')"
              :entity-type="entityType"
              :entity-id="entityId"
              field-name="resource_description_zh"
              style="height: 300px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.resources.form.descriptionEn')" path="resource_description_en">
            <I18nMdEditor
              v-model="formData.resource_description_en"
              :placeholder="t('admin.resources.form.placeholders.descriptionEn')"
              :entity-type="entityType"
              :entity-id="entityId"
              field-name="resource_description_en"
              style="height: 300px; width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.resources.form.locationZh')" path="resource_location_zh">
            <n-input
              v-model:value="formData.resource_location_zh"
              :placeholder="t('admin.resources.form.placeholders.locationZh')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.resources.form.locationEn')" path="resource_location_en">
            <n-input
              v-model:value="formData.resource_location_en"
              :placeholder="t('admin.resources.form.placeholders.locationEn')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.resources.form.url')" path="resource_url">
            <n-input
              v-model:value="formData.resource_url"
              :placeholder="t('admin.resources.form.placeholders.url')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.resources.form.contactInfo')" path="contact_info">
            <n-input
              v-model:value="formData.contact_info"
              :placeholder="t('admin.resources.form.placeholders.contactInfo')"
              style="width: 100%"
            />
          </n-form-item>
          <n-form-item :label="t('admin.resources.form.image')" path="resource_image">
            <div class="image-upload-container">
              <!-- 已選擇的圖片預覽 -->
              <div v-if="hasResourceImageToShow" class="image-preview">
                <img 
                  :src="getResourceImageUrl()" 
                  :alt="t('admin.resources.form.imageAlt')" 
                  class="resource-image-preview"
                />
                <div class="image-actions">
                  <n-button size="small" @click="openCropper('resource_image', 'carousel')">
                    {{ props.editData && props.editData['resource_image'] ? t('admin.imageCropper.cropImage') : t('admin.common.fileUpload.selectImage') }}
                  </n-button>
                  <n-button size="small" type="error" @click="removeResourceImage()">
                    {{ t('admin.common.delete') }}
                  </n-button>
                </div>
              </div>
              <!-- 上傳按鈕 -->
              <n-button v-else @click="openCropper('resource_image', 'carousel')">
                {{ t('admin.common.fileUpload.selectImage') }}
              </n-button>
            </div>
          </n-form-item>
        </template>

        <!-- 管理員表單 -->
        <template v-if="moduleType === 'admins'">
          <!-- 密碼修改模式：只顯示密碼相關字段 -->
          <template v-if="passwordOnly">
            <n-form-item :label="t('admin.profile.currentPassword')" path="old_password" required>
              <n-input
                v-model:value="formData.old_password"
                type="password"
                :placeholder="t('admin.profile.placeholders.currentPassword')"
                style="width: 100%"
              />
            </n-form-item>
            <n-form-item :label="t('admin.profile.newPassword')" path="new_password" required>
              <n-input
                v-model:value="formData.new_password"
                type="password"
                :placeholder="t('admin.profile.placeholders.newPassword')"
                style="width: 100%"
              />
            </n-form-item>
            <n-form-item :label="t('admin.profile.confirmPassword')" path="confirm_password">
              <n-input
                v-model:value="formData.confirm_password"
                type="password"
                :placeholder="t('admin.profile.placeholders.confirmPassword')"
                style="width: 100%"
              />
            </n-form-item>
          </template>

          <!-- 重置密碼模式：只顯示新密碼相關字段（超級管理員功能） -->
          <template v-else-if="resetPasswordMode">
            <n-form-item :label="t('admin.admins.form.newPassword')" path="new_password" required>
              <n-input
                v-model:value="formData.new_password"
                type="password"
                :placeholder="t('admin.admins.form.placeholders.newPassword')"
                style="width: 100%"
              />
            </n-form-item>
            <n-form-item :label="t('admin.admins.form.confirmPassword')" path="confirm_password" required>
              <n-input
                v-model:value="formData.confirm_password"
                type="password"
                :placeholder="t('admin.admins.form.placeholders.confirmPassword')"
                style="width: 100%"
              />
            </n-form-item>
          </template>
          
          <!-- 正常管理員表單模式 -->
          <template v-else>
            <n-form-item :label="t('admin.admins.form.adminName')" path="admin_name" required>
              <n-input
                v-model:value="formData.admin_name"
                :placeholder="t('admin.admins.form.placeholders.adminName')"
                style="width: 100%"
              />
            </n-form-item>
            <n-form-item v-if="actionType === 'create'" :label="t('admin.admins.form.adminPass')" path="admin_pass" required>
              <n-input
                v-model:value="formData.admin_pass"
                type="password"
                :placeholder="t('admin.admins.form.placeholders.adminPass')"
                style="width: 100%"
              />
            </n-form-item>
            <n-form-item :label="t('admin.admins.form.isSuper')" path="is_super">
              <n-select
                v-model:value="formData.is_super"
                :options="adminTypeOptions"
                :placeholder="t('admin.admins.form.placeholders.isSuper')"
                style="width: 100%"
              />
            </n-form-item>
            <n-form-item v-if="actionType === 'edit'" :label="t('admin.admins.form.enable')" path="enable">
              <n-select
                v-model:value="formData.enable"
                :options="enableOptions"
                :placeholder="t('admin.admins.form.placeholders.enable')"
                style="width: 100%"
              />
            </n-form-item>
          </template>
        </template>
      </n-form>
      
      <!-- 圖片裁切 Modal -->
      <ImageCropperModal
        v-model="showCropper"
        :crop-type="cropType"
        @cropped="handleCroppedImage"
      />
    </div>

      <template #footer>
        <div class="modal-footer">
          <n-button @click="show = false">
            {{ t('admin.common.cancel') }}
          </n-button>
          <n-button
            type="primary"
            :loading="submitting"
            @click="handleSubmit"
          >
            {{ actionType === 'create' ? t('admin.common.create') : t('admin.common.update') }}
          </n-button>
        </div>
      </template>
    </n-card>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, nextTick, onMounted, onUnmounted } from 'vue';
import { useMessage } from 'naive-ui';
import { useI18n } from 'vue-i18n';
import { useAuthStore } from '@/stores/auth';
import { memberApi, paperApi, projectApi, newsApi, researchGroupApi, adminApi, authApi, resourceApi } from '@/services/api';
import { getMediaUrl } from '@/utils/media';
import { memberDescriptionTemplates } from '@/utils/memberTemplates';
import I18nMdEditor from '@/components/I18nMdEditor.vue';
import ImageCropperModal from '@/components/ImageCropperModal.vue';
import type { ApiResponse, Member, ResearchGroup, ApiError } from '@/types/api';

// Form data interfaces based on module types
interface MemberFormData {
  mem_name_zh?: string;
  mem_name_en?: string;
  mem_email?: string;
  mem_type?: number;
  job_type?: number;
  student_type?: number;
  student_grade?: number;
  graduation_year?: number;
  alumni_identity?: number;
  destination_zh?: string;
  destination_en?: string;
  research_group_id?: number | null;
  mem_desc_zh?: string;
  mem_desc_en?: string;
  mem_avatar?: string;
  mem_avatar_delete?: boolean;
}

interface PaperFormData {
  paper_title_zh?: string;
  paper_title_en?: string;
  paper_desc_zh?: string;
  paper_desc_en?: string;
  authors?: number[];
  all_authors_zh?: string;
  all_authors_en?: string;
  paper_venue?: string;
  paper_type?: number;
  paper_date?: number | null;
  paper_accept?: number;
  paper_url?: string;
  paper_file?: string;
  paper_file_delete?: boolean;
}

interface ProjectFormData {
  project_name_zh?: string;
  project_name_en?: string;
  project_desc_zh?: string;
  project_desc_en?: string;
  project_url?: string;
  project_date_start?: number | null;
  is_end?: number;
}

interface NewsFormData {
  news_type?: number;
  news_title_zh?: string;
  news_title_en?: string;
  news_content_zh?: string;
  news_content_en?: string;
  news_date?: number | null;
}

interface ResearchGroupFormData {
  research_group_name_zh?: string;
  research_group_name_en?: string;
  research_group_desc_zh?: string;
  research_group_desc_en?: string;
  mem_id?: number;
}

interface AdminFormData {
  admin_name?: string;
  admin_pass?: string;
  is_super?: number;
  enable?: number;
  old_password?: string;
  new_password?: string;
  confirm_password?: string;
  admin_id?: number;
}

interface ResourceFormData {
  resource_name_zh?: string;
  resource_name_en?: string;
  resource_description_zh?: string;
  resource_description_en?: string;
  resource_type?: number;
  resource_location_zh?: string;
  resource_location_en?: string;
  resource_url?: string;
  resource_file?: string;
  resource_image?: string;
  availability_status?: number;
  contact_info?: string;
  resource_id?: number;
}

type FormData = MemberFormData | PaperFormData | ProjectFormData | NewsFormData | ResearchGroupFormData | AdminFormData | ResourceFormData;

interface SelectOption {
  label: string;
  value: number | string | null;
}

interface FormRule {
  required?: boolean;
  message?: string;
  trigger: string | string[];
  min?: number;
  type?: string;
  validator?: (rule: unknown, value: unknown) => boolean | Error;
}

const { t, locale } = useI18n();
const authStore = useAuthStore();

// Props
interface Props {
  modelValue: boolean;
  moduleType: 'members' | 'papers' | 'projects' | 'news' | 'research-groups' | 'admins' | 'resources';
  actionType: 'create' | 'edit';
  editData?: Record<string, unknown>;
  passwordOnly?: boolean; // 新增：仅密码修改模式
  resetPasswordMode?: boolean; // 新增：重置密码模式（超級管理員功能）
}

const props = withDefaults(defineProps<Props>(), {
  editData: () => ({}),
  passwordOnly: false,
  resetPasswordMode: false
});

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: boolean];
  'success': [data: Record<string, unknown>];
}>();

// Reactive data
const show = ref(props.modelValue);
const formRef = ref<{ validate: () => Promise<void>; restoreValidation: (fields?: string[]) => void } | null>(null);
const submitting = ref(false);
const message = useMessage();
const isMobile = ref(window.innerWidth <= 768);

// Loading states
const loadingGroups = ref(false);
const loadingMembers = ref(false);

// Form data - using a generic Record type that can be narrowed based on module type
const formData = reactive<Record<string, unknown>>({});
const uploadedFiles = reactive<Record<string, File>>({});

// 資源圖片文件列表已移除，改用統一的圖片處理方式

// 計算是否有頭像需要顯示
const hasAvatarToShow = computed(() => {
  // 如果有新上傳的文件
  if (uploadedFiles['mem_avatar']) {
    return true;
  }
  
  // 如果是編輯模式且有現有頭像，但沒有被標記為刪除
  if (props.actionType === 'edit' && props.editData && props.editData['mem_avatar_path']) {
    // 檢查是否被標記為刪除
    if (formData['mem_avatar_delete']) {
      return false;
    }
    return true;
  }
  
  return false;
});

// 計算是否有預覽圖片需要顯示
const hasPreviewImageToShow = computed(() => {
  // 如果有新上傳的文件
  if (uploadedFiles['preview_img']) {
    return true;
  }
  
  // 如果是編輯模式且有現有預覽圖片，但沒有被標記為刪除
  if (props.actionType === 'edit' && props.editData && props.editData['preview_img']) {
    // 檢查是否被標記為刪除
    if (formData['preview_img_delete']) {
      return false;
    }
    return true;
  }
  
  return false;
});

// 計算是否有資源圖片需要顯示
const hasResourceImageToShow = computed(() => {
  // 如果有新上傳的文件
  if (uploadedFiles['resource_image']) {
    return true;
  }
  
  // 如果是編輯模式且有現有資源圖片，但沒有被標記為刪除
  if (props.actionType === 'edit' && props.editData && props.editData['resource_image']) {
    // 檢查是否被標記為刪除
    if (formData['resource_image_delete']) {
      return false;
    }
    return true;
  }
  
  return false;
});

// Image cropper states
const showCropper = ref(false);
const cropType = ref<'avatar' | 'logo' | 'carousel'>('avatar');
const currentImageField = ref<string>('');

// Options
const memberTypeOptions = computed(() => [
  { label: t('admin.common.memberTypes.teacher'), value: 0 },
  { label: t('admin.common.memberTypes.student'), value: 1 },
  { label: t('admin.common.memberTypes.alumni'), value: 2 }
]);

// 教師職務類型選項
const jobTypeOptions = computed(() => [
  { label: t('admin.common.jobTypes.professor'), value: 0 },
  { label: t('admin.common.jobTypes.associateProfessor'), value: 1 },
  { label: t('admin.common.jobTypes.lecturer'), value: 2 },
  { label: t('admin.common.jobTypes.assistantResearcher'), value: 3 },
  { label: t('admin.common.jobTypes.postdoc'), value: 4 }
]);

// 學生類型選項
const studentTypeOptions = computed(() => [
  { label: t('admin.common.studentTypes.phd'), value: 0 },
  { label: t('admin.common.studentTypes.master'), value: 1 },
  { label: t('admin.common.studentTypes.undergraduate'), value: 2 }
]);

// 校友身份類型選項
const alumniIdentityOptions = computed(() => [
  { label: t('admin.common.alumniIdentity.phd'), value: 0 },
  { label: t('admin.common.alumniIdentity.master'), value: 1 },
  { label: t('admin.common.alumniIdentity.undergraduate'), value: 2 },
  { label: t('admin.common.alumniIdentity.teacher'), value: 3 },
  { label: t('admin.common.alumniIdentity.other'), value: 4 }
]);

const paperTypeOptions = computed(() => [
  { label: t('admin.common.paperTypes.conference'), value: 0 },
  { label: t('admin.common.paperTypes.journal'), value: 1 },
  { label: t('admin.common.paperTypes.patent'), value: 2 },
  { label: t('admin.common.paperTypes.book'), value: 3 },
  { label: t('admin.common.paperTypes.other'), value: 4 }
]);

const paperAcceptOptions = computed(() => [
  { label: t('admin.common.paperStatus.submitting'), value: 0 },
  { label: t('admin.common.paperStatus.accepted'), value: 1 }
]);

const projectStatusOptions = computed(() => [
  { label: t('admin.common.projectStatus.ongoing'), value: 0 },
  { label: t('admin.common.projectStatus.completed'), value: 1 }
]);

const newsTypeOptions = computed(() => [
  { label: t('admin.common.newsTypes.publication'), value: 0 },
  { label: t('admin.common.newsTypes.award'), value: 1 },
  { label: t('admin.common.newsTypes.activity'), value: 2 }
]);

const adminTypeOptions = computed(() => [
  { label: t('admin.admins.normalAdmin'), value: 0 },
  { label: t('admin.admins.superAdmin'), value: 1 }
]);

const enableOptions = computed(() => [
  { label: t('admin.common.disabled'), value: 0 },
  { label: t('admin.common.enabled'), value: 1 }
]);

const resourceTypeOptions = computed(() => [
  { label: t('admin.common.resourceTypes.equipment'), value: 0 },
  { label: t('admin.common.resourceTypes.software'), value: 1 },
  { label: t('admin.common.resourceTypes.database'), value: 2 },
  { label: t('admin.common.resourceTypes.dataset'), value: 3 },
  { label: t('admin.common.resourceTypes.other'), value: 4 }
]);

const resourceStatusOptions = computed(() => [
  { label: t('admin.common.resourceStatus.unavailable'), value: 0 },
  { label: t('admin.common.resourceStatus.available'), value: 1 },
  { label: t('admin.common.resourceStatus.maintenance'), value: 2 }
]);

const researchGroupOptions = ref<SelectOption[]>([]);
const memberOptions = ref<SelectOption[]>([]);

// 包含「無」選項的課題組選擇列表
const researchGroupOptionsWithNone = computed(() => {
  const noneOption: SelectOption = {
    label: t('admin.members.form.group.none'),
    value: -1
  };
  return [noneOption, ...researchGroupOptions.value];
});

// 計算實體信息，用於圖片上傳追蹤
const entityType = computed(() => {
  const typeMap = {
    'members': 'member',
    'papers': 'paper',
    'projects': 'project',
    'news': 'news',
    'research-groups': 'research_group',
    'resources': 'resource'
  };
  return typeMap[props.moduleType as keyof typeof typeMap] || '';
});

const entityId = computed(() => {
  if (props.actionType !== 'edit' || !props.editData) return 0;
  
  const idFields = {
    'members': 'mem_id',
    'papers': 'paper_id',
    'projects': 'project_id',
    'news': 'news_id',
    'research-groups': 'research_group_id',
    'resources': 'resource_id'
  };
  
  const idField = idFields[props.moduleType as keyof typeof idFields];
  return (props.editData[idField] as number) || 0;
});

// Computed
const modalTitle = computed(() => {
  // 如果是僅密碼修改模式
  if (props.passwordOnly) {
    return t('admin.user.changePassword');
  }
  
  // 如果是重置密碼模式
  if (props.resetPasswordMode) {
    return t('admin.admins.resetPassword');
  }

  // Map module types to correct title keys
  const moduleKeyMap: Record<string, string> = {
    'members': 'Member',
    'papers': 'Paper', 
    'projects': 'Project',
    'news': 'News',
    'research-groups': 'Group',
    'admins': 'Admin',
    'resources': 'Resource'
  };
  
  const actionKey = props.actionType === 'create' ? 'create' : 'edit';
  const moduleKey = moduleKeyMap[props.moduleType] || 'Member';
  
  return t(`admin.quickAction.modalTitle.${actionKey}${moduleKey}`);
});

// Form rules - 使用固定的规则对象
const formRules = computed(() => {
  const rules: Record<string, FormRule[]> = {};
  
  if (props.moduleType === 'members') {
    rules.mem_name_zh = [{ required: true, message: t('admin.members.form.validation.nameZhRequired'), trigger: 'blur' }];
    rules.mem_name_en = [{ required: true, message: t('admin.members.form.validation.nameEnRequired'), trigger: 'blur' }];
    rules.mem_email = [
      { required: true, message: t('admin.members.form.validation.emailRequired'), trigger: 'blur' },
      { type: 'email', message: t('admin.common.validationMessages.invalidEmail'), trigger: 'blur' }
    ];
    rules.mem_type = [{
      required: false,
      validator: (rule: unknown, value: unknown) => {
        if (value === null || value === undefined || value === '') {
          return new Error(t('admin.members.form.validation.typeRequired'));
        }
        // 檢查成員類型是否為有效值 (0, 1, 2)
        if (![0, 1, 2].includes(value as number)) {
          return new Error(t('admin.members.form.validation.typeRequired'));
        }
        return true;
      },
      trigger: 'change'
    }];
    // research_group_id is now optional for all member types - removed validation
    
    // 條件性驗證規則 - 使用 validator 函數動態檢查
    rules.job_type = [{
      required: false,
      validator: (rule: unknown, value: unknown) => {
        if ((formData as MemberFormData).mem_type === 0 && (value === null || value === undefined || value === '')) {
          return new Error(t('admin.members.form.validation.jobTypeRequired'));
        }
        return true;
      },
      trigger: ['change', 'blur']
    }];
    
    rules.student_type = [{
      required: false,
      validator: (rule: unknown, value: unknown) => {
        if ((formData as MemberFormData).mem_type === 1 && (value === null || value === undefined || value === '')) {
          return new Error(t('admin.members.form.validation.studentTypeRequired'));
        }
        return true;
      },
      trigger: ['change', 'blur']
    }];
    
    rules.student_grade = [{
      required: false,
      validator: (rule: unknown, value: unknown) => {
        if ((formData as MemberFormData).mem_type === 1) {
          if (value === null || value === undefined || value === '') {
            return new Error(t('admin.members.form.validation.studentGradeRequired'));
          }
          if (typeof value === 'number' && (value < 1 || value > 10)) {
            return new Error(t('admin.members.form.validation.studentGradeRange'));
          }
        }
        return true;
      },
      trigger: ['change', 'blur']
    }];
    
  } else if (props.moduleType === 'papers') {
    rules.paper_title_zh = [{ required: true, message: t('admin.papers.form.validation.titleZhRequired'), trigger: 'blur' }];
    rules.paper_type = [{
      required: false,
      validator: (rule: unknown, value: unknown) => {
        if (value === null || value === undefined || value === '') {
          return new Error(t('admin.papers.form.validation.typeRequired'));
        }
        return true;
      },
      trigger: 'change'
    }];
    rules.paper_accept = [{
      required: false,
      validator: (rule: unknown, value: unknown) => {
        if (value === null || value === undefined || value === '') {
          return new Error(t('admin.papers.form.validation.statusRequired'));
        }
        return true;
      },
      trigger: 'change'
    }];
    rules.paper_date = [{
      required: false,
      validator: (rule: unknown, value: unknown) => {
        if (value === null || value === undefined || value === '') {
          return new Error(t('admin.papers.form.validation.dateRequired'));
        }
        return true;
      },
      trigger: 'change'
    }];
  } else if (props.moduleType === 'projects') {
    rules.project_name_zh = [{ required: true, message: t('admin.projects.form.validation.nameZhRequired'), trigger: 'blur' }];
  } else if (props.moduleType === 'news') {
    rules.news_type = [{
      required: false,
      validator: (rule: unknown, value: unknown) => {
        if (value === null || value === undefined || value === '') {
          return new Error(t('admin.news.form.validation.typeRequired'));
        }
        return true;
      },
      trigger: 'change'
    }];
    // 新聞標題必填校驗 - 至少需要中文或英文標題之一
    rules.news_title_zh = [{
      required: false,
      validator: (rule: unknown, value: unknown) => {
        const titleZh = value as string;
        const titleEn = formData.news_title_en;
        if (!titleZh && !titleEn) {
          return new Error(t('admin.news.form.validation.titleRequired'));
        }
        return true;
      },
      trigger: 'blur'
    }];
    rules.news_title_en = [{
      required: false,
      validator: (rule: unknown, value: unknown) => {
        const titleEn = value as string;
        const titleZh = formData.news_title_zh;
        if (!titleEn && !titleZh) {
          return new Error(t('admin.news.form.validation.titleRequired'));
        }
        return true;
      },
      trigger: 'blur'
    }];
    // 新聞內容改為非必填
    rules.news_date = [{
      required: false,
      validator: (rule: unknown, value: unknown) => {
        if (value === null || value === undefined || value === '') {
          return new Error(t('admin.news.form.validation.dateRequired'));
        }
        return true;
      },
      trigger: 'change'
    }];
  } else if (props.moduleType === 'research-groups') {
    rules.research_group_name_zh = [{ required: true, message: t('admin.groups.form.validation.nameZhRequired'), trigger: 'blur' }];
  } else if (props.moduleType === 'admins') {
    if (props.passwordOnly) {
      // 密碼修改模式的驗證規則
      rules.old_password = [{ required: true, message: t('admin.profile.validation.currentPasswordRequired'), trigger: 'blur' }];
      rules.new_password = [
        { required: true, message: t('admin.profile.validation.newPasswordRequired'), trigger: 'blur' },
        { min: 8, message: t('admin.profile.validation.passwordMinLength'), trigger: 'blur' }
      ];
      rules.confirm_password = [
        { required: true, message: t('admin.profile.validation.confirmPasswordRequired'), trigger: 'blur' },
        {
          message: t('admin.profile.validation.passwordNotMatch'),
          validator: (rule: unknown, value: unknown) => {
            if (typeof value === 'string' && value !== (formData as AdminFormData).new_password) {
              return new Error(t('admin.profile.validation.passwordNotMatch'));
            }
            return true;
          },
          trigger: ['blur', 'change']
        }
      ];
    } else if (props.resetPasswordMode) {
      // 重置密碼模式的驗證規則
      rules.new_password = [
        { required: true, message: t('admin.admins.form.validation.newPasswordRequired'), trigger: 'blur' },
        { min: 8, message: t('admin.profile.validation.passwordMinLength'), trigger: 'blur' }
      ];
      rules.confirm_password = [
        { required: true, message: t('admin.admins.form.validation.confirmPasswordRequired'), trigger: 'blur' },
        {
          message: t('admin.profile.validation.passwordNotMatch'),
          validator: (rule: unknown, value: unknown) => {
            if (typeof value === 'string' && value !== (formData as AdminFormData).new_password) {
              return new Error(t('admin.profile.validation.passwordNotMatch'));
            }
            return true;
          },
          trigger: ['blur', 'change']
        }
      ];
    } else {
      // 正常管理員表單模式的驗證規則
      rules.admin_name = [{ required: true, message: t('admin.admins.form.validation.adminNameRequired'), trigger: 'blur' }];
      if (props.actionType === 'create') {
        rules.admin_pass = [
          { required: true, message: t('admin.admins.form.validation.adminPassRequired'), trigger: 'blur' },
          { min: 8, message: t('admin.profile.validation.passwordMinLength'), trigger: 'blur' }
        ];
      }
    }
  } else if (props.moduleType === 'resources') {
    rules.resource_name_zh = [{ required: true, message: t('admin.resources.form.validation.nameZhRequired'), trigger: 'blur' }];
    rules.resource_type = [{
      required: false,
      validator: (rule: unknown, value: unknown) => {
        if (value === null || value === undefined || value === '') {
          return new Error(t('admin.resources.form.validation.typeRequired'));
        }
        return true;
      },
      trigger: 'change'
    }];
    rules.availability_status = [{
      required: false,
      validator: (rule: unknown, value: unknown) => {
        if (value === null || value === undefined || value === '') {
          return new Error(t('admin.resources.form.validation.availabilityStatusRequired'));
        }
        return true;
      },
      trigger: 'change'
    }];
  }
  
  return rules;
});

// Watchers
watch(
  () => props.modelValue,
  (newValue) => {
    show.value = newValue;
    if (newValue) {
      resetForm();
      loadOptionsData();
      if (props.actionType === 'edit' && props.editData) {
        nextTick(() => {
          const editDataCopy = { ...props.editData };
          
          // 轉換日期字段為時間戳
          if (editDataCopy.paper_date && typeof editDataCopy.paper_date === 'string') {
            editDataCopy.paper_date = parseDateForForm(editDataCopy.paper_date);
          }
          if (editDataCopy.news_date && typeof editDataCopy.news_date === 'string') {
            editDataCopy.news_date = parseDateForForm(editDataCopy.news_date);
          }
          if (editDataCopy.project_date_start && typeof editDataCopy.project_date_start === 'string') {
            editDataCopy.project_date_start = parseDateForForm(editDataCopy.project_date_start);
          }
          
          // 處理論文作者數據：將authors對象數組轉換為mem_id數組
          if (props.moduleType === 'papers' && editDataCopy.authors && Array.isArray(editDataCopy.authors)) {
            editDataCopy.authors = editDataCopy.authors.map((author: { mem_id: number }) => author.mem_id);
            console.log('轉換後的作者ID數組:', editDataCopy.authors);
          }
          
          // 處理成員課題組字段：將 null 值轉換為 -1 以便在下拉框中正確顯示
          if (props.moduleType === 'members' && editDataCopy.research_group_id === null) {
            editDataCopy.research_group_id = -1;
          }
          
          Object.assign(formData, editDataCopy);
          
          // 數據加載完成後清除驗證錯誤
          nextTick(() => {
            formRef.value?.restoreValidation();
          });
        });
      }
    }
  }
);

watch(show, (newValue) => {
  emit('update:modelValue', newValue);
});

// Watch locale changes to reload options with correct language
watch(locale, () => {
  if (show.value) {
    loadOptionsData();
  }
});

// Watch member type changes to clear conditional fields and revalidate
watch(() => (formData as MemberFormData).mem_type, (newType, oldType) => {
  if (props.moduleType === 'members' && newType !== oldType) {
    // 清除條件性字段
    if (oldType === 0) {
      // 從教師切換到其他類型，清除職務類型
      delete formData.job_type;
    } else if (oldType === 1) {
      // 從學生切換到其他類型，清除學生相關字段
      delete formData.student_type;
      delete formData.student_grade;
    } else if (oldType === 2) {
      // 從校友切換到其他類型，清除去向字段
      delete formData.graduation_year;
      delete formData.alumni_identity;
      delete formData.destination_zh;
      delete formData.destination_en;
    }
    
    // 重新驗證條件性字段來清除錯誤狀態
    nextTick(() => {
      if (formRef.value) {
        // 使用 restoreValidation 來清除特定字段的驗證狀態
        formRef.value.restoreValidation(['job_type', 'student_type', 'student_grade']);
      }
    });
  }
});

// 檢查屏幕尺寸
const checkScreenSize = () => {
  isMobile.value = window.innerWidth <= 768;
};

// 監聽窗口大小變化
onMounted(() => {
  window.addEventListener('resize', checkScreenSize);
  checkScreenSize();
});

onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize);
});

// Methods
const getMemberDescriptionTemplate = (language: 'zh' | 'en') => {
  return memberDescriptionTemplates[language] || memberDescriptionTemplates.zh;
};

const resetForm = () => {
  // 清空 formData 對象，但保留響應式特性
  Object.keys(formData).forEach(key => {
    delete formData[key];
  });
  
  // 初始化字符串字段為空字符串或模板，防止 undefined 問題
  if (props.moduleType === 'members') {
    // 為新增成員設置描述模板
    if (props.actionType === 'create') {
      formData.mem_desc_zh = getMemberDescriptionTemplate('zh');
      formData.mem_desc_en = getMemberDescriptionTemplate('en');
    } else {
      formData.mem_desc_zh = '';
      formData.mem_desc_en = '';
    }
  } else if (props.moduleType === 'papers') {
    formData.paper_desc_zh = '';
    formData.paper_desc_en = '';
    formData.authors = [];
    formData.all_authors_zh = '';
    formData.all_authors_en = '';
  } else if (props.moduleType === 'projects') {
    formData.project_desc_zh = '';
    formData.project_desc_en = '';
  } else if (props.moduleType === 'news') {
    formData.news_title_zh = '';
    formData.news_title_en = '';
    formData.news_content_zh = '';
    formData.news_content_en = '';
  } else if (props.moduleType === 'research-groups') {
    formData.research_group_desc_zh = '';
    formData.research_group_desc_en = '';
  } else if (props.moduleType === 'resources') {
    formData.resource_description_zh = '';
    formData.resource_description_en = '';
  }
  
  // 清空上傳文件對象
  Object.keys(uploadedFiles).forEach(key => {
    delete uploadedFiles[key];
  });
  
  // 重置表單驗證狀態
  formRef.value?.restoreValidation();
};

const handleModalClose = (value: boolean) => {
  if (!value) {
    resetForm();
  }
};

const loadOptionsData = async () => {
  // 成員相關模塊需要加載課題組數據
  if (props.moduleType === 'members') {
    await loadResearchGroups();
  }
  
  // 論文和課題組模塊需要加載成員數據  
  if (props.moduleType === 'papers' || props.moduleType === 'research-groups') {
    await loadMembers();
  }
};

const loadResearchGroups = async () => {
  try {
    loadingGroups.value = true;
    const response = await researchGroupApi.getResearchGroups({ all: 'true' });
    // 檢查響應結構，處理實際的 API 返回格式
    if (response.code === 0 && response.data) {
      researchGroupOptions.value = response.data.items.map((group: ResearchGroup) => ({
        label: locale.value === 'zh' 
          ? (group.research_group_name_zh || group.research_group_name_en)
          : (group.research_group_name_en || group.research_group_name_zh),
        value: group.research_group_id
      }));
    }
  } catch (error) {
    console.error(t('admin.quickAction.messages.loadGroupsFailed'), error);
  } finally {
    loadingGroups.value = false;
  }
};

const loadMembers = async () => {
  try {
    loadingMembers.value = true;
    
    // 獲取所有類型的成員，包括教師、學生、校友
    const response = await memberApi.getMembers({ all: 'true' });
    
    // 檢查響應結構，處理實際的 API 返回格式
    if (response.code === 0 && response.data) {
      memberOptions.value = response.data.items.map((member: Member) => {
        const name = locale.value === 'zh'
          ? (member.mem_name_zh || member.mem_name_en)
          : (member.mem_name_en || member.mem_name_zh);
        
        // 獲取成員類型標籤
        const memberTypeLabels = {
          0: t('admin.common.memberTypes.teacher'),
          1: t('admin.common.memberTypes.student'),
          2: t('admin.common.memberTypes.alumni')
        };
        const typeLabel = memberTypeLabels[member.mem_type as keyof typeof memberTypeLabels] || '';
        
        return {
          label: `${name} (${member.mem_email}) - ${typeLabel}`,
          value: member.mem_id
        };
      });
      console.log(`成功加載 ${memberOptions.value.length} 個成員選項`);
    }
  } catch (error) {
    console.error('加載成員失敗:', error);
  } finally {
    loadingMembers.value = false;
  }
};

// 成員選項過濾函數
const filterMemberOption = (pattern: string, option: SelectOption) => {
  const searchPattern = pattern.toLowerCase();
  const label = option.label.toLowerCase();
  
  // 支持按姓名、郵箱、類型搜索
  return label.includes(searchPattern);
};

const formatDateForApi = (date: unknown) => {
  if (!date) return '';
  const d = new Date(date as string | number | Date);
  return d.toISOString().split('T')[0];
};

// 將字符串日期轉換為時間戳（用於日期選擇器）
const parseDateForForm = (dateString: string): number | null => {
  if (!dateString) return null;
  const date = new Date(dateString);
  return isNaN(date.getTime()) ? null : date.getTime();
};

// 文件處理方法
interface FileListItem {
  id: string;
  name: string;
  status: string;
  url: string;
}

interface FileChangeEvent {
  fileList: Array<{ file?: File }>;
}

const getDefaultFileList = (fieldName: string): FileListItem[] => {
  if (props.actionType === 'edit' && props.editData) {
    let filePath: string | undefined;
    
    // 特殊處理成員頭像字段
    if (fieldName === 'mem_avatar') {
      filePath = props.editData['mem_avatar_path'] as string | undefined;
    } else {
      filePath = props.editData[`${fieldName}_path`] as string | undefined;
    }
    
    if (filePath && typeof filePath === 'string') {
      return [{
        id: fieldName,
        name: filePath.split('/').pop() || 'file',
        status: 'finished',
        url: getMediaUrl(filePath)
      }];
    }
  }
  return [];
};

const handleFileChange = (fieldName: string, { fileList }: FileChangeEvent) => {
  if (fileList.length > 0) {
    const file = fileList[0].file;
    if (file) {
      uploadedFiles[fieldName] = file;
      // 如果用戶上傳新文件，清除刪除標記
      if (fieldName === 'paper_file') {
        delete formData[`${fieldName}_delete`];
      }
    }
  } else {
    delete uploadedFiles[fieldName];
  }
};

const handleFileRemove = (fieldName: string) => {
  // 刪除新上傳的文件
  delete uploadedFiles[fieldName];
  
  // 如果是編輯模式且有現有文件，標記為刪除
  if (props.actionType === 'edit' && props.editData) {
    if (fieldName === 'paper_file' && props.editData['paper_file_path']) {
      // 在formData中設置刪除標記
      formData[`${fieldName}_delete`] = true;
    }
  }
};

// Image handling methods removed - now all image uploads use the unified cropper approach

const removePreviewImage = (fieldName: string) => {
  // 刪除新上傳的文件
  delete uploadedFiles[fieldName];
  
  // 如果是編輯模式，標記為刪除
  if (props.actionType === 'edit') {
    if (fieldName === 'preview_img') {
      formData['preview_img_delete'] = true;
    }
  }
};

// Image cropper methods
const openCropper = (fieldName: string, type: 'avatar' | 'logo' | 'carousel') => {
  currentImageField.value = fieldName;
  cropType.value = type;
  showCropper.value = true;
};

const handleCroppedImage = (croppedFile: File) => {
  if (currentImageField.value) {
    uploadedFiles[currentImageField.value] = croppedFile;
    
    // 如果用戶上傳新圖片，清除刪除標記
    if (currentImageField.value === 'mem_avatar') {
      delete formData['mem_avatar_delete'];
    } else if (currentImageField.value === 'preview_img') {
      delete formData['preview_img_delete'];
    }
    
    currentImageField.value = '';
  }
};

const removeImage = (fieldName: string) => {
  // 刪除新上傳的文件
  delete uploadedFiles[fieldName];
  
  // 如果是編輯模式且有現有圖片，標記為刪除
  if (props.actionType === 'edit' && props.editData) {
    if (fieldName === 'mem_avatar' && props.editData['mem_avatar_path']) {
      // 在formData中設置刪除標記
      formData[`${fieldName}_delete`] = true;
    }
  }
};

const getImagePreview = (fieldName: string): string => {
  if (uploadedFiles[fieldName]) {
    return URL.createObjectURL(uploadedFiles[fieldName]);
  }
  
  // 如果是編輯模式且有現有圖片
  if (props.actionType === 'edit' && props.editData) {
    let imagePath: string | undefined;
    
    // 特殊處理成員頭像字段
    if (fieldName === 'mem_avatar') {
      imagePath = props.editData['mem_avatar_path'] as string | undefined;
      // 如果被標記為刪除，不顯示
      if (formData['mem_avatar_delete']) {
        return '';
      }
    } else {
      imagePath = props.editData[`${fieldName}_path`] as string | undefined;
    }
    
    if (imagePath && typeof imagePath === 'string') {
      return getMediaUrl(imagePath);
    }
  }
  
  return '';
};

const getPreviewImageUrl = (fieldName: string): string => {
  if (uploadedFiles[fieldName]) {
    return URL.createObjectURL(uploadedFiles[fieldName]);
  }
  
  // 如果是編輯模式且有現有預覽圖片
  if (props.actionType === 'edit' && props.editData) {
    let imagePath: string | undefined;
    
    if (fieldName === 'preview_img') {
      imagePath = props.editData['preview_img'] as string | undefined;
      // 如果被標記為刪除，不顯示
      if (formData['preview_img_delete']) {
        return '';
      }
    }
    
    if (imagePath && typeof imagePath === 'string') {
      return getMediaUrl(imagePath);
    }
  }
  
  return '';
};

// 資源圖片處理函數
const removeResourceImage = () => {
  // 刪除新上傳的文件
  delete uploadedFiles['resource_image'];
  
  // 如果是編輯模式且有現有圖片，標記為刪除
  if (props.actionType === 'edit' && props.editData && props.editData['resource_image']) {
    formData['resource_image_delete'] = true;
  }
};

// 獲取資源圖片URL
const getResourceImageUrl = (): string => {
  if (uploadedFiles['resource_image']) {
    return URL.createObjectURL(uploadedFiles['resource_image']);
  }
  
  // 如果是編輯模式且有現有資源圖片
  if (props.actionType === 'edit' && props.editData && props.editData['resource_image']) {
    // 如果被標記為刪除，不顯示
    if (formData['resource_image_delete']) {
      return '';
    }
    return getMediaUrl(props.editData['resource_image'] as string);
  }
  
  return '';
};

const handleSubmit = async () => {
  try {
    // 密碼修改模式的特殊處理
    if (props.passwordOnly && props.moduleType === 'admins') {
      await formRef.value?.validate();
      submitting.value = true;

      try {
        await authApi.changePassword(formData.old_password as string, formData.new_password as string);
        message.success(t('admin.profile.messages.passwordChangeSuccess'));
        emit('success', {} as Record<string, unknown>);
        show.value = false;
        return;
      } catch (error: unknown) {
        const apiError = error as ApiError;
        const errorMessage = apiError?.message || t('admin.profile.messages.passwordChangeFailed');
        message.error(errorMessage);
        return;
      } finally {
        submitting.value = false;
      }
    }

    // 重置密碼模式的特殊處理
    if (props.resetPasswordMode && props.moduleType === 'admins') {
      await formRef.value?.validate();
      submitting.value = true;

      try {
        const adminId = props.editData?.admin_id as number;
        await adminApi.resetAdminPassword(adminId, formData.new_password as string);
        message.success(t('admin.admins.messages.passwordResetSuccess'));
        emit('success', {} as Record<string, unknown>);
        show.value = false;
        return;
      } catch (error: unknown) {
        const apiError = error as ApiError;
        const errorMessage = apiError?.message || t('admin.admins.messages.passwordResetFailed');
        message.error(errorMessage);
        return;
      } finally {
        submitting.value = false;
      }
    }

    // 對於管理員操作，檢查權限（密碼修改和重置模式除外）
    if (props.moduleType === 'admins' && !props.passwordOnly && !props.resetPasswordMode) {
      // 編輯管理員時，檢查是否為超級管理員且不是編輯其他超級管理員
      if (props.actionType === 'edit') {
        if (!authStore.isSuperAdmin) {
          message.error(t('admin.admins.noEditPermission'));
          return;
        }
        
        // 在密碼模式下允許編輯自己，但在正常編輯模式下不允許
        if (formData.admin_id === authStore.admin?.admin_id) {
          message.error(t('admin.admins.cannotEditSelf'));
          return;
        }
        
        // 不能編輯其他超級管理員
        if (props.editData?.is_super === 1) {
          message.error(t('admin.admins.cannotEditSuperAdmin'));
          return;
        }
      }
      
      // 創建管理員時，檢查是否為超級管理員
      if (props.actionType === 'create' && !authStore.isSuperAdmin) {
        message.error(t('admin.admins.noCreatePermission'));
        return;
      }
    }

    await formRef.value?.validate();
    submitting.value = true;

    // 準備提交數據
    // 准备提交数据
    let submitData: FormData | Record<string, unknown>;
    // 检查是否有实际的文件需要上传
    const hasFiles = Object.keys(uploadedFiles).some(key => uploadedFiles[key] instanceof File);
    
    // 过滤并清理表单数据，确保不包含函数或无效值
    const cleanFormData = Object.keys(formData).reduce((acc: Record<string, unknown>, key) => {
      const value = formData[key];
      // 檢查是否為有效值 - 明確處理各種數據類型
      let isValidValue = false;
      
      if (typeof value === 'number') {
        // 數值類型（包括 0）都是有效的
        isValidValue = true;
      } else if (typeof value === 'string') {
        // 字符串類型（包括空字符串）都是有效的，空字符串在某些字段中是合法值
        isValidValue = true;
      } else if (typeof value === 'boolean') {
        // 布爾值都是有效的
        isValidValue = true;
      } else if (Array.isArray(value)) {
        // 數組都是有效的
        isValidValue = true;
      } else if (value instanceof Date) {
        // 日期對象都是有效的
        isValidValue = true;
      } else if (value === null && (
        key === 'research_group_id' || 
        key === 'job_type' || 
        key === 'student_type' || 
        key === 'student_grade'
      )) {
        // 特殊處理：這些字段的 null 值是有效的（代表選擇了「無」或未設置）
        isValidValue = true;
      } else if (value === -1 && key === 'research_group_id') {
        // 特殊處理：research_group_id 為 -1 時轉換為 null（代表選擇了「無」）
        acc[key] = null;
        return acc; // 直接返回，避免後續處理
      } else if (value === undefined || value === null || typeof value === 'function') {
        // undefined、null（除了特殊字段）、function 等都是無效的
        isValidValue = false;
      } else {
        // 其他類型（如對象）需要進一步檢查
        isValidValue = value != null;
      }
      
      if (isValidValue) {
        acc[key] = value;
      }
      return acc;
    }, {});
    
    // 特殊处理论文作者格式转换
    if (props.moduleType === 'papers' && cleanFormData.authors && Array.isArray(cleanFormData.authors)) {
      // 将简单的 mem_id 数组转换为后端期望的格式
      cleanFormData.authors = (cleanFormData.authors as number[]).map((mem_id, index) => ({
        mem_id: mem_id,
        author_order: index + 1,
        is_corresponding: index === 0 ? 1 : 0  // 第一个作者默认为通讯作者
      }));
    }
    
    if (hasFiles) {
      // 使用 FormData 处理文件上传
      const formDataObj = new FormData();
      submitData = formDataObj as FormData;
      
      // 添加清理后的表单字段
      Object.keys(cleanFormData).forEach(key => {
        let value = cleanFormData[key];
        
        // 格式化日期字段
        if (key.includes('date') && value) {
          value = formatDateForApi(value);
        }
        
        // 确保值是可序列化的字符串或数字
        if (Array.isArray(value)) {
          // 处理数组数据，如authors
          if (value.length > 0) {
            // 特殊处理 authors 数组 - 需要将对象数组序列化为JSON字符串
            if (key === 'authors' && props.moduleType === 'papers') {
              formDataObj.append(key, JSON.stringify(value));
            } else {
              // 其他数组按索引添加
              value.forEach((item, index) => {
                formDataObj.append(`${key}[${index}]`, String(item));
              });
            }
          } else {
            // 空数组的处理：添加一个特殊标记表示这是一个空数组
            formDataObj.append(`${key}_empty`, 'true');
          }
        } else if (value === null) {
          // null 值特殊处理：用空字符串表示
          formDataObj.append(key, '');
        } else {
          formDataObj.append(key, String(value));
        }
      });
      
      // 添加文件
      Object.keys(uploadedFiles).forEach(key => {
        const file = uploadedFiles[key];
        if (file instanceof File) {
          formDataObj.append(key, file);
        }
      });
      
    } else {
      // 普通 JSON 提交
      submitData = { ...cleanFormData };
      
      // 格式化日期欄位
      const submitDataObj = submitData as Record<string, unknown>;
      if (submitDataObj.paper_date) {
        submitDataObj.paper_date = formatDateForApi(submitDataObj.paper_date);
      }
      if (submitDataObj.news_date) {
        submitDataObj.news_date = formatDateForApi(submitDataObj.news_date);
      }
      if (submitDataObj.project_date_start) {
        submitDataObj.project_date_start = formatDateForApi(submitDataObj.project_date_start);
      }
    }

    let response: ApiResponse<unknown>;
    const apis = {
      members: memberApi,
      papers: paperApi,
      projects: projectApi,
      news: newsApi,
      'research-groups': researchGroupApi,
      admins: adminApi,
      resources: resourceApi
    };

    const api = apis[props.moduleType];
    
    if (props.actionType === 'create') {
      const createMethods = {
        members: 'createMember',
        papers: 'createPaper',
        projects: 'createProject',
        news: 'createNews',
        'research-groups': 'createResearchGroup',
        admins: 'createAdmin',
        resources: 'createResource'
      };
      response = await (api as unknown as Record<string, (data: FormData | Record<string, unknown>) => Promise<ApiResponse<unknown>>>)[createMethods[props.moduleType]](submitData);
    } else {
      const updateMethods = {
        members: 'updateMember',
        papers: 'updatePaper',
        projects: 'updateProject',
        news: 'updateNews',
        'research-groups': 'updateResearchGroup',
        admins: 'updateAdmin',
        resources: 'updateResource'
      };
      const idField = {
        members: 'mem_id',
        papers: 'paper_id',
        projects: 'project_id',
        news: 'news_id',
        'research-groups': 'research_group_id',
        admins: 'admin_id',
        resources: 'resource_id'
      };
      const id = props.editData?.[idField[props.moduleType]];
      response = await (api as unknown as Record<string, (id: number, data: FormData | Record<string, unknown>) => Promise<ApiResponse<unknown>>>)[updateMethods[props.moduleType]](id as number, submitData);
    }

    // 檢查 API 響應結構
    if (response.code === 0) {
      const successMessage = props.actionType === 'create' 
        ? t('admin.quickAction.messages.createSuccess')
        : t('admin.quickAction.messages.updateSuccess');
      message.success(successMessage);
      emit('success', response.data as Record<string, unknown>);
      show.value = false;
    } else {
      message.error(response.message || t('admin.quickAction.messages.operationFailed'));
    }
  } catch (error) {
    if (error instanceof Error && error.message) {
      message.error(error.message);
    } else {
      message.error(t('admin.quickAction.messages.checkInput'));
    }
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.quick-action-modal :deep(.n-modal) {
  padding: 1rem;
}

.modal-card {
  margin: 0 auto;
}

.modal-form {
  max-height: 70vh;
  overflow-y: auto;
  padding-right: 8px;
  margin-right: -8px;
}

/* 自定義滾動條樣式 */
.modal-form::-webkit-scrollbar {
  width: 6px;
}

.modal-form::-webkit-scrollbar-track {
  background: transparent;
}

.modal-form::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.modal-form::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 1rem;
}

/* 移動端樣式調整 */
@media (max-width: 768px) {
  .quick-action-modal :deep(.n-modal) {
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
  
  .modal-form {
    max-height: 60vh;
    padding-right: 6px;
    margin-right: -6px;
  }
  
  .modal-form :deep(.n-form-item) {
    margin-bottom: 1rem;
  }
  
  .modal-form :deep(.n-form-item-label) {
    margin-bottom: 0.5rem;
    font-weight: 500;
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
  .quick-action-modal :deep(.n-modal) {
    padding: 0.25rem;
  }
  
  .modal-card :deep(.n-card__header) {
    padding: 0.75rem 0.75rem 0.5rem 0.75rem;
  }
  
  .modal-card :deep(.n-card__content) {
    padding: 0.5rem 0.75rem;
  }
  
  .modal-card :deep(.n-card__footer) {
    padding: 0.5rem 0.75rem 0.75rem 0.75rem;
  }
  
  .modal-form {
    max-height: 55vh;
    padding-right: 4px;
    margin-right: -4px;
  }
  
  .modal-form :deep(.n-form-item) {
    margin-bottom: 0.75rem;
  }
}

/* MarkdownEditor 在移動端的調整 */
@media (max-width: 768px) {
  .modal-form :deep(.markdown-editor) {
    min-height: 100px;
  }
  
  .modal-form :deep(.n-input__textarea-el) {
    min-height: 100px !important;
  }
}

/* 上傳組件在移動端的調整 */
@media (max-width: 768px) {
  .modal-form :deep(.n-upload) {
    width: 100%;
  }
  
  .modal-form :deep(.n-upload .n-button) {
    width: 100%;
  }
}

/* 圖片上傳容器樣式 */
.image-upload-container {
  width: 100%;
}

.image-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border: 2px dashed #e0e0e0;
  border-radius: 8px;
  background-color: #fafafa;
}

.avatar-preview {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
  border: 3px solid #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logo-preview {
  max-width: 200px;
  max-height: 100px;
  object-fit: contain;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}

.carousel-preview {
  width: 200px;
  height: auto;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}

.image-actions {
  display: flex;
  gap: 0.5rem;
}

/* 暗色主題 */
[data-theme="dark"] .image-preview,
.dark .image-preview {
  background-color: #2d2d2d;
  border-color: #424242;
}

[data-theme="dark"] .avatar-preview,
.dark .avatar-preview {
  border-color: #424242;
}

[data-theme="dark"] .logo-preview,
.dark .logo-preview,
[data-theme="dark"] .carousel-preview,
.dark .carousel-preview {
  border-color: #424242;
}

/* 論文預覽圖片樣式 */
.preview-image {
  width: 200px;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
  border: 2px solid #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 資源圖片樣式 */
.resource-image-preview {
  width: 200px;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
  border: 2px solid #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 暗色主題圖片樣式 */
[data-theme="dark"] .preview-image,
.dark .preview-image,
[data-theme="dark"] .resource-image-preview,
.dark .resource-image-preview {
  border-color: #424242;
}

/* 移動端圖片預覽調整 */
@media (max-width: 768px) {
  .image-preview {
    padding: 0.75rem;
  }
  
  .avatar-preview {
    width: 80px;
    height: 80px;
  }
  
  .logo-preview {
    max-width: 150px;
    max-height: 80px;
  }
  
  .carousel-preview {
    width: 150px;
  }
  
  .preview-image {
    width: 150px;
    height: 112px;
  }
  
  .resource-image-preview {
    width: 150px;
    height: 112px;
  }
  
  .image-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .image-actions .n-button {
    width: 100%;
  }
}
</style>