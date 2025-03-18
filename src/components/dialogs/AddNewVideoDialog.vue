<script setup lang="ts">
import { toast } from 'vue3-toastify'
import Draggable from 'vuedraggable'
import { VForm } from 'vuetify/components/VForm'

import type { ArticleViewModel, CreateArticleForm } from '@/@db/apps/articles/types'
import type { BackgroundVideoViewModel } from '@/@db/apps/materials/types'
import { VideoStatus } from '@/@db/apps/videos/enums'
import type { CreateVideoForm } from '@/@db/apps/videos/types'

interface Props {
  isVisible: boolean
}

interface Emit {
  (e: 'update:isVisible', value: boolean): void
  (e: 'success'): void
}

// const { global } = useTheme()
const props = defineProps<Props>()
const emit = defineEmits<Emit>()
const { URL } = window

const isAddVideoDialogVisible = ref(props.isVisible)
const isBulkAddArticlesDialogOpen = ref(false)
const isImagePreviewVisible = ref(false)
const isDragging = ref(false)
const refVForm = ref<VForm | null>(null)

const bulkAddTextareaContent = ref('')
const bulkAddError = ref('')
const previewImageUrl = ref('')
const imageZoomScale = ref(1)

const videoForm = ref<CreateVideoForm>({
  article_ids: [],
  background_video_ids: null,
  name: null,
  status: VideoStatus.DRAFT,
  language: null,
  topic: null,
  context: null,
})

const newArticles = ref<CreateArticleForm[]>([])

const resetVideoForm = () => {
  videoForm.value = {
    article_ids: [],
    background_video_ids: null,
    name: null,
    status: VideoStatus.DRAFT,
    language: null,
    topic: null,
    context: null,
  }
}

const handleCreateVideo = async () => {
  const validationResult = await refVForm.value?.validate()
  const valid = validationResult?.valid ?? false
  if (!valid) {
    toast.error('Please fill in all required fields.')

    return
  }

  const newArticleIds: string[] = []

  const articleCreationPromises = newArticles.value.map(async article => {
    const formData = new FormData()

    formData.append('article_data', JSON.stringify({
      original_url: article.original_url,
      published_at: article.published_at,
    }))
    article.images.forEach(image => formData.append('image_files', image))

    const { data } = await useApi<any>(createUrl('/articles')).post(formData)

    return data.value
  })

  try {
    const articleCreationResults = await Promise.all(articleCreationPromises)

    articleCreationResults.forEach(articleData => {
      if (articleData && articleData.id)
        newArticleIds.push(articleData.id)
    })

    console.log('All articles created. New Article IDs:', newArticleIds)

    videoForm.value.article_ids = [...videoForm.value.article_ids, ...newArticleIds]

    const cleanedVideoFormPayload = removeEmptyValues(videoForm.value)

    const { response } = await useApi<any>(createUrl('/videos')).post(cleanedVideoFormPayload)

    if (response.value?.ok) {
      isAddVideoDialogVisible.value = false
      emit('success')
    }
  }
  catch (error) {
    console.error('Error creating articles:', error)
  }
}

const articlesAutoComplete = ref<ArticleViewModel[]>([])
const articleAutoCompleteSearch = ref('')

const handleFetchArticlesAutoComplete = async () => {
  const { data } = await useApi<any>(createUrl('/articles', {
    query: {
      size: 100,
      search: articleAutoCompleteSearch.value === '' ? undefined : articleAutoCompleteSearch.value,
    },
  }))

  if (data.value && data.value.items)
    articlesAutoComplete.value = data.value.items
}

const backgroundVideosAutoComplete = ref<BackgroundVideoViewModel[]>([])
const backgroundVideoAutoCompleteSearch = ref('')

