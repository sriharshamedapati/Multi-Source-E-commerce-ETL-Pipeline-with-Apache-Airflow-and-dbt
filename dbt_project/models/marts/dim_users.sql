{{ config(materialized='table') }}

SELECT
    user_id,
    email,
    created_at
FROM {{ source('staging', 'users') }}