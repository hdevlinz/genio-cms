import type { ArticleDetail } from '@/@db/apps/articles/types'
import type { VideoStatus } from '@/@db/apps/videos/enums'

export interface VideoViewModel {
  id: string
  title: string
  name?: string | null
  description?: string | null
  transcript?: string | null
  video_url?: string | null
  audio_url?: string | null
  date?: string | null
  duration?: string | null
  status: VideoStatus
  language?: string | null
  topic?: string | null
  keywords?: string[] | null
  context?: Record<string, any> | null
  created_at: string
  updated_at: string
}

export interface VideoDetail {
  id: string
  title: string
  name?: string | null
  description?: string | null
  transcript?: string | null
  video_url?: string | null
  audio_url?: string | null
  date?: string | null
  duration?: string | null
  status: VideoStatus
  language?: string | null
  topic?: string | null
  keywords?: string[] | null
  created_at: string
  updated_at: string
  articles?: ArticleDetail[] | null
}

export interface CreateVideo {
  article_ids?: string[] | null
  title: string
  name?: string | null
  description?: string | null
  transcript?: string | null
  video_url?: string | null
  audio_url?: string | null
  date?: string | null
  duration?: number | null
  status: VideoStatus
  language?: string | null
  topic?: string | null
  context?: Record<string, any> | null
}

export interface UpdateVideo {
  title?: string | null
  name?: string | null
  description?: string | null
  transcript?: string | null
  video_url?: string | null
  audio_url?: string | null
  date?: string | null
  duration?: number | null
  status?: VideoStatus | null
  language?: string | null
  topic?: string | null
  keywords?: string[] | null
  context?: Record<string, any> | null
}

export interface CreateVideoForm {
  article_ids: string[]
  background_video_ids?: string[] | null
  name?: string | null
  status: VideoStatus
  language?: string | null
  topic?: string | null
  context?: Record<string, any> | null
}

export type VideoList = VideoViewModel[]
