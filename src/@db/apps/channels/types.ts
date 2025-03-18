export interface ChannelViewModel {
  id: string
  name: string
  category: string
  created_at?: string | null
  updated_at?: string | null
}

export interface ChannelDetail {
  id: string
  name: string
  category: string
}

export interface CreateChannel {
  name: string
  category: string
}

export type ChannelList = ChannelViewModel[]
