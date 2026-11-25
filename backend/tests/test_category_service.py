from __future__ import annotations

import pytest

from app.application.services.category_service import CategoryService
from app.core.exceptions import EntityNotFoundError, ValidationError
from tests.conftest import FakeCategoryRepository


def build_service() -> tuple[CategoryService, FakeCategoryRepository]:
    repo = FakeCategoryRepository()
    return CategoryService(repo), repo


@pytest.mark.asyncio
async def test_create_category_generates_slug():
    service, _ = build_service()

    category = await service.create_category("World News")

    assert category.slug == "world-news"


@pytest.mark.asyncio
async def test_create_category_rejects_duplicate():
    service, _ = build_service()
    await service.create_category("Sports")

    with pytest.raises(ValidationError):
        await service.create_category("Sports")


@pytest.mark.asyncio
async def test_update_category_changes_name_and_slug():
    service, _ = build_service()
    category = await service.create_category("Tech")

    updated = await service.update_category(category.id, "Technology")

    assert updated.name == "Technology"
    assert updated.slug == "technology"


@pytest.mark.asyncio
async def test_delete_category_removes_it():
    service, repo = build_service()
    category = await service.create_category("Weather")

    await service.delete_category(category.id)

    assert await repo.get_by_id(category.id) is None


@pytest.mark.asyncio
async def test_update_missing_category_raises():
    service, _ = build_service()
    from uuid import uuid4

    with pytest.raises(EntityNotFoundError):
        await service.update_category(uuid4(), "Nope")
