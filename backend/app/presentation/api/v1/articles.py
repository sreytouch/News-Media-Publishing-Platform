from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.application.services.article_service import ArticleService
from app.core.dependencies import CurrentUser, get_article_service, get_current_user
from app.presentation.api.v1.schemas import (
    ArticleResponse,
    CreateArticleRequest,
    UpdateArticleRequest,
    article_to_response,
)

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("", response_model=list[ArticleResponse])
async def list_articles(
    status_filter: str | None = Query(default=None, alias="status"),
    category_id: UUID | None = Query(default=None),
    search: str | None = Query(default=None),
    _: CurrentUser = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
) -> list[ArticleResponse]:
    articles = await service.list_articles(
        status=status_filter, category_id=category_id, search=search
    )
    return [article_to_response(article) for article in articles]


@router.post("", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    payload: CreateArticleRequest,
    current_user: CurrentUser = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
) -> ArticleResponse:
    article = await service.create_article(
        title=payload.title,
        excerpt=payload.excerpt,
        body=payload.body,
        category_id=UUID(payload.category_id),
        author_id=current_user.user_id,
        tags=payload.tags,
        cover_image_url=payload.cover_image_url,
    )
    return article_to_response(article)


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: UUID,
    _: CurrentUser = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
) -> ArticleResponse:
    article = await service.get_article(article_id)
    return article_to_response(article)


@router.patch("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: UUID,
    payload: UpdateArticleRequest,
    _: CurrentUser = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
) -> ArticleResponse:
    article = await service.update_article(
        article_id,
        title=payload.title,
        excerpt=payload.excerpt,
        body=payload.body,
        category_id=UUID(payload.category_id) if payload.category_id else None,
        tags=payload.tags,
        cover_image_url=payload.cover_image_url,
        status=payload.status.value if payload.status else None,
    )
    return article_to_response(article)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: UUID,
    _: CurrentUser = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
) -> None:
    await service.delete_article(article_id)


@router.post("/{article_id}/publish", response_model=ArticleResponse)
async def publish_article(
    article_id: UUID,
    _: CurrentUser = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
) -> ArticleResponse:
    article = await service.publish_article(article_id)
    return article_to_response(article)


@router.post("/{article_id}/unpublish", response_model=ArticleResponse)
async def unpublish_article(
    article_id: UUID,
    _: CurrentUser = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
) -> ArticleResponse:
    article = await service.unpublish_article(article_id)
    return article_to_response(article)
