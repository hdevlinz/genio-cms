import { useAbility } from '@casl/vue'
import type { RouteLocationNormalized } from 'vue-router'

import type { NavGroup, NavLink } from '@layouts/types'

/**
 * Returns ability result if ACL is configured or else just return true
 * We should allow passing string | undefined to can because for admin ability we omit defining action & subject
 *
 * Useful if you don't know if ACL is configured or not
 * Used in @core files to handle absence of ACL without errors
 *
 * @param {string} action CASL Actions // https://casl.js.org/v4/en/guide/intro#basics
 * @param {string} subject CASL Subject // https://casl.js.org/v4/en/guide/intro#basics
 */
export const can = (action: string | undefined, subject: string | undefined) => {
  if (action === 'public' && subject === 'public')
    return true

  const vm = getCurrentInstance()

  if (!vm)
    return false

  const localCan = vm.proxy && '$can' in vm.proxy

  let subjects = [subject]
  if (subject && subject.includes('.')) {
    const parts = subject.split('.')

    subjects = parts.map((_, index) => parts.slice(0, index + 1).join('.'))
  }

  // @ts-expect-error We will get TS error in below line because we aren't using $can in component instance
  return subjects.some(sub => localCan ? vm.proxy?.$can(action, sub) : true)
}

/**
 * Check if user can view item based on it's ability
 * Based on item's action and subject & Hide group if all of it's children are hidden
 * @param {object} item navigation object item
 */
export const canViewNavMenuGroup = (item: NavGroup) => {
  if (can('manage', 'all'))
    return true

  const navigationLinks: NavLink[] = []

  const collectAllChildren = (items: (NavGroup | NavLink)[]) => {
    items.forEach(i => {
      if ('children' in i)
        collectAllChildren(i.children)
      else
        navigationLinks.push(i)
    })
  }

  collectAllChildren(item.children)

  const hasAnyVisibleChild = navigationLinks.some(i => can(i.action, i.subject))

  // If subject and action is defined in item => Return based on children visibility (Hide group if no child is visible)
  // Else check for ability using provided subject and action along with checking if has any visible child
  if (!(item.action && item.subject))
    return hasAnyVisibleChild

  return can(item.action, item.subject) && hasAnyVisibleChild
}

export const canNavigate = (to: RouteLocationNormalized) => {
  if (can('manage', 'all'))
    return true

  const ability = useAbility()

  return to.matched.some(route => {
    let subjects = [route.meta.subject]
    if (route.meta.subject && route.meta.subject.includes('.')) {
      const parts = route.meta.subject.split('.')

      subjects = parts.map((_, index) => parts.slice(0, index + 1).join('.'))
    }

    // @ts-expect-error We should allow passing string | undefined to can because for admin ability we omit defining action & subject
    return subjects.some(sub => ability.can(route.meta.action, sub))
  })
}
