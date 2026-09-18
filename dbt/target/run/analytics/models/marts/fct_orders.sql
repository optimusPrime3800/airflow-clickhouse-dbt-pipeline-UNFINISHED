
  
    
    
    
        
         


        insert into `raw_analytics`.`fct_orders__dbt_backup`
        ("order_id", "customer_id", "order_date", "status", "order_amount", "total_items")SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    SUM(oi.total_amount) AS order_amount,
    SUM(oi.quantity) AS total_items
FROM `raw_staging`.`stg_orders` o
JOIN `raw_staging`.`stg_order_items` oi
ON o.order_id = oi.order_id
GROUP BY
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status
  