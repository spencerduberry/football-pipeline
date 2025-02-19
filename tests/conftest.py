import pandas as pd
import pytest


@pytest.fixture
def get_mock_df_001():
    return pd.DataFrame(
        {"column1": [1, 2, 3, 4, 5, 6], "column2": ["A", "B", "C", "D", "E", "F"]}
    )
