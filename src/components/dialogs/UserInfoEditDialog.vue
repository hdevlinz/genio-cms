<script setup lang="ts">
interface UserData {
  id: string
  name: string
  email: string
  password: string
  is_superuser: boolean
  is_active: boolean
  onboarding_status: boolean
  profile: {
    display_name: string
    phone_number: string
    bio: string
    date_of_birth: string
    avatar: string | undefined
  }
}

interface Props {
  userData?: UserData
  isDialogVisible: boolean
}

interface Emit {
  (e: 'submit', value: UserData): void
  (e: 'update:isDialogVisible', val: boolean): void
}

const props = withDefaults(defineProps<Props>(), {
  userData: () => ({
    id: '',
    is_active: false,
    is_superuser: false,
    onboarding_status: false,
    name: '',
    email: '',
    password: '',
    profile: {
      bio: '',
      date_of_birth: '',
      display_name: '',
      phone_number: '',
      avatar: undefined,
    },
  }),
})

const emit = defineEmits<Emit>()

const userData = ref<UserData>(structuredClone(toRaw(props.userData)))

watch(() => props, () => {
  userData.value = structuredClone(toRaw(props.userData))
})

const onFormSubmit = async () => {
  emit('update:isDialogVisible', false)
  emit('submit', { ...userData.value, profile: { ...userData.value.profile, avatar: undefined } })
}

const onFormReset = () => {
  userData.value = structuredClone(toRaw(props.userData))

  emit('update:isDialogVisible', false)
}

const dialogVisibleUpdate = (val: boolean) => {
  emit('update:isDialogVisible', val)
}
</script>

<template>
  <VDialog
    :width="$vuetify.display.smAndDown ? 'auto' : 900 "
    :model-value="props.isDialogVisible"
    @update:model-value="dialogVisibleUpdate"
  >
    <VCard class="pa-sm-11 pa-3">
      <!-- 👉 dialog close btn -->
      <DialogCloseBtn
        variant="text"
        size="default"
        @click="onFormReset"
      />

      <VCardText class="pt-5">
        <div class="text-center pb-6">
          <h4 class="text-h4 mb-2">
            Edit User Information
          </h4>
          <div class="text-body-1">
            Updating user details will receive a privacy audit.
          </div>
        </div>

        <!-- 👉 Form -->
        <VForm
          class="mt-4"
          @submit.prevent="onFormSubmit"
        >
          <VRow>
            <!-- 👉 User Name  -->

            <VCol cols="12">
              <VTextField
                v-model="userData.name"
                label="Name"
                placeholder="Admin"
              />
            </VCol>

            <!-- 👉 Email -->
            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="userData.email"
                label="Email"
                placeholder="admin@email.com"
              />
            </VCol>

            <!-- 👉 Password -->
            <VCol
              cols="12"
              md="6"
            >
              <VTextField
                v-model="userData.password"
                label="Password"
                placeholder="Password"
                type="password"
              />
            </VCol>

            <!-- 👉 Status -->
            <VCol
              cols="12"
              md="6"
            >
              <VCheckbox
                v-model="userData.is_active"
                label="Active"
              />
              <VCheckbox
                v-model="userData.onboarding_status"
                label="Onboarding Status"
              />
            </VCol>

            <VDivider class="my-4" />
            <VCol
              v-if="userData.profile"
              cols="6"
            >
              <VTextField
                v-model="userData.profile.display_name"
                label="Display Name"
                placeholder="Display Name"
              />
            </VCol>

            <VCol
              v-if="userData.profile"
              cols="6"
              md="6"
            >
              <VTextField
                v-model="userData.profile.phone_number"
                label="Phone Number"
                placeholder="Phone Number"
              />
            </VCol>

            <VTextarea
              v-if="userData.profile"
              v-model="userData.profile.bio"
              label="Bio"
              placeholder="Bio"
            />

            <!-- 👉 Submit and Cancel -->
            <VCol
              cols="12"
              class="d-flex flex-wrap justify-center gap-4"
            >
              <VBtn type="submit">
                Submit
              </VBtn>

              <VBtn
                color="secondary"
                variant="outlined"
                @click="onFormReset"
              >
                Cancel
              </VBtn>
            </VCol>
          </VRow>
          <VRow />
        </VForm>
      </VCardText>
    </VCard>
  </VDialog>
</template>
