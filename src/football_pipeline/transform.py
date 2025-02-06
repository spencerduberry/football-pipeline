"""Module for transform functions."""

import uuid
from datetime import datetime

import pandas as pd


def add_ingestion_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add uuids and timestamp into a copy of the inputted dataframe for identification.
    """
    updated_df = df.copy()
    updated_df["source_guid"] = [str(uuid.uuid4()) for _ in range(len(updated_df))]
    updated_df["batch_guid"] = str(uuid.uuid4())
    updated_df["ingestion_datetime"] = datetime.now()
    return updated_df
