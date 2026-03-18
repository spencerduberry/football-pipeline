{{ config(materialized="incremental") }}

with
    unnested_stats_temp as (
        select *, unnest(stats) as unnested_stats from {{ ref("bronze_fixtures") }}
    ),

    exploded_stats_arrays as (
        select
            *,
            unnested_stats.identifier,
            unnest(unnested_stats.a) as a_stats,
            unnest(unnested_stats.h) as h_stats
        from unnested_stats_temp
    ),

    home_stats as (
        select
            id as fixture_id,
            identifier as event_id,
            team_h as team_id,
            h_stats.element as player_id,
            h_stats.value as value
        from exploded_stats_arrays
    ),

    away_stats as (
        select
            id as fixture_id,
            identifier as event_id,
            team_a as team_id,
            a_stats.element as player_id,
            a_stats.value as value
        from exploded_stats_arrays
    ),

    all_stats as (
        select *
        from away_stats

        union all

        select *
        from home_stats
    )

select *
from all_stats
where player_id is not null and value is not null
