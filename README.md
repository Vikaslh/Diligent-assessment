# Synthetic E-Commerce Data Pipeline

This project demonstrates an end-to-end flow for generating synthetic e-commerce data, loading it into SQLite, and running analytical queries.

## Data Generation
- `scripts/generate_data.py` creates five CSV files under `data/` with 20–30 records and consistent relationships (customers ↔ orders ↔ products ↔ reviews).
- Run `python3 scripts/generate_data.py` to regenerate the datasets.

## Database Ingestion
- `scripts/ingest_data.py` builds `data/ecom.db`, creates normalized tables, and loads the CSV data using `sqlite3`.
- Run `python3 scripts/ingest_data.py` after regenerating the data to refresh the database.

## Analytics Queries
- `scripts/query_data.py` joins customers, orders, order items, products, and reviews to produce sample insights:
  - Customer order counts with average review ratings.
  - Top products by total revenue.
  - Products with multiple reviews and average scores.
- Run `python3 scripts/query_data.py` to print query results to the console.

## Project Structure
- `data/` – Generated CSV datasets and the SQLite database.
- `scripts/` – Python utilities for data generation, ingestion, and querying.

Use relative paths when running scripts from the project root (e.g., `/Users/vikaslh/Desktop/whatsappmcp`).

# Diligent-assessment
