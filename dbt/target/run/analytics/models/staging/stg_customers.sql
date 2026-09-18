

  create or replace view `raw_staging`.`stg_customers` 
  
    
  
  
    
    
  as (
    SELECT
    customer_id,
    name,
    email,
    city,
    registration_date
FROM `raw`.`customers`
    
  )
      
      
                    -- end_of_sql
                    
                    