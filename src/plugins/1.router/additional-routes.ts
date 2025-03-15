import type { RouteRecordRaw } from 'vue-router/auto'

// 👉 Redirects
export const redirects: RouteRecordRaw[] = [
  // ℹ️ We are redirecting to different pages based on role.
  // NOTE: Role is just for UI purposes. ACL is based on abilities.
  {
    path: '/',
    name: 'index',
    redirect: to => {
      return { name: 'dashboard' }
      // TODO: Get type from backend
      // const userData = useCookie<Record<string, unknown> | null | undefined>('userData')
      // const isSuperuser = userData.value?.is_superuser

      // if (isSuperuser === true)
      //   return { name: 'dashboard' }

      // return { name: 'login', query: to.query }
    },
  },
]

export const routes: RouteRecordRaw[] = [
]
