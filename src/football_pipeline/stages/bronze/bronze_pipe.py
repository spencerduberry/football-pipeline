import pandas as pd

from src.football_pipeline.adapters.io_wrapper import FileType, IOWrapper
from src.football_pipeline.stages.bronze.data_structures import (
    BronzeSchema,
)

# prints raw fictures table
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
