import pandas as pd
import pytest

from football_pipeline.stages.bronze.data_structures import BronzeTeams
from football_pipeline.stages.bronze.table_validators import generic_bronze_validation

TEAM_INPUT_DF = pd.DataFrame(
    [
        {"id": 0, "name": "Arsenal", "position": 1, "short_name": "ARS"},
        {"id": 1, "name": "a", "position": 2, "short_name": "AVL"},
        {"id": 2, "name": "Chelsea", "position": 33, "short_name": "CHE"},
        {"id": 3, "name": "Liverpool", "position": 4, "short_name": "LIVE"},
        {"id": 4, "name": "Man Utd", "position": 5, "short_name": "MNU"},
        {"id": 5, "name": "Newcastle", "position": 6, "short_name": "NEW"},
    ]
)

TEAM_EXPECTED_RESULT = (
    pd.DataFrame(
        [
            {"id": 4, "name": "Man Utd", "position": 5, "short_name": "MNU"},
            {"id": 5, "name": "Newcastle", "position": 6, "short_name": "NEW"},
        ]
    ),
    pd.DataFrame(
        [
            {
                "id": 0,
                "name": "Arsenal",
                "position": 1,
                "short_name": "ARS",
                "error": "'id' must be >= 1: 0",
            },
            {
                "id": 1,
                "name": "a",
                "position": 2,
                "short_name": "AVL",
                "error": "Length of 'name' must be >= 2: 1",
            },
            {
                "id": 2,
                "name": "Chelsea",
                "position": 33,
                "short_name": "CHE",
                "error": "'position' must be < 21: 33",
            },
            {
                "id": 3,
                "name": "Liverpool",
                "position": 4,
                "short_name": "LIVE",
                "error": "'short_name' must match regex '[A-Z]{3}' ('LIVE' doesn't)",
            },
        ]
    ),
)


@pytest.mark.parametrize(
    "inp_df, validator_cls, expected_result",
    [
        pytest.param(
            TEAM_INPUT_DF,
            BronzeTeams,
            TEAM_EXPECTED_RESULT,
            id="Ensure separates BronzeTeamFixture valid and invalid records",
        ),
    ],
)
def test_generic_bronze_validation(inp_df, validator_cls, expected_result):
    expected_valid, expected_invalid = expected_result

    actual_valid, actual_invalid = generic_bronze_validation(inp_df, validator_cls)

    assert actual_valid.to_dict("records") == expected_valid.to_dict("records")
    assert actual_invalid.to_dict("records") == expected_invalid.to_dict("records")
