<script setup lang="ts">
import { StatusCodes } from 'http-status-codes'
import { VFileInput } from 'vuetify/components/VFileInput'

import type { BackgroundVideoList, BackgroundVideoViewModel } from '@/@db/apps/materials/types'
import { OrderByMapping } from '@/@db/enums'

const backgroundVideoHeaders = [
  { title: '#', key: 'index', sortable: false, width: '3.125rem' },
  { title: 'Name', key: 'name', sortable: false },
  { title: 'Size', key: 'size', sortable: false },
  { title: 'Active', key: 'is_active', sortable: false },
  { title: 'Created At', key: 'created_at', sortable: true },
  { title: 'Updated At', key: 'updated_at', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false },
]

const backgroundVideoList = ref<BackgroundVideoList>([])
const totalBackgroundVideos = ref(0)
const backgroundVideoPage = ref(1)
const backgroundVideoSize = ref(10)
const backgroundVideoOrderBy = ref('-created_at')
const backgroundVideoSearchQuery = ref('')
const backgroundVideoCancelNextFetch = ref(false)

const isSubmitLoading = ref(false)
const isAddVideoDialogVisible = ref(false)
const selectedVideoFiles = ref<File[]>([])
const refFileInput = ref<VFileInput | null>(null)

const {
  selectedItem,
  confirmationQuestion,
  dialogVisible,
  openConfirmDialog,
  handleConfirmation,
  updateDialogVisible,
} = useConfirmChangeDialog()

const handleFetchBackgroundVideos = async () => {
  if (backgroundVideoCancelNextFetch.value) {
    backgroundVideoCancelNextFetch.value = false

    return
  }

  const { data } = await useApi<any>(createUrl('/materials/background-videos', {
    query: {
      page: backgroundVideoPage.value,
      size: backgroundVideoSize.value,
      order_by: backgroundVideoOrderBy.value,
      search: backgroundVideoSearchQuery.value,
    },
  }))

  if (data.value && data.value.items) {
    backgroundVideoList.value = data.value.items.map((item: BackgroundVideoViewModel, index: number) => ({
      ...item,
      index: (backgroundVideoPage.value - 1) * backgroundVideoSize.value + index + 1,
    }))
    totalBackgroundVideos.value = data.value.total
  }
}

const handleUploadBackgroundVideos = async () => {
  isAddVideoDialogVisible.value = false
  isSubmitLoading.value = true
  try {
    const formData = new FormData()

    selectedVideoFiles.value.forEach(file => formData.append('files', file))

    const { statusCode } = await useApi<any>(createUrl('/materials/background-videos')).post(formData)

    if (statusCode.value === StatusCodes.CREATED) {
      selectedVideoFiles.value = []
      handleFetchBackgroundVideos()
    }
  }
  finally {
    isSubmitLoading.value = false
  }
}

const handleUpdateStatus = async (confirmed: boolean) => {
  if (confirmed && selectedItem.value) {
    const newActiveStatus = !selectedItem.value.is_active
    const selectedBackgroundVideoId = selectedItem.value.id

    await useApi<any>(`/materials/background-videos/${selectedItem.value.id}`).put({
      name: selectedItem.value.name,
      is_active: newActiveStatus,
    })

    const updatedItem = backgroundVideoList.value.find(backgroundVideo => backgroundVideo.id === selectedBackgroundVideoId)
    if (updatedItem)
      updatedItem.is_active = newActiveStatus
  }
  selectedItem.value = null
}

const handleDeleteBackgroundVideo = async (confirmed: boolean) => {
  if (confirmed && selectedItem.value) {
    const { statusCode } = await useApi<any>(createUrl(`/materials/background-videos/${selectedItem.value.id}`)).delete()

    if (statusCode.value === StatusCodes.NO_CONTENT)
      handleFetchBackgroundVideos()
  }

  selectedItem.value = null
}

const handleSearchBackgroundVideos = () => {
  handleFetchBackgroundVideos()
  backgroundVideoCancelNextFetch.value = true
}

const handleUploadButtonClick = () => {
  refFileInput.value?.click()
}

const handleVideoFilesChange = (event: any) => {
  selectedVideoFiles.value = Array.from(event.target.files)
  isAddVideoDialogVisible.value = true
}

watch([backgroundVideoPage, backgroundVideoSize, backgroundVideoSearchQuery], handleFetchBackgroundVideos, { immediate: true })
</script>

