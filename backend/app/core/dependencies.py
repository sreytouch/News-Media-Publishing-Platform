from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.article_service import ArticleService
from app.application.services.auth_service import AuthService
from app.application.services.category_service import CategoryService
from app.application.services.dashboard_service import DashboardService
from app.application.services.public_service import PublicService
from app.core.config import Settings, get_settings
from app.core.security import JwtTokenService, PasswordHasher
from app.infrastructure.db.session import get_db_session
from app.infrastructure.repositories.sqlalchemy_article_repository import (
    SqlAlchemyArticleRepository,
)
from app.infrastructure.repositories.sqlalchemy_category_repository import (
    SqlAlchemyCategoryRepository,
)
from app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@dataclass(slots=True)
class CurrentUser:
    user_id: UUID
    role: str


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


def get_token_service(settings: Settings = Depends(get_settings)) -> JwtTokenService:
    return JwtTokenService(
        secret=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        access_minutes=settings.access_token_minutes,
    )


def get_auth_service(
    session: AsyncSession = Depends(get_db_session),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
    token_service: JwtTokenService = Depends(get_token_service),
) -> AuthService:
    return AuthService(
        user_repository=SqlAlchemyUserRepository(session),
        password_hasher=password_hasher,
        token_service=token_service,
    )


def get_category_service(session: AsyncSession = Depends(get_db_session)) -> CategoryService:
    return CategoryService(category_repository=SqlAlchemyCategoryRepository(session))


def get_article_service(session: AsyncSession = Depends(get_db_session)) -> ArticleService:
    return ArticleService(
        article_repository=SqlAlchemyArticleRepository(session),
        category_repository=SqlAlchemyCategoryRepository(session),
    )


def get_public_service(session: AsyncSession = Depends(get_db_session)) -> PublicService:
    return PublicService(
        article_repository=SqlAlchemyArticleRepository(session),
        category_repository=SqlAlchemyCategoryRepository(session),
        user_repository=SqlAlchemyUserRepository(session),
    )


def get_dashboard_service(session: AsyncSession = Depends(get_db_session)) -> DashboardService:
    return DashboardService(article_repository=SqlAlchemyArticleRepository(session))


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    token_service: JwtTokenService = Depends(get_token_service),
) -> CurrentUser:
    try:
        payload = token_service.decode_access_token(token)
    except Exception as exc:  # pragma: no cover - framework boundary
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token."
        ) from exc
    return CurrentUser(user_id=UUID(payload["sub"]), role=payload["role"])
