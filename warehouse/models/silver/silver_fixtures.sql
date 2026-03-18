{{ config (materialized="incremental") }}

select {{ dbt_utils.star(from=ref("bronze_fixtures"), except=["stats"]) }}
from {{ ref("bronze_fixtures") }}
where finished = true
