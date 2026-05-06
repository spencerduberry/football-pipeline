{{ config(materialized="incremental", unique_key="id") }}

select code, id, name, short_name, filename, ingest_datetime
from {{ ref("silver_base_teams") }}
