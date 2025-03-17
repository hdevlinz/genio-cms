<script setup lang="ts">
import type { ChannelList, ChannelViewModel } from '@/@db/app/channels/types'
import AddEditChannelDrawer from '@/views/apps/channels/AddEditChannelDrawer.vue'

definePage({
  meta: {
    public: true,

    // subject: 'news.channels',
    // action: 'read',
  },
})

const isAddEditChannelDrawerVisible = ref(false)
const selectedChannel = ref<ChannelViewModel | null>(null)

const articleHeaders = [
  { title: '#', key: 'index', sortable: false, width: '3.125rem' },
  { title: 'Name', key: 'name', sortable: false },
  { title: 'Category', key: 'category', sortable: false },
  { title: 'Created At', key: 'created_at', sortable: true },
  { title: 'Updated At', key: 'updated_at', sortable: true },
]

const channels = ref<ChannelList>([])
const totalChannels = ref(0)
const channelPage = ref(1)
const channelSize = ref(10)
const channelSearchQuery = ref('')
const channelCancelNextFetch = ref(false)

const handleFetchChannels = async () => {
  if (channelCancelNextFetch.value) {
    channelCancelNextFetch.value = false

    return
  }

  const { data } = await useApi<any>(createUrl('/news/channels', {
    query: {
      page: channelPage.value,
      size: channelSize.value,
      search: channelSearchQuery.value,
    },
  }))

  if (data.value && data.value.items) {
    channels.value = data.value.items.map((item: ChannelViewModel, index: number) => ({
      ...item,
      index: (channelPage.value - 1) * channelSize.value + index + 1,
    }))
    totalChannels.value = data.value.total
  }
}

const handleSearchChannels = () => {
  handleFetchChannels()
  channelCancelNextFetch.value = true
}

const handleClickChannel = (event: any, row: any) => {
  selectedChannel.value = row.item
  isAddEditChannelDrawerVisible.value = true
}

watch([channelPage, channelSize, channelSearchQuery], handleFetchChannels, { immediate: true })

watch(() => isAddEditChannelDrawerVisible.value, val => {
  if (!val)
    selectedChannel.value = null
})
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
            <!-- 👉 Search Channels -->
            <VTextField
              v-model="channelSearchQuery"
              placeholder="Search Channels..."
              density="compact"
              class="me-4"
              @keydown.enter="handleSearchChannels"
            />
          </div>

          <div class="d-flex align-center gap-4">
            <VBtn
              color="primary"
              @click="isAddEditChannelDrawerVisible = true"
            >
              Create New Channel
            </VBtn>
          </div>
        </div>

        <VDataTableServer
          v-model:items-per-page="channelSize"
          v-model:page="channelPage"
          :headers="articleHeaders"
          :items="channels"
          :items-length="totalChannels"
          class="text-no-wrap rounded-0"
          @click:row="handleClickChannel"
        >
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
                  v-model="channelSize"
                  class="per-page-select"
                  variant="plain"
                  :items="[10, 20, 25, 50, 100]"
                />
              </div>
              <p class="d-flex align-center text-base text-high-emphasis me-2 mb-0">
                {{ paginationMeta({ page: channelPage, itemsPerPage: channelSize }, totalChannels) }}
              </p>
              <div class="d-flex gap-x-2 align-center me-2">
                <VBtn
                  class="flip-in-rtl"
                  icon="ri-arrow-left-s-line"
                  variant="text"
                  density="comfortable"
                  color="high-emphasis"
                  :disabled="channelPage <= 1"
                  @click="channelPage = Math.max(1, channelPage - 1)"
                />
                <VBtn
                  class="flip-in-rtl"
                  icon="ri-arrow-right-s-line"
                  density="comfortable"
                  variant="text"
                  color="high-emphasis"
                  :disabled="channelPage >= Math.ceil(totalChannels / channelSize)"
                  @click="channelPage = Math.min(Math.ceil(totalChannels / channelSize), channelPage + 1)"
                />
              </div>
            </div>
          </template>
        </VDataTableServer>
      </vcardtext>
    </VCard>

    <AddEditChannelDrawer
      v-model:isDrawerOpen="isAddEditChannelDrawerVisible"
      :item-data="selectedChannel"
      @success="handleFetchChannels"
    />
  </section>
</template>

<style lang="scss" scoped>
// Empty Style
</style>
