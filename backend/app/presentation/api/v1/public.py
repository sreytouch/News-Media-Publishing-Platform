from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.application.services.public_service import PublicService
from app.core.dependencies import get_public_service
from app.presentation.api.v1.schemas import (
    CategoryResponse,
    PublicArticleDetail,
    PublicArticleList,
    category_to_response,
)

router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/categories", response_model=list[CategoryResponse])
async def list_public_categories(
    service: PublicService = Depends(get_public_service),
) -> list[CategoryResponse]:
    categories = await service.list_categories()
    return [category_to_response(category) for category in categories]


@router.get("/articles", response_model=PublicArticleList)
async def list_public_articles(
    category: str | None = Query(default=None),
    tag: str | None = Query(default=None),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    service: PublicService = Depends(get_public_service),
) -> PublicArticleList:
    payload = await service.list_articles(
        category_slug=category, tag=tag, search=search, page=page, page_size=page_size
    )
    return PublicArticleList.model_validate(payload)


@router.get("/articles/{slug}", response_model=PublicArticleDetail)
async def get_public_article(
    slug: str, service: PublicService = Depends(get_public_service)
) -> PublicArticleDetail:
    payload = await service.get_article(slug)
    return PublicArticleDetail.model_validate(payload)
