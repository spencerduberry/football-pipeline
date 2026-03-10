{{ config (materialized="incremental") }}

select distinct hash(lower(trim(cast(event as text)))) as id, event

from
    (
        select distinct event_id as event from {{ ref("bronze_stats") }}
    ) as distinct_values
