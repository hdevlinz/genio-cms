import dashboard from './dashboard'

import news from '@/navigation/vertical/news'
import type { VerticalNavItems } from '@layouts/types'

export default [
  ...dashboard,
  ...news,
] as VerticalNavItems
