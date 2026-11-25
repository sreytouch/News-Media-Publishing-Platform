from fastapi import APIRouter

from app.presentation.api.v1.articles import router as articles_router
from app.presentation.api.v1.auth import router as auth_router
from app.presentation.api.v1.categories import router as categories_router
from app.presentation.api.v1.dashboard import router as dashboard_router
from app.presentation.api.v1.public import router as public_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(categories_router)
api_router.include_router(articles_router)
api_router.include_router(dashboard_router)
api_router.include_router(public_router)
