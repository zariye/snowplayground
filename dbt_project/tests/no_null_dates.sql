-- tests/no_null_dates.sql

SELECT *
FROM {{ ref('my_first_dbt_model') }}
WHERE today IS NULL
