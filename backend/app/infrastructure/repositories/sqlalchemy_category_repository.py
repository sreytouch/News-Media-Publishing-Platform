from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.category import Category
from app.infrastructure.db.models import CategoryModel


class SqlAlchemyCategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, category: Category) -> Category:
        model = CategoryModel(id=category.id, name=category.name, slug=category.slug)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, category_id: UUID) -> Category | None:
        model = await self._session.get(CategoryModel, category_id)
        return self._to_domain(model) if model else None

    async def get_by_slug(self, slug: str) -> Category | None:
        result = await self._session.execute(
            select(CategoryModel).where(CategoryModel.slug == slug)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Category]:
        result = await self._session.execute(select(CategoryModel).order_by(CategoryModel.name))
        return [self._to_domain(model) for model in result.scalars().all()]

    async def update(self, category: Category) -> Category:
        model = await self._session.get(CategoryModel, category.id)
        if model is None:
            raise ValueError("Category not found for update.")
        model.name = category.name
        model.slug = category.slug
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def delete(self, category_id: UUID) -> None:
        model = await self._session.get(CategoryModel, category_id)
        if model is None:
            return
        await self._session.delete(model)
        await self._session.commit()

    @staticmethod
    def _to_domain(model: CategoryModel) -> Category:
        return Category(id=model.id, name=model.name, slug=model.slug)
