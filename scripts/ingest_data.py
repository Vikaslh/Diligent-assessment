"""
Load synthetic CSV datasets into a SQLite database.
"""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "ecom.db"

TABLE_DEFINITIONS = {
    "customers": """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL
        );
    """,
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        );
    """,
    "orders": """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
    """,
    "order_items": """
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
    """,
    "reviews": """
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
    """,
}


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def cast_row(table: str, row: dict[str, str]) -> tuple:
    if table == "customers":
        return (
            int(row["customer_id"]),
            row["name"],
            row["email"],
            row["city"],
        )
    if table == "products":
        return (
            int(row["product_id"]),
            row["name"],
            row["category"],
            float(row["price"]),
        )
    if table == "orders":
        return (
            int(row["order_id"]),
            int(row["customer_id"]),
            row["order_date"],
            float(row["total_amount"]),
        )
    if table == "order_items":
        return (
            int(row["order_item_id"]),
            int(row["order_id"]),
            int(row["product_id"]),
            int(row["quantity"]),
        )
    if table == "reviews":
        return (
            int(row["review_id"]),
            int(row["customer_id"]),
            int(row["product_id"]),
            int(row["rating"]),
            row["comment"],
        )
    raise ValueError(f"Unhandled table: {table}")


def insert_rows(conn: sqlite3.Connection, table: str, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    placeholders = ",".join("?" for _ in rows[0])
    sql = f"INSERT OR REPLACE INTO {table} VALUES ({placeholders})"
    casted_rows = [cast_row(table, row) for row in rows]
    conn.executemany(sql, casted_rows)


def main() -> None:
    DB_PATH.unlink(missing_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        for ddl in TABLE_DEFINITIONS.values():
            conn.execute(ddl)

        mapping = {
            "customers": DATA_DIR / "customers.csv",
            "products": DATA_DIR / "products.csv",
            "orders": DATA_DIR / "orders.csv",
            "order_items": DATA_DIR / "order_items.csv",
            "reviews": DATA_DIR / "reviews.csv",
        }

        for table, csv_path in mapping.items():
            rows = load_csv_rows(csv_path)
            insert_rows(conn, table, rows)
            print(f"Loaded {len(rows)} rows into {table}")

        conn.commit()

    print(f"SQLite database created at {DB_PATH.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()

