import pandas as pd
import numpy as np
from pathlib import Path
import uuid
import time


SEED = 42

N_CUSTOMERS = 100_000
N_PRODUCTS = 10_000
N_ORDERS = 1_000_000

OUTPUT_DIR = Path("/opt/airflow/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(SEED)




def generate_uuid(n):
    """
    Быстро создаёт n UUID.
    """
    return [str(uuid.uuid4()) for _ in range(n)]



def generate_customers(n):

    print(f"Generating {n:,} customers...")

    cities = np.array([
        "Москва",
        "Санкт-Петербург",
        "Казань",
        "Екатеринбург",
        "Новосибирск",
        "Нижний Новгород",
        "Самара",
        "Уфа",
        "Пермь",
        "Ростов-на-Дону"
    ])

    customer_ids = np.arange(
        1,
        n + 1,
        dtype=np.int64
    )

    names = np.array([
        f"Customer_{i}"
        for i in customer_ids
    ])

    emails = np.array([
        f"customer_{i}@example.com"
        for i in customer_ids
    ])

    city = rng.choice(
        cities,
        size=n
    )

    start_date = np.datetime64("2023-01-01")
    end_date = np.datetime64("2026-08-01")

    days = (
        end_date - start_date
    ).astype("timedelta64[D]").astype(int)

    registration_date = (
        start_date
        + rng.integers(
            0,
            days,
            size=n
        ).astype("timedelta64[D]")
    )

    df = pd.DataFrame({
        "customer_id": customer_ids,
        "name": names,
        "email": emails,
        "city": city,
        "registration_date": registration_date
    })

    return df




def generate_products(n):

    print(f"Generating {n:,} products...")

    categories = np.array([
        "Electronics",
        "Home",
        "Clothing",
        "Sports",
        "Books"
    ])

    product_names = np.array([
        "Smartphone",
        "Laptop",
        "Tablet",
        "Headphones",
        "Monitor",
        "Vacuum Cleaner",
        "Kettle",
        "Microwave",
        "Coffee Machine",
        "Blender",
        "T-Shirt",
        "Jeans",
        "Jacket",
        "Shoes",
        "Sweater",
        "Bicycle",
        "Dumbbells",
        "Football",
        "Tennis Racket",
        "Backpack",
        "Programming Book",
        "Math Book",
        "Novel",
        "History Book",
        "Science Book"
    ])

    product_ids = np.arange(
        1,
        n + 1,
        dtype=np.int64
    )

    category = rng.choice(
        categories,
        size=n
    )

    product_name = rng.choice(
        product_names,
        size=n
    )

    # Lognormal позволяет получить распределение цен,
    # похожее на реальный e-commerce
    price = np.round(
        rng.lognormal(
            mean=7.5,
            sigma=1.0,
            size=n
        ),
        2
    )


    price = np.clip(
        price,
        100,
        500_000
    )

    df = pd.DataFrame({
        "product_id": product_ids,
        "product_name": product_name,
        "category": category,
        "price": price
    })

    return df



def generate_orders(
    n_orders,
    n_customers
):

    print(f"Generating {n_orders:,} orders...")

    order_ids = np.array(
        generate_uuid(n_orders)
    )

    customer_ids = rng.integers(
        1,
        n_customers + 1,
        size=n_orders,
        dtype=np.int64
    )



    start_date = np.datetime64(
        "2025-01-01T00:00:00"
    )

    end_date = np.datetime64(
        "2026-08-01T00:00:00"
    )

    seconds = (
        end_date - start_date
    ).astype("timedelta64[s]").astype(np.int64)

    random_seconds = rng.integers(
        0,
        seconds,
        size=n_orders
    )

    order_date = (
        start_date
        + random_seconds.astype(
            "timedelta64[s]"
        )
    )

    statuses = np.array([
        "completed",
        "pending",
        "cancelled",
        "returned"
    ])

    status = rng.choice(
        statuses,
        size=n_orders,
        p=[
            0.70,
            0.10,
            0.10,
            0.10
        ]
    )

    df = pd.DataFrame({
        "order_id": order_ids,
        "customer_id": customer_ids,
        "order_date": order_date,
        "status": status
    })

    return df

def generate_order_items(orders,products):

    print("Generating order items...")

    n_orders = len(orders)

    items_per_order = rng.choice(
        np.array([1, 2, 3, 4, 5]),
        size=n_orders,
        p=[
            0.25,
            0.30,
            0.25,
            0.15,
            0.05
        ]
    )

    total_items = items_per_order.sum()

    print(
        f"Generating approximately "
        f"{total_items:,} order items..."
    )

    order_ids = np.repeat(
        orders["order_id"].values,
        items_per_order
    )

    product_ids = rng.integers(
        1,
        len(products) + 1,
        size=total_items,
        dtype=np.int64
    )

    quantity = rng.integers(
        1,
        6,
        size=total_items,
        dtype=np.int8
    )


    #получаем цену товара через NumPy-массив,


    prices = products["price"].values

    price = prices[
        product_ids - 1
    ]

    total_amount = np.round(
        quantity * price,
        2
    )

    order_item_ids = np.array(
        generate_uuid(total_items)
    )

    df = pd.DataFrame({
        "order_item_id": order_item_ids,
        "order_id": order_ids,
        "product_id": product_ids,
        "quantity": quantity,
        "price": price,
        "total_amount": total_amount
    })

    return df


def save_data(
    customers,
    products,
    orders,
    order_items
):

    print("\nSaving Parquet files...")

    customers.to_parquet(
        OUTPUT_DIR / "customers.parquet",
        index=False
    )

    print("customers.parquet saved")

    products.to_parquet(
        OUTPUT_DIR / "products.parquet",
        index=False
    )

    print("products.parquet  saved")

    orders.to_parquet(
        OUTPUT_DIR / "orders.parquet",
        index=False
    )

    print("orders.parquet saved")

    order_items.to_parquet(
        OUTPUT_DIR / "order_items.parquet",
        index=False
    )

    print("order_items.parquet saved")



def main():

    start_time = time.time()

    
    print("SYNTHETIC E-COMMERCE DATA GENERATOR")


    customers = generate_customers(
        N_CUSTOMERS
    )

    print(
        f"Customers: {len(customers):,}"
    )

    products = generate_products(
        N_PRODUCTS
    )

    print(
        f"Products: {len(products):,}"
    )

    orders = generate_orders(
        N_ORDERS,
        N_CUSTOMERS
    )

    print(
        f"Orders: {len(orders):,}"
    )

    order_items = generate_order_items(
        orders,
        products
    )

    print(
        f"Order items: {len(order_items):,}"
    )

    save_data(
        customers,
        products,
        orders,
        order_items
    )

    elapsed = time.time() - start_time

    print("\n" + "=" * 60)
    print("FINISHED")
    print("=" * 60)

    print(
        f"Customers:   {len(customers):,}"
    )

    print(
        f"Products:    {len(products):,}"
    )

    print(
        f"Orders:      {len(orders):,}"
    )

    print(
        f"Order items: {len(order_items):,}"
    )

    print(
        f"Time:        {elapsed:.2f} seconds"
    )

    print(
        f"Output:      {OUTPUT_DIR.absolute()}"
    )


if __name__ == "__main__":
    main()