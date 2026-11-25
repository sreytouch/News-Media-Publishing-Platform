from __future__ import annotations

from uuid import UUID

from app.core.exceptions import EntityNotFoundError, ValidationError
from app.core.slugs import slugify
from app.domain.entities.category import Category
from app.domain.repositories.protocols import CategoryRepository


class CategoryService:
    def __init__(self, category_repository: CategoryRepository) -> None:
        self._categories = category_repository

    async def list_categories(self) -> list[Category]:
        return await self._categories.list_all()

    async def create_category(self, name: str) -> Category:
        slug = slugify(name)
        if await self._categories.get_by_slug(slug) is not None:
            raise ValidationError("A category with this name already exists.")
        return await self._categories.create(Category(name=name, slug=slug))

    async def update_category(self, category_id: UUID, name: str) -> Category:
        category = await self._categories.get_by_id(category_id)
        if category is None:
            raise EntityNotFoundError("Category not found.")
        new_slug = slugify(name)
        conflict = await self._categories.get_by_slug(new_slug)
        if conflict is not None and conflict.id != category_id:
            raise ValidationError("A category with this name already exists.")
        category.name = name
        category.slug = new_slug
        return await self._categories.update(category)

    async def delete_category(self, category_id: UUID) -> None:
        category = await self._categories.get_by_id(category_id)
        if category is None:
            raise EntityNotFoundError("Category not found.")
        await self._categories.delete(category_id)
