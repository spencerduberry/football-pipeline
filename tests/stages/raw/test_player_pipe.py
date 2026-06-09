import polars as pl

from football_pipeline.adapters.fs_wrapper import FakeFSLocal
from football_pipeline.adapters.io_wrapper import FakeIOWrapper
from football_pipeline.adapters.logger import FakeLogger
from football_pipeline.adapters.repo import Repo
from football_pipeline.adapters.time import fake_new_guid, fake_time_now
from football_pipeline.stages.raw.player_pipe import run_raw_player_layer

HISTORY_P1 = {
    "element": [1, 1],
    "fixture": [9, 11],
    "opponent_team": [14, 11],
    "total_points": [10, 6],
    "was_home": [False, True],
    "kickoff_time": ["2025-08-17T15:30:00Z", "2025-08-23T16:30:00Z"],
    "team_h_score": [0, 5],
    "team_a_score": [1, 0],
    "round": [1, 2],
    "modified": [False, False],
    "minutes": [90, 90],
    "goals_scored": [0, 0],
    "assists": [0, 0],
    "clean_sheets": [1, 1],
    "goals_conceded": [0, 0],
    "own_goals": [0, 0],
    "penalties_saved": [0, 0],
    "penalties_missed": [0, 0],
    "yellow_cards": [1, 0],
    "red_cards": [0, 0],
    "saves": [7, 1],
    "bonus": [3, 0],
    "bps": [38, 28],
    "influence": ["49.2", "13.4"],
    "creativity": ["0.0", "0.0"],
    "threat": ["0.0", "0.0"],
    "ict_index": ["4.9", "1.3"],
    "clearances_blocks_interceptions": [1, 0],
    "recoveries": [13, 3],
    "tackles": [0, 0],
    "defensive_contribution": [0, 0],
    "starts": [1, 1],
    "expected_goals": ["0.00", "0.00"],
    "expected_assists": ["0.00", "0.00"],
    "expected_goal_involvements": ["0.00", "0.00"],
    "expected_goals_conceded": ["1.52", "0.17"],
    "value": [55, 55],
    "transfers_balance": [0, 218659],
    "selected": [1531911, 2284634],
    "transfers_in": [0, 277339],
    "transfers_out": [0, 58680],
}


HISTORY_P2 = {
    "element": [9, 9],
    "fixture": [361, 373],
    "opponent_team": [3, 8],
    "total_points": [0, 0],
    "was_home": [True, False],
    "kickoff_time": ["2026-05-18T19:00:00Z", "2026-05-24T15:00:00Z"],
    "team_h_score": [1, 1],
    "team_a_score": [0, 2],
    "round": [37, 38],
    "modified": [False, False],
    "minutes": [0, 0],
    "goals_scored": [0, 0],
    "assists": [0, 0],
    "clean_sheets": [0, 0],
    "goals_conceded": [0, 0],
    "own_goals": [0, 0],
    "penalties_saved": [0, 0],
    "penalties_missed": [0, 0],
    "yellow_cards": [0, 0],
    "red_cards": [0, 0],
    "saves": [0, 0],
    "bonus": [0, 0],
    "bps": [0, 0],
    "influence": ["0.0", "0.0"],
    "creativity": ["0.0", "0.0"],
    "threat": ["0.0", "0.0"],
    "ict_index": ["0.0", "0.0"],
    "clearances_blocks_interceptions": [0, 0],
    "recoveries": [0, 0],
    "tackles": [0, 0],
    "defensive_contribution": [0, 0],
    "starts": [0, 0],
    "expected_goals": ["0.00", "0.00"],
    "expected_assists": ["0.00", "0.00"],
    "expected_goal_involvements": ["0.00", "0.00"],
    "expected_goals_conceded": ["0.00", "0.00"],
    "value": [54, 54],
    "transfers_balance": [-3, -6],
    "selected": [6110, 6104],
    "transfers_in": [0, 0],
    "transfers_out": [3, 6],
}


