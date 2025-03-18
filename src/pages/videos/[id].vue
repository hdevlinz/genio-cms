<script setup lang="ts">
import download from 'downloadjs'

import { VideoStatus, VideoStatusMapping } from '@/@db/apps/videos/enums'
import type { VideoDetail } from '@/@db/apps/videos/types'

definePage({
  meta: {
    public: true,

    // subject: 'news.videos',
    // action: 'read',
  },
})

const router = useRouter()
const route = useRoute('videos-id')

const isLoading = ref(false)
const videoDetail = ref<VideoDetail | null>(null)

const handleFetchVideoDetail = async () => {
  if (!route.params.id)
    return

  isLoading.value = true
  try {
    const { data } = await useApi<any>(createUrl(`/videos/${route.params.id}`))

    if (data.value)
      videoDetail.value = data.value
  }
  finally {
    isLoading.value = false
  }
}

const handleDownloadVideo = async () => {
  if (videoDetail.value && videoDetail.value.video_url) {
    const fileName = videoDetail.value.title?.toLocaleLowerCase().replace(/[^a-z0-9]/gi, '_').replace(/_+$/, '') || 'video'

    download(videoDetail.value.video_url, `${fileName}.mp4`, 'video/mp4')
  }
}

watch(() => route.params.id, handleFetchVideoDetail, { immediate: true })
</script>

<template>
  <div>
    <VCard
      class="pa-4"
      flat
    >
      <VCardTitle class="v-card-title">
        Video Detail
        <div>
          <VBtn
            color="secondary"
            variant="outlined"
            class="me-2"
            @click="() => router.back()"
          >
            Back
          </VBtn>
          <VBtn
            v-if="videoDetail?.status === VideoStatus.COMPLETED"
            color="primary"
            @click="handleDownloadVideo"
          >
            Download Video
          </VBtn>
        </div>
      </VCardTitle>

      <VCardText
        v-if="videoDetail"
        class="v-card-text"
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
                  {{ videoDetail.title || 'N/A' }}
                </VListItemSubtitle>
              </VListItem>

              <VListItem class="list-item">
                <VListItemTitle class="list-item-title">
                  Name
                </VListItemTitle>
                <VListItemSubtitle class="list-item-subtitle">
                  {{ videoDetail.name || 'N/A' }}
                </VListItemSubtitle>
              </VListItem>

              <VListItem class="list-item">
                <VListItemTitle class="list-item-title">
                  Description
                </VListItemTitle>
                <VListItemSubtitle class="list-item-subtitle">
                  {{ videoDetail.description || 'N/A' }}
                </VListItemSubtitle>
              </VListItem>

              <VListItem class="list-item">
                <VListItemTitle class="list-item-title">
                  Creation Date
                </VListItemTitle>
                <VListItemSubtitle class="list-item-subtitle">
                  {{ formatDateToTimeAgoString(videoDetail.created_at) }}
                </VListItemSubtitle>
              </VListItem>

              <VListItem class="list-item">
                <VListItemTitle class="list-item-title mb-1">
                  Status
                </VListItemTitle>
                <VListItemSubtitle class="list-item-subtitle">
                  <VChip
                    :color="VideoStatusMapping[videoDetail.status]?.color || 'grey'"
                    rounded="lg"
                  >
                    {{ VideoStatusMapping[videoDetail.status]?.label || 'Unknown' }}
                  </VChip>
                </VListItemSubtitle>
              </VListItem>

              <VListItem
                v-if="videoDetail.video_url"
                class="list-item"
              >
                <VListItemTitle class="list-item-title">
                  Video URL
                </VListItemTitle>
                <VListItemSubtitle class="list-item-subtitle">
                  <a
                    :href="videoDetail.video_url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="video-url-link"
                  >
                    {{ videoDetail.video_url }}
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
                v-if="videoDetail.video_url"
                controls
                class="video-preview"
                :src="videoDetail.video_url"
              />

              <div
                v-else
                class="no-preview"
              >
                <span>No video preview available</span>
              </div>
            </div>
          </VCol>
        </VRow>

        <VDivider class="my-6" />

        <h6 class="section-title mb-3">
          Articles
        </h6>

        <div v-if="videoDetail.articles && videoDetail.articles.length > 0">
          <VCard
            v-for="article in videoDetail.articles"
            :key="article.id"
            variant="tonal"
            class="article-preview-card"
          >
            <VCardItem>
              <VCardTitle class="article-card-title">
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
              </VCardTitle>

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

      <VCardText v-else-if="!isLoading && !videoDetail">
        <div class="no-preview">
          <span>No video detail available</span>
        </div>
      </VCardText>

      <VCardText
        v-if="isLoading"
        class="loading-text mt-6 text-center d-flex align-center justify-center w-100 h-100"
      >
        <VProgressCircular
          color="primary"
          class="me-2"
          indeterminate
        />
        Loading...
      </VCardText>
    </VCard>
  </div>
</template>

<style lang="scss" scoped>
.v-card-title {
   display: flex;
   justify-content: space-between;
   align-items: center;
   padding-bottom: 1rem;
   border-bottom: 0.0625rem solid #e0e0e0;
   font-size: 1.25rem;
   font-weight: 500;
}

.v-card-text {
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
</style>
