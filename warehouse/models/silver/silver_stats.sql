{{ config (materialized="incremental") }}

with
    joined as (
        select
            stats.fixture_id,
            events.id as event_id,
            stats.team_id,
            stats.player_id,
            stats.value,
            stats.filename
        from {{ ref("bronze_stats") }} as stats
        inner join {{ ref("bronze_events") }} as events on stats.event_id = events.event
    )

select *
from joined
