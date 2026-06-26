
# Buguard Asset Management AI

Buguard Asset Management AI is a high-performance **Asset Management System (AMS)** designed for the DarkAtlas Attack Surface Monitoring task. It features intelligent data ingestion, automated relationship mapping, and natural language querying.

It combines:
- **FastAPI** for asynchronous API endpoints
- **PostgreSQL (SQLAlchemy)** for structured asset storage
- **OpenAI API** for intelligent natural language analysis
- **Alembic** for seamless database schema migrations

---

## Project Structure

| Directory / File | Description |
|---|---|
| `src/main.py` | FastAPI entrypoint and application configuration. |
| `src/routes/` | API endpoint definitions (Assets, Analysis, NLP Querying). |
| `src/model/` | Core logic, repository pattern, and service layers. |
| `src/model/db_schema/` | SQLAlchemy models and database schema definitions. |
| `src/controller/ai/` | LLM orchestration, prompt engineering, and AI logic. |
| `alembic/` | Database migration scripts and configuration. |
| `docker/` | Docker Compose orchestration files. |

---

## Requirements

- Python `3.10+`
- PostgreSQL `+ Qdrant (if running without Docker)`
- Docker `(recommended)`

System dependencies (Ubuntu):

```bash
sudo apt update
sudo apt install -y libpq-dev gcc python3-dev
```
---

## Local Setup (Without Docker)

### 1) Create and activate a virtual environment

```bash
python3 -m venv buguard
source buguard/bin/activate
```

(Optional) Setup you command line interface for better readability
```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

### 2) Install Python dependencies
```bash
pip install -r requirements.txt
```
### 3) Configure environment variables
```bash
cp .env.example .env
```
Update your `.env` file with the required credentials:

- DATABASE_URL (e.g., postgresql+asyncpg://user:password@localhost:5432/darkatlas)

- OPENAI_API_KEY 

### 4) Run Database Migrations
```bash
cd src/model/db_Schema/darkatls
alembic upgrade head
```
### 5) Run the API
```bash
uvicorn src.main:app --reload --port 5000
```
Note:
- you need to be on the main path to run API :
    -  BUGUARD/
- API Documentation (Swagger): http://localhost:5000/docs
---

## Docker Setup
From the project root:
```bash
docker compose -f docker/docker-compose.yml up --build -d
```
---
## Core API Workflows

### 1. Asset Management (Upsert)
- **POST** `/api/v1/assets/import`
  - Uploads or updates assets in bulk. Automatically handles parent-child relationships and maintains the Asset Graph.

### 2. Natural Language Querying
- **POST** `/api/v1/query/query`
  - Takes a natural language question, converts it to SQL using an LLM, and retrieves relevant assets from the database.

### 3. Asset Retrieval
- **GET** `/api/v1/assets/{asset_id}`
  - Fetches individual asset details including its incoming and outgoing relationships.

### 4. Risk Scoring & Summarization
- **POST** `/api/v1/analyze/risk`
  - Performs a deep-dive security assessment for an asset or a group of assets. Produces a risk score and a concise summary, identifying critical issues such as expired certificates, sensitive exposed services, and end-of-life (EOL) technologies.
---
## Notes
- **Database Migrations**: If you modify the db_schema, ensure you generate new migrations using alembic revision --autogenerate before running upgrade head.

- **LLM Quota**: When testing the NLP Query endpoint, monitor your OpenAI API usage to avoid hitting rate limits.

- **Environment**: Ensure your .env file is properly configured before launching the application.