import pandas as pd

from src.football_pipeline.adapters.io_wrapper import FileType, IOWrapper
from src.football_pipeline.stages.bronze.data_structures import (
    BronzeSchema,
)

# prints raw fixtures table
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)
io = IOWrapper()
df = io.read(
    r"C:\Users\spenc\github\football-pipeline\data\00_raw\fantasy_premierleague_com_api_fixtures\20251007_191523.parquet",
    FileType.PARQUET,
)
df


# works on player, teams, fixtures tables
def generic_bronze_transform(config_path: str, table: BronzeSchema):
    io = IOWrapper()
    df = io.read(config_path, FileType.PARQUET)
    valid, invalid = [], []
    rows = df.to_dict("records")

    for row in rows:
        try:
            valid_row = table.from_dict(row)
            valid.append(valid_row)

        except ValueError as e:
            row["error"] = e.args
            invalid.append(row)
    output = pd.DataFrame([row.to_dict() for row in valid])

    return output


def bronze_stats_event_transform(df: pd.DataFrame) -> pd.DataFrame:
    raw_columns = df[["id", "team_h", "team_a", "stats"]]
    exploded_columns = raw_columns.explode("stats").reset_index(drop=True)
    serialised_columns = (
        exploded_columns["stats"].apply(pd.Series).reset_index(drop=True)
    )
    concat_df = pd.concat([exploded_columns, serialised_columns], axis=1)
    a_table = concat_df.explode("a")
    h_table = concat_df.explode("h")

    def transform_stats_list(stats_df: pd.DataFrame, team_columns: list):
        team, players = team_columns
        stats = (
            stats_df[["id", "identifier"] + team_columns]
            .dropna()
            .reset_index(drop=True)
        )
        unpacked_players = stats[players].apply(pd.Series).reset_index(drop=True)
        output = pd.concat([stats, unpacked_players], axis=1)
        output = output.drop(columns=players).rename(
            columns={
                "id": "fixture_id",
                team: "team_id",
                "identifier": "event_id",
                "element": "player_id",
            }
        )

        return output

    final_a_table = transform_stats_list(a_table, ["team_a", "a"])
    final_h_table = transform_stats_list(h_table, ["team_h", "h"])
    output = pd.concat([final_a_table, final_h_table])
    event_map = {
        idx: name for idx, name in enumerate(sorted(output["event_id"].unique()))
    }
    event_table = pd.DataFrame(event_map.items(), columns=["event_index", "event_id"])

    return output, event_table
