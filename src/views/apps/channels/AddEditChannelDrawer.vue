<script setup lang="ts">
import { PerfectScrollbar } from 'vue3-perfect-scrollbar'
import { toast } from 'vue3-toastify'
import { VForm } from 'vuetify/components/VForm'

import type { ChannelViewModel, CreateChannel } from '@/@db/app/channels/types'

interface Props {
  isDrawerOpen: boolean
  itemData?: ChannelViewModel | null
}

interface Emit {
  (e: 'update:isDrawerOpen', value: boolean): void
  (e: 'success'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emit>()

const refVForm = ref<VForm>()
const isEdit = ref(false)

const form = ref<CreateChannel>({
  name: '',
  category: '',
})

const resetState = () => {
  form.value = {
    name: '',
    category: '',
  }
  isEdit.value = false
  refVForm.value?.reset()
}

const handleDrawerModelValueUpdate = (val: boolean) => {
  if (!val)
    resetState()

  emit('update:isDrawerOpen', val)
}

const onSubmit = () => {
  refVForm.value?.validate().then(async ({ valid }) => {
    if (!valid)
      return

    let endpoint = '/news/channels'
    endpoint = isEdit.value ? `${endpoint}/${props.itemData?.id}` : endpoint

    const { response } = await useApi(createUrl(endpoint))[isEdit.value ? 'put' : 'post'](form.value)

    if (response.value?.ok) {
      toast.success(`Channel ${isEdit.value ? 'updated' : 'added'} successfully`)
      handleDrawerModelValueUpdate(false)
      emit('success')
    }
  })
}

watch(() => props.itemData, val => {
  if (isNullOrUndefined(val))
    return

  isEdit.value = true
  form.value = {
    name: val.name,
    category: val.category,
  }
})
</script>

<template>
  <VNavigationDrawer
    temporary
    :width="600"
    location="end"
    class="scrollable-content"
    :model-value="props.isDrawerOpen"
    @update:model-value="handleDrawerModelValueUpdate"
  >
    <AppDrawerHeaderSection
      :title="`${isEdit ? 'Edit' : 'Add New'} Channel`"
      @cancel="handleDrawerModelValueUpdate(false)"
    />

    <VDivider />

    <PerfectScrollbar :options="{ wheelPropagation: false }">
      <VCard flat>
        <VCardText>
          <VForm
            ref="refVForm"
            @submit.prevent="onSubmit"
          >
            <VRow>
              <VCol cols="12">
                <VTextField
                  v-model="form.name"
                  label="Channel Name"
                  :rules="[requiredValidator]"
                  placeholder="Enter channel name"
                />
              </VCol>

              <VCol cols="12">
                <VTextField
                  v-model="form.category"
                  label="Channel Category"
                  :rules="[requiredValidator]"
                  placeholder="Enter channel category"
                />
              </VCol>

              <VCol cols="12">
                <VBtn
                  type="submit"
                  class="me-4"
                >
                  {{ isEdit ? 'Update' : 'Add' }}
                </VBtn>

                <VBtn
                  type="reset"
                  variant="outlined"
                  color="error"
                  @click="handleDrawerModelValueUpdate(false)"
                >
                  Cancel
                </VBtn>
              </VCol>
            </VRow>
          </VForm>
        </VCardText>
      </VCard>
    </PerfectScrollbar>
  </VNavigationDrawer>
</template>
