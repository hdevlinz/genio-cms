import type { Material } from '@/@db/apps/materials/base'

export interface BackgroundVideoViewModel extends Material {
  duration: number
  height: number
  width: number
}

export interface BackgroundVideoSchema extends Material {
  duration: number
  height: number
  width: number
}

export interface CreateBackgroundVideoSchema extends Material {
  duration: number
  height: number
  width: number
}

export interface UpdateBackgroundVideoSchema extends Material {
}

export type BackgroundVideoList = BackgroundVideoViewModel[]
