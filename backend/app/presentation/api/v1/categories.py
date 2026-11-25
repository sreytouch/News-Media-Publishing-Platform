from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.application.services.category_service import CategoryService
from app.core.dependencies import CurrentUser, get_category_service, get_current_user
from app.presentation.api.v1.schemas import (
    CategoryResponse,
    CreateCategoryRequest,
    UpdateCategoryRequest,
    category_to_response,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=list[CategoryResponse])
async def list_categories(
    _: CurrentUser = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
) -> list[CategoryResponse]:
    categories = await service.list_categories()
    return [category_to_response(category) for category in categories]


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CreateCategoryRequest,
    _: CurrentUser = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
) -> CategoryResponse:
    category = await service.create_category(payload.name)
    return category_to_response(category)


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    payload: UpdateCategoryRequest,
    _: CurrentUser = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
) -> CategoryResponse:
    category = await service.update_category(category_id, payload.name)
    return category_to_response(category)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    _: CurrentUser = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
) -> None:
    await service.delete_category(category_id)
