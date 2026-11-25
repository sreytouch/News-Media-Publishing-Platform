from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import PasswordHasher
from app.core.slugs import slugify
from app.domain.entities.common import ArticleStatus, Role
from app.infrastructure.db.models import ArticleModel, CategoryModel, UserModel

DEMO_ADMIN_EMAIL = "admin@nmpp.local"
DEMO_ADMIN_PASSWORD = "Password123!"

_CATEGORIES = ["Technology", "Business", "Science", "Culture"]

_ARTICLES = [
    {
        "title": "AI Newsrooms Reshape How the World Reads",
        "excerpt": "Editorial teams are adopting AI copilots to move faster without losing trust.",
        "category": "Technology",
        "status": ArticleStatus.PUBLISHED,
        "tags": ["ai", "media", "newsroom"],
        "cover": "https://picsum.photos/seed/ai-news/1200/600",
        "views": 342,
    },
    {
        "title": "Markets Rally as Central Banks Signal a Pause",
        "excerpt": "Investors cheered a softer tone from policymakers this week.",
        "category": "Business",
        "status": ArticleStatus.PUBLISHED,
        "tags": ["markets", "economy"],
        "cover": "https://picsum.photos/seed/markets/1200/600",
        "views": 198,
    },
    {
        "title": "A New Telescope Peers Into the Early Universe",
        "excerpt": "Astronomers share first images that push the boundary of what we can see.",
        "category": "Science",
        "status": ArticleStatus.PUBLISHED,
        "tags": ["space", "astronomy"],
        "cover": "https://picsum.photos/seed/telescope/1200/600",
        "views": 271,
    },
    {
        "title": "The Quiet Revival of Independent Cinema",
        "excerpt": "Small studios are finding big audiences through streaming and word of mouth.",
        "category": "Culture",
        "status": ArticleStatus.PUBLISHED,
        "tags": ["film", "culture"],
        "cover": "https://picsum.photos/seed/cinema/1200/600",
        "views": 120,
    },
    {
        "title": "Draft: Inside the Next Wave of Battery Tech",
        "excerpt": "A working draft exploring solid-state batteries and what comes next.",
        "category": "Science",
        "status": ArticleStatus.DRAFT,
        "tags": ["energy", "batteries"],
        "cover": None,
        "views": 0,
    },
    {
        "title": "Draft: Remote Work and the Future of Cities",
        "excerpt": "Notes on how distributed teams are reshaping urban economies.",
        "category": "Business",
        "status": ArticleStatus.DRAFT,
        "tags": ["work", "cities"],
        "cover": None,
        "views": 0,
    },
]

_BODY = (
    "## Overview\n\n"
    "This is sample article body content rendered as Markdown. It exists so the public "
    "reading feed and the editorial back-office have realistic data to display.\n\n"
    "### Key points\n\n"
    "- Written by the seeded demo author.\n"
    "- Includes a category, tags, and an excerpt.\n"
    "- Ready to be edited, published, or archived from the editorial UI.\n\n"
    "> Publishing is the art of turning drafts into trusted stories."
)


async def seed_database(session: AsyncSession) -> None:
    existing = await session.execute(select(func.count()).select_from(UserModel))
    if existing.scalar_one() > 0:
        return

    hasher = PasswordHasher()
    admin = UserModel(
        email=DEMO_ADMIN_EMAIL,
        password_hash=hasher.hash_password(DEMO_ADMIN_PASSWORD),
        full_name="NMPP Admin",
        role=Role.ADMIN,
    )
    session.add(admin)
    await session.flush()

    categories: dict[str, CategoryModel] = {}
    for name in _CATEGORIES:
        category = CategoryModel(name=name, slug=slugify(name))
        session.add(category)
        categories[name] = category
    await session.flush()

    now = datetime.now(UTC)
    for index, item in enumerate(_ARTICLES):
        published_at = (
            now - timedelta(days=index) if item["status"] == ArticleStatus.PUBLISHED else None
        )
        session.add(
            ArticleModel(
                title=item["title"],
                slug=slugify(item["title"]),
                excerpt=item["excerpt"],
                body=_BODY,
                cover_image_url=item["cover"],
                status=item["status"],
                category_id=categories[item["category"]].id,
                author_id=admin.id,
                tags=item["tags"],
                published_at=published_at,
                view_count=item["views"],
            )
        )

    await session.commit()
