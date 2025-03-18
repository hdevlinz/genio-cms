export interface Material {
  id: string
  name: string
  size?: number | null
  path: string
  ext?: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface CreateMaterial {
  name: string
  size?: number | null
  path: string
  ext?: string | null
}

export interface UpdateMaterial {
  name?: string | null
  is_active?: boolean | null
}