<template>
  <div
    v-if="isSubmitLoading"
    class="position-fixed d-flex align-center justify-center"
    style="z-index: 99999999; inset: 0; background: rgba(0, 0, 0, 0.5);"
  >
    <VProgressCircular
      color="primary"
      class="me-2"
      indeterminate
    />
    <span class="text-white">Submitting...</span>
  </div>

  <VCard class="pa-4">
    <VCardtext class="d-flex align-center justify-space-between flex-wrap gap-4">
      <div class="d-flex align-center flex-grow-1 justify-space-between flex-wrap gap-4 mb-4">
        <div
          class="d-flex align-center flex-grow-1"
          style="max-width: 25rem; inline-size: 24.0625rem;"
        >
          <!-- 👉 Search Background Videos -->
          <VTextField
            v-model="backgroundVideoSearchQuery"
            placeholder="Search Background Videos..."
            density="compact"
            class="me-4"
            @keydown.enter="handleSearchBackgroundVideos"
          />
        </div>

        <div class="d-flex align-center gap-4">
          <VBtn
            color="primary"
            @click="handleUploadButtonClick"
          >
            Upload Background Videos
          </VBtn>

          <VFileInput
            ref="refFileInput"
            type="file"
            multiple
            accept="video/*"
            class="d-none"
            @change="handleVideoFilesChange"
          />
        </div>
      </div>

      <VDataTableServer
        v-model:items-per-page="backgroundVideoSize"
        v-model:page="backgroundVideoPage"
        :headers="backgroundVideoHeaders"
        :items="backgroundVideoList"
        :items-length="totalBackgroundVideos"
        class="text-no-wrap rounded-0"
        must-sort
        @update:sort-by="(event) => {
          if (!isEmptyArray(event)) {
            const { key, order } = event[0]
            backgroundVideoOrderBy = `${OrderByMapping[order as keyof typeof OrderByMapping]}${key}`
          }
        }"
      >
        <template #item.size="{ item }">
          {{ item.size ? formatFileSize(item.size) : '-' }}
        </template>

        <template #item.is_active="{ item }">
          <VChip
            :color="item.is_active ? 'success' : 'secondary'"
            class="text-white"
            small
            style="cursor: pointer;"
            @click="openConfirmDialog(
              item,
              `You sure you want to ${item.is_active ? 'deactivate' : 'activate'}?`,
              handleUpdateStatus,
            )"
          >
            {{ item.is_active ? 'Active' : 'Inactive' }}
          </VChip>
        </template>

        <template #item.created_at="{ item }">
          {{ formatDateToTimeAgoString(item.created_at) }}
        </template>

        <template #item.updated_at="{ item }">
          {{ formatDateToTimeAgoString(item.updated_at) }}
        </template>

        <template #item.actions="{ item }">
          <IconBtn
            size="small"
            color="error"
            @click="openConfirmDialog(
              item,
              `Are you sure you want to delete this background video?`,
              handleDeleteBackgroundVideo,
            )"
          >
            <VIcon icon="ri-delete-bin-6-fill" />
          </IconBtn>
        </template>

        <template #bottom>
          <VDivider />
          <div class="d-flex justify-end flex-wrap gap-x-6 px-2 py-1">
            <div class="d-flex align-center gap-x-2 text-medium-emphasis text-base">
              Rows Per Page:
              <VSelect
                v-model="backgroundVideoSize"
                class="per-page-select"
                variant="plain"
                :items="[10, 20, 25, 50, 100]"
              />
            </div>
            <p class="d-flex align-center text-base text-high-emphasis me-2 mb-0">
              {{ paginationMeta({ page: backgroundVideoPage, itemsPerPage: backgroundVideoSize }, totalBackgroundVideos) }}
            </p>
            <div class="d-flex gap-x-2 align-center me-2">
              <VBtn
                class="flip-in-rtl"
                icon="ri-arrow-left-s-line"
                variant="text"
                density="comfortable"
                color="high-emphasis"
                :disabled="backgroundVideoPage <= 1"
                @click="backgroundVideoPage = Math.max(1, backgroundVideoPage - 1)"
              />
              <VBtn
                class="flip-in-rtl"
                icon="ri-arrow-right-s-line"
                density="comfortable"
                variant="text"
                color="high-emphasis"
                :disabled="backgroundVideoPage >= Math.ceil(totalBackgroundVideos / backgroundVideoSize)"
                @click="backgroundVideoPage = Math.min(Math.ceil(totalBackgroundVideos / backgroundVideoSize), backgroundVideoPage + 1)"
              />
            </div>
          </div>
        </template>
      </VDataTableServer>
    </VCardText>
  </VCard>

  <!-- Upload Video List Dialog -->
  <VDialog
    v-model="isAddVideoDialogVisible"
    width="900"
  >
    <VCard class="pa-4">
      <VCardTitle>
        Selected Videos
      </VCardTitle>

      <VCardText>
        <VList>
          <VListItem
            v-for="(file, index) in selectedVideoFiles"
            :key="index"
          >
            <VListItemTitle>{{ file.name }}</VListItemTitle>

            <VListItemSubtitle>{{ formatFileSize(file.size) }}</VListItemSubtitle>
          </VListItem>
        </VList>
      </VCardText>

      <VCardActions class="justify-end">
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
          variant="tonal"
          @click="handleUploadBackgroundVideos"
        >
          Upload
        </VBtn>
      </VCardActions>
    </VCard>
  </VDialog>

  <ConfirmDialog
    :confirmation-question="confirmationQuestion"
    :is-dialog-visible="dialogVisible"
    confirm-title="Confirmed!"
    confirm-msg="Background video deleted successfully."
    cancel-title="Cancelled"
    cancel-msg="Your action has been cancelled."
    @update:is-dialog-visible="updateDialogVisible"
    @confirm="handleConfirmation"
  />
</template>

<style lang="scss" scoped>
// Empty Style
</style>
