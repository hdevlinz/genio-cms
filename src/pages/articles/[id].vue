<script setup lang="ts">
import { Carousel, Navigation, Slide } from 'vue3-carousel'

import type { ArticleDetail } from '@/@db/app/articles/types'

definePage({
  meta: {
    public: true,

    // subject: 'news.articles',
    // action: 'read',
  },
})

const router = useRouter()
const route = useRoute('articles-id')

const currentSlide = ref(0)

const galleryConfig = {
  itemsToShow: 1,
  wrapAround: true,
  slideEffect: 'fade' as const,
  mouseDrag: false,
  touchDrag: false,
  height: 500,
}

const thumbnailsConfig = {
  height: 100,
  itemsToShow: 6,
  wrapAround: true,
  touchDrag: false,
  gap: 10,
}

const isLoading = ref(false)
const articleDetail = ref<ArticleDetail | null>(null)

const handleFetchArticleDetail = async () => {
  if (!route.params.id)
    return

  isLoading.value = true
  try {
    const { data } = await useApi<any>(createUrl(`/news/articles/${route.params.id}`))

    if (data.value)
      articleDetail.value = data.value
  }
  finally {
    isLoading.value = false
  }
}

const slideTo = (nextSlide: number) => (currentSlide.value = nextSlide)

watch(() => route.params.id, handleFetchArticleDetail, { immediate: true })
</script>

<template>
  <div>
    <VCard class="pa-4">
      <VCardTitle class="text-h5 v-card-title">
        Article Detail
        <div class="dialog-actions">
          <VBtn
            color="secondary"
            variant="outlined"
            class="me-2"
            @click="() => router.back()"
          >
            Back
          </VBtn>
        </div>
      </VCardTitle>

      <VCardText
        v-if="articleDetail"
        class="pt-4"
      >
        <VRow>
          <VCol cols="12">
            <VTextField
              v-model="articleDetail.title"
              label="Title"
              variant="outlined"
              readonly
            />
          </VCol>

          <VCol cols="12">
            <VTextarea
              v-model="articleDetail.content"
              label="Content"
              variant="outlined"
              rows="5"
              readonly
            />
          </VCol>

          <VCol cols="12">
            <VTextField
              v-model="articleDetail.original_url"
              label="Original URL"
              variant="outlined"
              readonly
            />
          </VCol>

          <VCol
            v-if="articleDetail.images && articleDetail.images.length > 0"
            cols="12"
          >
            <div>Images</div>
            <Carousel
              id="gallery"
              v-bind="galleryConfig"
              v-model="currentSlide"
            >
              <Slide
                v-for="(image, index) in articleDetail.images"
                :key="index"
              >
                <img
                  :src="image"
                  alt="Article Image"
                  class="gallery-image"
                >
              </Slide>
            </Carousel>

            <Carousel
              id="thumbnails"
              v-bind="thumbnailsConfig"
              v-model="currentSlide"
            >
              <Slide
                v-for="(image, index) in articleDetail.images"
                :key="index"
              >
                <template #default="{ currentIndex, isActive }">
                  <div
                    class="thumbnail"
                    :class="[{ 'is-active': isActive }]"
                    @click="slideTo(currentIndex)"
                  >
                    <img
                      :src="image"
                      alt="Article Image"
                      class="thumbnail-image"
                    >
                  </div>
                </template>
              </Slide>

              <template #addons>
                <Navigation />
              </template>
            </Carousel>
          </VCol>

          <VCol cols="12">
            <div>Related URLs</div>
            <ul>
              <li
                v-for="(url, index) in articleDetail.related_urls"
                :key="index"
              >
                <a
                  :href="url"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {{ url }}
                </a>
              </li>
            </ul>
          </VCol>
        </VRow>
      </VCardText>

      <VCardText v-else-if="!isLoading && !articleDetail">
        <div class="no-preview">
          <span>No article detail available</span>
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

.carousel {
  --vc-nav-background: rgba(255, 255, 255, 0.7);
  --vc-nav-border-radius: 100%;
}

img {
  border-radius: 8px;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.gallery-image {
  border-radius: 16px;
}

#thumbnails {
  margin-top: 10px;
}

.thumbnail {
  height: 100%;
  width: 100%;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.3s ease-in-out;
}

.thumbnail.is-active,
.thumbnail:hover {
  opacity: 1;
}
</style>
