import type { ChannelDetail } from '@/@db/app/channels/types'

export interface ArticleViewModel {
  id: string
  channel_id: number
  title: string
  content: string
  original_url: string
  related_urls: string[]
  images: string[]
  created_at?: string | null
  updated_at?: string | null
}

export interface ArticleDetail {
  id: string
  title: string
  content: string
  original_url: string
  related_urls: string[]
  images: string[]
  created_at?: string | null
  updated_at?: string | null
  channel: ChannelDetail
}

// export interface CreateArticle {
//   channel_id: string
//   title: string
//   content: string
//   original_url: string
//   images: string[]
// }

export type ArticleList = ArticleViewModel[]
