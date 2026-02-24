import argparse

import pandas as pd

from football_pipeline.adapters.fs_wrapper import FSLocal
from football_pipeline.adapters.io_wrapper import FileType, IOWrapper
from football_pipeline.adapters.logger import RealLogger
from football_pipeline.adapters.repo import Repo
from football_pipeline.adapters.time import new_guid, time_now
from football_pipeline.stages.bronze.data_structures import (
    BronzeEvent,
    BronzeFixture,
    BronzePlayer,
    BronzeStats,
    BronzeTeams,
)
from football_pipeline.stages.bronze.table_validators import (
    bronze_stats_event_transform,
    generic_bronze_validation,
)


def run_bronze_pipe(config_path: str, repo: Repo) -> dict[str, bool]:
    config = repo.io.read(config_path, FileType.YAML)
    repo.logger.info(msg="successfully read yaml.", config_path=config_path)
    if not config:
        return {"valid_config": False}
    sources = config.get("sources")
    validator_map = {
        "teams": BronzeTeams,
        "fixtures": BronzeFixture,
        "players": BronzePlayer,
    }

    date_time = repo.time_func()

    for k, v in sources.items():
        files = repo.fs.list_files(v["read_path"])
        print(k, files)
        df = pd.concat([repo.io.read(file, FileType.PARQUET) for file in files])
        if k == "stats_events":
            stats_table, events_table = bronze_stats_event_transform(df)
            print(stats_table)
            print(events_table)
            for table, validator, dir_name in (
                (stats_table, BronzeStats, "stats"),
                (events_table, BronzeEvent, "events"),
            ):
                valid, invalid = generic_bronze_validation(table, validator)
                valid_save_path = (
                    f"{config['save_root']}/valid/{dir_name}/{date_time}.parquet"
                )
                repo.io.write(valid_save_path, valid, FileType.PARQUET)
                invalid_save_path = (
                    f"{config['save_root']}/invalid/{dir_name}/{date_time}.parquet"
                )
                repo.io.write(invalid_save_path, invalid, FileType.PARQUET)
            continue

        valid, invalid = generic_bronze_validation(df, validator_map[k])
        valid_save_path = f"{config['save_root']}/valid/{k}/{date_time}.parquet"
        repo.io.write(valid_save_path, valid, FileType.PARQUET)
        invalid_save_path = f"{config['save_root']}/invalid/{k}/{date_time}.parquet"
        repo.io.write(invalid_save_path, invalid, FileType.PARQUET)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse config path")
    parser.add_argument(
        "--config-path", type=str, help="Path to the configuration file"
    )
    args = parser.parse_args()
    repo = Repo(
        io=IOWrapper(),
        fs=FSLocal(),
        logger=RealLogger(__file__),
        time_func=time_now,
        guid_func=new_guid,
    )
    print(run_bronze_pipe(args.config_path, repo))
