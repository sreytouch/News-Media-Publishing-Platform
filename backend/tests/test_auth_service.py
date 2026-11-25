from __future__ import annotations

import pytest

from app.application.services.auth_service import AuthService
from app.core.exceptions import AuthenticationError, ValidationError
from tests.conftest import FakeUserRepository


def build_service(password_hasher, token_service) -> tuple[AuthService, FakeUserRepository]:
    users = FakeUserRepository()
    return AuthService(users, password_hasher, token_service), users


@pytest.mark.asyncio
async def test_register_creates_user(password_hasher, token_service):
    service, _ = build_service(password_hasher, token_service)

    user = await service.register("editor@example.com", "Password123!", "Editor", "editor")

    assert user.email == "editor@example.com"
    assert user.role == "editor"


@pytest.mark.asyncio
async def test_register_rejects_duplicate_email(password_hasher, token_service):
    service, _ = build_service(password_hasher, token_service)
    await service.register("dup@example.com", "Password123!", "First", "writer")

    with pytest.raises(ValidationError):
        await service.register("dup@example.com", "Password123!", "Second", "writer")


@pytest.mark.asyncio
async def test_login_returns_access_token(password_hasher, token_service):
    service, _ = build_service(password_hasher, token_service)
    await service.register("login@example.com", "Password123!", "Login User", "admin")

    tokens = await service.login("login@example.com", "Password123!")

    assert tokens.access_token
    assert tokens.token_type == "bearer"
    payload = token_service.decode_access_token(tokens.access_token)
    assert payload["role"] == "admin"


@pytest.mark.asyncio
async def test_login_rejects_bad_password(password_hasher, token_service):
    service, _ = build_service(password_hasher, token_service)
    await service.register("bad@example.com", "Password123!", "User", "writer")

    with pytest.raises(AuthenticationError):
        await service.login("bad@example.com", "WrongPassword!")
