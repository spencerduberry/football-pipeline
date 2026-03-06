from football_pipeline.adapters.fs_wrapper import FakeFSLocal
from football_pipeline.adapters.io_wrapper import FakeIOWrapper
from football_pipeline.adapters.logger import FakeLogger
from football_pipeline.adapters.repo import Repo
from football_pipeline.adapters.time import fake_new_guid, fake_time_now
from football_pipeline.stages.raw.raw_pipe import run_raw_layer

FIXTURES_DATA = [
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
]


STATICS_DATA = {
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
}


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
        "https://fantasy.premierleague.com/api/fixtures/": FIXTURES_DATA,
        "https://fantasy.premierleague.com/api/bootstrap-static/": STATICS_DATA,
    }
    repo = Repo(
        io=FakeIOWrapper(db),
        fs=FakeFSLocal(db),
        logger=FakeLogger(__file__),
        time_func=fake_time_now,
        guid_func=fake_new_guid,
    )

    _res = run_raw_layer("path/to/config.yaml", repo)
    assert repo.io.db["./data/00_raw/matches/20250425_232355.json"] == FIXTURES_DATA
    assert repo.io.db["./data/00_raw/statics/20250425_232355.json"] == STATICS_DATA
