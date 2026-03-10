{{ config(materialized="incremental") }}

with
    unnested as (
        select unnest(element_types) as element_nested from {{ ref("bronze_statics") }}
    )

select
    element_nested.id as id,
    element_nested.plural_name as plural_name,
    element_nested.plural_name_short as plural_name_short,
    element_nested.singular_name as singular_name,
    element_nested.singular_name_short as singular_name_short,
    element_nested.squad_select as squad_select,
    element_nested.squad_min_select as squad_min_select,
    element_nested.squad_max_select as squad_max_select,
    element_nested.squad_min_play as squad_min_play,
    element_nested.squad_max_play as squad_max_play,
    element_nested.ui_shirt_specific as ui_shirt_specific,
    element_nested.sub_positions_locked as sub_positions_locked,
    element_nested.element_count as element_count
from unnested
