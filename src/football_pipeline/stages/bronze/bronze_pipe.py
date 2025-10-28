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


# outputs a dict of events (might be able to use for player player match stats)
def bronze_event_transform(config_path: str, table: BronzeSchema):
    io = IOWrapper()
    df = io.read(config_path, FileType.PARQUET)
    events = {}
    stats_list = df.iloc[0]["stats"]

    for i, event in enumerate(stats_list):
        all_values = event.values()
        last_value = list(all_values)[-1]
        last_val_var = last_value
        events[i + 1] = last_val_var

    output = pd.DataFrame.from_dict(events, orient="index")
    output = output.reset_index().rename(columns={"index": "ID"})
    output = output.rename(columns={"ID": "Event_ID", 0: "Event"})

    return output


def bronze_stats_transform(config_path: str, table: BronzeSchema):
    io = IOWrapper()
    df = io.read(config_path, FileType.PARQUET)
    events = bronze_event_transform(config_path, table)
    bronze_stats = []

    for i, row in enumerate(df):
        fixture_id = df.iloc[i]["id"]
        stats_list = df.iloc[i]["stats"]
        for event in stats_list:
            away_key = list(event.keys())[0]
            home_key = list(event.keys())[1]
            event_name = list(event.values())[2]
            event_id = events.loc[events["Event"] == event_name, "Event_ID"].iloc[0]
            team_mapping = {
                away_key: "team_a",
                home_key: "team_h",
            }

            for stat_key, team_col in team_mapping.items():
                for player in event[stat_key]:
                    team_id = df.iloc[i][team_col]
                    player_id = list(player.values())[0]
                    bronze_stats.append(
                        {
                            "Event_ID": event_id,
                            "Team_ID": team_id,
                            "Fixture_ID": fixture_id,
                            "Player_ID": player_id,
                        }
                    )

    output = pd.DataFrame(bronze_stats)

    return output
