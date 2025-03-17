import json
import urllib.request

import pandas as pd
import yaml

from football_pipeline.logger import log_func
from football_pipeline.utils import sanitize_url


@log_func
def read_yaml(path: str) -> dict:
    """
    Loads a YAML file from the given path and returns its contents as a dict.

    Args:
        path: the path to the YAML file.

    Returns:
        A dict representation of the YAML file or an empty dict on error.
    """
    try:
        with open(path, "r") as file:
            data = yaml.safe_load(file)

        if data is None:
            print(f"Warning: {path} is empty or invalid YAML. Returning empty dict.")
            return {}

        return data

    except Exception as e:
        print(f"Error loading YAML from {path}: {e}")
        return {}


@log_func
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


@log_func
def extract_data(url_path: str, keys: list = None) -> dict[str, pd.DataFrame]:
    """
    Takes a URL, loads the contents into a JSON object, and returns a dict of DataFrames.

    Args:
        url_path (str): _description_
        keys (list, optional): _description_. Defaults to None.

    Returns:
        dict[str, pd.DataFrame]: _description_
    """
    keys = keys or []
    dfs, fails = {}, []

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        request = urllib.request.Request(url_path, headers=headers)

        with urllib.request.urlopen(request) as url:
            data = json.load(url)

    except Exception as e:
        print(f"{e} for {url_path}")
        return [{"err": e, "path": url_path}]

    if isinstance(data, dict):
        for k, v in data.items():
            if k in keys and isinstance(v, list):
                try:
                    dfs[k] = pd.DataFrame(v)
                except Exception as e:
                    print(f"{e} for {k}")
                    fails.append({"err": e, "key": k})

    if isinstance(data, list):
        try:
            sanitized_key = sanitize_url(url_path)
            dfs[sanitized_key] = pd.DataFrame(data)
        except Exception as e:
            print(e)
            fails.append({"err": e, "key": sanitized_key})

    if fails:
        return fails
    return dfs
