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

    return output


"""def bronze_stats_transform(config_path: str, table: BronzeSchema):
    io = IOWrapper()
    df = io.read(config_path, FileType.PARQUET)
    events = bronze_event_transform(config_path, table)
    bronze_stats = []

    for i, row in enumerate(df):
        fixture_id = df.iloc[i]['id']
        stats_list = df.iloc[i]['stats']
        for dict in stats_list:
            first_key = list(df.keys())[0]
            list_of_dicts = list(dict.keys())[first_key]
            for player in list_of_dicts:
                bronze_stats.append({"Event_ID": , "Team_ID": , "Fixture_ID": fixture_id, "Player_ID": player})

    return"""
