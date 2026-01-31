{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

SELECT
    order_id,
    user_id,
    product_id,
    -- Mapping 'amount' to 'total_price' based on your \d output
    amount AS total_price,
    -- We'll cast order_date to timestamp to ensure dbt can handle it
    CAST(order_date AS TIMESTAMP) AS order_date
FROM {{ source('staging', 'orders') }}

{% if is_incremental() %}
  -- This filter ensures only new records are added
  WHERE CAST(order_date AS TIMESTAMP) > (SELECT MAX(order_date) FROM {{ this }})
{% endif %}