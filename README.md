# Eurostat nasa_10_nf_tr ETL Pipeline

## Overview

This repository contains an ETL pipeline that:

- extracts annual non-financial transaction data from the Eurostat `nasa_10_nf_tr` dataset, with specific filters (GEO = IE and TIME = 2021, 2022, 2023)
- transforms JSON-stat data into a normalized long table,
- loads the data into PostgreSQL using deterministic SHA-256 IDs, making inserts and updates idempotent.

## Requirements

- Python 3.10+
- Docker Desktop (recommended)
- Optional: PostgreSQL client for local inspection (or if not using Docker)

## Setup

### Option 1: Docker setup (recommended for quickest setup)

1. Build and start the services.

```bash
docker compose up --build
```

This will start:
- a PostgreSQL database container
- the ETL container, which runs Alembic migrations and then executes the pipeline

2. To stop everything later:

```bash
docker compose down
```

### Option 2: Local Python setup

1. Create and activate a virtual environment.

If using Python 3.14, please run the command below in PowerShell, as this version is currently experiencing issues with Bash in this project (as of 07/07/2026).

**Linux/macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```bash
pip install -r dependencies.txt
```

3. Configure your database connection.

Install PostgreSQL locally (see the official PostgreSQL download page), then create a database:

```sql
CREATE DATABASE nasa_etl;
```

Copy the example environment file:

```bash
cp .env.example .env
```

If you are using PowerShell on Windows, use:

```powershell
Copy-Item .env.example .env
```

Then update `DATABASE_URL` in your `.env` file.

4. Run Alembic migrations.

```bash
alembic upgrade head
```

5. Run the pipeline.

```bash
python runner.py
```

## Verifying the data

Once loaded, the data is stored in the `eurostat_nasa_nf_tr` table. To inspect it, you can use psql locally or connect to the running database container.

```sql
\dt
SELECT COUNT(*) FROM eurostat_nasa_nf_tr;
SELECT * FROM eurostat_nasa_nf_tr LIMIT 10;
```

## Notes

- The ETL orchestration is implemented in `runner.py`.
- Extraction, transformation, and load logic are separated into `src/etl_pipeline`.
- `dependencies.txt` pins the exact versions of the project's Python dependencies.
