# Eurostat nasa_10_nf_tr ETL Pipeline

## Overview

This repository contains an ETL pipeline that:

- extracts annual non-financial transaction data from the Eurostat `nasa_10_nf_tr` dataset, with specific filters.
- transforms JSON-stat data into a normalized long table,
- loads the results into PostgreSQL with deterministic SHA-256 IDs
so inserting and updating becomes easier.

## Requirements

- Python 3.10+
- PostgreSQL 14+

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows PowerShell
# or
source .venv/bin/activate       # bash / Linux
```

2. Install dependencies.

```bash
pip install -r dependencies.txt
```

3. Configure your database connection.

- Update `DATABASE_URL` in your .env file

4. Run Alembic migrations.

```bash
alembic upgrade head
```

5. Run the pipeline.

```bash
python runner.py
```

## Notes

- The ETL orchestration is implemented in `runner.py`.
- Extraction, transformation, and load logic are separated into `src/etl_pipeline`.
- `dependencies.txt` pins the exact package versions of the libs used in this environment.
