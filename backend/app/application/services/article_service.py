from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from app.core.exceptions import EntityNotFoundError, ValidationError
from app.core.slugs import slugify
from app.domain.entities.article import Article
from app.domain.entities.common import ArticleStatus
from app.domain.repositories.protocols import ArticleRepository, CategoryRepository


class ArticleService:
    def __init__(
        self,
        article_repository: ArticleRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self._articles = article_repository
        self._categories = category_repository

    async def _unique_slug(self, title: str) -> str:
        base = slugify(title)
        candidate = base
        counter = 2
        while await self._articles.slug_exists(candidate):
            candidate = f"{base}-{counter}"
            counter += 1
        return candidate

    async def create_article(
        self,
        title: str,
        excerpt: str,
        body: str,
        category_id: UUID,
        author_id: UUID,
        tags: list[str] | None = None,
        cover_image_url: str | None = None,
    ) -> Article:
        if await self._categories.get_by_id(category_id) is None:
            raise ValidationError("Category not found.")
        article = Article(
            title=title,
            slug=await self._unique_slug(title),
            excerpt=excerpt,
            body=body,
            category_id=category_id,
            author_id=author_id,
            tags=tags or [],
            cover_image_url=cover_image_url,
            status=ArticleStatus.DRAFT,
        )
        return await self._articles.create(article)

    async def get_article(self, article_id: UUID) -> Article:
        article = await self._articles.get_by_id(article_id)
        if article is None:
            raise EntityNotFoundError("Article not found.")
        return article

    async def list_articles(
        self,
        status: str | None = None,
        category_id: UUID | None = None,
        search: str | None = None,
    ) -> list[Article]:
        return await self._articles.list_editorial(
            status=status, category_id=category_id, search=search
        )

    async def update_article(
        self,
        article_id: UUID,
        *,
        title: str | None = None,
        excerpt: str | None = None,
        body: str | None = None,
        category_id: UUID | None = None,
        tags: list[str] | None = None,
        cover_image_url: str | None = None,
        status: str | None = None,
    ) -> Article:
        article = await self.get_article(article_id)
        if title is not None:
            article.title = title
        if excerpt is not None:
            article.excerpt = excerpt
        if body is not None:
            article.body = body
        if category_id is not None:
            if await self._categories.get_by_id(category_id) is None:
                raise ValidationError("Category not found.")
            article.category_id = category_id
        if tags is not None:
            article.tags = tags
        if cover_image_url is not None:
            article.cover_image_url = cover_image_url
        if status is not None:
            article.status = ArticleStatus(status)
        article.updated_at = datetime.now(UTC)
        return await self._articles.update(article)

    async def delete_article(self, article_id: UUID) -> None:
        await self.get_article(article_id)
        await self._articles.delete(article_id)

    async def publish_article(self, article_id: UUID) -> Article:
        article = await self.get_article(article_id)
        article.status = ArticleStatus.PUBLISHED
        article.published_at = datetime.now(UTC)
        article.updated_at = datetime.now(UTC)
        return await self._articles.update(article)

    async def unpublish_article(self, article_id: UUID) -> Article:
        article = await self.get_article(article_id)
        article.status = ArticleStatus.DRAFT
        article.published_at = None
        article.updated_at = datetime.now(UTC)
        return await self._articles.update(article)
