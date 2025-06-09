{% macro summarize_by_country(table) %}
    SELECT
        country,
        COUNT(*) AS record_count
    FROM {{ table }}
    GROUP BY country
    ORDER BY record_count DESC
{% endmacro %}