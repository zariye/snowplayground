SELECT
  today,
  UPPER(message) AS upper_message
FROM {{ ref('my_first_dbt_model') }}


