import {
  Article,
  AuthUser,
  Category,
  DashboardStats,
  PublicArticleDetail,
  PublicArticleList,
} from "../types/models";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

type HttpMethod = "GET" | "POST" | "PATCH" | "DELETE";

async function request<T>(path: string, method: HttpMethod, token?: string, body?: unknown): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: "Request failed." }));
    throw new Error(payload.detail ?? "Request failed.");
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

interface RawAuthUser {
  id: string;
  email: string;
  full_name: string;
  role: AuthUser["role"];
}

function toAuthUser(raw: RawAuthUser): AuthUser {
  return { id: raw.id, email: raw.email, fullName: raw.full_name, role: raw.role };
}

export interface ArticlePayload {
  title: string;
  excerpt: string;
  body: string;
  category_id: string;
  tags: string[];
  cover_image_url: string | null;
}

export const api = {
  // ---- Auth ----
  login: (payload: { email: string; password: string }) =>
    request<{ access_token: string; token_type: string }>("/auth/login", "POST", undefined, payload),
  me: async (token: string) => toAuthUser(await request<RawAuthUser>("/auth/me", "GET", token)),

  // ---- Categories (editorial) ----
  getCategories: (token: string) => request<Category[]>("/categories", "GET", token),
  createCategory: (token: string, payload: { name: string }) =>
    request<Category>("/categories", "POST", token, payload),
  updateCategory: (token: string, id: string, payload: { name: string }) =>
    request<Category>(`/categories/${id}`, "PATCH", token, payload),
  deleteCategory: (token: string, id: string) => request<void>(`/categories/${id}`, "DELETE", token),

  // ---- Articles (editorial) ----
  getArticles: (token: string, params: URLSearchParams) =>
    request<Article[]>(`/articles?${params.toString()}`, "GET", token),
  getArticle: (token: string, id: string) => request<Article>(`/articles/${id}`, "GET", token),
  createArticle: (token: string, payload: ArticlePayload) =>
    request<Article>("/articles", "POST", token, payload),
  updateArticle: (token: string, id: string, payload: Partial<ArticlePayload> & { status?: string }) =>
    request<Article>(`/articles/${id}`, "PATCH", token, payload),
  deleteArticle: (token: string, id: string) => request<void>(`/articles/${id}`, "DELETE", token),
  publishArticle: (token: string, id: string) => request<Article>(`/articles/${id}/publish`, "POST", token),
  unpublishArticle: (token: string, id: string) =>
    request<Article>(`/articles/${id}/unpublish`, "POST", token),

  // ---- Dashboard ----
  getDashboard: (token: string) => request<DashboardStats>("/dashboard/stats", "GET", token),

  // ---- Public ----
  getPublicCategories: () => request<Category[]>("/public/categories", "GET"),
  getPublicArticles: (params: URLSearchParams) =>
    request<PublicArticleList>(`/public/articles?${params.toString()}`, "GET"),
  getPublicArticle: (slug: string) =>
    request<PublicArticleDetail>(`/public/articles/${encodeURIComponent(slug)}`, "GET"),
};
