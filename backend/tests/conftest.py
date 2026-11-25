from __future__ import annotations

import copy
from uuid import UUID, uuid4

import pytest

from app.core.security import JwtTokenService, PasswordHasher
from app.domain.entities.article import Article
from app.domain.entities.category import Category
from app.domain.entities.common import ArticleStatus, Role
from app.domain.entities.user import User


class FakeUserRepository:
    def __init__(self) -> None:
        self.users_by_id: dict[UUID, User] = {}
        self.users_by_email: dict[str, User] = {}

    async def create(self, user: User) -> User:
        self.users_by_id[user.id] = user
        self.users_by_email[user.email] = user
        return user

    async def get_by_email(self, email: str) -> User | None:
        return self.users_by_email.get(email)

    async def get_by_id(self, user_id: UUID) -> User | None:
        return self.users_by_id.get(user_id)


class FakeCategoryRepository:
    def __init__(self) -> None:
        self.categories: dict[UUID, Category] = {}

    async def create(self, category: Category) -> Category:
        self.categories[category.id] = category
        return category

    async def get_by_id(self, category_id: UUID) -> Category | None:
        return self.categories.get(category_id)

    async def get_by_slug(self, slug: str) -> Category | None:
        return next((c for c in self.categories.values() if c.slug == slug), None)

    async def list_all(self) -> list[Category]:
        return sorted(self.categories.values(), key=lambda c: c.name)

    async def update(self, category: Category) -> Category:
        self.categories[category.id] = category
        return category

    async def delete(self, category_id: UUID) -> None:
        self.categories.pop(category_id, None)


class FakeArticleRepository:
    def __init__(self) -> None:
        self.articles: dict[UUID, Article] = {}

    async def create(self, article: Article) -> Article:
        self.articles[article.id] = article
        return article

    async def get_by_id(self, article_id: UUID) -> Article | None:
        article = self.articles.get(article_id)
        return copy.deepcopy(article) if article else None

    async def get_by_slug(self, slug: str) -> Article | None:
        article = next((a for a in self.articles.values() if a.slug == slug), None)
        return copy.deepcopy(article) if article else None

    async def slug_exists(self, slug: str) -> bool:
        return any(a.slug == slug for a in self.articles.values())

    async def update(self, article: Article) -> Article:
        self.articles[article.id] = article
        return article

    async def delete(self, article_id: UUID) -> None:
        self.articles.pop(article_id, None)

    async def list_editorial(self, status=None, category_id=None, search=None):
        results = list(self.articles.values())
        if status:
            results = [a for a in results if a.status.value == status]
        if category_id:
            results = [a for a in results if a.category_id == category_id]
        if search:
            lowered = search.lower()
            results = [
                a for a in results if lowered in a.title.lower() or lowered in a.excerpt.lower()
            ]
        return results

    async def list_public(self, category_id=None, tag=None, search=None, limit=20, offset=0):
        results = [a for a in self.articles.values() if a.status == ArticleStatus.PUBLISHED]
        if category_id:
            results = [a for a in results if a.category_id == category_id]
        if tag:
            results = [a for a in results if tag in a.tags]
        if search:
            lowered = search.lower()
            results = [
                a for a in results if lowered in a.title.lower() or lowered in a.excerpt.lower()
            ]
        total = len(results)
        return results[offset : offset + limit], total

    async def increment_view_count(self, article_id: UUID) -> None:
        article = self.articles.get(article_id)
        if article is not None:
            article.view_count += 1

    async def statistics(self) -> dict:
        articles = list(self.articles.values())
        by_status = {status.value: 0 for status in ArticleStatus}
        for article in articles:
            by_status[article.status.value] += 1
        return {
            "total_articles": len(articles),
            "published": by_status[ArticleStatus.PUBLISHED.value],
            "drafts": by_status[ArticleStatus.DRAFT.value],
            "archived": by_status[ArticleStatus.ARCHIVED.value],
            "by_category": [],
            "top_viewed": [
                {"title": a.title, "slug": a.slug, "view_count": a.view_count}
                for a in sorted(articles, key=lambda a: a.view_count, reverse=True)[:5]
            ],
        }


@pytest.fixture
def password_hasher() -> PasswordHasher:
    return PasswordHasher()


@pytest.fixture
def token_service() -> JwtTokenService:
    return JwtTokenService("test-secret-key-with-plenty-of-characters", "HS256", access_minutes=60)


@pytest.fixture
def sample_user(password_hasher: PasswordHasher) -> User:
    return User(
        email="writer@example.com",
        password_hash=password_hasher.hash_password("Password123!"),
        full_name="Sample Writer",
        role=Role.WRITER,
    )


@pytest.fixture
def sample_category() -> Category:
    return Category(name="Technology", slug="technology")


@pytest.fixture
def sample_article(sample_category: Category, sample_user: User) -> Article:
    return Article(
        title="Breaking News",
        slug="breaking-news",
        excerpt="A short excerpt.",
        body="Full body content.",
        category_id=sample_category.id,
        author_id=sample_user.id,
    )


@pytest.fixture
def new_uuid() -> UUID:
    return uuid4()
