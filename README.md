# ❤️ Connectly - date platform api 

[![Abblix OIDC Server](https://i.imgur.com/lnqJyfc.png)](https://github.com/Maksim-Volosh/wildberries-catalog-api)


[![Python](https://img.shields.io/badge/Python-3.12.3-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.22-blue?logo=telegram)](https://aiogram.dev/)
[![OpenAI](https://img.shields.io/badge/OpenAI-2.16-green?logo=)](https://openai.com/api/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.11-purple?logo=pydantic)](https://docs.pydantic.dev/latest/)
[![PyTest](https://img.shields.io/badge/Pytest-2.11-purple?logo=pytest)](https://docs.pytest.org/en/stable/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-purple?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker--Compose-ready-blue?logo=docker)](https://docs.docker.com/compose/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-6.2-red?logo=redis)](https://redis.io/)
[![Pytest](https://img.shields.io/badge/Pytest-tested-brightgreen?logo=pytest)](https://docs.pytest.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Clean--Architecture-yellowgreen)](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html)
[![License](https://img.shields.io/github/license/Maksim-Volosh/dating-platform-api)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/Maksim-Volosh/dating-platform-api?color=purple)](https://github.com/Maksim-Volosh/dating-platform-api/commits/main)
[![Repo Size](https://img.shields.io/github/repo-size/Maksim-Volosh/dating-platform-api)](https://github.com/Maksim-Volosh/dating-platform-api)
[![Open Issues](https://img.shields.io/github/issues/Maksim-Volosh/dating-platform-api?label=issues)](https://github.com/Maksim-Volosh/dating-platform-api/issues)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)](https://github.com/Maksim-Volosh/dating-platform-api/pulls)
[![Made with love by Maksim](https://img.shields.io/badge/made%20with-%E2%9D%A4-red)](https://github.com/Maksim-Volosh)

⭐ Star us on GitHub — it motivates us a lot!

[![Share on X](https://img.shields.io/badge/share-000000?logo=x&logoColor=white)](https://x.com/intent/tweet?text=Check%20out%20this%20project%20on%20GitHub:%20https://github.com/Maksim-Volosh/dating-platform-api%20%23Django%20%23API%20%23CleanArchitecture)
[![Share on Facebook](https://img.shields.io/badge/share-1877F2?logo=facebook&logoColor=white)](https://www.facebook.com/sharer/sharer.php?u=https://github.com/Maksim-Volosh/dating-platform-api)
[![Share on Reddit](https://img.shields.io/badge/share-FF4500?logo=reddit&logoColor=white)](https://www.reddit.com/submit?title=Check%20out%20this%20project%20on%20GitHub:%20https://github.com/Maksim-Volosh/dating-platform-api)
[![Share on Telegram](https://img.shields.io/badge/share-0088CC?logo=telegram&logoColor=white)](https://t.me/share/url?url=https://github.com/Maksim-Volosh/dating-platform-api&text=Check%20out%20this%20project%20on%20GitHub)



## 📚 Table of Contents

- [🎓 About](#-about)
- [📌 Features](#-features)
- [🧱 Tech Stack](#-tech-stack)
- [🚀 Installation](#-installation)
- [🎯 Endpoints](#-endpoints)
  - [POST /api/v1/parse_products/](#post-apiv1parse_products-parse-products-by-query-for-pages-and-save-to-database)
  - [GET /api/v1/products/](#get-apiv1products-get-products-by-filters)
- [🧩 Models](#models)
- [📦 Serializers](#serializers)
- [🧠 Use Cases](#use-cases)
- [⚠️ Exceptions](#exceptions)
- [✅ Testing](#testing)

<br>


## 🎓 About

This project is a **production-style matchmaking backend** built with **FastAPI** and a Clean Architecture-inspired layering
(**domain → application → infrastructure → API**).  
It implements the full flow for a dating/deck platform: **user profiles**, **photo management**, **candidate deck generation**
(geo + preference filtering), **swipes**, and a lightweight **inbox/likes** layer.

On top of the HTTP API, the project also includes a **Telegram Bot (aiogram v3)** that acts as a real client:
registration via FSM, profile browsing, likes/inbox, and AI actions — all through the backend API using an HTTP client with API-key auth.

Persistence is handled with **PostgreSQL + SQLAlchemy (async)** and **Alembic migrations**, while **Redis** is used for
fast deck/inbox operations and **rate limiting** (especially for AI endpoints).

<br>

## 📌 Features

- **Clean Architecture Layers**: Domain entities & interfaces, application use cases/services, infrastructure adapters, thin API routers 
- **API Key Authentication**: Header-based auth (`X-API-KEY`) to protect API endpoints 
- **Users**: Create/update users, patch description, and fetch profile view (incl. distance for a viewer) 
- **Photos**: User photo management with validation and limits (up to 3 photos in bot UX) 
- **Deck Generation**: Personalized deck based on geo (location → bbox/distance) and preference filtering; served as “next profile” UX 
- **Swipes**: Like/dislike flow with persistence + side-effects (notifications & inbox count updates) 
- **Inbox / Likes Flow**: Cached inbox/likes count and “view who liked you” flow inside the bot 
- **AI Helpers**:
  - AI profile analysis
  - AI match opener generation (bot callback-based UX) 
- **Rate Limiting (Redis)**: Throttling for AI requests with user-friendly “limit reached” UX 
- **Telegram Bot (aiogram v3)**:
  - FSM registration (name/age/location/description/gender/preferences/photos)
  - Browsing/swiping, likes/inbox, profile menu actions
  - Bot startup/shutdown lifecycle and HTTP session management 
- **Migrations (Alembic)**: Versioned schema changes for database evolution
- **Testing Setup**: pytest + pytest-asyncio, with at least AI service test coverage

<br>

## 🧱 Tech Stack

| Technology            | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| 🐍 Python 3.12        | Main language (async-first backend + bot)                                   |
| ⚡ FastAPI             | HTTP API framework (routers, dependencies, OpenAPI/Swagger)                 |
| 🧩 Pydantic v2         | Data validation + DTOs/schemas + settings management                         |
| 🗄️ SQLAlchemy 2 (async) | Async ORM / DB access layer for PostgreSQL                                   |
| 🧬 Alembic             | Database migrations & schema versioning                                     |
| 🐘 PostgreSQL          | Primary relational database                                                 |
| 🔴 Redis               | Deck/inbox caching + rate limiting storage                                  |
| 🤖 Aiogram v3          | Telegram bot (FSM registration + flows, uses the API as a client)          |
| 🧠 OpenAI SDK / OpenRouter | AI integrations via OpenAI-compatible chat completions                    |
| 🌐 HTTP Client (async) | Bot/API outbound calls (async HTTP client for external requests)           |
| 🐳 Docker              | Containerized development & deployment                                      |
| 🧩 Docker Compose      | Local stack orchestration (API + Postgres + Redis)                          |
| 🧪 Pytest              | Testing framework                                                           |
| ⏱️ pytest-asyncio       | Async test support for coroutines / async services                           |
| 🧱 Clean Architecture   | Layering: domain → application → infrastructure → API                       |

<br>

## 🏗️ Architecture Layers (Clean-ish)

The project follows a Clean Architecture-inspired structure with clear boundaries between business logic and infrastructure.

- **`domain/`**
  - Pure business layer: **entities**, **interfaces (ports)**, **domain exceptions**
  - Stateless domain services (no I/O), e.g. **`haversine`**, **`bounding_box`**

- **`application/`**
  - **Use cases** (orchestrate business scenarios)
  - Application services that combine domain logic + ports:
    - **deck building**
    - **geo filtering**
    - **swipe filtering**
    - **inbox side-effects on swipe**
    - **AI formatting/validation pipeline**

- **`infrastructure/`**
  - Adapters and external integrations:
    - **SQLAlchemy repositories** (PostgreSQL)
    - **Redis caches** (deck/inbox)
    - **Redis rate limiter**
    - **OpenRouter / OpenAI-compatible AI client**
    - low-level helpers (serialization, keys, TTL policies)

- **`api/`**
  - FastAPI delivery layer:
    - **routers**
    - **request/response schemas**
    - **dependencies** (auth, rate limit, DI wiring)

- **`core/`**
  - Cross-cutting configuration and wiring:
    - **settings / config**
    - **DI container / providers**
    - app initialization (startup/shutdown)

<br>

## 🚀 Installation

This project can be launched locally using **Docker Compose**.

#### ✅ Clone the Repository
---

```bash
git clone https://github.com/Maksim-Volosh/dating-platform-api.git
cd dating-platform-api
```

#### ⚙️ Configure API Environment Variables
---

The project is configured via environment variables using a nested settings structure (`APP_CONFIG__...`).
For local development, copy the template and fill in the **[required values.](#)**

##### 1. Create your `.env` from template:

  ```bash
  cp .env.template .env
  ```

##### 2. Update the required variables (database, redis, api key, AI config).

You can use this as a baseline for local runs:

```env
APP_CONFIG__DB__URL=postgresql+asyncpg://user:password@db:5432/app_db
APP_CONFIG__DB__ECHO=False
APP_CONFIG__DB__ECHO_POOL=False
APP_CONFIG__DB__POOL_SIZE=5
APP_CONFIG__DB__MAX_OVERFLOW=10
APP_CONFIG__STATIC__URL=/uploads
APP_CONFIG__SECURITY__API_KEY=[api_key]
APP_CONFIG__CACHE__URL=redis://redis:6379/0
APP_CONFIG__DETAILS__TITLE=Dating Platform API
APP_CONFIG__DETAILS__DESCRIPTION=API for the Dating Platform
APP_CONFIG__DECK__MAX_SIZE=20
APP_CONFIG__DECK__TIMEOUT=3600
APP_CONFIG__DECK__RADIUS_STEPS_KM=[5,10,15,20]
APP_CONFIG__AI__BASE_URL=https://openrouter.ai/api/v1
APP_CONFIG__AI__API_KEY=[ai_key]
APP_CONFIG__AI__TIMEOUT=40
APP_CONFIG__AI_RATE_LIMITS__PROFILE_ANALYZE__LIMIT=3
APP_CONFIG__AI_RATE_LIMITS__PROFILE_ANALYZE__WINDOW_SEC=3600
APP_CONFIG__AI_RATE_LIMITS__MATCH_OPENER__LIMIT=5
APP_CONFIG__AI_RATE_LIMITS__MATCH_OPENER__WINDOW_SEC=3600
```

#### 🚀 Build and start API service
---

##### 1. Run docker compose:

```bash
docker compose up --build
```
##### 2. Find container name: docker ps:
  ```bash
  CONTAINER ID   IMAGE          COMMAND       NAMES
  abcd1234ef56   myapp-image    "uvicorn ..." my_running_container
  ```

##### 3. Apply migrations

> Run this in a separate terminal while containers are up.

```bash
docker compose exec my_running_container alembic upgrade head
```

##### 3. Open Swagger

* API docs: `http://localhost:8000/docs`
* OpenAPI JSON: `http://localhost:8000/openapi.json`


#### ⚙️ Configure BOT Environment Variables
---

You need to create a bot in telegram via `@BotFather`, get the `bot_token` and set it in the `bot/.env` file:

```env
BOT_TOKEN=[bot_token]
```

#### 🧠 Run Telegram Bot
---
Now run the bot in a separate terminal:

```bash
python bot/main.py
```

#### 🧪 Running Tests (inside Docker)
---
All tests can be run inside the docker container:
```bash
docker compose exec my_running_container pytest -v
``` 

<br>

## 📚 API Reference

> Full interactive docs are available in Swagger (OpenAPI).  
> This section explains **what each endpoint group does** and **what errors to expect**.

#### 🔐 Authentication
---
  All endpoints are protected with an API key:

  - Header: `X-API-KEY: <your_key>`
  - Missing/invalid key → **401 Unauthorized**

#### 👤 Users
---

**Purpose:** create/update user profiles and fetch profile views.

Typical operations:
- Create user (registration)
- Update profile fields (bio/description, preferences, location)
- Get profile view (optionally with distance to viewer)

Common errors:
- **400 Bad Request** — invalid payload (missing fields, wrong types)
- **404 Not Found** — user does not exist
- **401 Unauthorized** — missing/invalid API key

#### 🖼️ Photos
---

**Purpose:** manage user photos (upload/list/delete).

Notes:
- Enforces photo constraints (e.g. limits/validation)

Common errors:
- **400 Bad Request** — invalid payload / constraints violation
- **404 Not Found** — user or photo not found
- **401 Unauthorized** — missing/invalid API key

#### 🎴 Deck
---

**Purpose:** get the next candidate from a personalized deck.

How it works (high-level):
- Tries to serve candidates from Redis deck cache
- If cache is empty → rebuilds deck using geo + preference filters

Common errors:
- **404 Not Found** — no candidates found / empty deck after rebuild 
- **400 Bad Request** — invalid user context
- **401 Unauthorized** — missing/invalid API key

#### 👍👎 Swipes
---

**Purpose:** persist swipe decisions and trigger side effects (likes/inbox).

Typical operations:
- Like / dislike a candidate
- Update existing swipe 

Common errors:
- **400 Bad Request** — invalid payload (same user/candidate, invalid action)
- **404 Not Found** — user or candidate not found
- **401 Unauthorized** — missing/invalid API key

#### 📥 Inbox / Likes
---

**Purpose:** quick access to "incoming likes" / inbox items.

Typical operations:
- Get inbox count
- Peek items
- Ack/mark processed

Common errors:
- **404 Not Found** — inbox empty / user not found 
- **401 Unauthorized** — missing/invalid API key

#### 🤖 AI
---

**Purpose:** AI helpers (profile analysis / opener generation).

Important behavior:
- Protected by Redis-based rate limiting
- Uses OpenAI-compatible client (OpenRouter)
- Upstream timeouts/errors are handled gracefully

Common errors:
- **429 Too Many Requests** — rate limit exceeded (cooldown applies)
- **503 Service Unavailable** — upstream AI timeout / connection issue
- **400 Bad Request** — invalid payload
- **401 Unauthorized** — missing/invalid API key

