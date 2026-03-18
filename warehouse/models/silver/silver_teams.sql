{{ config(materialized="incremental") }}

with
    unnested_teams as (select unnest(teams) as teams from {{ ref("bronze_statics") }}),

    exploded_again as (select teams.* from unnested_teams)

select *
from exploded_again
