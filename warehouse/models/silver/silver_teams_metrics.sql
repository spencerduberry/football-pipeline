{{ config(materialized="incremental") }}

select
    id,
    draw,
    form,
    loss,
    played,
    points,
    position,
    strength,
    team_division,
    unavailable,
    win,
    strength_overall_home,
    strength_overall_away,
    strength_attack_home,
    strength_attack_away,
    strength_defence_home,
    strength_defence_away,
    pulse_id,
    filename,
    ingest_datetime,
    {{ dbt.current_timestamp() }} as version_datetime
from {{ ref("silver_base_teams") }}
