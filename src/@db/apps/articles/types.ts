export interface ArticleViewModel {
  id: string
  content?: string | null
  original_url: string
  published_at?: string | null
  image_urls?: string[] | null
  created_at: string
  updated_at: string
}

export interface ArticleDetail {
  id: string
  content?: string | null
  original_url: string
  published_at?: string | null
  image_urls?: string[] | null
  created_at: string
  updated_at: string
}

export interface CreateArticle {
  content?: string | null
  original_url: string
  published_at?: string | null
  image_urls?: string[] | null
}

export interface UpdateArticle {
  content?: string | null
  original_url?: string | null
  published_at?: string | null
  image_urls?: string[] | null
}

export interface CreateArticleForm {
  original_url: string
  published_at?: Date | null
  images: (string | File)[]
}

export type ArticleList = ArticleViewModel[]
