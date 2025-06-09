-- models/enriched_model.sql
SELECT
  a.today,
  a.message,
  b.country_name
FROM {{ ref('my_first_dbt_model') }} a
LEFT JOIN {{ ref('country_codes') }} b
  ON a.message = b.country_code
