{{ config(materialized="incremental") }}

with
    staged as (
        select *, {{ dbt.current_timestamp() }} AS ingest_datetime from read_json("./data/000_raw/statics/*.json", filename = true)
    )

select *
from staged
