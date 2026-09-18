

  create or replace view `raw_staging`.`stg_orders` 
  
    
  
  
    
    
  as (
    SELECT
    order_id,
    customer_id,
    order_date,
    status
FROM `raw`.`orders`
    
  )
      
      
                    -- end_of_sql
                    
                    