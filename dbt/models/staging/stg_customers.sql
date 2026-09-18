SELECT
    customer_id,
    name,
    email,
    city,
    registration_date
FROM {{ source('raw', 'customers') }}
