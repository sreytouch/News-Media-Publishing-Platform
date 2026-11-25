from __future__ import annotations

from uuid import uuid4

import pytest

from app.application.services.article_service import ArticleService
from app.core.exceptions import ValidationError
from app.domain.entities.common import ArticleStatus
from tests.conftest import FakeArticleRepository, FakeCategoryRepository


async def build_service():
    articles = FakeArticleRepository()
    categories = FakeCategoryRepository()
    service = ArticleService(articles, categories)
    from app.domain.entities.category import Category

    category = Category(name="Technology", slug="technology")
    await categories.create(category)
    return service, articles, category


@pytest.mark.asyncio
async def test_create_article_generates_slug_and_draft_status():
    service, _, category = await build_service()

    article = await service.create_article(
        title="Hello World",
        excerpt="x",
        body="y",
        category_id=category.id,
        author_id=uuid4(),
    )

    assert article.slug == "hello-world"
    assert article.status == ArticleStatus.DRAFT
    assert article.published_at is None


@pytest.mark.asyncio
async def test_create_article_enforces_unique_slug():
    service, _, category = await build_service()
    author = uuid4()

    first = await service.create_article("Same Title", "a", "b", category.id, author)
    second = await service.create_article("Same Title", "a", "b", category.id, author)
    third = await service.create_article("Same Title", "a", "b", category.id, author)

    assert first.slug == "same-title"
    assert second.slug == "same-title-2"
    assert third.slug == "same-title-3"


@pytest.mark.asyncio
async def test_create_article_requires_existing_category():
    service, _, _ = await build_service()

    with pytest.raises(ValidationError):
        await service.create_article("Orphan", "a", "b", uuid4(), uuid4())


@pytest.mark.asyncio
async def test_publish_then_unpublish_workflow():
    service, _, category = await build_service()
    article = await service.create_article("Workflow", "a", "b", category.id, uuid4())

    published = await service.publish_article(article.id)
    assert published.status == ArticleStatus.PUBLISHED
    assert published.published_at is not None

    unpublished = await service.unpublish_article(article.id)
    assert unpublished.status == ArticleStatus.DRAFT
    assert unpublished.published_at is None


@pytest.mark.asyncio
async def test_list_articles_filters_by_status():
    service, _, category = await build_service()
    author = uuid4()
    draft = await service.create_article("Draft One", "a", "b", category.id, author)
    live = await service.create_article("Live One", "a", "b", category.id, author)
    await service.publish_article(live.id)

    drafts = await service.list_articles(status="draft")
    published = await service.list_articles(status="published")

    assert [a.id for a in drafts] == [draft.id]
    assert [a.id for a in published] == [live.id]
