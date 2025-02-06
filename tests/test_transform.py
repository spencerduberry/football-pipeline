import pandas as pd
import pytest

from src.football_pipeline.transform import add_ingestion_columns


@pytest.fixture
def get_mock_df_001():
    return pd.DataFrame(
        {"column1": [1, 2, 3, 4, 5, 6], "column2": ["A", "B", "C", "D", "E", "F"]}
    )


@pytest.mark.parametrize(
    "fixture_name, column, expected_unique_values",
    [
        pytest.param(
            "get_mock_df_001",
            "source_guid",
            6,
            id="Ensure unique source_guid for all rows",
        ),
        pytest.param(
            "get_mock_df_001", "batch_guid", 1, id="Ensure same batch_guid for all rows"
        ),
        pytest.param(
            "get_mock_df_001",
            "ingestion_datetime",
            1,
            id="Ensure same datetime for all rows",
        ),
    ],
)
def test_add_ingestion_columns(request, fixture_name, column, expected_unique_values):
    inp_df = request.getfixturevalue(fixture_name)
    result = add_ingestion_columns(inp_df)
    assert all(inp_df.eq(result[inp_df.columns]))  # the given data is unchanged
    assert result[column].nunique() == expected_unique_values
