CREATE DATABASE IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.customers
(
    customer_id Int64,
    name String,
    email String,
    city String,
    registration_date DateTime64(3)
)
ENGINE = MergeTree()
ORDER BY customer_id;


CREATE TABLE IF NOT EXISTS raw.products
(
    product_id Int64,
    product_name String,
    category String,
    price Float64
)
ENGINE = MergeTree()
ORDER BY product_id;


CREATE TABLE IF NOT EXISTS raw.orders
(
    order_id String,
    customer_id Int64,
    order_date DateTime64(3),
    status String
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(order_date)
ORDER BY (order_date, order_id);


CREATE TABLE IF NOT EXISTS raw.order_items
(
    order_item_id String,
    order_id String,
    product_id Int64,
    quantity Int8,
    price Float64,
    total_amount Float64
)
ENGINE = MergeTree()
ORDER BY order_id;