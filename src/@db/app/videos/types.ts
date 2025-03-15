import type { ArticleDetail } from '@/@db/app/articles/types'
import type { ChannelDetail } from '@/@db/app/channels/types'
import type { VideoStatus } from '@/@db/app/videos/enums'

export interface VideoViewModel {
  id: string
  channel_id: string
  article_ids: string[]
  title: string
  description: string
  status: VideoStatus
  result_video_url: string
  audio_file: string
  video_segments: string[]
  created_at?: string | null
  updated_at?: string | null
}

export interface VideoDetail {
  id: string
  title?: string | null
  description?: string | null
  status: VideoStatus
  result_video_url?: string | null
  audio_file?: string | null
  video_segments?: string[] | null
  related_urls?: string[] | null
  created_at?: string | null
  updated_at?: string | null
  channel: ChannelDetail
  articles: ArticleDetail[]
}

export interface NewVideoForm {
  status: VideoStatus
  articles: Array<{
    title: string
    content: string
    original_url: string
    images: File[]
  }>
}

export type VideoList = VideoViewModel[]
