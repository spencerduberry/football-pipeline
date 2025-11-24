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


@pytest.fixture
def team_input_df():
    return pd.DataFrame(
        {
            "id": [0, 1, 2, 3, 4, 5],
            "name": ["Arsenal", "a", "Chelsea", "Liverpool", "Man Utd", "Newcastle"],
            "position": [1, 2, 33, 4, 5, 6],
            "short_name": ["ARS", "AVL", "CHE", "LIVE", "MNU", "NEW"],
        }
    )


@pytest.fixture
def team_expected_result():
    return (
        pd.DataFrame(
            {
                "id": [4, 5],
                "name": ["Man Utd", "Newcastle"],
                "position": [5, 6],
                "short_name": ["MNU", "NEW"],
            }
        ),
        pd.DataFrame(
            {
                "id": [0, 1, 2, 3],
                "name": ["Arsenal", "a", "Chelsea", "Liverpool"],
                "position": [1, 2, 33, 4],
                "short_name": ["ARS", "AVL", "CHE", "LIVE"],
                "error": [
                    ("'id' must be >= 1: 0",),
                    ("Length of 'name' must be >= 2: 1",),
                    ("'position' must be < 21: 33",),
                    ("'short_name' must match regex '[A-Z]{3}' ('LIVE' doesn't)",),
                ],
            }
        ),
    )
