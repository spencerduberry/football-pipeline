"""Module for transform functions."""

import uuid
from datetime import datetime

import pandas as pd

from football_pipeline.logger import log_func


@log_func
def add_ingestion_columns(
    df: pd.DataFrame, batch_guid: str, date_time: datetime
) -> pd.DataFrame:
    """
    Add uuids and timestamp into a copy of the inputted dataframe for identification.
    """
    updated_df = df.copy()
    updated_df["source_guid"] = [str(uuid.uuid4()) for _ in range(len(updated_df))]
    updated_df["batch_guid"] = batch_guid
    updated_df["ingestion_datetime"] = date_time
    return updated_df