const handleFetchBackgroundVideosAutoComplete = async () => {
  const { data } = await useApi<any>(createUrl('/materials/background-videos', {
    query: {
      size: 100,
      search: backgroundVideoAutoCompleteSearch.value === '' ? undefined : backgroundVideoAutoCompleteSearch.value,
    },
  }))

  if (data.value && data.value.items)
    backgroundVideosAutoComplete.value = data.value.items
}

const handleJumpToArticle = (index: number) => {
  const articleId = `article-${index}`
  const articleElement = document.getElementById(articleId)

  articleElement?.scrollIntoView({ behavior: 'smooth' })
}

const handleAddArticle = async () => {
  newArticles.value.push({
    original_url: '',
    published_at: null,
    images: [],
  })

  await nextTick(() => handleJumpToArticle(newArticles.value.length - 1))
}

const handleBulkAddArticles = async () => {
  bulkAddError.value = ''

  const urls = bulkAddTextareaContent.value.split('\n').filter(url => url.trim() !== '')
  const validUrls = []

  for (const url of urls) {
    if (urlValidator(url))
      validUrls.push(url.trim())
    else
      bulkAddError.value = 'Please enter valid URLs.'
  }

  if (bulkAddError.value === '') {
    validUrls.forEach(url => {
      newArticles.value.push({
        original_url: url,
        published_at: null,
        images: [],
      })
    })
    isBulkAddArticlesDialogOpen.value = false
    bulkAddTextareaContent.value = ''

    await nextTick(() => handleJumpToArticle(newArticles.value.length - 1))
  }
}

const handleRemoveArticle = (index: number) => {
  if (newArticles.value.length > 1)
    newArticles.value.splice(index, 1)
}

const handleImagesChange = (articleIndex: number, files: File[]) => {
  newArticles.value[articleIndex].images = [...newArticles.value[articleIndex].images, ...files]
}

const handleRemoveImage = (articleIndex: number, imageIndex: number) => {
  newArticles.value[articleIndex].images.splice(imageIndex, 1)
}

const openImageViewer = (imageUrl: string) => {
  previewImageUrl.value = imageUrl
  isImagePreviewVisible.value = true
  imageZoomScale.value = 1
}

const closeImageViewer = () => {
  isImagePreviewVisible.value = false
  previewImageUrl.value = ''
  imageZoomScale.value = 1
}

const handleImageWheelZoom = (event: WheelEvent) => {
  event.preventDefault() // Prevent page scroll

  const zoomSpeed = 0.002 // Adjust zoom speed

  imageZoomScale.value += -event.deltaY * zoomSpeed

  // Clamp zoom scale
  imageZoomScale.value = Math.max(0.5, Math.min(imageZoomScale.value, 5)) // Zoom between 50% and 500%
}

watch(isAddVideoDialogVisible, newValue => {
  emit('update:isVisible', newValue)

  if (!newValue)
    resetVideoForm()
})

watch(isBulkAddArticlesDialogOpen, newValue => {
  if (!newValue) {
    bulkAddTextareaContent.value = ''
    bulkAddError.value = ''
  }
})

watch(() => props.isVisible, newValue => {
  isAddVideoDialogVisible.value = newValue
})
</script>

