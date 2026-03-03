{{ config (materialized="incremental") }}

select hash(lower(trim(cast(event_id as text)))) as id, event_id as event_id

from
    (
        select distinct event_id as event_id from {{ ref("bronze_stats") }}
    ) as distinct_values
