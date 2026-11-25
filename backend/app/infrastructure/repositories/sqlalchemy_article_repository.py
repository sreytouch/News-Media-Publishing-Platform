from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.article import Article
from app.domain.entities.common import ArticleStatus
from app.infrastructure.db.models import ArticleModel, CategoryModel


class SqlAlchemyArticleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, article: Article) -> Article:
        model = self._to_model(article)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, article_id: UUID) -> Article | None:
        model = await self._session.get(ArticleModel, article_id)
        return self._to_domain(model) if model else None

    async def get_by_slug(self, slug: str) -> Article | None:
        result = await self._session.execute(
            select(ArticleModel).where(ArticleModel.slug == slug)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def slug_exists(self, slug: str) -> bool:
        result = await self._session.execute(
            select(ArticleModel.id).where(ArticleModel.slug == slug)
        )
        return result.first() is not None

    async def update(self, article: Article) -> Article:
        model = await self._session.get(ArticleModel, article.id)
        if model is None:
            raise ValueError("Article not found for update.")
        model.title = article.title
        model.slug = article.slug
        model.excerpt = article.excerpt
        model.body = article.body
        model.cover_image_url = article.cover_image_url
        model.status = article.status
        model.category_id = article.category_id
        model.tags = article.tags
        model.published_at = article.published_at
        model.view_count = article.view_count
        model.updated_at = article.updated_at
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def delete(self, article_id: UUID) -> None:
        model = await self._session.get(ArticleModel, article_id)
        if model is None:
            return
        await self._session.delete(model)
        await self._session.commit()

    async def list_editorial(
        self,
        status: str | None = None,
        category_id: UUID | None = None,
        search: str | None = None,
    ) -> list[Article]:
        query = select(ArticleModel).order_by(ArticleModel.updated_at.desc())
        if status:
            query = query.where(ArticleModel.status == ArticleStatus(status))
        if category_id:
            query = query.where(ArticleModel.category_id == category_id)
        if search:
            pattern = f"%{search.lower()}%"
            query = query.where(
                or_(
                    func.lower(ArticleModel.title).like(pattern),
                    func.lower(ArticleModel.excerpt).like(pattern),
                )
            )
        result = await self._session.execute(query)
        return [self._to_domain(model) for model in result.scalars().all()]

    async def list_public(
        self,
        category_id: UUID | None = None,
        tag: str | None = None,
        search: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Article], int]:
        query = select(ArticleModel).where(ArticleModel.status == ArticleStatus.PUBLISHED)
        if category_id:
            query = query.where(ArticleModel.category_id == category_id)
        if search:
            pattern = f"%{search.lower()}%"
            query = query.where(
                or_(
                    func.lower(ArticleModel.title).like(pattern),
                    func.lower(ArticleModel.excerpt).like(pattern),
                )
            )
        query = query.order_by(ArticleModel.published_at.desc())
        result = await self._session.execute(query)
        articles = [self._to_domain(model) for model in result.scalars().all()]
        if tag:
            articles = [article for article in articles if tag in article.tags]
        total = len(articles)
        return articles[offset : offset + limit], total

    async def increment_view_count(self, article_id: UUID) -> None:
        model = await self._session.get(ArticleModel, article_id)
        if model is None:
            return
        model.view_count += 1
        await self._session.commit()

    async def statistics(self) -> dict:
        result = await self._session.execute(select(ArticleModel))
        articles = list(result.scalars().all())

        categories = await self._session.execute(select(CategoryModel))
        category_names = {category.id: category.name for category in categories.scalars().all()}

        by_status = {status.value: 0 for status in ArticleStatus}
        by_category: dict[str, int] = {}
        for article in articles:
            by_status[article.status.value] = by_status.get(article.status.value, 0) + 1
            name = category_names.get(article.category_id, "Uncategorized")
            by_category[name] = by_category.get(name, 0) + 1

        top = sorted(articles, key=lambda item: item.view_count, reverse=True)[:5]
        return {
            "total_articles": len(articles),
            "published": by_status.get(ArticleStatus.PUBLISHED.value, 0),
            "drafts": by_status.get(ArticleStatus.DRAFT.value, 0),
            "archived": by_status.get(ArticleStatus.ARCHIVED.value, 0),
            "by_category": [
                {"category": name, "count": count} for name, count in by_category.items()
            ],
            "top_viewed": [
                {"title": article.title, "slug": article.slug, "view_count": article.view_count}
                for article in top
            ],
        }

    @staticmethod
    def _to_model(article: Article) -> ArticleModel:
        return ArticleModel(
            id=article.id,
            title=article.title,
            slug=article.slug,
            excerpt=article.excerpt,
            body=article.body,
            cover_image_url=article.cover_image_url,
            status=article.status,
            category_id=article.category_id,
            author_id=article.author_id,
            tags=article.tags,
            published_at=article.published_at,
            view_count=article.view_count,
            created_at=article.created_at,
            updated_at=article.updated_at,
        )

    @staticmethod
    def _to_domain(model: ArticleModel) -> Article:
        return Article(
            id=model.id,
            title=model.title,
            slug=model.slug,
            excerpt=model.excerpt,
            body=model.body,
            cover_image_url=model.cover_image_url,
            status=model.status,
            category_id=model.category_id,
            author_id=model.author_id,
            tags=list(model.tags or []),
            published_at=model.published_at,
            view_count=model.view_count,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
