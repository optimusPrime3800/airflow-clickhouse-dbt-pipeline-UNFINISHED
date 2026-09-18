

  create or replace view `raw_staging`.`stg_products` 
  
    
  
  
    
    
  as (
    SELECT
    product_id,
    product_name,
    category,
    price
FROM `raw`.`products`
    
  )
      
      
                    -- end_of_sql
                    
                    