import datetime

import pandas as pd
import pytest

from football_pipeline.stages.bronze.bronze_pipe import generic_bronze_transform
from football_pipeline.stages.bronze.data_structures import (
    BronzeEvent,
    BronzeFixture,
    BronzePlayer,
    BronzeStats,
    BronzeTeams,
)

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


PLAYER_INPUT_DF = pd.DataFrame(
    [
        {
            "id": 0,
            "team": 1,
            "element_type": 3,
            "first_name": "Dirk",
            "second_name": "Diggler",
            "status": "a",
            "birth_date": "1999-12-31",
        },
        {
            "id": 1,
            "team": 2,
            "element_type": 5,
            "first_name": "Dirk",
            "second_name": "Diggler",
            "status": "d",
            "birth_date": "1999-12-31",
        },
        {
            "id": 2,
            "team": 3,
            "element_type": 1,
            "first_name": "D1rk",
            "second_name": "Diggler",
            "status": "i",
            "birth_date": "1999-12-31",
        },
        {
            "id": 3,
            "team": 4,
            "element_type": 2,
            "first_name": "Dirk",
            "second_name": "Diggler",
            "status": "f",
            "birth_date": "1999-12-31",
        },
        {
            "id": 4,
            "team": 5,
            "element_type": 3,
            "first_name": "Dirk",
            "second_name": "Diggler",
            "status": "d",
            "birth_date": "19999-12-31",
        },
        {
            "id": 5,
            "team": 6,
            "element_type": 4,
            "first_name": "Dirk",
            "second_name": "Diggler",
            "status": "a",
            "birth_date": "1999-12-31",
        },
    ]
)


PLAYER_EXPECTED_RESULT = (
    pd.DataFrame(
        [
            {
                "id": 5,
                "team": 6,
                "element_type": 4,
                "first_name": "dirk",
                "second_name": "diggler",
                "status": "a",
                "birth_date": datetime.date(1999, 12, 31),
            },
        ]
    ),
    pd.DataFrame(
        [
            {
                "id": 0,
                "team": 1,
                "element_type": 3,
                "error": "'id' must be >= 1: 0",
                "first_name": "Dirk",
                "second_name": "Diggler",
                "status": "a",
                "birth_date": "1999-12-31",
            },
            {
                "id": 1,
                "team": 2,
                "element_type": 5,
                "error": "'element_type' must be in range(1, 5) (got 5)",
                "first_name": "Dirk",
                "second_name": "Diggler",
                "status": "d",
                "birth_date": "1999-12-31",
            },
            {
                "id": 2,
                "team": 3,
                "element_type": 1,
                "error": "'first_name' must match regex '^[\\\\D\\\\s]+$' ('d1rk' doesn't)",
                "first_name": "D1rk",
                "second_name": "Diggler",
                "status": "i",
                "birth_date": "1999-12-31",
            },
            {
                "id": 3,
                "team": 4,
                "element_type": 2,
                "error": "'status' must be in ['a', 'd', 'i', 'u'] (got 'f')",
                "first_name": "Dirk",
                "second_name": "Diggler",
                "status": "f",
                "birth_date": "1999-12-31",
            },
            {
                "id": 4,
                "team": 5,
                "element_type": 3,
                "error": "time data '19999-12-3' does not match format '%Y-%m-%d'",
                "first_name": "Dirk",
                "second_name": "Diggler",
                "status": "d",
                "birth_date": "19999-12-31",
            },
        ]
    ),
)

EVENT_INPUT_DF = pd.DataFrame(
    [
        {"event_id": 0, "event": "red_card"},
        {"event_id": 1, "event": "r"},
        {"event_id": 2, "event": "yellow_card"},
    ]
)


EVENT_EXPECTED_RESULT = (
    pd.DataFrame(
        [
            {"event_id": 2, "event": "yellow_card"},
        ]
    ),
    pd.DataFrame(
        [
            {
                "event_id": 0,
                "event": "red_card",
                "error": "'event_id' must be >= 1: 0",
            },
            {
                "event_id": 1,
                "event": "r",
                "error": "Length of 'event' must be >= 2: 1",
            },
        ]
    ),
)

STATS_INPUT_DF = pd.DataFrame(
    [
        {
            "event_id": 0,
            "team_id": 1,
            "fixture_id": 2,
            "player_id": 3,
        },
        {
            "event_id": 1,
            "team_id": 2,
            "fixture_id": 3,
            "player_id": 4,
        },
    ]
)


