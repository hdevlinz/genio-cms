<script setup lang="ts">
import { VideoStatusMapping } from '@/@db/apps/videos/enums'
import type { VideoList, VideoViewModel } from '@/@db/apps/videos/types'
import { OrderByMapping } from '@/@db/enums'

definePage({
  meta: {
    public: true,

    // subject: 'news.videos',
    // action: 'read',
  },
})

const router = useRouter()

const isAddVideoDialogVisible = ref(false)

const videoHeaders = [
  { title: '#', key: 'index', sortable: false, width: '3.125rem' },
  { title: 'Status', key: 'status', sortable: false },
  { title: 'Title', key: 'title', sortable: false },
  { title: 'Name', key: 'name', sortable: false },
  { title: 'Description', key: 'description', sortable: false },
  { title: 'Duration', key: 'duration', sortable: false },
  { title: 'Language', key: 'language', sortable: false },
  { title: 'Topic', key: 'topic', sortable: false },
  { title: 'Created At', key: 'created_at', sortable: true },
  { title: 'Updated At', key: 'updated_at', sortable: true },
]

const videoList = ref<VideoList>([])
const totalVideos = ref(0)
const videoPage = ref(1)
const videoSize = ref(10)
const videoOrderBy = ref('-created_at')
const videoSearchQuery = ref('')
const videoCancelNextFetch = ref(false)

const handleFetchVideos = async () => {
  if (videoCancelNextFetch.value) {
    videoCancelNextFetch.value = false

    return
  }

  const { data } = await useApi<any>(createUrl('/videos', {
    query: {
      page: videoPage.value,
      size: videoSize.value,
      order_by: videoOrderBy.value,
      search: videoSearchQuery.value,
    },
  }))

  if (data.value && data.value.items) {
    videoList.value = data.value.items.map((item: VideoViewModel, index: number) => ({
      ...item,
      index: (videoPage.value - 1) * videoSize.value + index + 1,
    }))
    totalVideos.value = data.value.total
  }
}

const handleSearchVideos = () => {
  handleFetchVideos()
  videoCancelNextFetch.value = true
}

const handleClickVideo = (event: any, row: any) => {
  router.push({ name: 'videos-id', params: { id: row.item.id } })
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
          :items="videoList"
          :items-length="totalVideos"
          class="text-no-wrap rounded-0"
          must-sort
          @click:row="handleClickVideo"
          @update:sort-by="(event) => {
            if (!isEmptyArray(event)) {
              const { key, order } = event[0]
              videoOrderBy = `${OrderByMapping[order as keyof typeof OrderByMapping]}${key}`
            }
          }"
        >
          <template #item.status="{ item }">
            <VChip :color="VideoStatusMapping[item.status].color">
              {{ VideoStatusMapping[item.status].label }}
            </VChip>
          </template>

          <template #item.duration="{ item }">
            {{ formatNumber(item.duration) }}
          </template>

          <template #item.description="{ item }">
            {{ item.description ? truncateString(item.description, 66) : '-' }}
          </template>

          <template #item.created_at="{ item }">
            {{ formatDateToTimeAgoString(item.created_at) }}
          </template>

          <template #item.updated_at="{ item }">
            {{ formatDateToTimeAgoString(item.updated_at) }}
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
                {{ paginationMeta({ page: videoPage, itemsPerPage: videoSize }, totalVideos) }}
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
                  :disabled="videoPage >= Math.ceil(totalVideos / videoSize)"
                  @click="videoPage = Math.min(Math.ceil(totalVideos / videoSize), videoPage + 1)"
                />
              </div>
            </div>
          </template>
        </VDataTableServer>
      </vcardtext>
    </VCard>

    <AddNewVideoDialog
      v-model:isVisible="isAddVideoDialogVisible"
      @success="handleFetchVideos"
    />
  </section>
</template>

<style lang="scss" scoped>
// Empty Style
</style>
