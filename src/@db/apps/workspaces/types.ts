export interface WorkspaceViewModel {
  id: string
  name: string
  created_at?: string | null
  updated_at?: string | null
}

export interface WorkspaceDetail {
  id: string
  name: string
}

export type WorkspaceList = WorkspaceViewModel[]
