import type { MongoAbility, MongoQuery } from '@casl/ability'
import { debounce } from 'lodash'

import type { Actions, Subjects } from '@/plugins/casl/ability'

export const truncateString = (data: string, maxLength: number) => {
  return data.length > maxLength ? `${data.substring(0, maxLength)}...` : data
}

export const watchWithDebounce = (refs: Ref<any>[], callback: () => void, delay = 300, immediate: boolean = true) => {
  watch(refs, debounce(callback, delay), { immediate })
}

export const paginationMeta = <T extends { page: number; itemsPerPage: number }>(options: T, total: number) => {
  const start = (options.page - 1) * options.itemsPerPage + 1
  const end = Math.min(options.page * options.itemsPerPage, total)

  return `${total === 0 ? 0 : start} - ${end} of ${total}`
}

export const removeEmptyValues = (obj: any): any => {
  if (obj === null || obj === undefined || obj === '')
    return undefined

  if (typeof obj !== 'object')
    return obj

  if (Array.isArray(obj))
    return obj.map(removeEmptyValues).filter(v => v !== undefined)

  const newObj: { [key: string]: any } = {}
  for (const key in obj) {
    if (Object.hasOwnProperty.call(obj, key)) {
      const value = removeEmptyValues(obj[key])
      if (value !== undefined)
        newObj[key] = value
    }
  }

  return Object.keys(newObj).length > 0 ? newObj : undefined
}

export const setAuthCookies = (ability: MongoAbility<[Actions, Subjects], MongoQuery>, res: any) => {
  ability.update(res.ability_rules)

  useCookie('userData').value = JSON.stringify(res.user_data)
  useCookie('userAbilityRules').value = res.ability_rules
  useCookie('accessToken').value = res.access_token
  useCookie('refreshToken').value = res.refresh_token
  useCookie('accessTokenExpiresAt').value = (res.access_token_expired_at * 1000).toString() // convert to milliseconds
}

export const clearAuthCookies = (ability: MongoAbility<[Actions, Subjects], MongoQuery>) => {
  ability.update([])

  useCookie('userData').value = null
  useCookie('userAbilityRules').value = null
  useCookie('accessToken').value = null
  useCookie('refreshToken').value = null
  useCookie('accessTokenExpiresAt').value = null
}
