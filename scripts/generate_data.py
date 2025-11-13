"""
Generate synthetic CSV datasets for a small e-commerce system.
"""

from __future__ import annotations

import csv
import random
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)

CITIES = [
    "New York",
    "San Francisco",
    "Chicago",
    "Austin",
    "Seattle",
    "Boston",
]

FIRST_NAMES = [
    "Alex",
    "Jordan",
    "Taylor",
    "Riley",
    "Casey",
    "Morgan",
    "Jamie",
    "Avery",
    "Reese",
    "Skyler",
    "Parker",
    "Rowan",
    "Hayden",
    "Quinn",
    "Elliot",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Jackson",
    "Martinez",
]

PRODUCT_CATEGORIES = {
    "Electronics": [
        ("Wireless Earbuds", 79.99),
        ("Smartphone Case", 19.99),
        ("Bluetooth Speaker", 49.99),
        ("Portable Charger", 39.99),
        ("Smartwatch", 129.99),
    ],
    "Home": [
        ("Ceramic Mug Set", 24.99),
        ("Throw Blanket", 34.99),
        ("LED Desk Lamp", 45.50),
        ("Aromatherapy Diffuser", 29.99),
        ("Indoor Plant Kit", 27.49),
    ],
    "Fitness": [
        ("Yoga Mat", 32.00),
        ("Resistance Bands", 21.50),
        ("Insulated Water Bottle", 25.00),
        ("Foam Roller", 28.75),
        ("Adjustable Dumbbell", 199.00),
    ],
    "Books": [
        ("Productivity Planner", 18.95),
        ("Design Thinking Guide", 22.00),
        ("Modern Cooking", 30.00),
        ("Mindfulness Workbook", 16.50),
        ("Startup Playbook", 26.00),
    ],
}

COMMENTS = [
    "Loved it! Highly recommend.",
    "Works as expected. Would buy again.",
    "Quality could be better, but good value overall.",
    "Fantastic customer service and fast shipping.",
    "Not satisfied with the durability.",
    "Exceeded my expectations!",
    "Makes daily life so much easier.",
    "Gifted it to a friend and they loved it.",
    "Helpful addition to my routine.",
    "Packaging was damaged, but product is fine.",
]


def generate_customers(count: int = 24) -> list[dict[str, str]]:
    customers = []
    for idx in range(count):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        name = f"{first} {last}"
        email = f"{first.lower()}.{last.lower()}@example.com"
        city = random.choice(CITIES)
        customers.append(
            {
                "customer_id": idx + 1,
                "name": name,
                "email": email,
                "city": city,
            }
        )
    return customers


def generate_products() -> list[dict[str, str]]:
    products = []
    product_id = 1
    for category, items in PRODUCT_CATEGORIES.items():
        for name, price in items:
            products.append(
                {
                    "product_id": product_id,
                    "name": name,
                    "category": category,
                    "price": f"{price:.2f}",
                }
            )
            product_id += 1
    return products


def daterange(days_back: int = 120) -> datetime:
    base_date = datetime.now()
    delta_days = random.randint(0, days_back)
    time_offset = timedelta(days=delta_days, hours=random.randint(0, 23))
    return base_date - time_offset


def generate_orders(
    customers: list[dict[str, str]],
    products: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    orders = []
    order_items = []

    order_id = 1
    order_item_id = 1
    product_lookup = {int(p["product_id"]): float(p["price"]) for p in products}

    for customer in customers:
        customer_orders = random.randint(0, 3)
        for _ in range(customer_orders):
            order_date = daterange()
            item_count = random.randint(1, 4)
            items = []
            subtotal = 0.0

            chosen_products = random.sample(products, item_count)
            for product in chosen_products:
                pid = int(product["product_id"])
                quantity = random.randint(1, 3)
                line_total = product_lookup[pid] * quantity
                subtotal += line_total
                items.append(
                    {
                        "order_item_id": order_item_id,
                        "order_id": order_id,
                        "product_id": pid,
                        "quantity": quantity,
                    }
                )
                order_item_id += 1

            orders.append(
                {
                    "order_id": order_id,
                    "customer_id": int(customer["customer_id"]),
                    "order_date": order_date.strftime("%Y-%m-%d"),
                    "total_amount": f"{subtotal:.2f}",
                }
            )
            order_items.extend(items)
            order_id += 1

    return orders, order_items


def generate_reviews(
    customers: list[dict[str, str]],
    products: list[dict[str, str]],
) -> list[dict[str, str]]:
    reviews = []
    review_id = 1

    customer_product_pairs = set()
    for _ in range(28):
        customer = random.choice(customers)
        product = random.choice(products)
        key = (customer["customer_id"], product["product_id"])
        if key in customer_product_pairs:
            continue
        customer_product_pairs.add(key)
        rating = random.randint(1, 5)
        comment = random.choice(COMMENTS)
        reviews.append(
            {
                "review_id": review_id,
                "customer_id": customer["customer_id"],
                "product_id": product["product_id"],
                "rating": rating,
                "comment": comment,
            }
        )
        review_id += 1
    return reviews


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    customers = generate_customers()
    products = generate_products()
    orders, order_items = generate_orders(customers, products)
    reviews = generate_reviews(customers, products)

    write_csv(
        DATA_DIR / "customers.csv",
        ["customer_id", "name", "email", "city"],
        customers,
    )
    write_csv(
        DATA_DIR / "products.csv",
        ["product_id", "name", "category", "price"],
        products,
    )
    write_csv(
        DATA_DIR / "orders.csv",
        ["order_id", "customer_id", "order_date", "total_amount"],
        orders,
    )
    write_csv(
        DATA_DIR / "order_items.csv",
        ["order_item_id", "order_id", "product_id", "quantity"],
        order_items,
    )
    write_csv(
        DATA_DIR / "reviews.csv",
        ["review_id", "customer_id", "product_id", "rating", "comment"],
        reviews,
    )

    totals_by_customer = defaultdict(float)
    for order in orders:
        totals_by_customer[order["customer_id"]] += float(order["total_amount"])

    print(f"Generated {len(customers)} customers")
    print(f"Generated {len(products)} products")
    print(f"Generated {len(orders)} orders")
    print(f"Generated {len(order_items)} order items")
    print(f"Generated {len(reviews)} reviews")
    top_customer = max(totals_by_customer, key=totals_by_customer.get, default=None)
    if top_customer:
        print(f"Top customer by spend: {top_customer} (${totals_by_customer[top_customer]:.2f})")


if __name__ == "__main__":
    main()

