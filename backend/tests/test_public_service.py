from __future__ import annotations

from uuid import uuid4

import pytest

from app.application.services.article_service import ArticleService
from app.application.services.public_service import PublicService
from app.core.exceptions import EntityNotFoundError
from app.domain.entities.category import Category
from app.domain.entities.user import User
from tests.conftest import FakeArticleRepository, FakeCategoryRepository, FakeUserRepository


async def build():
    articles = FakeArticleRepository()
    categories = FakeCategoryRepository()
    users = FakeUserRepository()

    author = User(
        email="a@example.com",
        password_hash="x",
        full_name="Author Name",
        role="writer",  # type: ignore[arg-type]
    )
    await users.create(author)
    category = Category(name="Technology", slug="technology")
    await categories.create(category)

    article_service = ArticleService(articles, categories)
    public_service = PublicService(articles, categories, users)
    return article_service, public_service, category, author


@pytest.mark.asyncio
async def test_public_feed_returns_only_published():
    article_service, public_service, category, author = await build()
    draft = await article_service.create_article("Draft", "a", "b", category.id, author.id)
    live = await article_service.create_article("Live", "a", "b", category.id, author.id)
    await article_service.publish_article(live.id)

    result = await public_service.list_articles()

    slugs = {item["slug"] for item in result["items"]}
    assert live.slug in slugs
    assert draft.slug not in slugs
    assert result["total"] == 1


@pytest.mark.asyncio
async def test_public_article_detail_increments_view_count():
    article_service, public_service, category, author = await build()
    live = await article_service.create_article("Viewed", "a", "b", category.id, author.id)
    await article_service.publish_article(live.id)

    first = await public_service.get_article(live.slug)
    second = await public_service.get_article(live.slug)

    assert first["view_count"] == 1
    assert second["view_count"] == 2
    assert first["author_name"] == "Author Name"
    assert first["category_slug"] == "technology"


@pytest.mark.asyncio
async def test_public_article_detail_hidden_for_draft():
    article_service, public_service, category, author = await build()
    draft = await article_service.create_article("Hidden", "a", "b", category.id, author.id)

    with pytest.raises(EntityNotFoundError):
        await public_service.get_article(draft.slug)


@pytest.mark.asyncio
async def test_public_feed_filters_by_category_slug():
    article_service, public_service, category, author = await build()
    live = await article_service.create_article("Tech Story", "a", "b", category.id, author.id)
    await article_service.publish_article(live.id)

    matching = await public_service.list_articles(category_slug="technology")
    missing = await public_service.list_articles(category_slug="does-not-exist")

    assert matching["total"] == 1
    assert missing["total"] == 0


@pytest.mark.asyncio
async def test_missing_article_raises():
    _, public_service, _, _ = await build()

    with pytest.raises(EntityNotFoundError):
        await public_service.get_article(str(uuid4()))
