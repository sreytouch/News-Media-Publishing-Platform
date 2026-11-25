from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.domain.entities.common import ArticleStatus


@dataclass(slots=True)
class Article:
    title: str
    slug: str
    excerpt: str
    body: str
    category_id: UUID
    author_id: UUID
    id: UUID = field(default_factory=uuid4)
    cover_image_url: str | None = None
    status: ArticleStatus = ArticleStatus.DRAFT
    tags: list[str] = field(default_factory=list)
    published_at: datetime | None = None
    view_count: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
