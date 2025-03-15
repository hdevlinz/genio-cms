<script setup lang="ts">
import { PerfectScrollbar } from 'vue3-perfect-scrollbar'

import { clearAuthCookies } from '@/utils/helper'

const router = useRouter()
const ability = useAbility()

// TODO: Get type from backend
const userData = useCookie<Record<string, unknown> | null | undefined>('userData')

const logout = async () => {
  try {
    await $api('/auth/logout', {
      method: 'POST',
      body: {
        refresh_token: useCookie('refreshToken').value,
      },
    })
  }
  catch (error) {
    console.error(error)
  }
  finally {
    // Clear all cookies
    clearAuthCookies(ability)

    // Redirect to login page
    await router.push('/login')
  }
}

const userProfileList = [
  { type: 'divider' },
  {
    type: 'navItem',
    badgeProps: { },
    icon: 'ri-user-line',
    title: 'Profile',
    to: { name: 'users-me' },
  },
  { type: 'divider' },
]
</script>

<template>
  <VBadge
    v-if="userData"
    dot
    bordered
    location="bottom right"
    offset-x="3"
    offset-y="3"
    color="success"
  >
    <VAvatar
      class="cursor-pointer"
      size="38"
    >
      <VIcon icon="ri-user-line" />
      <!-- SECTION Menu -->
      <VMenu
        activator="parent"
        width="230"
        location="bottom end"
        offset="15px"
      >
        <VList>
          <!-- 👉 User Avatar & Name -->
          <VListItem>
            <template #prepend>
              <VListItemAction start>
                <VBadge
                  dot
                  location="bottom right"
                  offset-x="3"
                  offset-y="3"
                  color="success"
                >
                  <VAvatar
                    color="primary"
                    variant="tonal"
                  >
                    <span class="text-5xl font-weight-medium">
                      {{ avatarText(userData?.name as string) }}
                    </span>
                  </VAvatar>
                </VBadge>
              </VListItemAction>
            </template>

            <h6 class="text-sm font-weight-medium">
              {{ userData.name }}
            </h6>
          </VListItem>

          <PerfectScrollbar :options="{ wheelPropagation: false }">
            <template
              v-for="item in userProfileList"
              :key="item.title"
            >
              <VListItem
                v-if="item.type === 'navItem'"
                :to="item.to"
              >
                <template #prepend>
                  <VIcon
                    :icon="item.icon"
                    size="22"
                  />
                </template>

                <VListItemTitle>{{ item.title }}</VListItemTitle>

                <template
                  v-if="item.badgeProps"
                  #append
                >
                  <VBadge
                    inline
                    v-bind="item.badgeProps"
                  />
                </template>
              </VListItem>

              <VDivider
                v-else
                class="my-1"
              />
            </template>

            <VListItem>
              <VBtn
                block
                color="error"
                append-icon="ri-logout-box-r-line"
                @click="logout"
              >
                Logout
              </VBtn>
            </VListItem>
          </PerfectScrollbar>
        </VList>
      </VMenu>
      <!-- !SECTION -->
    </VAvatar>
  </VBadge>
</template>
