{{ config(materialized="incremental") }}

with
    staged as (
        select * from read_json("./data/000_raw/matches/*.json", filename = true)
    )

select *
from staged