<template>
  <VDialog
    v-model="isAddVideoDialogVisible"
    width="1200"
    scrollable
  >
    <VCard
      class="pa-6"
      flat
    >
      <VCardTitle class="text-h5 mb-4 dialog-title">
        Create New Video
        <div class="dialog-actions">
          <VBtn
            color="secondary"
            variant="outlined"
            class="me-2"
            @click="isAddVideoDialogVisible = false"
          >
            Cancel
          </VBtn>

          <VBtn
            color="primary"
            @click="handleCreateVideo"
          >
            Create
          </VBtn>
        </div>
      </VCardTitle>

      <VCardText>
        <VForm
          ref="refVForm"
          @submit.prevent="handleCreateVideo"
        >
          <VRow>
            <VCol cols="12">
              <p class="text-subtitle-1 font-weight-bold mb-2">
                Name:
              </p>

              <VTextField
                v-model="videoForm.name"
                label="Name (Optional)"
                placeholder="Name"
                variant="outlined"
                class="mb-3"
              />
            </VCol>

            <VCol cols="6">
              <p class="text-subtitle-1 font-weight-bold mb-2">
                Language:
              </p>

              <VTextField
                v-model="videoForm.language"
                label="Language (Optional)"
                placeholder="Language"
                variant="outlined"
                class="mb-3"
              />
            </VCol>

            <VCol cols="6">
              <p class="text-subtitle-1 font-weight-bold mb-2">
                Topic:
              </p>

              <VTextField
                v-model="videoForm.topic"
                label="Topic (Optional)"
                placeholder="Topic"
                variant="outlined"
                class="mb-3"
              />
            </VCol>

            <VCol cols="12">
              <p class="text-subtitle-1 font-weight-bold mb-2">
                Status:
              </p>

              <VRadioGroup
                v-model="videoForm.status"
                class="video-status-radio-group"
                column
              >
                <VRadio
                  label="Draft - Save but don't process"
                  :value="VideoStatus.DRAFT"
                />
                <VRadio
                  label="Pending - Start processing immediately"
                  :value="VideoStatus.PENDING"
                />
              </VRadioGroup>
            </VCol>

            <VCol cols="6">
              <VAutocomplete
                v-model="videoForm.article_ids"
                v-model:search="articleAutoCompleteSearch"
                :items="articlesAutoComplete"
                item-title="original_url"
                item-value="id"
                label="Existing Articles"
                placeholder="Existing Articles"
                multiple
                chips
                closable-chips
                clear-on-select
                no-data-text="No articles available"
                @focus="handleFetchArticlesAutoComplete"
              />
            </VCol>

            <VCol cols="6">
              <VAutocomplete
                v-model="videoForm.background_video_ids"
                v-model:search="backgroundVideoAutoCompleteSearch"
                :items="backgroundVideosAutoComplete"
                item-title="name"
                item-value="id"
                label="Existing Background Videos"
                placeholder="Existing Background Videos"
                multiple
                chips
                closable-chips
                clear-on-select
                no-data-text="No background videos available"
                @focus="handleFetchBackgroundVideosAutoComplete"
              />
            </VCol>

            <VCol
              cols="12"
              class="articles-section"
            >
              <p class="text-subtitle-1 font-weight-bold mb-2">
                Articles:
              </p>

              <div class="article-buttons mb-4">
                <VBtn
                  variant="tonal"
                  color="primary"
                  class="me-2"
                  @click="handleAddArticle"
                >
                  <VIcon
                    start
                    icon="ri-add-line"
                  />
                  Add New Article
                </VBtn>
                <VBtn
                  color="primary"
                  variant="tonal"
                  @click="isBulkAddArticlesDialogOpen = true"
                >
                  <VIcon
                    start
                    icon="ri-file-text-line"
                  />
                  Bulk Add by URLs
                </VBtn>
              </div>

              <VCard
                v-for="(article, articleIndex) in newArticles"
                :id="`article-${articleIndex}`"
                :key="articleIndex"
                flat
                class="mb-6 article-card"
              >
                <VCardTitle class="article-card-title">
                  Article #{{ articleIndex + 1 }}
                  <VBtn
                    v-if="newArticles.length > 1"
                    color="error"
                    variant="text"
                    icon="ri-delete-bin-line"
                    size="small"
                    class="remove-article-btn"
                    @click="handleRemoveArticle(articleIndex)"
                  />
                </VCardTitle>

                <VCardText>
                  <VRow>
                    <VCol cols="12">
                      <VTextField
                        v-model="article.original_url"
                        label="Original URL"
                        placeholder="Original URL"
                        variant="outlined"
                        :rules="[requiredValidator]"
                      />
                    </VCol>

                    <!--
                      <VCol cols="6">
                      <VueDatePicker
                      v-model="article.published_at"
                      :dark="global.name.value === 'dark'"
                      :enable-time-picker="false"
                      position="center"
                      label="Published At"
                      placeholder="Published At"
                      auto-apply
                      teleport
                      time-picker-inline
                      />
                      </VCol>
                    -->
                  </VRow>

                  <div class="image-section">
                    <p class="text-subtitle-2 font-weight-bold mb-2">
                      Images:
                    </p>

                    <div
                      v-if="article.images.length === 0"
                      class="image-upload-initial"
                    >
                      <label
                        :for="`image-upload-${articleIndex}`"
                        class="image-upload-label"
                      >
                        <div class="image-upload-icon">
                          <VIcon
                            icon="ri-image-add-line"
                            size="x-large"
                          />
                          <p class="mt-1">Upload Images</p>
                        </div>

                        <VFileInput
                          :id="`image-upload-${articleIndex}`"
                          key="fileInputKey"
                          variant="outlined"
                          accept="image/*"
                          multiple
                          hide-details
                          class="d-none"
                          @change="(e: any) => handleImagesChange(articleIndex, Array.from(e.target.files || []))"
                        />
                      </label>
                    </div>

                    <div
                      v-else
                      class="image-list-section"
                    >
                      <Draggable
                        v-model="newArticles[articleIndex].images"
                        item-key="name"
                        class="image-list-container"
                        @start="isDragging = true"
                        @end="isDragging = false"
                      >
                        <template #item="{ element, index: imageIndex }">
                          <div class="image-list-item">
                            <VImg
                              :src="URL.createObjectURL(element)"
                              max-height="100"
                              max-width="100"
                              cover
                              class="image-preview-small"
                            />

                            <div class="image-details">
                              <p class="file-name">
                                {{ element.name }}
                              </p>

                              <p class="file-size">
                                Index: {{ imageIndex + 1 }} - Size: {{ formatFileSize(element.size) }}
                              </p>

                              <div class="image-actions">
                                <VBtn
                                  color="primary"
                                  variant="text"
                                  size="small"
                                  @click="openImageViewer(URL.createObjectURL(element))"
                                >
                                  View
                                </VBtn>

                                <VBtn
                                  color="error"
                                  variant="text"
                                  size="small"
                                  @click="handleRemoveImage(articleIndex, imageIndex)"
                                >
                                  Delete
                                </VBtn>
                              </div>
                            </div>
                          </div>
                        </template>
                      </Draggable>

                      <label
                        :for="`image-upload-${articleIndex}`"
                        class="image-add-more-label"
                      >
                        <VBtn
                          icon="ri-add-line"
                          variant="tonal"
                          color="primary"
                        />
                        <span>Add Images</span>
                        <VFileInput
                          :id="`image-upload-${articleIndex}`"
                          key="fileInputKey"
                          variant="outlined"
                          accept="image/*"
                          multiple
                          hide-details
                          class="d-none"
                          @change="(e: any) => handleImagesChange(articleIndex, Array.from(e.target.files || []))"
                        />
                      </label>
                    </div>
                  </div>
                </VCardText>
              </VCard>
            </VCol>
          </VRow>
        </VForm>
      </VCardText>
    </VCard>
  </VDialog>

  <!-- Bulk Add Dialog -->
  <VDialog
    v-model="isBulkAddArticlesDialogOpen"
    width="600"
  >
    <VCard class="pa-3">
      <VCardTitle>Bulk Add Articles</VCardTitle>

      <VCardText>
        <VTextarea
          v-model="bulkAddTextareaContent"
          label="Enter URLs (one per line)"
          rows="5"
          variant="outlined"
        />
        <p
          v-if="bulkAddError"
          class="text-error mt-3"
        >
          {{ bulkAddError }}
        </p>
      </VCardText>

      <VCardActions class="justify-end">
        <VBtn
          color="primary"
          variant="tonal"
          @click="handleBulkAddArticles"
        >
          Confirm
        </VBtn>
      </VCardActions>
    </VCard>
  </VDialog>

  <!-- Image Preview Dialog -->
  <VDialog
    v-model="isImagePreviewVisible"
    fullscreen
    class="image-fullscreen-dialog"
  >
    <VCard
      flat
      class="fullscreen-card"
    >
      <VCardTitle class="preview-dialog-title">
        <div class="preview-dialog-actions">
          <VBtn
            icon="ri-close-line"
            color="white"
            variant="text"
            @click="closeImageViewer"
          />
        </div>
      </VCardTitle>

      <VCardText class="preview-dialog-content">
        <VImg
          :src="previewImageUrl"
          contain
          :style="{ transform: `scale(${imageZoomScale})` }"
          class="zoomable-image"
          @wheel.prevent="handleImageWheelZoom"
        />
      </VCardText>
    </VCard>
  </VDialog>
