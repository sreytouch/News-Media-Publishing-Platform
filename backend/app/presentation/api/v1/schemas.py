from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.entities.article import Article
from app.domain.entities.category import Category
from app.domain.entities.common import ArticleStatus


# ---- Categories ----
class CreateCategoryRequest(BaseModel):
    name: str


class UpdateCategoryRequest(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: str
    name: str
    slug: str


# ---- Articles (editorial) ----
class CreateArticleRequest(BaseModel):
    title: str
    excerpt: str = ""
    body: str = ""
    category_id: str
    tags: list[str] = Field(default_factory=list)
    cover_image_url: str | None = None


class UpdateArticleRequest(BaseModel):
    title: str | None = None
    excerpt: str | None = None
    body: str | None = None
    category_id: str | None = None
    tags: list[str] | None = None
    cover_image_url: str | None = None
    status: ArticleStatus | None = None


class ArticleResponse(BaseModel):
    id: str
    title: str
    slug: str
    excerpt: str
    body: str
    cover_image_url: str | None
    status: str
    category_id: str
    author_id: str
    tags: list[str]
    published_at: datetime | None
    view_count: int
    created_at: datetime
    updated_at: datetime


# ---- Dashboard ----
class CategoryCount(BaseModel):
    category: str
    count: int


class TopViewed(BaseModel):
    title: str
    slug: str
    view_count: int


class DashboardStatsResponse(BaseModel):
    total_articles: int
    published: int
    drafts: int
    archived: int
    by_category: list[CategoryCount]
    top_viewed: list[TopViewed]


# ---- Public ----
class PublicArticleSummary(BaseModel):
    id: str
    title: str
    slug: str
    excerpt: str
    cover_image_url: str | None
    tags: list[str]
    published_at: datetime | None
    view_count: int
    category_name: str | None
    category_slug: str | None
    author_name: str | None


class PublicArticleDetail(PublicArticleSummary):
    body: str


class PublicArticleList(BaseModel):
    items: list[PublicArticleSummary]
    total: int
    page: int
    page_size: int


def category_to_response(category: Category) -> CategoryResponse:
    return CategoryResponse(id=str(category.id), name=category.name, slug=category.slug)


def article_to_response(article: Article) -> ArticleResponse:
    return ArticleResponse(
        id=str(article.id),
        title=article.title,
        slug=article.slug,
        excerpt=article.excerpt,
        body=article.body,
        cover_image_url=article.cover_image_url,
        status=article.status.value,
        category_id=str(article.category_id),
        author_id=str(article.author_id),
        tags=article.tags,
        published_at=article.published_at,
        view_count=article.view_count,
        created_at=article.created_at,
        updated_at=article.updated_at,
    )
