from __future__ import annotations

from app.domain.repositories.protocols import ArticleRepository


class DashboardService:
    def __init__(self, article_repository: ArticleRepository) -> None:
        self._articles = article_repository

    async def get_statistics(self) -> dict:
        return await self._articles.statistics()
