{% test no_null_dates(model) %}
    SELECT *
    FROM {{ model }}
    WHERE today IS NULL
{% endtest %}