# Scheduling API

Multi-tenant scheduling API for businesses built with FastAPI, PostgreSQL and AWS.

## Tech Stack

- **Language:** Python 3.13
- **Framework:** FastAPI
- **Database:** PostgreSQL (coming soon)
- **Cloud:** AWS (coming soon)
- **Containers:** Docker (coming soon)

## Getting Started

### Prerequisites

- Python 3.13+
- Poetry 2.x

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

3. Run the API
```bash
   poetry run uvicorn app.main:app --reload
```

4. Access the docs# scheduling-api
Multi-tenant scheduling API built with FastAPI, PostgreSQL and AWS

http://localhost:8000/docs

## API Endpoints

| Method | Endpoint  | Description          |
|--------|-----------|----------------------|
| GET    | /health   | Health check         |
| GET    | /docs     | Swagger UI           |

## Project Status

🚧 Under active development — Sprint 1 in progress.
