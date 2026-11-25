from __future__ import annotations

from app.core.exceptions import EntityNotFoundError
from app.domain.entities.article import Article
from app.domain.entities.category import Category
from app.domain.entities.common import ArticleStatus
from app.domain.repositories.protocols import (
    ArticleRepository,
    CategoryRepository,
    UserRepository,
)


class PublicService:
    def __init__(
        self,
        article_repository: ArticleRepository,
        category_repository: CategoryRepository,
        user_repository: UserRepository,
    ) -> None:
        self._articles = article_repository
        self._categories = category_repository
        self._users = user_repository

    async def list_categories(self) -> list[Category]:
        return await self._categories.list_all()

    async def list_articles(
        self,
        category_slug: str | None = None,
        tag: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> dict:
        category_id = None
        if category_slug:
            category = await self._categories.get_by_slug(category_slug)
            if category is None:
                return {"items": [], "total": 0, "page": page, "page_size": page_size}
            category_id = category.id

        offset = max(page - 1, 0) * page_size
        articles, total = await self._articles.list_public(
            category_id=category_id,
            tag=tag,
            search=search,
            limit=page_size,
            offset=offset,
        )
        items = [await self._to_summary(article) for article in articles]
        return {"items": items, "total": total, "page": page, "page_size": page_size}

    async def get_article(self, slug: str) -> dict:
        article = await self._articles.get_by_slug(slug)
        if article is None or article.status != ArticleStatus.PUBLISHED:
            raise EntityNotFoundError("Article not found.")
        await self._articles.increment_view_count(article.id)
        article.view_count += 1
        return await self._to_detail(article)

    async def _meta(self, article: Article) -> dict:
        category = await self._categories.get_by_id(article.category_id)
        author = await self._users.get_by_id(article.author_id)
        return {
            "category_name": category.name if category else None,
            "category_slug": category.slug if category else None,
            "author_name": author.full_name if author else None,
        }

    async def _to_summary(self, article: Article) -> dict:
        meta = await self._meta(article)
        return {
            "id": str(article.id),
            "title": article.title,
            "slug": article.slug,
            "excerpt": article.excerpt,
            "cover_image_url": article.cover_image_url,
            "tags": article.tags,
            "published_at": article.published_at,
            "view_count": article.view_count,
            **meta,
        }

    async def _to_detail(self, article: Article) -> dict:
        summary = await self._to_summary(article)
        summary["body"] = article.body
        return summary
