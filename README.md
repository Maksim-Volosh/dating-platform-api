# ❤️ Connectly - Dating Platform API

[![Banner](assets/Connectly.png)](https://github.com/Maksim-Volosh/dating-platform-api)


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

[![Share on X](https://img.shields.io/badge/share-000000?logo=x&logoColor=white)](https://x.com/intent/tweet?text=Check%20out%20this%20project%20on%20GitHub:%20https://github.com/Maksim-Volosh/dating-platform-api)
[![Share on Facebook](https://img.shields.io/badge/share-1877F2?logo=facebook&logoColor=white)](https://www.facebook.com/sharer/sharer.php?u=https://github.com/Maksim-Volosh/dating-platform-api)
[![Share on Reddit](https://img.shields.io/badge/share-FF4500?logo=reddit&logoColor=white)](https://www.reddit.com/submit?title=Check%20out%20this%20project%20on%20GitHub:%20https://github.com/Maksim-Volosh/dating-platform-api)
[![Share on Telegram](https://img.shields.io/badge/share-0088CC?logo=telegram&logoColor=white)](https://t.me/share/url?url=https://github.com/Maksim-Volosh/dating-platform-api&text=Check%20out%20this%20project%20on%20GitHub)



## 📚 Table of Contents

- [🎓 About](#-about)
- [📌 Features](#-features)
- [🧱 Tech Stack](#-tech-stack)
- [📁 Project Structure (high-level)](#-project-structure-high-level)
- [🏗️ Architecture Layers (Clean-ish)](#️-architecture-layers-clean-ish)
- [🚀 Installation](#-installation)
  - [✅ Clone the Repository](#-clone-the-repository)
  - [⚙️ Configure API Environment Variables](#️-configure-api-environment-variables)
  - [🚀 Build and start API service](#-build-and-start-api-service)
  - [⚙️ Configure BOT Environment Variables](#️-configure-bot-environment-variables)
  - [🧠 Run Telegram Bot](#-run-telegram-bot)
  - [🧪 Running Tests (inside Docker)](#-running-tests-inside-docker)
- [⚙️ Environment Variables Reference](#️-environment-variables-reference)
  - [🧩 Core / App Metadata](#-core--app-metadata)
  - [🔐 Security](#-security)
  - [🐘 Database (PostgreSQL)](#-database-postgresql)
  - [🔴 Cache (Redis)](#-cache-redis)
  - [🗂️ Static Files / Uploads](#️-static-files--uploads)
  - [🎴 Deck (Candidate Feed)](#-deck-candidate-feed)
  - [📥 Inbox](#-inbox)
  - [🤖 AI (OpenRouter / OpenAI-compatible)](#-ai-openrouter--openai-compatible)
  - [🚦 AI Rate Limits (Redis)](#-ai-rate-limits-redis)
- [📚 API Reference](#-api-reference)
  - [🔐 Authentication](#-authentication)
  - [👤 Users](#-users)
  - [🖼️ Photos](#️-photos)
  - [🎴 Deck](#-deck)
  - [👍👎 Swipes](#-swipes)
  - [📥 Inbox / Likes](#-inbox--likes)
  - [🤖 AI](#-ai)



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

## 📁 Project Structure (high-level)

The repository is organized around clean boundaries: **domain (pure logic)** → **application (use cases)** → **infrastructure (I/O)** → **api (delivery)**, plus a separate **Telegram bot client**.

```
.
├── alembic/                     # Alembic migrations (DB schema history)
├── app/
│   ├── api/v1/                  # FastAPI routers + schemas + dependencies
│   │   ├── dependencies/        # auth, rate limiting dependencies
│   │   ├── mappers/             # mappers (DTOs <-> entities)
│   │   ├── routers/             # ai, deck, inbox, photo, swipe, user
│   │   └── schemas/             # request/response DTOs
│   ├── application/             # Orchestration layer
│   │   ├── services/            # app services (deck builder, filters, inbox, ai formatting)
│   │   └── use_cases/           # business scenarios (create user, next deck, swipe, ai, etc.)
│   ├── core/                    # configuration + DI composition
│   │   └── composition/         # container + wiring helpers
│   ├── domain/                  # Pure domain (no I/O)
│   │   ├── entities/            # dataclasses: user, swipe, photo, inbox, bbox
│   │   ├── interfaces/          # ports (repos/caches/clients contracts)
│   │   ├── exceptions/          # domain exceptions (mapped to HTTP in API layer)
│   │   └── services/            # pure services (haversine, bounding_box)
│   ├── infrastructure/          # Adapters (I/O)
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── repositories/        # PostgreSQL repos + Redis caches + external clients
│   │   ├── rate_limit/          # redis rate limiter implementation
│   │   └── helpers/             # db/redis/openai helpers
│   └── main.py                  # FastAPI app entrypoint
├── bot/                         # Telegram bot client (aiogram v3)
│   ├── app/
│   │   ├── handlers/            # aiogram handlers (routing)
│   │   ├── flows/               # multi-step flows (registration, swipe, ai, profile)
│   │   ├── presenters/          # UI text formatting (messages/keyboards)
│   │   ├── services/            # bot services calling API (users/deck/swipe/inbox/ai)
│   │   ├── infrastructure/      # HTTP client + API client + error mapping
│   │   ├── states/              # FSM states
│   │   └── container.py         # bot DI container
│   ├── config.py
│   └── run.py
├── tests/                       # Unit tests (services + use cases)
├── docker-compose.yml           # local stack: api + postgres + redis
├── Dockerfile
└── requirements.txt
```

> If you’re reviewing this project: start from `app/application/use_cases/` and follow dependencies into `domain/` and `infrastructure/`.


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

## 🔁 Data Flows (text diagrams)

Below are the main user-facing scenarios, shown as simplified request-to-response pipelines.

#### 1) Create User → Preload Deck

```

POST /api/.../users
→ Router (validation)
→ CreateUserUseCase
→ UserRepository.create (PostgreSQL)
→ DeckBuilderService.build_for_user
→ bounding_box(user_location, radius_steps)
→ CandidateRepository.find_by_preferences_and_bbox (PostgreSQL)
→ SwipeFilterService.filter (exclude already swiped)
→ GeoCandidateFilterService.filter (distance / radius rules)
→ DeckCache.save (Redis LIST + TTL)
→ 201 Created (user)

```

**Result:** after registration the user already has a ready-to-use deck cached in Redis.

---

#### 2) Get Next Candidate → Cache First → Rebuild on Miss

```

GET /api/.../deck/next
→ Router
→ GetNextCandidateUseCase
→ DeckCache.lpop (Redis)
→ HIT  → return candidate_id
→ MISS → rebuild deck:
→ bounding_box(user_location, radius_steps)
→ CandidateRepository.find_by_preferences_and_bbox (PostgreSQL)
→ SwipeFilterService.filter
→ GeoCandidateFilterService.filter
→ DeckCache.save (Redis LIST + TTL)
→ DeckCache.lpop (Redis)
→ 200 OK (candidate profile)

```

**Why this is good:** hot path is O(1) Redis `LPOP`, rebuild happens only when needed.

---

#### 3) Swipe → Persist in DB → Inbox Side-effect

```

POST /api/.../swipes
→ Router
→ SwipeUseCase
→ normalize input
→ SwipeRepository.create_or_update (PostgreSQL)
→ if LIKE:
→ InboxService.on_like
→ InboxCache.push (Redis LIST)
→ InboxCache.dedup (Redis SET)
→ set TTL / update counters
→ 200 OK (swipe result)

```

**Result:** swipes are persistent, while inbox UX stays fast via Redis.

---

#### 4) AI Endpoints → Rate Limiting → AI Client → Safe Fallback

```

POST /api/.../ai/{telegram_id}/...
→ RateLimiterDependency (Redis)
→ if exceeded → 429 Too Many Requests
→ AIUseCase
→ (optional) load user/profile context (PostgreSQL)
→ IAIClientRepository.complete(...)
→ OpenRouter/OpenAI-compatible client
→ format / validate output
→ on upstream timeout/error → 503 Service Unavailable
→ 200 OK (AI response)

```

**Why this is safe:** AI calls are throttled, and upstream failures degrade gracefully.

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
If you don't want to chage the default configuration, you can use the `.env.template` file to create your own `.env` file.

If you want to change the default configuration, copy the template and fill in the **[required values.](#️-environment-variables-reference)**

##### 1. Create your `.env` from template:

  ```bash
  cp .env.template .env
  ```

##### 2. Update the required variables (database, redis, api key, AI config).

You can use this as a baseline for local runs:

```env
APP_CONFIG__DETAILS__TITLE=Dating Platform API
APP_CONFIG__DETAILS__DESCRIPTION=API for the Dating Platform
APP_CONFIG__SECURITY__API_KEY=key
APP_CONFIG__API__PREFIX=/api
APP_CONFIG__RUN__HOST=0.0.0.0
APP_CONFIG__RUN__PORT=8000
APP_CONFIG__RUN__RELOAD=True
APP_CONFIG__DB__URL=postgresql+asyncpg://postgres_user:postgres_password@db:5432/dating_platform_db
APP_CONFIG__DB__ECHO=0
APP_CONFIG__DB__ECHO_POOL=False
APP_CONFIG__DB__POOL_SIZE=5
APP_CONFIG__DB__MAX_OVERFLOW=10
APP_CONFIG__CACHE__URL=redis://redis:6379/0
APP_CONFIG__STATIC__DIRECTORY=./uploads
APP_CONFIG__STATIC__URL=/uploads
APP_CONFIG__DECK__MAX_SIZE=20
APP_CONFIG__DECK__TIMEOUT=3600
APP_CONFIG__DECK__RADIUS_STEPS_KM=[5,10,15,20]
APP_CONFIG__INBOX__TIMEOUT=604800
APP_CONFIG__AI__BASE_URL=https://openrouter.ai/api/v1
APP_CONFIG__AI__MODEL=openrouter/free
APP_CONFIG__AI__API_KEY=sk-or-v1-REPLACE_ME
APP_CONFIG__AI__TIMEOUT=40
APP_CONFIG__AI_RATE_LIMITS__PROFILE_ANALYZE__LIMIT=5
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
API_URL=[http://localhost:8000/api/v1] # or your API endpoint
API_KEY=[your_api_key] # your APP_CONFIG__SECURITY__API_KEY in .env 
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

## ⚙️ Environment Variables Reference

All configuration is loaded from `.env` using nested keys with prefix `APP_CONFIG__`  
(see `SettingsConfigDict(env_nested_delimiter="__", env_prefix="APP_CONFIG__")`).

### 🧩 Core / App Metadata

- `APP_CONFIG__DETAILS__TITLE`  
  Swagger/OpenAPI title shown in `/docs`.

- `APP_CONFIG__DETAILS__DESCRIPTION`  
  Swagger/OpenAPI description shown in `/docs`.

- `APP_CONFIG__API__PREFIX`  
  Global API prefix (default: `/api`). Useful if you want versioning like `/api/v1`.

- `APP_CONFIG__RUN__HOST`  
  Host to bind the server (default: `0.0.0.0`).

- `APP_CONFIG__RUN__PORT`  
  Port to bind the server (default: `8000`).

- `APP_CONFIG__RUN__RELOAD`  
  Auto-reload for development (default: `True`).  
  In production should be `False`.

---

### 🔐 Security

- `APP_CONFIG__SECURITY__API_KEY`  
  API key used to protect endpoints.  
  Passed via header: `X-API-KEY: <your_key>`.

---

### 🐘 Database (PostgreSQL)

- `APP_CONFIG__DB__URL`  
  Async SQLAlchemy DSN for Postgres.  
  Format: `postgresql+asyncpg://user:password@host:port/dbname`.

- `APP_CONFIG__DB__ECHO`  
  SQL query logging (default: `False`).  
  Useful for debugging.

- `APP_CONFIG__DB__ECHO_POOL`  
  Connection pool logging (default: `False`).

- `APP_CONFIG__DB__POOL_SIZE`  
  Base DB connection pool size (default in code: `50`, often set lower locally).

- `APP_CONFIG__DB__MAX_OVERFLOW`  
  Extra connections above pool size allowed (default: `10`).

---

### 🔴 Cache (Redis)

- `APP_CONFIG__CACHE__URL`  
  Redis connection URL used for:
  - deck caching
  - inbox caching
  - rate limiting  
  Example: `redis://redis:6379/0`.

---

### 🗂️ Static Files / Uploads

- `APP_CONFIG__STATIC__DIRECTORY`  
  Directory where uploaded files are stored (default: `./uploads`).

- `APP_CONFIG__STATIC__URL`  
  URL prefix for serving uploaded files (default: `/uploads`).

---

### 🎴 Deck (Candidate Feed)

- `APP_CONFIG__DECK__MAX_SIZE`  
  Maximum number of candidates stored in a deck (Redis list).

- `APP_CONFIG__DECK__TIMEOUT`  
  Deck TTL in seconds (how long the cached deck lives in Redis).

- `APP_CONFIG__DECK__RADIUS_STEPS_KM`  
  Radius expansion steps (km) used when building a deck.  
  Example: `[5,10,15,20]`  
  Meaning: if not enough candidates were found nearby, the search radius increases by these steps.

---

### 📥 Inbox

- `APP_CONFIG__INBOX__TIMEOUT`  
  Inbox TTL in seconds (default: `604800` = 7 days).  
  Controls how long cached inbox items/count are stored in Redis.

---

### 🤖 AI (OpenRouter / OpenAI-compatible)

- `APP_CONFIG__AI__BASE_URL`  
  Base URL for OpenAI-compatible API provider.  
  Example: `https://openrouter.ai/api/v1`.

- `APP_CONFIG__AI__MODEL`  
  AI model used for analysis (default: `openrouter/free`).

- `APP_CONFIG__AI__API_KEY`  
  API key for the AI provider.  
  **Do not commit real keys into git** — keep it only in `.env`.

- `APP_CONFIG__AI__TIMEOUT`  
  Timeout for AI requests in seconds (default in code: `20`).

---

### 🚦 AI Rate Limits (Redis)

Each AI endpoint has its own rate limit rule (limit + time window).

**Profile Analyze**
- `APP_CONFIG__AI_RATE_LIMITS__PROFILE_ANALYZE__LIMIT`  
  Max requests per window for profile analysis.
- `APP_CONFIG__AI_RATE_LIMITS__PROFILE_ANALYZE__WINDOW_SEC`  
  Window duration in seconds.

**Match Opener**
- `APP_CONFIG__AI_RATE_LIMITS__MATCH_OPENER__LIMIT`  
  Max requests per window for opener generation.
- `APP_CONFIG__AI_RATE_LIMITS__MATCH_OPENER__WINDOW_SEC`  
  Window duration in seconds.

If the limit is exceeded, API returns **429 Too Many Requests**.


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

