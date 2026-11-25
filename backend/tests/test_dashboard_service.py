from __future__ import annotations

from uuid import uuid4

import pytest

from app.application.services.article_service import ArticleService
from app.application.services.dashboard_service import DashboardService
from app.domain.entities.category import Category
from tests.conftest import FakeArticleRepository, FakeCategoryRepository


@pytest.mark.asyncio
async def test_dashboard_stats_counts_by_status():
    articles = FakeArticleRepository()
    categories = FakeCategoryRepository()
    category = Category(name="Technology", slug="technology")
    await categories.create(category)
    article_service = ArticleService(articles, categories)
    dashboard = DashboardService(articles)
    author = uuid4()

    draft = await article_service.create_article("Draft", "a", "b", category.id, author)
    live = await article_service.create_article("Live", "a", "b", category.id, author)
    await article_service.publish_article(live.id)

    stats = await dashboard.get_statistics()

    assert stats["total_articles"] == 2
    assert stats["published"] == 1
    assert stats["drafts"] == 1
    assert stats["archived"] == 0
    assert any(item["slug"] == draft.slug for item in stats["top_viewed"])
