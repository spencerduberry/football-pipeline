{{ config(materialized="incremental") }}

with staged as (select * from {{ ref("bronze_fixtures") }})
