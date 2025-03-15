<script setup lang="ts">
import download from 'downloadjs'

import { VideoStatus } from '@/@db/app/videos/enums'
import type { VideoDetail } from '@/@db/app/videos/types'
import { VideoStatusMapping } from '@/@db/enums'

interface Props {
  isVisible: boolean
  videoId?: string | null
  workspaceId?: string | null
  channelId?: string | null
}

interface Emit {
  (e: 'update:isVisible', value: boolean): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emit>()

const isPreviewDialogVisible = ref(props.isVisible)
const videoDetails = ref<VideoDetail | null>(null)
const isLoading = ref(false)

const handleFetchVideoDetails = async () => {
  isLoading.value = true
  try {
    const { data } = await useApi<any>(createUrl(`/news/videos/${props.videoId}`))

    if (data.value)
      videoDetails.value = data.value
  }
  finally {
    isLoading.value = false
  }
}

const handleDownloadVideo = async () => {
  if (videoDetails.value && videoDetails.value.result_video_url) {
    const fileName = videoDetails.value.title?.toLocaleLowerCase().replace(/[^a-z0-9]/gi, '_').replace(/_+$/, '') || 'video'

    download(videoDetails.value.result_video_url, `${fileName}.mp4`, 'video/mp4')
  }
}

watch(isPreviewDialogVisible, newValue => emit('update:isVisible', newValue))

watch(() => props.videoId, newValue => {
  if (newValue && isPreviewDialogVisible.value)
    handleFetchVideoDetails()
})

watch(() => props.isVisible, newValue => {
  isPreviewDialogVisible.value = newValue
  if (newValue)
    handleFetchVideoDetails()
  else
    videoDetails.value = null
})
</script>

<template>
  <VDialog
    v-model="isPreviewDialogVisible"
    width="1200"
    class="video-preview-dialog"
  >
    <VCard
      class="pa-4"
      flat
    >
      <VCardTitle class="preview-card-title">
        Video Preview
        <div class="dialog-actions">
          <VBtn
            v-if="videoDetails?.status === VideoStatus.COMPLETED"
            color="primary"
            tooltip="Download Video"
            location="bottom"
            @click="handleDownloadVideo"
          >
            Download
          </VBtn>
        </div>
      </VCardTitle>

      <VCardText
        v-if="videoDetails"
        class="preview-card-text"
      >
        <VRow>
          <VCol
            cols="12"
            md="6"
          >
            <h6 class="section-title">
              Video Information
            </h6>

            <VList lines="two">
              <VListItem class="list-item">
                <VListItemTitle class="list-item-title">
                  Title
                </VListItemTitle>
                <VListItemSubtitle class="list-item-subtitle">
                  {{ videoDetails.title || 'N/A' }}
                </VListItemSubtitle>
              </VListItem>

              <VListItem class="list-item">
                <VListItemTitle class="list-item-title">
                  Channel
                </VListItemTitle>
                <VListItemSubtitle class="list-item-subtitle">
                  {{ videoDetails.channel?.category || 'N/A' }}
                </VListItemSubtitle>
              </VListItem>

              <VListItem class="list-item">
                <VListItemTitle class="list-item-title">
                  Description
                </VListItemTitle>
                <VListItemSubtitle class="list-item-subtitle">
                  {{ videoDetails.description || 'N/A' }}
                </VListItemSubtitle>
              </VListItem>

              <VListItem class="list-item">
                <VListItemTitle class="list-item-title">
                  Creation Date
                </VListItemTitle>
                <VListItemSubtitle class="list-item-subtitle">
                  {{ formatDateToTimeAgoString(videoDetails.created_at) }}
                </VListItemSubtitle>
              </VListItem>

              <VListItem class="list-item">
                <VListItemTitle class="list-item-title mb-1">
                  Status
                </VListItemTitle>
                <VListItemSubtitle class="list-item-subtitle">
                  <VChip
                    :color="VideoStatusMapping[videoDetails.status]?.color || 'grey'"
                    rounded="lg"
                  >
                    {{ VideoStatusMapping[videoDetails.status]?.label || 'Unknown' }}
                  </VChip>
                </VListItemSubtitle>
              </VListItem>