</template>

<style lang="scss" scoped>
.dialog-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 0.0625rem solid #e0e0e0;

  .dialog-actions {
    display: flex;
  }
}

.video-status-radio-group {
  padding-left: 1rem;
}

.articles-section {
  .article-buttons {
    display: flex;
    position: sticky;
    top: 0;
    z-index: 10;
    background-color: #312d4b;
    padding-top: 1rem;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
  }
}

.article-card {
  border: 0.0625rem solid #e0e0e0;
  border-radius: 0.5rem;
}

.article-card-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 0.0625rem solid #e0e0e0;
  font-weight: 500;
  margin-bottom: 1rem;

  .remove-article-btn {
    margin-left: 1rem;
  }
}

.image-section {
  margin-top: 1.25rem;

  .image-upload-initial {
    .image-upload-label {
      display: inline-flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 1rem;
      border: 0.125rem dashed #9e9e9e;
      border-radius: 0.5rem;
      cursor: pointer;
      transition: border-color 0.3s;
      text-align: center;
      width: 7.5rem;
      height: 7.5rem;

      &:hover {
        border-color: #42a5f5;
      }

      .image-upload-icon {
        display: flex;
        flex-direction: column;
        align-items: center;
        color: #757575;
      }
    }
  }

  .image-list-section {
    .image-list {
      list-style: none;
      padding: 0;
      min-height: 6.25rem;
    }

    .image-list-item {
      display: flex;
      align-items: center;
      padding: 0.75rem 0;
      border-bottom: 0.0625rem solid #f0f0f0;
      cursor: move;

      &:last-child {
        border-bottom: none;
      }

      .image-preview-small {
          margin-right: 1rem;
          border-radius: 0.25rem;
          overflow: hidden;
          border: 0.0625rem solid #e0e0e0;
        }

      .image-details {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;

        .file-name {
          font-weight: 500;
          margin-bottom: 0.25rem;
        }

        .file-size {
          font-size: 0.875rem;
          color: #757575;
        }

        .image-actions {
          display: flex;
          gap: 0.5rem;
          margin-top: 0.5rem;
        }
      }
    }

    .image-add-more-label {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      cursor: pointer;
      margin-top: 1rem;

      span {
        font-weight: 500;
        color: #3f51b5;
      }
    }
  }
}

.image-fullscreen-dialog {
  .v-dialog__content {
    max-width: 100%;
    max-height: 100%;
    overflow: hidden;
  }

  .v-card.fullscreen-card {
    width: 100vw;
    height: 100vh;
    max-width: 100vw;
    max-height: 100vh;
    border-radius: 0;
    background-color: black;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .v-card-title.preview-dialog-title {
    display: flex;
    justify-content: flex-end;
    padding: 1rem;
    color: white;
    border-bottom: none;
  }

  .v-card-text.preview-dialog-content {
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    overflow: hidden;
  }

  .preview-dialog-actions {
    display: flex;
    justify-content: flex-end;
  }

  .zoomable-image {
    cursor: zoom-in;
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    display: block;
  }
}
</style>
