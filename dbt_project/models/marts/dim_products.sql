{{ config(materialized='table') }}

SELECT
    p.product_id,
    p.name,
    p.price,
    i.stock_quantity
FROM {{ source('staging', 'products') }} p
LEFT JOIN {{ source('staging', 'inventory') }} i ON p.product_id = i.product_id