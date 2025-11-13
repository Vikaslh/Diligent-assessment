"""
Run sample analytical queries against the synthetic e-commerce database.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Sequence


ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "data" / "ecom.db"


def connect(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found at {db_path}")
    return sqlite3.connect(db_path)


def print_results(title: str, headers: Sequence[str], rows: Iterable[Sequence[object]]) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    print(" | ".join(headers))
    print("-" * (len(" | ".join(headers))))
    for row in rows:
        print(" | ".join(str(item) for item in row))


def customer_order_summary(conn: sqlite3.Connection) -> None:
    query = """
        SELECT
            c.name AS customer_name,
            COUNT(DISTINCT o.order_id) AS total_orders,
            COALESCE(ROUND(AVG(r.rating), 2), 'N/A') AS average_rating
        FROM customers c
        LEFT JOIN orders o ON o.customer_id = c.customer_id
        LEFT JOIN reviews r ON r.customer_id = c.customer_id
        GROUP BY c.customer_id
        ORDER BY total_orders DESC, c.name ASC;
    """
    rows = conn.execute(query).fetchall()
    print_results(
        "Customer Orders and Ratings",
        ("Customer", "Total Orders", "Average Rating"),
        rows,
    )


def top_products_by_revenue(conn: sqlite3.Connection) -> None:
    query = """
        SELECT
            p.name,
            p.category,
            SUM(oi.quantity) AS units_sold,
            ROUND(SUM(oi.quantity * p.price), 2) AS revenue
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY p.product_id
        ORDER BY revenue DESC
        LIMIT 10;
    """
    rows = conn.execute(query).fetchall()
    print_results(
        "Top Products by Revenue",
        ("Product", "Category", "Units Sold", "Revenue ($)"),
        rows,
    )


def average_rating_by_product(conn: sqlite3.Connection) -> None:
    query = """
        SELECT
            p.name,
            COUNT(r.review_id) AS review_count,
            ROUND(AVG(r.rating), 2) AS avg_rating
        FROM products p
        JOIN reviews r ON r.product_id = p.product_id
        GROUP BY p.product_id
        HAVING review_count >= 2
        ORDER BY avg_rating DESC, review_count DESC;
    """
    rows = conn.execute(query).fetchall()
    print_results(
        "Products with Multiple Reviews",
        ("Product", "Review Count", "Average Rating"),
        rows,
    )


def main() -> None:
    with connect(DB_PATH) as conn:
        customer_order_summary(conn)
        top_products_by_revenue(conn)
        average_rating_by_product(conn)


if __name__ == "__main__":
    main()