              <VListItem
                v-if="videoDetails.result_video_url"
                class="list-item"
              >
                <VListItemTitle class="list-item-title">
                  Video URL
                </VListItemTitle>
                <VListItemSubtitle class="list-item-subtitle">
                  <a
                    :href="videoDetails.result_video_url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="video-url-link"
                  >
                    {{ videoDetails.result_video_url }}
                    <VIcon
                      size="small"
                      icon="ri-external-link-line"
                    />
                  </a>
                </VListItemSubtitle>
              </VListItem>
            </VList>
          </VCol>

          <VCol
            cols="12"
            md="6"
          >
            <h6 class="section-title mb-2">
              Video Preview
            </h6>

            <div class="video-preview-container">
              <video
                v-if="videoDetails.result_video_url"
                controls
                class="video-preview"
                :src="videoDetails.result_video_url"
              />

              <div
                v-else
                class="no-preview"
              >
                <span>No video or image preview available</span>
              </div>
            </div>
          </VCol>
        </VRow>

        <VDivider class="my-6" />

        <h6 class="section-title mb-3">
          Articles
        </h6>

        <div v-if="videoDetails.articles && videoDetails.articles.length > 0">
          <VCard
            v-for="article in videoDetails.articles"
            :key="article.id"
            variant="tonal"
            class="article-preview-card"
          >
            <VCardItem>
              <VCardTitle class="article-card-title">
                {{ article.title }}
              </VCardTitle>

              <VCardText class="article-card-text">
                <a
                  :href="article.original_url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="article-url-link"
                >
                  {{ article.original_url }}
                  <VIcon
                    size="small"
                    icon="ri-external-link-line"
                  />
                </a>
              </VCardText>

              <VCardText class="article-card-text">
                {{ article.content }}
              </VCardText>
            </VCardItem>
          </VCard>
        </div>

        <div
          v-else
          class="no-articles"
        >
          No articles associated with this video.
        </div>
      </VCardText>

      <VCardText v-else-if="!isLoading && !videoDetails">
        <div class="no-preview">
          <span>No video details available</span>
        </div>
      </VCardText>

      <VCardText
        v-if="isLoading"
        class="loading-text"
      >
        <VProgressCircular
          indeterminate
          color="primary"
          class="me-2"
        />
        Loading
      </VCardText>
    </VCard>
  </VDialog>
</template>

<style lang="scss" scoped>
.video-preview-dialog {
  .preview-card-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 1rem;
    border-bottom: 0.0625rem solid #e0e0e0;
    font-size: 1.25rem;
    font-weight: 500;
  }

  .preview-card-text {
    padding-top: 1.5rem;
  }

  .section-title {
    font-size: 1rem;
    font-weight: 500;
    margin-top: 1rem;
  }

  .list-item {
    padding: 0 !important;

    .list-item-title {
      font-weight: bold;
    }

    .list-item-subtitle {
      color: var(--v-theme-text-base);
    }
  }

  .video-url-link, .article-url-link {
    text-decoration: none;
    display: inline-flex;
    align-items: center;

    &:hover {
      text-decoration: underline;
    }
  }

  .video-preview-container {
    position: relative;
    border-radius: 0.5rem;
    overflow: hidden;

    .video-preview {
      width: 100%;
      aspect-ratio: 16 / 9;
    }
  }

  .image-previews {
    display: flex;
    gap: 0.5rem;
    overflow-x: auto;
    padding-top: 0.5rem;
  }

  .image-preview-item {
    border-radius: 0.5rem;
  }

  .no-preview, .no-articles, .loading-text {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 15.625rem;
    border-radius: 0.5rem;
    color: #777;
  }

  .article-preview-card {
    margin-bottom: 1rem;
    border-radius: 0.5rem;

    .v-card-item {
      padding: 1.25rem;
    }

    .article-card-title {
      font-weight: 500;
      margin-bottom: 0.5rem;
    }

    .article-card-text {
      color: var(--v-theme-text-base);
      padding: 0 !important;
    }
  }
}
</style>
