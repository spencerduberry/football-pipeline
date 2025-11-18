from football_pipeline.adapters.fs_wrapper import FakeFSLocal
from football_pipeline.adapters.io_wrapper import FakeIOWrapper
from football_pipeline.adapters.logger import FakeLogger
from football_pipeline.adapters.repo import Repo
from football_pipeline.adapters.time import fake_new_guid, fake_time_now
from football_pipeline.stages.pipe_001_raw import run_raw_layer


def test_run_raw_layer():
    db = {
        "path/to/config.yaml": {
            "endpoints": {
                "matches": {
                    "keys": [],
                    "path": "https://fantasy.premierleague.com/api/fixtures/",
                },
                "statics": {
                    "keys": ["element_types", "elements", "teams"],
                    "path": "https://fantasy.premierleague.com/api/bootstrap-static/",
                },
            },
            "save_root": "./data/00_raw",
        },
        "https://fantasy.premierleague.com/api/fixtures/": [
            {
                "code": 2561895,
                "event": 1,
            },
            {
                "code": 2561896,
                "event": 1,
            },
            {
                "code": 2561897,
                "event": 1,
            },
        ],
        "https://fantasy.premierleague.com/api/bootstrap-static/": {
            "chips": [
                {
                    "id": 1,
                    "name": "wildcard",
                }
            ],
            "events": [
                {
                    "id": 1,
                    "name": "Gameweek 1",
                }
            ],
            "phases": [
                {
                    "id": 1,
                    "name": "Overall",
                }
            ],
            "teams": [
                {
                    "code": 3,
                    "draw": 0,
                }
            ],
            "element_stats": [{"label": "Minutes played", "name": "minutes"}],
            "element_types": [
                {
                    "id": 1,
                    "plural_name": "Goalkeepers",
                }
            ],
            "elements": [
                {
                    "can_transact": True,
                    "can_select": True,
                }
            ],
        },
    }
    repo = Repo(
        io=FakeIOWrapper(db),
        fs=FakeFSLocal(db),
        logger=FakeLogger(__file__),
        time_func=fake_time_now,
        guid_func=fake_new_guid,
    )

    _res = run_raw_layer("path/to/config.yaml", repo)

    assert repo.io.db["./data/00_raw/element_types/20250425_232355.parquet"].to_dict(
        "records"
    ) == [
        {
            "id": 1,
            "plural_name": "Goalkeepers",
            "batch_guid": "123432424-absdbfdf",
            "ingestion_datetime": "20250425_232355",
        }
    ]
    assert repo.io.db["./data/00_raw/elements/20250425_232355.parquet"].to_dict(
        "records"
    ) == [
        {
            "can_transact": True,
            "can_select": True,
            "batch_guid": "123432424-absdbfdf",
            "ingestion_datetime": "20250425_232355",
        }
    ]
    assert repo.io.db[
        "./data/00_raw/fantasy_premierleague_com_api_fixtures/20250425_232355.parquet"
    ].to_dict("records") == [
        {
            "code": 2561895,
            "event": 1,
            "batch_guid": "123432424-absdbfdf",
            "ingestion_datetime": "20250425_232355",
        },
        {
            "code": 2561896,
            "event": 1,
            "batch_guid": "123432424-absdbfdf",
            "ingestion_datetime": "20250425_232355",
        },
        {
            "code": 2561897,
            "event": 1,
            "batch_guid": "123432424-absdbfdf",
            "ingestion_datetime": "20250425_232355",
        },
    ]
    assert repo.io.db["./data/00_raw/teams/20250425_232355.parquet"].to_dict(
        "records"
    ) == [
        {
            "code": 3,
            "draw": 0,
            "batch_guid": "123432424-absdbfdf",
            "ingestion_datetime": "20250425_232355",
        }
    ]
