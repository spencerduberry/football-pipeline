import pandas as pd
import pytest


@pytest.fixture
def get_mock_df_001():
    return pd.DataFrame(
        {"column1": [1, 2, 3, 4, 5, 6], "column2": ["A", "B", "C", "D", "E", "F"]}
    )


@pytest.fixture
def response_dict():
    return {
        "key_a": [{"col": 1}, {"col": 2}, {"col": 3}],
        "key_b": [{"col": 4}, {"col": 5}, {"col": 6}],
        "key_c": [{"col": 7}, {"col": 8}, {"col": 9}],
    }


@pytest.fixture
def response_list():
    return [{"col": 1}, {"col": 2}, {"col": 3}]
