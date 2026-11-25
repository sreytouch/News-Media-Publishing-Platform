export type Role = "admin" | "editor" | "writer";

export type ArticleStatus = "draft" | "published" | "archived";

export interface AuthUser {
  id: string;
  email: string;
  fullName: string;
  role: Role;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
}

export interface Article {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  body: string;
  cover_image_url: string | null;
  status: ArticleStatus;
  category_id: string;
  author_id: string;
  tags: string[];
  published_at: string | null;
  view_count: number;
  created_at: string;
  updated_at: string;
}

export interface DashboardStats {
  total_articles: number;
  published: number;
  drafts: number;
  archived: number;
  by_category: Array<{ category: string; count: number }>;
  top_viewed: Array<{ title: string; slug: string; view_count: number }>;
}

export interface PublicArticleSummary {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  cover_image_url: string | null;
  tags: string[];
  published_at: string | null;
  view_count: number;
  category_name: string | null;
  category_slug: string | null;
  author_name: string | null;
}

export interface PublicArticleDetail extends PublicArticleSummary {
  body: string;
}

export interface PublicArticleList {
  items: PublicArticleSummary[];
  total: number;
  page: number;
  page_size: number;
}
