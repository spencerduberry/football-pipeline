import os

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
    except Exception as e:
        print(f"{path} is not a valid path: {e}")
        return False

    return True
