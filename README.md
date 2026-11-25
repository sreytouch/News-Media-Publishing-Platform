# News Media Publishing Platform (NMPP)

A full-stack content management system for publishing news articles. NMPP has two areas:

- **Public reading feed** — anyone can browse published articles, filter by category, and read
  full stories (each read increments a view counter).
- **Editorial back-office** — authenticated staff manage categories and articles, move stories
  through a draft → published → archived workflow, and track publishing health on a dashboard.

![News Media Publishing Platform](./image.png)

## Domain

- **User** — `id`, `email` (unique), `password_hash`, `full_name`, `role` (`admin` | `editor` |
  `writer`), `created_at`.
- **Category** — `id`, `name`, `slug` (unique).
- **Article** — `id`, `title`, `slug` (unique), `excerpt`, `body` (Markdown), `cover_image_url`,
  `status` (`draft` | `published` | `archived`), `category_id`, `author_id`, `tags` (JSON list),
  `published_at`, `view_count`, `created_at`, `updated_at`.

## Tech stack

**Backend** — FastAPI, async SQLAlchemy 2.0, Pydantic v2 / pydantic-settings, PyJWT, PBKDF2
password hashing, pytest. Layered into `domain` / `application` / `infrastructure` / `presentation`.
The database is **SQLite via aiosqlite** by default, so there is no external Postgres/Redis to run.
Tables are created on startup and a demo dataset is seeded automatically.

**Frontend** — React 18 + TypeScript + Vite, MUI v6, react-router-dom v6,
@tanstack/react-query v5, zustand v5, react-hook-form v7, chart.js + react-chartjs-2.

## Project layout

```
news-media-publishing-platform/
  backend/    # FastAPI application + pytest tests
  frontend/   # React + Vite single-page app
  docker-compose.yml
```

## Running the backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

The API runs at http://localhost:8000. Interactive Swagger docs are at http://localhost:8000/docs.
On first startup the app creates `nmpp.db`, seeds a demo admin, categories, and sample articles.

Run the tests:

```bash
cd backend
pytest -q
```

## Running the frontend

```bash
cd frontend
npm install
cp .env.example .env   # VITE_API_BASE_URL defaults to http://localhost:8000/api/v1
npm run dev
```

The app runs at http://localhost:5173.

## Running with Docker

```bash
docker compose up --build
```

- API: http://localhost:8000
- Web: http://localhost:5173

## Seeded demo login

```
email:    admin@nmpp.local
password: Password123!
```

## API surface (prefix `/api/v1`)

**Editorial (JWT required)**

- `POST /auth/register`, `POST /auth/login`, `GET /auth/me`
- `GET/POST /categories`, `PATCH/DELETE /categories/{id}`
- `GET/POST /articles`, `GET/PATCH/DELETE /articles/{id}`,
  `POST /articles/{id}/publish`, `POST /articles/{id}/unpublish`
- `GET /dashboard/stats`

**Public (no auth)**

- `GET /public/articles` (published only; paginate; filter by category slug, tag, search)
- `GET /public/articles/{slug}` (full article; increments `view_count`)
- `GET /public/categories`

## Frontend areas

- **Public** — `/` (headlines feed with category filter) and `/article/:slug` (full story).
- **Editorial** — `/login`, then `/admin` (dashboard), `/admin/articles`, `/admin/categories`.
  The JWT is held in a zustand store and persisted to localStorage; the API client attaches it as
  a Bearer token.
