import pytest
from football_pipeline.stages.bronze.bronze_pipe import generic_bronze_transform

@pytest.mark.parametrize(
    "fixture_name",
    [
        pytest.param(
            "get_mock_df_002",
            id="Ensure only valid rows returned",
        )
    ]
)

def test_generic_bronze_transform(request, fixture_name, BronzeTeamsFixture):
    inp_df = request.getfixturevalue(fixture_name)
    result = generic_bronze_transform(inp_df, BronzeTeamsFixture)
    assert len(result) == 2