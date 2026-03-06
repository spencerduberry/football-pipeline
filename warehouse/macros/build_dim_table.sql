{% macro build_dim_hash_id_multiple_columns(table_ref, col_names) %}

    select
        hash(
            {% for col in col_names %}
                lower(
                    trim(cast({{ col }} as text))
                ) {{ " || '_' || " if not loop.last }}
            {% endfor %}
        ) as id,
        {% for col in col_names %}
            {{ col }} as {{ col }} {% if not loop.last %}, {% endif %}
        {% endfor %}
    from
        (
            select distinct
                {% for col in col_names %}
                    , {{ col }} as {{ col }} {% if not loop.last %}, {% endif %}
                {% endfor %}
            from {{ table_ref }}
        ) as distinct_values
{% endmacro %}
