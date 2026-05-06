{% test has_expected_columns(model, column_names) %}

    with
        expected_columns as (

            {% for col in column_names %}
                select lower('{{ col }}') as column_name
                {% if not loop.last %}
                    union all
                {% endif %}
            {% endfor %}

        ),

        actual_columns as (

            select lower(column_name) as column_name
            from information_schema.columns
            where
                lower(table_name) = lower('{{ model.identifier }}')
                and lower(table_schema) = lower('{{ model.schema }}')

        )

    select expected_columns.column_name
    from expected_columns
    left join
        actual_columns on expected_columns.column_name = actual_columns.column_name
    where actual_columns.column_name is null

{% endtest %}
