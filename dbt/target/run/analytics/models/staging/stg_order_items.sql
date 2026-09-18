

  create or replace view `raw_staging`.`stg_order_items` 
  
    
  
  
    
    
  as (
    SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    price,
    total_amount
FROM `raw`.`order_items`
    
  )
      
      
                    -- end_of_sql
                    
                    