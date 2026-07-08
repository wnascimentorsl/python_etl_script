# CRITIQUE.md

## Overview
This is a simple structured pipeline project that aims to extract, transform and load a specific dataset from Eurostat website/API (nasa_10_nf_tr) as a development test.

---

## Architectural Choices
- I did some research about the extraction methods available in the API documentation from the user guides (https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-introduction) and found the option to use JSON-stat data. With some research, I found a Python library that deals with that with ease, which led me in that direction. Also, JSON is commonly parsed in a lot of languages.

Firstly I created a single-file ETL script, but then I thought to sharpen it a bit and make each step a new file so readability and future refactoring would be easier.

I looked for libraries that would assist in the coding process of different steps as they were necessary:
- **Alembic / SQLAlchemy:** For migrations, as other languages that I worked with use migrations. This project could simply use pure SQL in a .txt file, but to make it easier for other people using this project, I chose Alembic.
- **pyjstat / Pandas:** To deal with JSON-stat data along with Pandas, which was used for processing the datasets.
- **Psycopg2:** Used to manage the PostgreSQL connection and execute queries.
- **Pytest:** Used as a testing framework

---

## AI Tools
- Used AI to accelerate the initial project setup and environment configuration.
- Used AI to summarize Eurostat API documentation while verifying implementation details manually.
- Used AI for boilerplate generation (dependency list, Docker setup, etc.).

---

## Architecture Modifications
- Schedule recurring pipeline executions using Cron (or a workflow orchestrator). For larger deployments, I would consider an orchestration tool such as Prefect to manage scheduling, retries, and monitoring. I would have to study more about it first, but I would probably go for that idea.
- The same structure could be applied but with configurations for different URLs, different tables, params, etc.
- I'd create tables for dimension references so that it occupies less storage. For example, mapping GEO -> IE to an ID takes less space than writing the full GEO string many times (Star Schema normalization).
- The Eurostat API can't handle big API requests, so there could an implementation to fetch the request in smaller query chunks. Or the extract method could be refactored to use the full extracted TSV file option. For this development I chose some filters that could be handled by the API.
- Increase unit test coverage. Add end-to-end tests validating the complete ETL workflow.
- Refactor the modules even more then just ETL files, to isolate responsibilities and improve scalability. For example, we could decouple the raw SQL execution from the Load class into its own database layer.
