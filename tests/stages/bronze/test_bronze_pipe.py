import pytest

from football_pipeline.stages.bronze.bronze_pipe import generic_bronze_transform
from football_pipeline.stages.bronze.data_structures import BronzeTeams


@pytest.mark.parametrize(
    "inp_df_fixt_name, validator_cls, expected_result_fixt_name",
    [
        pytest.param(
            "team_input_df",
            BronzeTeams,
            "team_expected_result",
            id="Ensure separates BronzeTeamFixture valid and invalid records",
        ),
    ],
)
def test_generic_bronze_transform(
    request, inp_df_fixt_name, validator_cls, expected_result_fixt_name
):
    inp_df = request.getfixturevalue(inp_df_fixt_name)
    expected_valid, expected_invalid = request.getfixturevalue(
        expected_result_fixt_name
    )

    validator_instance = validator_cls(
        id=1, name="Valid Dummy", position=1, short_name="DMY"
    )
    actual_valid, actual_invalid = generic_bronze_transform(inp_df, validator_instance)

    assert actual_valid.to_dict("records") == expected_valid.to_dict("records")
    assert actual_invalid.to_dict("records") == expected_invalid.to_dict("records")
