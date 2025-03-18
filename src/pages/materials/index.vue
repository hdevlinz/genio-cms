<script setup lang="ts">
import BackgroundVideosTab from '@/views/apps/materials/BackgroundVideosTab.vue'

definePage({
  meta: {
    public: true,

    // subject: 'news.articles',
    // action: 'read',
  },
})

const currentTab = ref('background-videos-tab')
</script>

<template>
  <section>
    <VCard>
      <VTabs
        v-model="currentTab"
        grow
        stacked
      >
        <VTab value="background-videos-tab">
          Background Videos
        </VTab>

        <VTab value="other-tab">
          Other Tab
        </VTab>
      </VTabs>

      <VWindow v-model="currentTab">
        <VWindowItem value="background-videos-tab">
          <BackgroundVideosTab />
        </VWindowItem>
      </VWindow>
    </VCard>
  </section>
</template>

<style lang="scss" scoped>
// Empty Style
</style>
