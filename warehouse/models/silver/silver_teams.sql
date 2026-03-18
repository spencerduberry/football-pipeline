{{ config(materialized="incremental") }}

with
    unnested_teams as (
        select unnest(teams) as teams, filename from {{ ref("bronze_statics") }}
    ),

    exploded_again as (select teams.*, filename from unnested_teams)

select *
from exploded_again
