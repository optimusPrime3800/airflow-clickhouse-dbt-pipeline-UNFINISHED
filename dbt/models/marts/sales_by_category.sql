SELECT
    p.category,
    SUM(oi.total_amount) AS revenue,
    SUM(oi.quantity) AS items_sold,
    COUNT(DISTINCT o.order_id) AS orders_count
FROM {{ ref('stg_order_items') }} oi
JOIN {{ ref('stg_orders') }} o
    ON oi.order_id = o.order_id
JOIN {{ ref('stg_products') }} p
    ON oi.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC