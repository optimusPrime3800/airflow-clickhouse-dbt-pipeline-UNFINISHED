SELECT
    toDate(order_date) AS sale_date,
    COUNT(*) AS orders_count,
    SUM(order_amount) AS revenue,
    SUM(total_items) AS items_sold
FROM {{ ref('fct_orders') }}
WHERE status = 'completed'
GROUP BY toDate(order_date)
ORDER BY toDate(order_date)