<script setup lang="ts">
import type { ArticleList, ArticleViewModel } from '@/@db/apps/articles/types'
import { OrderByMapping } from '@/@db/enums'

definePage({
  meta: {
    public: true,

    // subject: 'news.articles',
    // action: 'read',
  },
})

const router = useRouter()

const articleHeaders = [
  { title: '#', key: 'index', sortable: false, width: '3.125rem' },
  { title: 'Content', key: 'content', sortable: false },
  { title: 'Original URL', key: 'original_url', sortable: false },
  { title: 'Published At', key: 'published_at', sortable: true },
  { title: 'Created At', key: 'created_at', sortable: true },
  { title: 'Updated At', key: 'updated_at', sortable: true },
]

const articleList = ref<ArticleList>([])
const totalArticles = ref(0)
const articlePage = ref(1)
const articleSize = ref(10)
const articleOrderBy = ref('-created_at')
const articleSearchQuery = ref('')
const articleCancelNextFetch = ref(false)

const handleFetchChannelArticles = async () => {
  if (articleCancelNextFetch.value) {
    articleCancelNextFetch.value = false

    return
  }

  const { data } = await useApi<any>(createUrl('/articles', {
    query: {
      page: articlePage.value,
      size: articleSize.value,
      order_by: articleOrderBy.value,
      search: articleSearchQuery.value,
    },
  }))

  if (data.value && data.value.items) {
    articleList.value = data.value.items.map((item: ArticleViewModel, index: number) => ({
      ...item,
      index: (articlePage.value - 1) * articleSize.value + index + 1,
    }))
    totalArticles.value = data.value.total
  }
}

const handleSearchArticles = () => {
  handleFetchChannelArticles()
  articleCancelNextFetch.value = true
}

const handleClickArticle = (event: any, row: any) => {
  router.push({ name: 'articles-id', params: { id: row.item.id } })
}

watch([articlePage, articleSize, articleSearchQuery], handleFetchChannelArticles, { immediate: true })
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
            <!-- 👉 Search Articles -->
            <VTextField
              v-model="articleSearchQuery"
              placeholder="Search Articles..."
              density="compact"
              class="me-4"
              @keydown.enter="handleSearchArticles"
            />
          </div>
        </div>

        <VDataTableServer
          v-model:items-per-page="articleSize"
          v-model:page="articlePage"
          :headers="articleHeaders"
          :items="articleList"
          :items-length="totalArticles"
          class="text-no-wrap rounded-0"
          must-sort
          @click:row="handleClickArticle"
          @update:sort-by="(event) => {
            if (!isEmptyArray(event)) {
              const { key, order } = event[0]
              articleOrderBy = `${OrderByMapping[order as keyof typeof OrderByMapping]}${key}`
            }
          }"
        >
          <template #item.content="{ item }">
            {{ item.content ? truncateString(item.content, 66) : '-' }}
          </template>

          <template #item.original_url="{ item }">
            <a
              :href="item.original_url"
              target="_blank"
              rel="noopener noreferrer"
              @click="(event) => event.stopPropagation()"
            >
              {{ item.original_url }}
            </a>
          </template>

          <template #item.published_at="{ item }">
            {{ formatDateToTimeAgoString(item.published_at) }}
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
                  v-model="articleSize"
                  class="per-page-select"
                  variant="plain"
                  :items="[10, 20, 25, 50, 100]"
                />
              </div>
              <p class="d-flex align-center text-base text-high-emphasis me-2 mb-0">
                {{ paginationMeta({ page: articlePage, itemsPerPage: articleSize }, totalArticles) }}
              </p>
              <div class="d-flex gap-x-2 align-center me-2">
                <VBtn
                  class="flip-in-rtl"
                  icon="ri-arrow-left-s-line"
                  variant="text"
                  density="comfortable"
                  color="high-emphasis"
                  :disabled="articlePage <= 1"
                  @click="articlePage = Math.max(1, articlePage - 1)"
                />
                <VBtn
                  class="flip-in-rtl"
                  icon="ri-arrow-right-s-line"
                  density="comfortable"
                  variant="text"
                  color="high-emphasis"
                  :disabled="articlePage >= Math.ceil(totalArticles / articleSize)"
                  @click="articlePage = Math.min(Math.ceil(totalArticles / articleSize), articlePage + 1)"
                />
              </div>
            </div>
          </template>
        </VDataTableServer>
      </vcardtext>
    </VCard>
  </section>
</template>

<style lang="scss" scoped>
// Empty Style
</style>
