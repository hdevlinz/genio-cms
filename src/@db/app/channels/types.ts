import type { WorkspaceDetail } from '@/@db/app/workspaces/types'

export interface ChannelViewModel {
  id: string
  workspace_id: string
  name: string
  category: string
  created_at?: string | null
  updated_at?: string | null
}

export interface ChannelDetail {
  id: string
  name: string
  category: string
  created_at?: string | null
  updated_at?: string | null
  workspace: WorkspaceDetail
}

export interface CreateChannel {
  name: string
  category: string
}

export type ChannelList = ChannelViewModel[]
