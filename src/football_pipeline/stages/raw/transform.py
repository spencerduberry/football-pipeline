import re
import uuid
from datetime import datetime

import pandas as pd


def convert_data_to_df(
    data: dict | list, url_path: str, keys: list = None
) -> dict[str, pd.DataFrame]:
    keys = keys or []
    dfs, fails = {}, []

    if isinstance(data, dict):
        for k, v in data.items():
            if k in keys and isinstance(v, list):
                try:
                    dfs[k] = pd.DataFrame(v)
                except Exception as e:
                    fails.append({"err": e, "key": k})

    if isinstance(data, list):
        try:
            sanitized_key = sanitize_url(url_path)
            dfs[sanitized_key] = pd.DataFrame(data)
        except Exception as e:
            fails.append({"err": e, "key": sanitized_key})

    if fails:
        return fails
    return dfs


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


def sanitize_url(url: str) -> str:
    """Creates a short, valid dictionary key from a URL."""
    return re.sub(r"https?://|www\.|[^a-zA-Z0-9]", "_", url).strip("_")
