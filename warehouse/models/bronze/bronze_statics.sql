{{ config(materialized="incremental") }}

with
    staged as (
        select *
        from
            read_json(
                "./data/000_raw/statics/*.json", filename = true, union_by_name = true
            )
    )

select *
from staged