HISTORY_PAST_P1 = {
    "season_name": ["2021/22", "2022/23"],
    "element_code": [154561, 154561],
    "start_cost": [45, 45],
    "end_cost": [44, 48],
    "total_points": [95, 166],
    "minutes": [2160, 3420],
    "goals_scored": [0, 0],
    "assists": [0, 0],
    "clean_sheets": [8, 12],
    "goals_conceded": [27, 46],
    "own_goals": [0, 1],
    "penalties_saved": [0, 0],
    "penalties_missed": [0, 0],
    "yellow_cards": [1, 1],
    "red_cards": [0, 0],
    "saves": [78, 154],
    "bonus": [5, 20],
    "bps": [496, 822],
    "influence": ["593.4", "1146.0"],
    "creativity": ["10.0", "20.1"],
    "threat": ["0.0", "4.0"],
    "ict_index": ["60.1", "117.3"],
    "clearances_blocks_interceptions": [0, 0],
    "recoveries": [0, 0],
    "tackles": [0, 0],
    "defensive_contribution": [0, 0],
    "starts": [0, 38],
    "expected_goals": ["0.00", "0.11"],
    "expected_assists": ["0.00", "0.12"],
    "expected_goal_involvements": ["0.00", "0.23"],
    "expected_goals_conceded": ["0.00", "50.12"],
}


HISTORY_PAST_P2 = {
    "season_name": ["2023/24", "2024/25"],
    "element_code": [440854, 440854],
    "start_cost": [45, 50],
    "end_cost": [40, 49],
    "total_points": [67, 43],
    "minutes": [942, 1117],
    "goals_scored": [1, 1],
    "assists": [3, 0],
    "clean_sheets": [6, 3],
    "goals_conceded": [8, 15],
    "own_goals": [0, 0],
    "penalties_saved": [0, 0],
    "penalties_missed": [0, 0],
    "yellow_cards": [1, 1],
    "red_cards": [0, 0],
    "saves": [0, 0],
    "bonus": [1, 2],
    "bps": [260, 178],
    "influence": ["228.8", "267.2"],
    "creativity": ["106.9", "91.3"],
    "threat": ["90.0", "32.0"],
    "ict_index": ["42.7", "39.2"],
    "clearances_blocks_interceptions": [0, 0],
    "recoveries": [0, 0],
    "tackles": [0, 0],
    "defensive_contribution": [0, 93],
    "starts": [11, 10],
    "expected_goals": ["0.74", "0.17"],
    "expected_assists": ["0.60", "0.29"],
    "expected_goal_involvements": ["1.34", "0.46"],
    "expected_goals_conceded": ["5.15", "14.71"],
}


def test_run_player_pipe():
    db = {
        "path/to/config.yaml": {
            "save_root": "./data/000_raw",
            "endpoint": "https://fantasy.premierleague.com/api/element-summary",
            "min_player_id": 1,
            "max_player_id": 2,
        },
        "https://fantasy.premierleague.com/api/element-summary/1": {
            "history": HISTORY_P1,
            "history_past": HISTORY_PAST_P1,
        },
        "https://fantasy.premierleague.com/api/element-summary/2": {
            "history": HISTORY_P2,
            "history_past": HISTORY_PAST_P2,
        },
    }
    repo = Repo(
        io=FakeIOWrapper(db),
        fs=FakeFSLocal(db),
        logger=FakeLogger(__file__),
        time_func=fake_time_now,
        guid_func=fake_new_guid,
    )

    _res = run_raw_player_layer("path/to/config.yaml", repo)

    print(repo.io.db.keys())

    assert (
        repo.io.db["./data/000_raw/history/20250425_232355.parquet"].to_dicts()
        == pl.concat([pl.DataFrame(HISTORY_P1), pl.DataFrame(HISTORY_P2)]).to_dicts()
    )
    assert (
        repo.io.db["./data/000_raw/history_past/20250425_232355.parquet"].to_dicts()
        == pl.concat(
            [pl.DataFrame(HISTORY_PAST_P1), pl.DataFrame(HISTORY_PAST_P2)]
        ).to_dicts()
    )
