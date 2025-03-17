<script setup lang="ts">
import '@jaxtheprime/vue3-dropzone/dist/style.css'
import '@vuepic/vue-datepicker/dist/main.css'
import 'prismjs'
import 'prismjs/themes/prism-tomorrow.css'
import 'vanilla-jsoneditor/themes/jse-theme-dark.css'
import 'vue-json-pretty/lib/styles.css'
import 'vue3-carousel/carousel.css'
import 'vue3-toastify/dist/index.css'

import { useTheme } from 'vuetify'

import initCore from '@core/initCore'
import { initConfigStore, useConfigStore } from '@core/stores/config'

const { global } = useTheme()

// ℹ️ Sync current theme with initial loader theme
initCore()
initConfigStore()

const configStore = useConfigStore()
</script>

<template>
  <VLocaleProvider :rtl="configStore.isAppRTL">
    <!-- ℹ️ This is required to set the background color of active nav link based on currently active global theme's primary -->
    <VApp :style="`--v-global-theme-primary: ${hexToRgb(global.current.value.colors.primary)}`">
      <RouterView />

      <ScrollToTop />
    </VApp>
  </VLocaleProvider>
</template>
