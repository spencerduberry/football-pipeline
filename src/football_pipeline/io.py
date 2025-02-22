import json
import os
import urllib.request

import pandas as pd
import yaml


def read_yaml(path: str) -> dict:
    """
    Loads a YAML file from the given path and returns its contents as a dict.

    Args:
        path: the path to the YAML file.

    Returns:
        A dict representation of the YAML file or an empty dict on error.
    """
    try:
        abs_path = os.path.abspath(path)

        with open(path, "r") as file:
            data = yaml.safe_load(file)

        if data is None:
            print(
                f"Warning: {abs_path} is empty or invalid YAML. Returning empty dict."
            )
            return {}

        return data

    except Exception as e:
        print(f"Error loading YAML from {path}: {e}")
        return {}


def write_to_parquet(df: pd.DataFrame, path: str) -> bool:
    """
    Takes a pandas dataframe, converts to parquet format and saves it in the specified path.
    """
    if not path.endswith(".parquet"):
        print(
            f"{path} is an invalid file name. Please specify a .parquet file extension"
        )
        return False

    try:
        df.to_parquet(path)
        return True
    except Exception as e:
        print(f"{path} is not a valid path: {e}")
        return False


def extract_stats(match: dict):
    stats_dict = {
        stat["identifier"]: (len(stat["a"]), len(stat["h"])) for stat in match["stats"]
    }
    match.update(stats_dict)
    return match


def extract_data(url: str, keys=None):
    with urllib.request.urlopen(url) as response:
        data = json.load(response)

    if isinstance(data, dict):
        data_dfs = {}

        for key in keys:
            data_dfs[key] = pd.DataFrame(data[key])

        return data_dfs

    elif isinstance(data, list):
        unpacked_data = [extract_stats(match) for match in data]
        data_dfs = pd.DataFrame(unpacked_data)
        stat_cols = [stat["identifier"] for stat in data[0]["stats"]]
        for stat in stat_cols:
            data_dfs.rename(
                columns={stat: f"{stat}_a", f"{stat}_h": f"{stat}_h"}, inplace=True
            )

        data_dfs.drop(columns=["stats"])

        return data_dfs
