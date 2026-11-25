from __future__ import annotations

import re
from collections.abc import Callable

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    slug = _SLUG_RE.sub("-", value.lower().strip()).strip("-")
    return slug or "item"


def unique_slug(value: str, exists: Callable[[str], bool]) -> str:
    """Generate a slug from ``value`` that is unique according to ``exists``.

    ``exists`` returns True when a slug is already taken; suffixes -2, -3, ...
    are appended until an available slug is found.
    """
    base = slugify(value)
    candidate = base
    counter = 2
    while exists(candidate):
        candidate = f"{base}-{counter}"
        counter += 1
    return candidate
