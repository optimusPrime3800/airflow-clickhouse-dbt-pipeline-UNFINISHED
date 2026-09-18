SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    SUM(oi.total_amount) AS order_amount,
    SUM(oi.quantity) AS total_items
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('stg_order_items') }} oi
ON o.order_id = oi.order_id
GROUP BY
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status