STATS_EXPECTED_RESULT = (
    pd.DataFrame(
        [
            {
                "event_id": 1,
                "team_id": 2,
                "fixture_id": 3,
                "player_id": 4,
            },
        ]
    ),
    pd.DataFrame(
        [
            {
                "event_id": 0,
                "team_id": 1,
                "fixture_id": 2,
                "player_id": 3,
                "error": "'event_id' must be >= 1: 0",
            },
        ]
    ),
)

FIXTURE_INPUT_DF = pd.DataFrame(
    [
        {
            "id": 1,
            "started": True,
            "finished": False,
            "kickoff_time": "1999-12-31",
            "team_h": 1,
            "team_a": 2,
            "team_h_difficulty": 1,
            "team_a_difficulty": 2,
        },
        {
            "id": 0,
            "started": True,
            "finished": False,
            "kickoff_time": "1999-12-31",
            "team_h": 1,
            "team_a": 2,
            "team_h_difficulty": 1,
            "team_a_difficulty": 2,
        },
        {
            "id": 1,
            "started": True,
            "finished": "False",
            "kickoff_time": "1999-12-31",
            "team_h": 1,
            "team_a": 2,
            "team_h_difficulty": 1,
            "team_a_difficulty": 2,
        },
        {
            "id": 1,
            "started": True,
            "finished": False,
            "kickoff_time": "19999-12-31",
            "team_h": 1,
            "team_a": 2,
            "team_h_difficulty": 1,
            "team_a_difficulty": 2,
        },
        {
            "id": 1,
            "started": True,
            "finished": False,
            "kickoff_time": "1999-12-31",
            "team_h": 1,
            "team_a": 2,
            "team_h_difficulty": -1,
            "team_a_difficulty": 2,
        },
    ]
)


FIXTURE_EXPECTED_RESULT = (
    pd.DataFrame(
        [
            {
                "id": 1,
                "started": True,
                "finished": False,
                "kickoff_time": datetime.date(1999, 12, 31),
                "team_h": 1,
                "team_a": 2,
                "team_h_difficulty": 1,
                "team_a_difficulty": 2,
            },
        ]
    ),
    pd.DataFrame(
        [
            {
                "id": 0,
                "started": True,
                "finished": False,
                "kickoff_time": "1999-12-31",
                "team_h": 1,
                "team_a": 2,
                "team_h_difficulty": 1,
                "team_a_difficulty": 2,
                "error": "'id' must be >= 1: 0",
            },
            {
                "id": 1,
                "started": True,
                "finished": "False",
                "kickoff_time": "1999-12-31",
                "team_h": 1,
                "team_a": 2,
                "team_h_difficulty": 1,
                "team_a_difficulty": 2,
                "error": "'finished' must be <class 'bool'> (got 'False' that is a <class 'str'>).",
            },
            {
                "id": 1,
                "started": True,
                "finished": False,
                "kickoff_time": "19999-12-31",
                "team_h": 1,
                "team_a": 2,
                "team_h_difficulty": 1,
                "team_a_difficulty": 2,
                "error": "time data '19999-12-3' does not match format '%Y-%m-%d'",
            },
            {
                "id": 1,
                "started": True,
                "finished": False,
                "kickoff_time": "1999-12-31",
                "team_h": 1,
                "team_a": 2,
                "team_h_difficulty": -1,
                "team_a_difficulty": 2,
                "error": "'team_h_difficulty' must be >= 0: -1",
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
        pytest.param(
            PLAYER_INPUT_DF,
            BronzePlayer,
            PLAYER_EXPECTED_RESULT,
            id="Ensure separates BronzePlayerFixture valid and invalid records",
        ),
        pytest.param(
            EVENT_INPUT_DF,
            BronzeEvent,
            EVENT_EXPECTED_RESULT,
            id="Ensure separates BronzeEventFixture valid and invalid records",
        ),
        pytest.param(
            STATS_INPUT_DF,
            BronzeStats,
            STATS_EXPECTED_RESULT,
            id="Ensure separates BronzeStatsFixture valid and invalid records",
        ),
        pytest.param(
            FIXTURE_INPUT_DF,
            BronzeFixture,
            FIXTURE_EXPECTED_RESULT,
            id="Ensure separates BronzeFixtureFixture valid and invalid records",
        ),
    ],
)
def test_generic_bronze_transform(inp_df, validator_cls, expected_result):
    expected_valid, expected_invalid = expected_result

    actual_valid, actual_invalid = generic_bronze_transform(inp_df, validator_cls)

    assert actual_valid.to_dict("records") == expected_valid.to_dict("records")
    assert actual_invalid.to_dict("records") == expected_invalid.to_dict("records")
