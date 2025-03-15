<script setup lang="ts">
import type { VideoList, VideoViewModel } from '@/@db/app/videos/types'
import { VideoStatusMapping } from '@/@db/enums'

definePage({
  meta: {
    public: true,

    // subject: 'news.videos',
    // action: 'read',
  },
})

const isAddVideoDialogVisible = ref(false)
const isPreviewDialogVisible = ref(false)
const selectedVideoId = ref<string | null>(null)

const videoHeaders = [
  { title: '#', key: 'index', sortable: false, width: '3.125rem' },
  { title: 'Title', key: 'title', sortable: false },
  { title: 'Description', key: 'description', sortable: false },
  { title: 'Status', key: 'status', sortable: false },
  { title: 'Created At', key: 'created_at', sortable: true },
  { title: 'Updated At', key: 'updated_at', sortable: true },
]

const channelVideos = ref<VideoList>([])
const totalChannelVideos = ref(0)
const videoPage = ref(1)
const videoSize = ref(10)
const videoSearchQuery = ref('')
const videoCancelNextFetch = ref(false)

const handleFetchVideos = async () => {
  if (videoCancelNextFetch.value) {
    videoCancelNextFetch.value = false

    return
  }

  const { data } = await useApi<any>(createUrl('/news/videos', {
    query: {
      page: videoPage.value,
      size: videoSize.value,
      search: videoSearchQuery.value,
    },
  }))

  if (data.value && data.value.items) {
    channelVideos.value = data.value.items.map((item: VideoViewModel, index: number) => ({
      ...item,
      index: (videoPage.value - 1) * videoSize.value + index + 1,
    }))
    totalChannelVideos.value = data.value.total
  }
}

const handleSearchVideos = () => {
  handleFetchVideos()
  videoCancelNextFetch.value = true
}

const handleClickVideo = (event: any, row: any) => {
  selectedVideoId.value = row.item.id
  isPreviewDialogVisible.value = true
}

watch([videoPage, videoSize, videoSearchQuery], handleFetchVideos, { immediate: true })
</script>

<template>
  <section>
    <VCard>
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4">
        <div class="d-flex align-center flex-grow-1 justify-space-between flex-wrap gap-4 mb-4">
          <div
            class="d-flex align-center flex-grow-1"
            style="max-width: 25rem; inline-size: 24.0625rem;"
          >
            <!-- 👉 Search Videos -->
            <VTextField
              v-model="videoSearchQuery"
              placeholder="Search Videos..."
              density="compact"
              class="me-4"
              @keydown.enter="handleSearchVideos"
            />
          </div>

          <div class="d-flex align-center gap-4">
            <VBtn
              color="primary"
              @click="isAddVideoDialogVisible = true"
            >
              Create New Video
            </VBtn>
          </div>
        </div>

        <VDataTableServer
          v-model:items-per-page="videoSize"
          v-model:page="videoPage"
          :headers="videoHeaders"
          :items="channelVideos"
          :items-length="totalChannelVideos"
          class="text-no-wrap rounded-0"
          @click:row="handleClickVideo"
        >
          <template #item.description="{ item }">
            {{ truncateString(item.description, 66) }}
          </template>

          <template #item.created_at="{ item }">
            {{ formatDateToTimeAgoString(item.created_at) }}
          </template>

          <template #item.updated_at="{ item }">
            {{ formatDateToTimeAgoString(item.updated_at) }}
          </template>

          <template #item.status="{ item }">
            <VChip :color="VideoStatusMapping[item.status].color">
              {{ VideoStatusMapping[item.status].label }}
            </VChip>
          </template>

          <template #bottom>
            <VDivider />
            <div class="d-flex justify-end flex-wrap gap-x-6 px-2 py-1">
              <div class="d-flex align-center gap-x-2 text-medium-emphasis text-base">
                Rows Per Page:
                <VSelect
                  v-model="videoSize"
                  class="per-page-select"
                  variant="plain"
                  :items="[10, 20, 25, 50, 100]"
                />
              </div>
              <p class="d-flex align-center text-base text-high-emphasis me-2 mb-0">
                {{ paginationMeta({ page: videoPage, itemsPerPage: videoSize }, totalChannelVideos) }}
              </p>
              <div class="d-flex gap-x-2 align-center me-2">
                <VBtn
                  class="flip-in-rtl"
                  icon="ri-arrow-left-s-line"
                  variant="text"
                  density="comfortable"
                  color="high-emphasis"
                  :disabled="videoPage <= 1"
                  @click="videoPage = Math.max(1, videoPage - 1)"
                />
                <VBtn
                  class="flip-in-rtl"
                  icon="ri-arrow-right-s-line"
                  density="comfortable"
                  variant="text"
                  color="high-emphasis"
                  :disabled="videoPage >= Math.ceil(totalChannelVideos / videoSize)"
                  @click="videoPage = Math.min(Math.ceil(totalChannelVideos / videoSize), videoPage + 1)"
                />
              </div>
            </div>
          </template>
        </VDataTableServer>
      </vcardtext>
    </VCard>

    <AddNewVideoDialog v-model:isVisible="isAddVideoDialogVisible" />

    <VideoPreviewDialog
      v-model:isVisible="isPreviewDialogVisible"
      :video-id="selectedVideoId"
    />
  </section>
</template>

<style lang="scss" scoped>
// Empty Style
</style>
