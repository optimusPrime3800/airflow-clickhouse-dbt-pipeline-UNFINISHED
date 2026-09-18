
  
    
    
    
        
         


        insert into `raw_analytics`.`sales_daily__dbt_backup`
        ("sale_date", "orders_count", "revenue", "items_sold")SELECT
    toDate(order_date) AS sale_date,
    COUNT(*) AS orders_count,
    SUM(order_amount) AS revenue,
    SUM(total_items) AS items_sold
FROM `raw_analytics`.`fct_orders`
WHERE status = 'completed'
GROUP BY toDate(order_date)
ORDER BY toDate(order_date)
  