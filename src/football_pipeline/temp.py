import json
import urllib.request

import pandas as pd


def extract_data(url: str, keys: list):
    with urllib.request.urlopen(url) as response:
        data = json.load(response)

    data_dfs = {}

    for key in keys:
        data_dfs[key] = pd.DataFrame(data[key])

    return data_dfs
