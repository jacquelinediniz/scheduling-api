# Scheduling API

![CI](https://github.com/jacquelinediniz/scheduling-api/actions/workflows/ci.yml/badge.svg)

Multi-tenant scheduling API for businesses built with FastAPI, PostgreSQL and AWS.

## 🚀 Production

**API URL:** https://scheduling-api-l9yz.onrender.com  
**Swagger UI:** https://scheduling-api-l9yz.onrender.com/docs  
**Health Check:** https://scheduling-api-l9yz.onrender.com/health  

## 🏗️ Architecture

GitHub → GitHub Actions (CI/CD) → Render (API)
↓
AWS RDS PostgreSQL

## 🛠️ Tech Stack

- **Language:** Python 3.13
- **Framework:** FastAPI
- **Database:** PostgreSQL 16 (AWS RDS)
- **ORM:** SQLAlchemy 2.0 + Alembic
- **Auth:** JWT + OAuth2
- **Containers:** Docker
- **Cloud:** AWS (RDS, ECR, IAM) + Render
- **CI/CD:** GitHub Actions
- **Tests:** pytest + pytest-asyncio (71% coverage)

## 📋 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | /health | Health check | ❌ |
| GET | /docs | Swagger UI | ❌ |
| POST | /api/v1/tenants/ | Create tenant | ❌ |
| GET | /api/v1/tenants/ | List tenants | ❌ |
| GET | /api/v1/tenants/{id} | Get tenant | ❌ |
| PATCH | /api/v1/tenants/{id} | Update tenant | ❌ |
| DELETE | /api/v1/tenants/{id} | Delete tenant | ❌ |
| POST | /api/v1/auth/register | Register user | ❌ |
| POST | /api/v1/auth/login | Login | ❌ |
| GET | /api/v1/auth/me | Get current user | ✅ |
| POST | /api/v1/services/ | Create service | ✅ |
| GET | /api/v1/services/ | List services | ✅ |
| GET | /api/v1/services/{id} | Get service | ✅ |
| PATCH | /api/v1/services/{id} | Update service | ✅ |
| POST | /api/v1/appointments/ | Create appointment | ✅ |
| GET | /api/v1/appointments/ | List appointments | ✅ |
| GET | /api/v1/appointments/{id} | Get appointment | ✅ |
| PATCH | /api/v1/appointments/{id} | Update appointment | ✅ |

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- Poetry 2.x
- Docker Desktop

### Installation

1. Clone the repository
```bash
   git clone https://github.com/jacquelinediniz/scheduling-api.git
   cd scheduling-api
```

2. Install dependencies
```bash
   poetry install
```

3. Copy environment variables
```bash
   cp .env.example .env
```

4. Start the database
```bash
   docker compose up db -d
```

5. Run migrations
```bash
   poetry run alembic upgrade head
```

6. Start the API
```bash
   poetry run uvicorn app.main:app --reload
```

7. Access the docs
http://localhost:8000/docs

## 🧪 Tests

```bash
poetry run pytest tests/ -v --cov=app --cov-report=term-missing
```

## 📁 Project Structure

scheduling-api/
├── app/
│   ├── api/v1/endpoints/    # REST endpoints
│   ├── core/                # Config and security
│   ├── db/                  # Database session
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic
├── migrations/              # Alembic migrations
├── tests/                   # Automated tests
├── .github/workflows/       # CI/CD pipeline
├── docker-compose.yml
└── Dockerfile